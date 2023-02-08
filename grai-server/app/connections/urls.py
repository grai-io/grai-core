import json
import uuid

from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions.multitenant import Multitenant
from connections.tasks import run_update_server
from rest_framework import routers
from workspaces.permissions import HasWorkspaceAPIKey

from .models import Connection, Connector, Run
from .views import ConnectionViewSet, ConnectorViewSet, RunViewSet

app_name = "connections"

router = routers.SimpleRouter()
router.register("connections", ConnectionViewSet, basename="connections")
router.register("connectors", ConnectorViewSet, basename="connectors")
router.register("runs", RunViewSet, basename="runs")


@api_view(["POST"])
@permission_classes([(HasWorkspaceAPIKey | IsAuthenticated) & Multitenant])
def create_run(request):
    connector = None
    connection = None
    trigger = None

    connection_id = request.POST.get("connection_id")

    if connection_id is not None:
        connection = Connection.objects.get(id=connection_id)
        connector = connection.connector

    else:
        connector_name = request.POST.get("connector")

        if connector_name is None:
            raise Exception("You must provide a connector")

        connector = Connector.objects.get(name=connector_name)

        name = f"{connector.name} {uuid.uuid4()}"
        namespace = request.POST.get("namespace", "default")
        metadata = request.POST.get("metadata")
        secrets = request.POST.get("secrets")

        connection = Connection.objects.create(
            connector=connector,
            name=name,
            namespace=namespace,
            is_active=True,
            temp=True,
            metadata=json.loads(metadata) if metadata else None,
            secrets=json.loads(secrets) if secrets else None,
        )

    github_installation_id = request.POST.get("github_installation_id")
    if github_installation_id:
        from .github import Github

        git_owner = request.POST.get("git_owner")
        git_repo = request.POST.get("git_repo")
        git_head_sha = request.POST.get("git_head_sha")

        github = Github(owner=git_owner, repo=git_repo, installation_id=github_installation_id)
        check = github.create_check(head_sha=git_head_sha)

        trigger = {
            "installation_id": github_installation_id,
            "owner": git_owner,
            "repo": git_repo,
            "head_sha": git_head_sha,
            "check_id": check.id,
        }

    run = Run.objects.create(connection=connection, status="queued", trigger=trigger)

    run_update_server.delay(run.id)

    return Response({"id": run.id})


urlpatterns = router.urls + [
    path("external-runs/", create_run),
]

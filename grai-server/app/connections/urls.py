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


def get_connection(request) -> Connection:
    connection_id = request.POST.get("connection_id")

    if connection_id is not None:
        return Connection.objects.get(id=connection_id)

    connector_name = request.POST.get("connector")

    if connector_name is None:
        raise Exception("You must provide a connector or connection_id")

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
        metadata=json.loads(metadata) if metadata else {},
        secrets=json.loads(secrets) if secrets else {},
    )

    return connection


def get_trigger(request):
    git_owner = request.POST.get("git_owner")

    if git_owner is None:
        return None

    from .github import Github

    git_repo = request.POST.get("git_repo")
    git_head_sha = request.POST.get("git_head_sha")

    github = Github(owner=git_owner, repo=git_repo)
    check = github.create_check(head_sha=git_head_sha)

    return {
        "installation_id": github.installation_id,
        "owner": git_owner,
        "repo": git_repo,
        "head_sha": git_head_sha,
        "check_id": check.id,
    }


@api_view(["POST"])
@permission_classes([(HasWorkspaceAPIKey | IsAuthenticated) & Multitenant])
def create_run(request):
    connection = get_connection(request)
    trigger = get_trigger(request)

    action = request.POST.get("action", "tests")

    run = Run.objects.create(connection=connection, status="queued", trigger=trigger, action=action)

    run_update_server.delay(run.id)

    return Response({"id": run.id})


urlpatterns = router.urls + [
    path("external-runs/", create_run),
]

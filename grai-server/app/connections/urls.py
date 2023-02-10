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
from installations.models import Repository, Commit, Branch
from .views import ConnectionViewSet, ConnectorViewSet, RunViewSet
from installations.github import Github

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
    owner = request.POST.get("github_owner")

    if owner is None:
        return None, None

    repo = request.POST.get("github_repo")

    try:
        repository = Repository.objects.get(owner=owner, repo=repo)
    except Repository.DoesNotExist:
        raise Exception("Repository not found, have you installed the Grai Github App?")

    branch = request.POST.get("git_branch")
    head_sha = request.POST.get("git_head_sha")

    branch, created = Branch.objects.get_or_create(repository=repository, reference=branch)
    commit, created = Commit.objects.get_or_create(repository=repository, branch=branch, reference=head_sha)

    github = Github(owner=owner, repo=repo)
    check = github.create_check(head_sha=head_sha)

    return commit, {
        "installation_id": github.installation_id,
        "owner": owner,
        "repo": repo,
        "head_sha": head_sha,
        "check_id": check.id,
    }


@api_view(["POST"])
@permission_classes([(HasWorkspaceAPIKey | IsAuthenticated) & Multitenant])
def create_run(request):
    connection = get_connection(request)
    commit, trigger = get_trigger(request)

    action = request.POST.get("action", "tests")

    run = Run.objects.create(connection=connection, status="queued", commit=commit, trigger=trigger, action=action)

    run_update_server.delay(run.id)

    return Response({"id": run.id})


urlpatterns = router.urls + [
    path("external-runs/", create_run),
]

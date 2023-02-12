import json
import uuid

from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_multitenant.utils import get_current_tenant

from common.permissions.multitenant import Multitenant
from connections.tasks import run_update_server
from installations.github import Github
from installations.models import Branch, Commit, Repository, PullRequest
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


def get_trigger(request, action: str):
    owner = request.POST.get("github_owner")

    if owner is None:
        return None, None

    repo = request.POST.get("github_repo")

    try:
        repository = Repository.objects.get(owner=owner, repo=repo)
    except Repository.DoesNotExist:
        raise Exception("Repository not found, have you installed the Grai Github App?")

    branch_reference = request.POST.get("git_branch")
    head_sha = request.POST.get("git_head_sha")
    pr_reference = request.POST.get("github_pr_reference")

    pull_request = None

    branch, created = Branch.objects.get_or_create(repository=repository, reference=branch_reference)
    if pr_reference:
        pull_request, created = PullRequest.objects.get_or_create(repository=repository, reference=pr_reference)
    commit, created = Commit.objects.get_or_create(
        repository=repository, branch=branch, reference=head_sha, pull_request=pull_request
    )

    github = Github(owner=owner, repo=repo)

    workspace = get_current_tenant()
    details_url_start = (
        f"https://app.grai.io/{workspace.organisation.name}/{workspace.name}/reports/github/{owner}/{repo}/"
    )
    details_url = (
        f"{details_url_start}pulls/{pr_reference}"
        if pr_reference is not None
        else f"{details_url_start}branches/{branch_reference}"
    )

    output = (
        {
            "title": "Grai Test Summary",
            "summary": f"[View Test Report on Grai Cloud]({details_url})",
        }
        if action == "tests"
        else None
    )

    check = github.create_check(
        head_sha=head_sha,
        name="Grai Update" if action == "update" else "Grai Test",
        details_url=details_url,
        output=output,
    )

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
    action = request.POST.get("action", "tests")

    connection = get_connection(request)
    commit, trigger = get_trigger(request, action)

    run = Run.objects.create(connection=connection, status="queued", commit=commit, trigger=trigger, action=action)

    run_update_server.delay(run.id)

    return Response({"id": run.id})


urlpatterns = router.urls + [
    path("external-runs/", create_run),
]

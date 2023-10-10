import hashlib
import hmac
import json
import uuid
import logging

from django.urls import path
from django_multitenant.utils import get_current_tenant
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from common.permissions.multitenant import Multitenant
from connections.tasks import process_run
from installations.github import Github
from installations.models import Branch, Commit, PullRequest, Repository
from lineage.models import Source
from rest_framework import routers
from workspaces.models import Workspace

from .models import Connection, Connector, Run, RunFile
from .views import ConnectionViewSet, ConnectorViewSet, RunViewSet

app_name = "connections"

router = routers.SimpleRouter()
router.register("connections", ConnectionViewSet, basename="connections")
router.register("connectors", ConnectorViewSet, basename="connectors")
router.register("runs", RunViewSet, basename="runs")


class DisplayError(Exception):
    pass


def get_source(request) -> Source:
    source_id = request.POST.get("source_id")

    if source_id:
        return Source.objects.get(id=source_id)

    source_name = request.POST.get("source_name")

    if source_name is None:
        raise DisplayError("You must provide a source_id or source_name")

    source, created = Source.objects.get_or_create(name=source_name)

    return source


def get_connection(request) -> Connection:
    connection_id = request.POST.get("connection_id")

    if connection_id is not None:
        return Connection.objects.get(id=connection_id)

    connector_name = request.POST.get("connector_name")

    if connector_name is None:
        raise DisplayError("You must provide a connector or connection_id")

    source = get_source(request)

    connector = Connector.objects.get(name=connector_name)

    name = f"{connector.name} {uuid.uuid4()}"
    namespace = request.POST.get("connector_namespace", "default")
    metadata = request.POST.get("connector_metadata")
    secrets = request.POST.get("connector_secrets")

    connection = Connection.objects.create(
        connector=connector,
        source=source,
        name=name,
        namespace=namespace,
        is_active=True,
        temp=True,
        metadata=json.loads(metadata) if metadata else {},
        secrets=json.loads(secrets) if secrets else {},
    )

    return connection


def get_commit(
    owner: str,
    repo: str,
    branch_reference: str,
    pr_reference: str,
    pr_title: str,
    head_sha: str,
    commit_title: str,
):
    # Repository
    try:
        repository = Repository.objects.get(owner=owner, repo=repo)
    except Repository.DoesNotExist:
        raise DisplayError("Repository not found, have you installed the Grai Github App?")

    # Branch
    branch, created = Branch.objects.get_or_create(repository=repository, reference=branch_reference)

    # Pull Request
    pull_request = None

    if pr_reference:
        try:
            pull_request = PullRequest.objects.get(repository=repository, reference=pr_reference)
            pull_request.branch = branch
            pull_request.title = pr_title
            pull_request.save()
        except PullRequest.DoesNotExist:
            pull_request = PullRequest.objects.create(
                repository=repository,
                reference=pr_reference,
                branch=branch,
                title=pr_title,
            )

    # Commit
    commit = None
    try:
        commit = Commit.objects.get(repository=repository, reference=head_sha)
        commit.branch = branch
        commit.pull_request = pull_request
        commit.title = commit_title
        commit.save()

    except Commit.DoesNotExist:
        commit = Commit.objects.create(
            repository=repository,
            reference=head_sha,
            branch=branch,
            pull_request=pull_request,
            title=commit_title,
        )

    return commit


def get_trigger(request, action: str):
    owner = request.POST.get("github_owner")

    if owner is None:
        return None, None

    repo = request.POST.get("github_repo")
    branch_reference = request.POST.get("git_branch")
    head_sha = request.POST.get("git_head_sha")
    commit_title = request.POST.get("git_commit_message")
    pr_reference = request.POST.get("github_pr_reference")
    pr_title = request.POST.get("github_pr_title")

    commit = get_commit(owner, repo, branch_reference, pr_reference, pr_title, head_sha, commit_title)

    github = Github(owner=owner, repo=repo)

    workspace = Workspace.objects.get(id=get_current_tenant().id)
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
@permission_classes([Multitenant])
def create_run(request):
    action = request.POST.get("action", "tests")

    try:
        connection = get_connection(request)
        commit, trigger = get_trigger(request, action)

        run = Run.objects.create(
            connection=connection,
            status="queued",
            commit=commit,
            trigger=trigger,
            action=action,
            source=connection.source,
        )

        file = request.FILES.get("file", None)

        if file:
            runFile = RunFile(run=run)
            runFile.file = file
            runFile.save()

        process_run.delay(run.id)

        return Response({"id": run.id})
    except DisplayError as e:
        logging.exception(str(e))
        message = "An error was encountered while creating a run. The full error has been logged to the server."
        return Response({"error": message}, status=400)


def validate_webhook(request, secret: str):
    auth_header = request.headers.get("authorization", None)
    # secret = os.environ['MY_DBT_CLOUD_AUTH_TOKEN'].encode('utf-8')
    signature = hmac.new(secret.encode("utf-8"), request.body, hashlib.sha256).hexdigest()
    return signature == auth_header


@api_view(["POST"])
def dbt_cloud(request):
    body = json.loads(request.body)

    if body.get("data", {}).get("runStatus") != "Success":
        return Response({"status": "not-success"})

    try:
        connection = Connection.objects.get(
            connector__slug=Connector.DBT_CLOUD,
            schedules__type="dbt-cloud",
            schedules__dbt_cloud__job_id=body["data"]["jobId"],
        )
    except Connection.DoesNotExist:
        return Response({"status": "Connection not found"})

    is_valid = validate_webhook(request, connection.schedules.get("dbt_cloud", {}).get("hmac_secret"))

    if not is_valid:
        raise Exception("Invalid dbt cloud webhook signature")

    if not connection.is_active:
        return Response({"status": "Connection not active"})

    run = Run.objects.create(
        workspace=connection.workspace,
        connection=connection,
        status="queued",
        trigger=body,
        action=Run.UPDATE,
        source=connection.source,
    )

    process_run.delay(run.id)

    return Response({"status": "ok"})


urlpatterns = router.urls + [
    path("external-runs/", create_run),
    path("dbt-cloud/", dbt_cloud, name="dbt-cloud"),
]

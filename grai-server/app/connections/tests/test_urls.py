import hashlib
import hmac
import json
import types
import uuid
from unittest.mock import MagicMock

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from connections.models import Connection, Connector
from installations.models import Branch, Commit, PullRequest, Repository
from lineage.models import Source
from users.models import User
from workspaces.models import Membership, Organisation, Workspace, WorkspaceAPIKey


@pytest.fixture
def create_organisation(name: str = None) -> Organisation:
    return Organisation.objects.create(name=str(uuid.uuid4()) if name is None else name)


@pytest.fixture
def create_workspace(create_organisation, name: str = None) -> Workspace:
    return Workspace.objects.create(
        name=str(uuid.uuid4()) if name is None else name,
        organisation=create_organisation,
    )


@pytest.fixture
def test_organisation() -> Organisation:
    return Organisation.objects.create(name="Org1")


@pytest.fixture
def test_workspace(test_organisation) -> Workspace:
    return Workspace.objects.create(name="W10", organisation=test_organisation)


@pytest.fixture
def test_source(test_workspace) -> Source:
    return Source.objects.create(workspace=test_workspace, name=str(uuid.uuid4()))


@pytest.fixture
def test_password() -> str:
    return "strong-test-pass"


def generate_username() -> str:
    return f"{str(uuid.uuid4())}@gmail.com"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        kwargs.setdefault("username", generate_username())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def workspace_api_key(create_workspace, create_user) -> str:
    api_key, key = WorkspaceAPIKey.objects.create_key(
        name=str(uuid.uuid4()), workspace=create_workspace, created_by=create_user()
    )
    return key


@pytest.fixture
def auto_login_user(client, create_user: User, test_password: str, create_workspace: Workspace):
    def make_auto_login(user=None, workspace=None):
        if user is None:
            user = create_user()
            client.login(username=user.username, password=test_password)
        if workspace is None:
            workspace = create_workspace
        Membership.objects.create(role="admin", user=user, workspace=workspace)
        return client, user, workspace

    return make_auto_login


@pytest.fixture
def test_connector() -> Connector:
    return Connector.objects.create(name=str(uuid.uuid4()), slug=str(uuid.uuid4()))


@pytest.fixture
def test_dbt_cloud_connector() -> Connector:
    connector, created = Connector.objects.get_or_create(name=Connector.DBT_CLOUD, slug=Connector.DBT_CLOUD)

    return connector


@pytest.fixture
def test_openlineage_connector(create_workspace) -> Connector:
    connector, created = Connector.objects.get_or_create(name=Connector.OPEN_LINEAGE, slug=Connector.OPEN_LINEAGE)

    return connector


@pytest.fixture
def test_repository(create_workspace) -> Repository:
    return Repository.objects.create(
        workspace=create_workspace,
        owner="test_owner",
        repo="test_repo",
        type=Repository.GITHUB,
        installation_id=1234,
    )


@pytest.fixture
def test_branch(create_workspace, test_repository) -> Branch:
    return Branch.objects.create(
        workspace=create_workspace,
        repository=test_repository,
        reference=str(uuid.uuid4()),
    )


@pytest.fixture
def test_pull_request(create_workspace, test_repository, test_branch) -> PullRequest:
    return PullRequest.objects.create(
        workspace=create_workspace,
        repository=test_repository,
        branch=test_branch,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )


@pytest.fixture
def test_commit(create_workspace, test_repository, test_branch) -> Commit:
    return Commit.objects.create(
        workspace=create_workspace,
        repository=test_repository,
        branch=test_branch,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )


@pytest.fixture
def test_commit_with_pr(create_workspace, test_repository, test_branch, test_pull_request) -> Commit:
    return Commit.objects.create(
        workspace=create_workspace,
        repository=test_repository,
        branch=test_branch,
        pull_request=test_pull_request,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )


@pytest.mark.django_db
def test_create_run_connection(auto_login_user, test_connector, test_source):
    client, user, workspace = auto_login_user()

    connection = Connection.objects.create(
        workspace=workspace,
        connector=test_connector,
        name=str(uuid.uuid4()),
        source=test_source,
    )

    url = "/api/v1/external-runs/"
    response = client.post(
        url,
        {
            "connection_id": str(connection.id),
        },
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    run = response.json()
    assert run["id"] is not None


@pytest.mark.django_db
def test_create_run_connector_existing_source(auto_login_user, test_connector):
    client, user, workspace = auto_login_user()

    source = Source.objects.create(
        workspace=workspace,
        name=str(uuid.uuid4()),
    )

    url = "/api/v1/external-runs/"
    response = client.post(
        url,
        {
            "connector_name": test_connector.name,
            "source_id": str(source.id),
        },
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    run = response.json()
    assert run["id"] is not None


@pytest.mark.django_db
def test_create_run_connector_missing_source(auto_login_user, test_connector, test_source):
    client, user, workspace = auto_login_user()

    url = "/api/v1/external-runs/"
    response = client.post(
        url,
        {
            "connector_name": test_connector.name,
        },
    )
    assert response.status_code == 400
    assert response.json().get("error") == "You must provide a source_id or source_name"


@pytest.mark.django_db
def test_create_run_connector(auto_login_user, test_connector):
    client, user, workspace = auto_login_user()

    url = "/api/v1/external-runs/"
    response = client.post(
        url,
        {
            "connector_name": test_connector.name,
            "source_name": "test2",
        },
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    run = response.json()
    assert run["id"] is not None


@pytest.mark.django_db
def test_create_run_connector_file(auto_login_user, test_connector):
    client, user, workspace = auto_login_user()

    file = SimpleUploadedFile("manifest.json", b"file_content", content_type="test/json")

    url = "/api/v1/external-runs/"
    response = client.post(
        url,
        {"connector_name": test_connector.name, "file": file, "source_name": "test3"},
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    run = response.json()
    assert run["id"] is not None


@pytest.mark.django_db
def test_create_run_no_connector(auto_login_user, test_connector):
    client, user, workspace = auto_login_user()

    url = "/api/v1/external-runs/"

    response = client.post(url)

    assert response.status_code == 400
    assert response.json().get("error") == "You must provide a connector or connection_id"


@pytest.mark.django_db
def test_create_run_no_repo(auto_login_user, test_connector):
    client, user, workspace = auto_login_user()

    url = "/api/v1/external-runs/"

    response = client.post(
        url,
        {
            "connector_name": test_connector.name,
            "github_owner": "owner",
            "github_repo": "repo",
            "source_name": "test4",
        },
    )

    assert response.status_code == 400
    assert response.json().get("error") == "Repository not found, have you installed the Grai Github App?"


@pytest.mark.django_db
def test_create_run_connector_with_github(auto_login_user, test_connector, test_repository, mocker):
    mock = mocker.patch("connections.urls.Github")
    github_instance = MagicMock()
    check = types.SimpleNamespace()
    check.id = 1234
    github_instance.create_check.return_value = check
    github_instance.installation_id = 1234
    mock.return_value = github_instance

    client, user, workspace = auto_login_user()

    url = "/api/v1/external-runs/"
    response = client.post(
        url,
        {
            "connector_name": test_connector.name,
            "github_owner": test_repository.owner,
            "github_repo": test_repository.repo,
            "git_branch": "test_branch",
            "git_head_sha": "sha1234",
            "source_name": "test5",
        },
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    run = response.json()
    assert run["id"] is not None


@pytest.mark.django_db
def test_create_run_connector_with_commit(
    auto_login_user, test_connector, test_repository, test_branch, test_commit, mocker
):
    mock = mocker.patch("connections.urls.Github")
    github_instance = MagicMock()
    check = types.SimpleNamespace()
    check.id = 1234
    github_instance.create_check.return_value = check
    github_instance.installation_id = 1234
    mock.return_value = github_instance

    client, user, workspace = auto_login_user()

    url = "/api/v1/external-runs/"
    response = client.post(
        url,
        {
            "connector_name": test_connector.name,
            "github_owner": test_repository.owner,
            "github_repo": test_repository.repo,
            "git_branch": test_branch.reference,
            "git_head_sha": test_commit.reference,
            "source_name": "test6",
        },
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    run = response.json()
    assert run["id"] is not None


@pytest.mark.django_db
def test_create_run_connector_with_pull_request(
    auto_login_user, test_connector, test_repository, test_branch, test_commit, mocker
):
    mock = mocker.patch("connections.urls.Github")
    github_instance = MagicMock()
    check = types.SimpleNamespace()
    check.id = 1234
    github_instance.create_check.return_value = check
    github_instance.installation_id = 1234
    mock.return_value = github_instance

    client, user, workspace = auto_login_user()

    url = "/api/v1/external-runs/"
    response = client.post(
        url,
        {
            "connector_name": test_connector.name,
            "github_owner": test_repository.owner,
            "github_repo": test_repository.repo,
            "git_branch": test_branch.reference,
            "git_head_sha": test_commit.reference,
            "github_pr_reference": "123",
            "github_pr_title": "abc",
            "source_name": "test7",
        },
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    run = response.json()
    assert run["id"] is not None


@pytest.mark.django_db
def test_create_run_connector_with_existing_pull_request(
    auto_login_user,
    test_connector,
    test_repository,
    test_branch,
    test_pull_request,
    test_commit,
    mocker,
):
    mock = mocker.patch("connections.urls.Github")
    github_instance = MagicMock()
    check = types.SimpleNamespace()
    check.id = 1234
    github_instance.create_check.return_value = check
    github_instance.installation_id = 1234
    mock.return_value = github_instance

    client, user, workspace = auto_login_user()

    url = "/api/v1/external-runs/"
    response = client.post(
        url,
        {
            "connector_name": test_connector.name,
            "github_owner": test_repository.owner,
            "github_repo": test_repository.repo,
            "git_branch": test_branch.reference,
            "git_head_sha": test_commit.reference,
            "github_pr_reference": test_pull_request.reference,
            "github_pr_title": test_pull_request.title,
            "source_name": "test8",
        },
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    run = response.json()
    assert run["id"] is not None


@pytest.fixture
def hmac_secret() -> str:
    return "74d5de51a03ccbea9936aea756b2cc044d3816de"


@pytest.fixture
def test_connection_dbt_cloud(
    create_workspace, test_dbt_cloud_connector, hmac_secret, mocker, test_source
) -> Connection:
    mock = mocker.patch("connections.schedules.dbt_cloud.dbtCloudClient")

    dbt_cloud = types.SimpleNamespace()

    cloud = MagicMock()
    cloud.list_accounts.return_value = {"data": [{"id": 165072, "name": "test"}]}
    cloud.create_webhook.return_value = {
        "data": {
            "id": "1234webhook",
            "hmac_secret": hmac_secret,
        }
    }

    dbt_cloud.cloud = cloud

    mock.return_value = dbt_cloud

    workspace = create_workspace

    connection = Connection.objects.create(
        workspace=workspace,
        connector=test_dbt_cloud_connector,
        name=str(uuid.uuid4()),
        secrets={"api_key": "1234"},
        schedules={"dbt_cloud": {"job_id": "282191"}, "type": "dbt-cloud"},
        source=test_source,
    )

    return connection


@pytest.fixture
def test_connection_openlineage(create_workspace, test_openlineage_connector, test_source) -> Connection:
    connection = Connection.objects.create(
        workspace=create_workspace,
        connector=test_openlineage_connector,
        name=str(uuid.uuid4()),
        secrets={},
        source=test_source,
    )

    return connection


@pytest.mark.django_db
def test_dbt_cloud(test_connection_dbt_cloud, client, hmac_secret):
    url = "/api/v1/dbt-cloud/"

    body = {
        "accountId": 165072,
        "eventId": "wev_2PK5yEfjdZ7MJ78tUwedcI8TVWt",
        "timestamp": "2023-05-04T09:39:44.49564295Z",
        "eventType": "job.run.completed",
        "webhookId": "wsu_2PK4VE772408oHuYxq9BYDN6ONi",
        "webhookName": "Grai Webhook",
        "data": {
            "jobId": "282191",
            "jobName": "Production",
            "runId": "146889586",
            "environmentId": "189767",
            "environmentName": "Production",
            "dbtVersion": "1.4.6",
            "projectName": "Internal",
            "projectId": "242841",
            "runStatus": "Success",
            "runStatusCode": 10,
            "runStatusMessage": "None",
            "runReason": "Kicked off from the UI by edward@grai.io",
            "runStartedAt": "2023-05-04T09:39:02Z",
            "runFinishedAt": "2023-05-04T09:39:38Z",
        },
    }

    signature = hmac.new(hmac_secret.encode("utf-8"), json.dumps(body).encode("utf-8"), hashlib.sha256).hexdigest()

    response = client.post(
        url,
        body,
        headers={"authorization": signature},
        content_type="application/json",
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.django_db
def test_dbt_cloud_not_success(test_connection_dbt_cloud, client, hmac_secret):
    url = "/api/v1/dbt-cloud/"

    body = {
        "accountId": 165072,
        "eventId": "wev_2PK5yEfjdZ7MJ78tUwedcI8TVWt",
        "timestamp": "2023-05-04T09:39:44.49564295Z",
        "eventType": "job.run.completed",
        "webhookId": "wsu_2PK4VE772408oHuYxq9BYDN6ONi",
        "webhookName": "Grai Webhook",
        "data": {
            "jobId": "282191",
            "jobName": "Production",
            "runId": "146889586",
            "environmentId": "189767",
            "environmentName": "Production",
            "dbtVersion": "1.4.6",
            "projectName": "Internal",
            "projectId": "242841",
            "runStatus": "Running",
            "runStatusCode": 10,
            "runStatusMessage": "None",
            "runReason": "Kicked off from the UI by edward@grai.io",
            "runStartedAt": "2023-05-04T09:39:02Z",
            "runFinishedAt": "2023-05-04T09:39:38Z",
        },
    }

    signature = hmac.new(hmac_secret.encode("utf-8"), json.dumps(body).encode("utf-8"), hashlib.sha256).hexdigest()

    response = client.post(
        url,
        body,
        headers={"authorization": signature},
        content_type="application/json",
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    data = response.json()
    assert data["status"] == "not-success"


@pytest.mark.django_db
def test_dbt_cloud_no_connection(client, hmac_secret):
    url = "/api/v1/dbt-cloud/"

    body = {
        "accountId": 165072,
        "eventId": "wev_2PK5yEfjdZ7MJ78tUwedcI8TVWt",
        "timestamp": "2023-05-04T09:39:44.49564295Z",
        "eventType": "job.run.completed",
        "webhookId": "wsu_2PK4VE772408oHuYxq9BYDN6ONi",
        "webhookName": "Grai Webhook",
        "data": {
            "jobId": "282170",
            "jobName": "Production",
            "runId": "146889586",
            "environmentId": "189767",
            "environmentName": "Production",
            "dbtVersion": "1.4.6",
            "projectName": "Internal",
            "projectId": "242841",
            "runStatus": "Success",
            "runStatusCode": 10,
            "runStatusMessage": "None",
            "runReason": "Kicked off from the UI by edward@grai.io",
            "runStartedAt": "2023-05-04T09:39:02Z",
            "runFinishedAt": "2023-05-04T09:39:38Z",
        },
    }

    signature = hmac.new(hmac_secret.encode("utf-8"), json.dumps(body).encode("utf-8"), hashlib.sha256).hexdigest()

    response = client.post(
        url,
        body,
        headers={"authorization": signature},
        content_type="application/json",
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    data = response.json()
    assert data["status"] == "Connection not found"


@pytest.mark.django_db
def test_dbt_cloud_incorrect_signature(test_connection_dbt_cloud, client):
    url = "/api/v1/dbt-cloud/"

    body = {
        "accountId": 165072,
        "eventId": "wev_2PK5yEfjdZ7MJ78tUwedcI8TVWt",
        "timestamp": "2023-05-04T09:39:44.49564295Z",
        "eventType": "job.run.completed",
        "webhookId": "wsu_2PK4VE772408oHuYxq9BYDN6ONi",
        "webhookName": "Grai Webhook",
        "data": {
            "jobId": "282191",
            "jobName": "Production",
            "runId": "146889586",
            "environmentId": "189767",
            "environmentName": "Production",
            "dbtVersion": "1.4.6",
            "projectName": "Internal",
            "projectId": "242841",
            "runStatus": "Success",
            "runStatusCode": 10,
            "runStatusMessage": "None",
            "runReason": "Kicked off from the UI by edward@grai.io",
            "runStartedAt": "2023-05-04T09:39:02Z",
            "runFinishedAt": "2023-05-04T09:39:38Z",
        },
    }

    with pytest.raises(Exception) as e_info:
        client.post(
            url,
            body,
            headers={"authorization": "signature"},
            content_type="application/json",
        )

    assert str(e_info.value) == "Invalid dbt cloud webhook signature"


@pytest.mark.django_db
def test_dbt_cloud_not_active(test_connection_dbt_cloud, client, hmac_secret):
    test_connection_dbt_cloud.is_active = False
    test_connection_dbt_cloud.save()

    url = "/api/v1/dbt-cloud/"

    body = {
        "accountId": 165072,
        "eventId": "wev_2PK5yEfjdZ7MJ78tUwedcI8TVWt",
        "timestamp": "2023-05-04T09:39:44.49564295Z",
        "eventType": "job.run.completed",
        "webhookId": "wsu_2PK4VE772408oHuYxq9BYDN6ONi",
        "webhookName": "Grai Webhook",
        "data": {
            "jobId": "282191",
            "jobName": "Production",
            "runId": "146889586",
            "environmentId": "189767",
            "environmentName": "Production",
            "dbtVersion": "1.4.6",
            "projectName": "Internal",
            "projectId": "242841",
            "runStatus": "Success",
            "runStatusCode": 10,
            "runStatusMessage": "None",
            "runReason": "Kicked off from the UI by edward@grai.io",
            "runStartedAt": "2023-05-04T09:39:02Z",
            "runFinishedAt": "2023-05-04T09:39:38Z",
        },
    }

    signature = hmac.new(hmac_secret.encode("utf-8"), json.dumps(body).encode("utf-8"), hashlib.sha256).hexdigest()

    response = client.post(
        url,
        body,
        headers={"authorization": signature},
        content_type="application/json",
    )
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    data = response.json()
    assert data["status"] == "Connection not active"


@pytest.mark.django_db
def test_openlineage(client, test_connection_openlineage, workspace_api_key):
    url = reverse("connections:openlineage", args=[test_connection_openlineage.id])

    body = {}
    auth_headers = {
        "HTTP_AUTHORIZATION": f"Bearer {workspace_api_key}",
    }

    response = client.post(url, body, content_type="application/json", **auth_headers)

    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.django_db
def test_openlineage_no_connection(client, workspace_api_key):
    url = reverse("connections:openlineage", args=[uuid.uuid4()])

    body = {}
    auth_headers = {
        "HTTP_AUTHORIZATION": f"Bearer {workspace_api_key}",
    }
    response = client.post(url, body, content_type="application/json", **auth_headers)
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    data = response.json()
    assert data["status"] == "Connection not found"


@pytest.mark.django_db
def test_openlineage_invalid_api_key(client, test_connection_openlineage):
    url = reverse("connections:openlineage", args=[test_connection_openlineage.id])

    body = {}
    auth_headers = {
        "HTTP_AUTHORIZATION": f"Bearer {123}",
    }
    response = client.post(url, body, content_type="application/json", **auth_headers)
    assert response.status_code == 403, f"verb `get` failed on workspaces with status {response.status_code}"
    data = response.json()
    assert data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_openlineage_not_active(client, test_connection_openlineage, workspace_api_key):
    test_connection_openlineage.is_active = False
    test_connection_openlineage.save()

    url = reverse("connections:openlineage", args=[test_connection_openlineage.id])

    body = {}
    auth_headers = {
        "HTTP_AUTHORIZATION": f"Bearer {workspace_api_key}",
    }
    response = client.post(url, body, content_type="application/json", **auth_headers)
    assert response.status_code == 200, f"verb `get` failed on workspaces with status {response.status_code}"
    data = response.json()
    assert data["status"] == "Connection not active"

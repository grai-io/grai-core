import uuid

import pytest
from django_multitenant.utils import set_current_tenant

from installations.github import Github
from installations.models import Repository
from workspaces.models import Organisation, Workspace


@pytest.fixture
def create_organisation(name: str = None):
    return Organisation.objects.create(name=uuid.uuid4() if name is None else name)


@pytest.fixture
def create_workspace(create_organisation, name: str = None):
    return Workspace.objects.create(
        name=str(uuid.uuid4()) if name is None else name,
        organisation=create_organisation,
    )


@pytest.fixture
def create_repository(create_workspace):
    return Repository.objects.create(
        workspace=create_workspace, type="github", owner="owner", repo="repo", installation_id="1234"
    )


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def raise_for_status(self):
            pass

        def json(self):
            return self.json_data

    return MockResponse({"token": "tokenvalue", "expires_at": "1234"}, 200)


def mocked_requests_post_no_token(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def raise_for_status(self):
            pass

        def json(self):
            return self.json_data

    return MockResponse({"token": None, "expires_at": None, "message": "something went wrong"}, 200)


@pytest.mark.django_db
class TestInit:
    def test_init_with_installation_id(self, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        set_current_tenant(None)
        github = Github(owner="owner", repo="repo", installation_id="1234")
        assert github.owner == "owner"
        assert github.repo == "repo"
        assert github.installation_id == "1234"

    def test_init(self, create_repository, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        github = Github(owner="owner", repo="repo")
        assert github.owner == create_repository.owner
        assert github.repo == create_repository.repo
        assert github.installation_id == create_repository.installation_id

    def test_init_no_repository(self, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        with pytest.raises(Exception) as e_info:
            Github()
        assert str(e_info.value) == "Repository matching query does not exist."


@pytest.mark.django_db
class TestCreateCheck:
    def test_create_check(self, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        github = Github(owner="owner", repo="repo", installation_id="1234")

        check = github.create_check(head_sha="1234")

        assert check is not None

    def test_create_check_all(self, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        github = Github(owner="owner", repo="repo", installation_id="1234")

        check = github.create_check(
            head_sha="1234", external_id="123abc", name="Grai Tests", details_url="https://grai.io", output={}
        )

        assert check is not None

    def test_create_check_no_token(self, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post_no_token)

        with pytest.raises(Exception) as e_info:
            github = Github(owner="owner", repo="repo", installation_id="1234")
            github.create_check(head_sha="1234")

        assert str(e_info.value) == "something went wrong"


@pytest.mark.django_db
class TestStartCheck:
    def test_start_check(self, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        github = Github(owner="owner", repo="repo", installation_id="1234")

        check = github.create_check(head_sha="1234")
        github.start_check(check.id)


@pytest.mark.django_db
class TestCompleteCheck:
    def test_complete_check(self, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        github = Github(owner="owner", repo="repo", installation_id="1234")

        check = github.create_check(head_sha="1234")
        github.complete_check(check.id)


@pytest.mark.django_db
class TestGetRepos:
    def test_start_check(self, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        github = Github(owner="owner", repo="repo", installation_id="1234")

        repos = github.get_repos()

        assert repos is not None

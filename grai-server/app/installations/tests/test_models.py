import datetime
import uuid

import pytest

from installations.models import Branch, Commit, PullRequest, Repository
from workspaces.models import Organisation, Workspace


@pytest.fixture
def test_organisation():
    return Organisation.objects.create(name=str(uuid.uuid4()))


@pytest.fixture
def test_workspace(test_organisation):
    return Workspace.objects.create(name=str(uuid.uuid4()), organisation=test_organisation)


@pytest.fixture
def test_repository(test_workspace):
    return Repository.objects.create(
        workspace=test_workspace, type=Repository.GITHUB, owner=str(uuid.uuid4()), repo=str(uuid.uuid4())
    )


@pytest.fixture
def test_branch(test_workspace, test_repository):
    return Branch.objects.create(workspace=test_workspace, repository=test_repository, reference=str(uuid.uuid4()))


@pytest.mark.django_db
def test_repository_created(test_workspace):
    repository = Repository.objects.create(
        workspace=test_workspace, type=Repository.GITHUB, owner=str(uuid.uuid4()), repo=str(uuid.uuid4())
    )

    assert repository.id == uuid.UUID(str(repository.id))
    assert str(repository) == f"{repository.owner}/{repository.repo}"
    assert repository.type == Repository.GITHUB


@pytest.mark.django_db
def test_branch_created(test_workspace, test_repository):
    branch = Branch.objects.create(workspace=test_workspace, repository=test_repository, reference=str(uuid.uuid4()))

    assert branch.id == uuid.UUID(str(branch.id))
    assert str(branch) == branch.reference


@pytest.mark.django_db
def test_pull_request_created(test_workspace, test_repository, test_branch):
    pull_request = PullRequest.objects.create(
        workspace=test_workspace,
        repository=test_repository,
        branch=test_branch,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )

    assert pull_request.id == uuid.UUID(str(pull_request.id))
    assert str(pull_request) == pull_request.reference


@pytest.mark.django_db
def test_commit_created(test_workspace, test_repository, test_branch):
    commit = Commit.objects.create(
        workspace=test_workspace,
        repository=test_repository,
        branch=test_branch,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )

    assert commit.id == uuid.UUID(str(commit.id))
    assert str(commit) == commit.reference

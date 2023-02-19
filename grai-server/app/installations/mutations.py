import strawberry
from strawberry.types import Info

from api.common import IsAuthenticated, get_workspace
from api.types import BasicResult
from installations.github import Github
from installations.models import Repository as RepositoryModel


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def addInstallation(
        self,
        info: Info,
        workspaceId: strawberry.ID,
        installationId: int,
    ) -> BasicResult:
        workspace = await get_workspace(info, workspaceId)
        github = Github(installation_id=installationId)
        repos = github.get_repos()

        for repo in repos:
            await RepositoryModel.objects.aget_or_create(
                workspace=workspace,
                type=RepositoryModel.GITHUB,
                owner=repo.owner.login,
                repo=repo.name,
                installation_id=installationId,
            )

        return BasicResult(success=True)

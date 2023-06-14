from django.core.management.base import CommandError, CommandParser
from django_multitenant.utils import set_current_tenant
from django_tqdm import BaseCommand
from lineage.graph_cache import GraphCache
from workspaces.models import Workspace


class Command(BaseCommand):
    help = "Delete the lineage cache"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("workspace_id", type=str)

    def handle(self, *args, **options) -> None:
        workspace_id = options["workspace_id"]
        try:
            self.workspace = Workspace.objects.get(pk=workspace_id)

            set_current_tenant(self.workspace)

        except Workspace.DoesNotExist:
            raise CommandError('workspace "%s" does not exist' % workspace_id)

        self.cache = GraphCache(self.workspace)

        self.cache.clear_cache()
        self.stdout.write(self.style.SUCCESS('Successfully cleared cache for workspace "%s"' % self.workspace.name))

from django.core.management.base import CommandError, CommandParser
from django_multitenant.utils import set_current_tenant
from django_tqdm import BaseCommand
from query_chunk import chunk

from lineage.cache import GraphCache
from workspaces.models import Workspace


class Command(BaseCommand):
    help = "Build the lineage cache"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("workspace_id", type=str)

        parser.add_argument(
            "--delete",
            action="store_true",
        )

    def handle(self, *args, **options) -> None:
        workspace_id = options["workspace_id"]
        try:
            self.workspace = Workspace.objects.get(pk=workspace_id)

            set_current_tenant(self.workspace)

        except Workspace.DoesNotExist:
            raise CommandError('workspace "%s" does not exist' % workspace_id)

        self.cache = GraphCache(self.workspace)

        if options["delete"]:
            self.cache.clear_cache()
            self.stdout.write(self.style.SUCCESS('Successfully cleared cache for workspace "%s"' % self.workspace.name))

        self.build_cache()

        self.stdout.write(self.style.SUCCESS('Successfully built cache for workspace "%s"' % self.workspace.name))

    def build_cache(self):
        node_tqdm = self.tqdm(total=self.workspace.nodes.count())

        for node in chunk(self.workspace.nodes.all(), 10000):
            self.cache.cache_node(node)
            node_tqdm.update(1)

        edge_tqdm = self.tqdm(total=self.workspace.edges.count())

        for edge in chunk(self.workspace.edges.all(), 10000):
            self.cache.cache_edge(edge)
            edge_tqdm.update(1)

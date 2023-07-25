from typing import List

from django.core.management.base import CommandError, CommandParser
from django_multitenant.utils import set_current_tenant
from django_tqdm import BaseCommand
from query_chunk import chunk

from lineage.extended_graph_cache import ExtendedGraphCache
from workspaces.models import Workspace


class Command(BaseCommand):
    help = "Build the lineage cache"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("workspace_id", type=str, nargs="?", default=None)

        parser.add_argument(
            "--no-build",
            action="store_true",
        )

        parser.add_argument(
            "--layout",
            action="store_true",
        )

        parser.add_argument(
            "--delete",
            action="store_true",
        )

    def handle(self, *args, **options) -> None:
        workspace_id = options["workspace_id"]

        workspaces: List[Workspace] = []

        if workspace_id:
            try:
                workspace = Workspace.objects.get(pk=workspace_id)
                workspaces = [workspace]

            except Workspace.DoesNotExist:
                raise CommandError('workspace "%s" does not exist' % workspace_id)
        else:
            workspaces = Workspace.objects.all()

        for workspace in workspaces:
            self.handle_workspace(
                workspace,
                delete=options["delete"],
                layout=options["layout"],
                no_build=options["no_build"],
            )

    def handle_workspace(self, workspace: Workspace, delete: bool, layout: bool, no_build: bool):
        self.workspace = workspace

        set_current_tenant(self.workspace)

        self.cache = ExtendedGraphCache(self.workspace)

        if delete:
            self.cache.clear_cache()
            self.stdout.write(self.style.SUCCESS('Successfully cleared cache for workspace "%s"' % self.workspace.name))

        if not no_build:
            self.build_cache()

            self.stdout.write(self.style.SUCCESS('Successfully built cache for workspace "%s"' % self.workspace.name))

        if layout:
            self.stdout.write(self.style.SUCCESS('Starting layout cache for workspace "%s"' % self.workspace.name))

            self.cache.layout_graph()

            self.stdout.write(
                self.style.SUCCESS('Successfully layed out cache for workspace "%s"' % self.workspace.name)
            )

    def build_cache(self):
        node_tqdm = self.tqdm(total=self.workspace.nodes.count())

        for node in chunk(self.workspace.nodes.all(), 10000):
            self.cache.cache_node(node)
            node_tqdm.update(1)

        edge_tqdm = self.tqdm(total=self.workspace.edges.count())

        for edge in chunk(self.workspace.edges.all(), 10000):
            self.cache.cache_edge(edge)
            edge_tqdm.update(1)

from typing import List
from django.core.management.base import CommandError, CommandParser
from django_multitenant.utils import set_current_tenant
from django_tqdm import BaseCommand
from query_chunk import chunk
from grandalf.graphs import Vertex, Edge, Graph, graph_core
from grandalf.layouts import SugiyamaLayout

from lineage.graph_cache import GraphCache
from workspaces.models import Workspace


class Command(BaseCommand):
    help = "Build the lineage cache"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("workspace_id", type=str, nargs="?", default=None)

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
            self.handle_workspace(workspace, options["delete"])

    def handle_workspace(self, workspace: Workspace, delete: bool):
        self.workspace = workspace

        set_current_tenant(self.workspace)

        self.cache = GraphCache(self.workspace)

        if delete:
            self.cache.clear_cache()
            self.stdout.write(self.style.SUCCESS('Successfully cleared cache for workspace "%s"' % self.workspace.name))

        self.build_cache()

        self.layout_graph()

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

    def layout_graph(self):
        nodes = self.cache.get_tables()
        edges = self.cache.get_table_edges()

        vertexes = {}

        class defaultview(object):
            w, h = 100, 400

        for node in nodes:
            vertexes[node["id"]] = Vertex(node["id"])

        V = list(vertexes.values())

        for v in V:
            v.view = defaultview()

        E = [Edge(vertexes[edge["source_id"]], vertexes[edge["destination_id"]]) for edge in edges]

        # print(V)
        # print(E)

        g = Graph(V, E)

        sug = SugiyamaLayout(g.C[0])
        sug.init_all()
        sug.draw()

        for v in g.C[0].sV:
            self.cache.update_node(v.data, v.view.xy[1], v.view.xy[0])
            # print("%s: (%d,%d)" % (v.data, v.view.xy[0], v.view.xy[1]))

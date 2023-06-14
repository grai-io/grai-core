from typing import List
from django.core.management.base import CommandError, CommandParser
from django_multitenant.utils import set_current_tenant
from django_tqdm import BaseCommand
from query_chunk import chunk
from grandalf.graphs import Vertex, Edge, Graph
from grandalf.layouts import SugiyamaLayout

from lineage.graph_cache import GraphCache
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

        self.cache = GraphCache(self.workspace)

        if delete:
            self.cache.clear_cache()
            self.stdout.write(self.style.SUCCESS('Successfully cleared cache for workspace "%s"' % self.workspace.name))

        if not no_build:
            self.build_cache()

            self.stdout.write(self.style.SUCCESS('Successfully built cache for workspace "%s"' % self.workspace.name))

        if layout:
            self.stdout.write(self.style.SUCCESS('Starting layout cache for workspace "%s"' % self.workspace.name))

            self.layout_graph()

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

    def layout_graph(self):
        nodes = self.cache.get_tables()
        edges = self.cache.get_table_edges()

        vertexes = {}

        class defaultview(object):
            w, h = 200, 400

        for node in nodes:
            vertexes[node["id"]] = Vertex(node["id"])

        V = list(vertexes.values())

        for v in V:
            v.view = defaultview()

        E = [Edge(vertexes[edge["source_id"]], vertexes[edge["destination_id"]]) for edge in edges]

        g = Graph(V, E)

        print(len(V))
        print(len(E))
        print(len(g.C))

        graphs = []
        single_tables = []

        for graph in g.C:
            if len(graph.sV) == 1:
                node = graph.sV[0]

                single_tables.append(node)
                continue

            sug = SugiyamaLayout(graph)
            sug.init_all()
            sug.draw(20)

            minX = 0
            maxX = 0
            # minY = 0
            # maxY = 0

            for vertex in graph.sV:
                minX = min(minX, vertex.view.xy[1])
                maxX = max(maxX, vertex.view.xy[1])
                # minY = min(minY, vertex.view.xy[0])
                # maxY = max(maxY, vertex.view.xy[0])

            graphs.append(
                {
                    "minX": minX,
                    "maxX": maxX,
                    # "minY": minY,
                    # "maxY": maxY,
                    "nodes": graph.sV,
                }
            )

        x = 0
        y = 0

        for graph in graphs:
            for v in graph["nodes"]:
                self.cache.update_node(v.data, v.view.xy[1] + x + graph["minX"], v.view.xy[0])

            x += graph["maxX"] - graph["minX"] + 400

        start_x = x
        index = 0

        for table in single_tables:
            self.cache.update_node(table.data, x, y)

            if index > 20:
                y += 200
                x = start_x
                index = 0
                continue

            x += 500
            index += 1

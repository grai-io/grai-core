from celery import shared_task

from .graph_cache import GraphCache


@shared_task
def cache_node(id, delete: bool = False):
    from .models import Node

    node = Node.objects.get(pk=id)

    cache = GraphCache(node.workspace)
    if delete:
        cache.delete_node(node)
    else:
        cache.cache_node(node)

    layout(node.workspace.id)


@shared_task
def cache_edge(id, delete: bool = False):
    from .models import Edge

    edge = Edge.objects.get(pk=id)

    cache = GraphCache(edge.workspace)
    if delete:
        cache.delete_edge(edge)
    else:
        cache.cache_edge(edge)

    layout(edge.workspace.id)


@shared_task
def layout(id):
    from workspaces.models import Workspace

    workspace = Workspace.objects.get(pk=id)

    cache = GraphCache(workspace)

    cache.layout_graph()

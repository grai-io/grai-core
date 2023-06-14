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


@shared_task
def cache_edge(id, delete: bool = False):
    from .models import Edge

    edge = Edge.objects.get(pk=id)

    cache = GraphCache(edge.workspace)
    if delete:
        cache.delete_edge(edge)
    else:
        cache.cache_edge(edge)

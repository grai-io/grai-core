from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .graph_cache import GraphCache
from .models import Edge, Node, Source


@receiver(m2m_changed)
def post_m2m_changed(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    if action not in ["post_add", "post_remove", "post_clear"]:
        return

    if sender.__name__ not in ["Source_nodes", "Source_edges"]:
        return

    graph = GraphCache(instance.workspace_id)

    if model == Node:
        nodes = Node.objects.filter(pk__in=pk_set)

        for node in nodes:
            graph.cache_node(node)

    elif model == Edge:
        edges = Edge.objects.filter(pk__in=pk_set)

        for edge in edges:
            graph.cache_edge(edge)

    # else:
    #     raise Exception("Unexpected model type")

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .graph_cache import GraphCache
from .models import Node, Edge, Source


@receiver(m2m_changed)
def post_m2m_changed(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    if action not in ["post_add", "post_remove", "post_clear"]:
        return

    if sender.__name__ not in ["Source_nodes", "Source_edges"]:
        return

    if model not in [Node, Edge]:
        return

    graph = GraphCache(instance.workspace)

    if model == Node:
        nodes = Node.objects.filter(pk__in=pk_set)

        for node in nodes:
            graph.cache_node(node)

        return

    edges = Edge.objects.filter(pk__in=pk_set)

    for edge in edges:
        graph.cache_edge(edge)

from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Node


@register(Node)
class NodeIndex(AlgoliaIndex):
    fields = (
        "workspace_id",
        "id",
        "namespace",
        "name",
        "display_name",
        "data_source",
        "search_type",
        "is_active",
        "table_id",
    )
    settings = {
        "searchableAttributes": ["id", "namespace", "name", "display_name", "data_source"],
        "attributesForFaceting": ["workspace_id"],
    }
    index_name = "main"

from typing import List

from asgiref.sync import sync_to_async
from django.db import connection
from django.db.models import Q
from django.db.models.query import QuerySet
from workspaces.models import Workspace

from .models import Filter, Node


def get_ascestor_ids_by_tag(tag: str):
    nodes = Node.objects.raw(
        """WITH RECURSIVE list_nodes AS (
      SELECT nodes.id
      FROM public.lineage_node nodes
      WHERE (metadata->'grai'->>'tags')::jsonb ? %s
    UNION
      SELECT n.id
      FROM public.lineage_node n
      LEFT JOIN public.lineage_edge edges ON edges.destination_id = n.id
      LEFT JOIN public.lineage_edge up_edges ON up_edges.source_id = n.id AND up_edges.metadata->'grai'->>'edge_type' = 'TableToColumn'
      INNER JOIN list_nodes listn ON listn.id = edges.source_id OR listn.id = up_edges.destination_id
    )
SELECT *
FROM list_nodes""",
        [tag],
    )

    return [node.id for node in nodes]


def get_descendent_ids_by_tag(tag: str):
    nodes = Node.objects.raw(
        """WITH RECURSIVE list_nodes AS (
      SELECT nodes.id
      FROM public.lineage_node nodes
      WHERE (metadata->'grai'->>'tags')::jsonb ? %s
    UNION
      SELECT n.id
      FROM public.lineage_node n
      LEFT JOIN public.lineage_edge edges ON edges.source_id = n.id
      LEFT JOIN public.lineage_edge up_edges ON up_edges.destination_id = n.id AND up_edges.metadata->'grai'->>'edge_type' = 'TableToColumn'
      INNER JOIN list_nodes listn ON listn.id = edges.destination_id OR listn.id = up_edges.source_id
    )
SELECT *
FROM list_nodes""",
        [tag],
    )

    return [node.id for node in nodes]


async def apply_table_filter(queryset: QuerySet, filter: Filter):
    q_filter = Q()

    for row in filter.metadata:
        if row["type"] == "table":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    q_filter &= Q(metadata__grai__tags__contains=row["value"])
        elif row["type"] == "ancestor":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    ids = await sync_to_async(get_ascestor_ids_by_tag)(row["value"])
                    q_filter &= Q(id__in=ids)
        elif row["type"] == "no-ancestor":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    ids = await sync_to_async(get_ascestor_ids_by_tag)(row["value"])
                    q_filter &= ~Q(id__in=ids)
        elif row["type"] == "descendant":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    ids = await sync_to_async(get_descendent_ids_by_tag)(row["value"])
                    q_filter &= Q(id__in=ids)
        elif row["type"] == "no-descendant":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    ids = await sync_to_async(get_descendent_ids_by_tag)(row["value"])
                    q_filter &= ~Q(id__in=ids)
        else:
            raise Exception("Unknown filter type: " + row["type"])

    return queryset.filter(q_filter)


def get_tags(workspace: Workspace) -> List[str]:
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT DISTINCT tags #>> '{}'
FROM
(
    SELECT id, JSONB_ARRAY_ELEMENTS((metadata->'grai'->>'tags')::jsonb) AS tags
    FROM public.lineage_node
    WHERE workspace_id = %s
) AS foo""",
            [workspace.id],
        )
        rows = cursor.fetchall()

    return list([row[0] for row in rows])

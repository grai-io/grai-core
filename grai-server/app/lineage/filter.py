from django.db.models import Q
from django.db.models.query import QuerySet

from .models import Filter


def apply_table_filter(queryset: QuerySet, filter: Filter):
    q_filter = Q()

    for row in filter.metadata:
        if row["type"] == "table":
            if row["field"] == "tag":
                if row["operator"] == "contains":
                    q_filter &= Q(metadata__grai__tags__contains=row["value"])
        # elif row["type"] == "no-descendant":
        #     if row["field"] == "tag":
        #         if row["operator"] == "contains":
        #             q_filter &= ~Q(source_edges__destination__metadata__grai__tags__contains=row["value"])

    return queryset.filter(q_filter)

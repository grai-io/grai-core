from typing import Any, Iterable, List, Sequence

from django.db import models
from django_multitenant.models import TenantManagerMixin
from psqlextra.manager import PostgresManager

from .graph_cache import GraphCache


class CacheManager(TenantManagerMixin, models.Manager):
    def bulk_create(
        self,
        objs: Iterable[Any],
        batch_size: int | None = None,
        **kwargs,
    ) -> List:
        result = super().bulk_create(objs, **kwargs)

        if len(list(objs)) > 0:
            workspace = objs[0].workspace
            cache = GraphCache(workspace)

            for obj in objs:
                obj.cache_model(cache)

            cache.layout_graph()

        return result

    def bulk_update(
        self,
        objs: Iterable[Any],
        fields: Sequence[str],
        **kwargs,
    ) -> int:
        result = super().bulk_update(
            objs,
            fields,
            **kwargs,
        )

        if len(list(objs)) > 0:
            workspace = objs[0].workspace
            cache = GraphCache(workspace)

            for obj in objs:
                obj.cache_model(cache)

            cache.layout_graph()

        return result


class SourceManager(TenantManagerMixin, PostgresManager):
    pass

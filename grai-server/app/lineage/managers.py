from typing import Iterable, List, Sequence

from django.db import models
from django_multitenant.models import TenantManagerMixin

from .graph_cache import GraphCache


class CacheManager(TenantManagerMixin, models.Manager):
    def bulk_create(
        self,
        objs: Iterable,
        batch_size: int = None,
        **kwargs,
    ) -> List:
        result = super().bulk_create(objs, **kwargs)

        if len(objs) > 0:
            workspace = objs[0].workspace
            cache = GraphCache(workspace)

            for obj in objs:
                obj.cache_model(cache)

        return result

    def bulk_update(
        self,
        objs: Iterable,
        fields: Sequence[str],
        **kwargs,
    ) -> int:
        result = super().bulk_update(
            objs,
            fields,
            **kwargs,
        )

        if len(objs) > 0:
            workspace = objs[0].workspace
            cache = GraphCache(workspace)

            for obj in objs:
                obj.cache_model(cache)

        return result

from typing import Iterable, List, Optional, Sequence

from django.db import models
from django_multitenant.models import TenantManagerMixin

from .graph_cache import GraphCache


class CacheManager(TenantManagerMixin, models.Manager):
    def bulk_create(
        self,
        objs: Iterable,
        batch_size: int = None,
        ignore_conflicts: bool = False,
        update_conflicts: Sequence[str] = None,
        update_fields: Sequence[str] = None,
    ) -> List:
        result = super().bulk_create(objs, batch_size, ignore_conflicts, update_conflicts, update_fields)

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
        batch_size: int = None,
    ) -> int:
        result = super().bulk_update(objs, fields, batch_size)

        if len(objs) > 0:
            workspace = objs[0].workspace
            cache = GraphCache(workspace)

            for obj in objs:
                obj.cache_model(cache)

        return result

from typing import Any, Iterable, List, Sequence

from django.db import models
from django_multitenant.models import TenantManagerMixin
from psqlextra.manager import PostgresManager

from .graph_cache import GraphCache
from lineage.tasks import update_node_vector_index, EmbeddingTaskStatus
from django.core.cache import cache
from typing import TYPE_CHECKING, Iterator
import uuid

if TYPE_CHECKING:
    from lineage.models import Node


class CacheManager(TenantManagerMixin, models.Manager):
    @staticmethod
    def update_cache(objs: list):
        workspace = objs[0].workspace
        cache = GraphCache(workspace)

        for obj in objs:
            obj.cache_model(cache)

        cache.layout_graph()

    def bulk_create(
        self,
        objs: Iterable[Any],
        batch_size: int | None = None,
        **kwargs,
    ) -> List:
        objs = list(objs)

        result = super().bulk_create(objs, **kwargs)

        if len(objs) > 0:
            self.update_cache(objs)

        return result

    def bulk_update(
        self,
        objs: Iterable[Any],
        fields: Sequence[str],
        **kwargs,
    ) -> int:
        objs = list(objs)

        result = super().bulk_update(
            objs,
            fields,
            **kwargs,
        )

        if len(objs) > 0:
            self.update_cache(objs)

        return result


class NodeEmbeddingManager(models.Manager):
    @staticmethod
    def obj_generator(objs: Iterable["Node"], task_id: uuid.UUID) -> Iterator["Node"]:
        cache.set(f"lineage:NodeEmbeddingTasks:{task_id}", EmbeddingTaskStatus.WAIT, timeout=60 * 60 * 24)
        for obj in objs:
            yield obj
            update_node_vector_index.delay(obj.id)

    @staticmethod
    def start_task(task_id: uuid.UUID):
        cache_key = f"lineage:NodeEmbeddingTasks:{task_id}"
        cache.delete(cache_key)

    def bulk_create(self, objs: Iterable[Any], **kwargs) -> List:
        task_id = uuid.uuid4()
        result = super().bulk_create(self.obj_generator(objs, task_id), **kwargs)
        self.start_task(task_id)
        return result

    def bulk_update(self, objs: Iterable[Any], fields: Sequence[str], **kwargs) -> int:
        task_id = uuid.uuid4()
        result = super().bulk_update(self.obj_generator(objs, task_id), fields, **kwargs)
        self.start_task(task_id)
        return result


class NodeManager(NodeEmbeddingManager, CacheManager):
    pass


class SourceManager(TenantManagerMixin, PostgresManager):
    pass

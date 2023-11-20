import logging
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

import openai
from django.apps import apps
from django.core.cache import cache
from django_celery_beat.models import PeriodicTask, PeriodicTasks
from grai_schemas.serializers import GraiYamlSerializer

from celery import shared_task

if TYPE_CHECKING:
    from lineage.models import Node


class EmbeddingTaskStatus:
    WAIT = 0


def create_node_vector_index(node: "Node"):
    from connections.adapters.schemas import model_to_schema
    from lineage.models import NodeEmbeddings

    schema = model_to_schema(node, "NodeV1")
    content = GraiYamlSerializer.dump(schema)
    embedding_resp = openai.Embedding.create(input=content, model="text-embedding-ada-002")
    NodeEmbeddings.objects.update_or_create(node=node, embedding=embedding_resp.data[0].embedding)


def get_embedding_task_state(task_id: UUID | None) -> int | None:
    if task_id is None:
        return task_id

    cache_key = f"lineage:NodeEmbeddingTasks:{task_id}"
    return cache.get(cache_key, None)


@shared_task(bind=True, max_retries=None)
def update_node_vector_index(self, node_id: UUID, task_id: UUID | None = None):
    from lineage.models import Node

    logging.info(f"Creating embedding for node {node_id}")

    task_status = get_embedding_task_state(task_id)
    if task_status == EmbeddingTaskStatus.WAIT:
        logging.info(f"Task {task_id} is waiting")
        self.retry(countdown=10)
        return

    node = Node.objects.get(id=node_id)
    try:
        create_node_vector_index(node)
    except openai.error.RateLimitError:
        logging.info(f"Openai rate limit reach retrying in 10 seconds")
        self.retry(countdown=10)
        return


@shared_task
def bulk_update_embeddings():
    from lineage.models import Node

    task = PeriodicTask.objects.get(name="lineage:Node:bulk_update_embeddings")
    last_run_at = task.last_run_at if task.last_run_at is not None else datetime.min

    for node in Node.objects.filter(updated_at__gt=last_run_at).all():
        update_node_vector_index.delay(node.id)

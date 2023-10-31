from celery import shared_task
from uuid import UUID
import openai
import logging
from grai_schemas.serializers import GraiYamlSerializer
from django_celery_beat.models import PeriodicTask, PeriodicTasks
from datetime import datetime
from typing import TYPE_CHECKING
from django.apps import apps

if TYPE_CHECKING:
    from lineage.models import Node


def create_node_vector_index(node: "Node"):
    from connections.adapters.schemas import model_to_schema
    from lineage.models import NodeEmbeddings

    schema = model_to_schema(node, "NodeV1")
    content = GraiYamlSerializer.dump(schema)
    try:
        embedding_resp = openai.Embedding.create(input=content, model="text-embedding-ada-002")
    except:
        raise Exception(f"Encountered openai API error while creating embedding for {node_id}")

    NodeEmbeddings.objects.update_or_create(node=node, embedding=embedding_resp.data[0].embedding)


@shared_task
def update_node_vector_index(node_id: UUID):
    from lineage.models import Node

    logging.info(f"Creating embedding for node {node_id}")
    node = Node.objects.get(id=node_id)
    create_node_vector_index(node)


@shared_task
def bulk_update_embeddings():
    from lineage.models import Node

    task = PeriodicTask.objects.get(name="lineage:Node:bulk_update_embeddings")
    last_run_at = task.last_run_at if task.last_run_at is not None else datetime.min

    for node in Node.objects.filter(updated_at__gt=last_run_at).all():
        update_node_vector_index.delay(node.id)

import uuid

from django.db import models
from django.db.models import F, Q
from django_multitenant.models import TenantModel
from grai_schemas.serializers import GraiEncoder


from .graph_cache import GraphCache
from .graph_tasks import cache_edge, cache_node
from .managers import CacheManager, SourceManager
from pgvector.django import VectorField, HnswIndex
from django.conf import settings
from lineage.tasks import update_node_vector_index


class Node(TenantModel):
    objects = CacheManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    namespace = models.TextField(default="default")
    name = models.TextField()
    display_name = models.TextField()
    metadata = models.JSONField(default=dict, encoder=GraiEncoder)
    is_active = models.BooleanField(default=True)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="nodes",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.OneToOneField(
    #     "users.User", related_name="created_by", on_delete=models.PROTECT
    # )

    def search_type(self):
        return self.metadata.get("grai", {}).get("node_type", "Node")

    def search_enabled(self):
        return self.workspace.search_enabled

    def table_id(self):
        if self.search_type() == "Table":
            return self.id

        if self.search_type() == "Column":
            table = self.destination_edges.filter(metadata__grai__edge_type="TableToColumn").first()
            return table.source.id if table is not None else None

    def save(self, *args, **kwargs):
        self.set_names()
        super().save(*args, **kwargs)
        self.cache_model()

        if self.workspace.ai_enabled and settings.HAS_OPENAI:
            update_node_vector_index.delay(self.id)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cache_model(delete=True)

    def set_names(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.name
        return self

    def cache_model(self, cache: GraphCache | None = None, delete: bool = False):
        if cache:
            cache.cache_node(self)
        else:
            cache_node.delay(self.id, delete=delete)

    def __str__(self):
        return f"{self.display_name}"

    class TenantMeta:
        tenant_field_name = "workspace_id"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "namespace", "name"],
                name="Node namespaces/name uniqueness",
            )
        ]
        indexes = [
            models.Index(fields=["workspace", "namespace", "name"]),
            models.Index(
                "workspace",
                models.F("metadata__grai__node_type"),
                name="lineage_node_type",
            ),
        ]


class NodeEmbeddings(models.Model):
    embedding = VectorField(dimensions=1536)
    node = models.OneToOneField(
        Node,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        indexes = [
            HnswIndex(
                name="node_embedding_index",
                fields=["embedding"],
                m=64,
                ef_construction=128,  # should be at least 2x m.
                opclasses=["vector_ip_ops"],
            )
        ]


class Edge(TenantModel):
    objects = CacheManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    namespace = models.TextField(default="default")
    display_name = models.TextField()
    metadata = models.JSONField(default=dict, encoder=GraiEncoder)
    is_active = models.BooleanField(default=True)

    source = models.ForeignKey("Node", related_name="source_edges", on_delete=models.PROTECT)
    destination = models.ForeignKey("Node", related_name="destination_edges", on_delete=models.PROTECT)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="edges",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.OneToOneField("users.User", on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.set_names()
        super().save(*args, **kwargs)
        self.cache_model()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cache_model(delete=True)

    def set_names(self):
        if not self.name:
            self.name = str(self)
        if not self.display_name:
            self.display_name = self.name
        return self

    def cache_model(self, cache: GraphCache = None, delete: bool = False):
        if cache:
            cache.cache_edge(self)
        else:
            cache_edge.delay(self.id, delete=delete)

    def __str__(self):
        return f"{self.source} -> {self.destination}"

    class TenantMeta:
        tenant_field_name = "workspace_id"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(source=F("destination")),
                name="Edges are not allowed between the same nodes",
            ),
            models.UniqueConstraint(
                fields=["workspace", "namespace", "name"],
                name="Edge namespaces/name uniqueness",
            ),
            models.UniqueConstraint(
                fields=["source", "destination"],
                condition=Q(is_active=True),
                name="one_active_edge_between_nodes",
            ),
        ]
        indexes = [
            models.Index(fields=["workspace", "is_active"]),
            models.Index(fields=["workspace", "namespace", "name"]),
            models.Index(fields=["workspace", "source", "destination"]),
            models.Index(
                "workspace",
                models.F("metadata__grai__edge_type"),
                name="lineage_edge_type",
            ),
            models.Index(
                models.F("metadata__grai__edge_type"),
                "source",
                name="lineage_edge_type_source",
            ),
            models.Index(
                models.F("metadata__grai__edge_type"),
                "destination",
                name="lineage_edge_type_destination",
            ),
        ]


class Filter(TenantModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    metadata = models.JSONField(default=dict)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="filters",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "users.User",
        related_name="filters",
        on_delete=models.CASCADE,
    )

    class TenantMeta:
        tenant_field_name = "workspace_id"


class Event(TenantModel):
    SUCCESS = "success"
    ERROR = "error"
    CANCELLED = "cancelled"

    EVENT_STATUS = [
        (SUCCESS, "success"),
        (ERROR, "error"),
        (CANCELLED, "cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=255)
    date = models.DateTimeField()
    status = models.CharField(max_length=255, choices=EVENT_STATUS, default="success")
    metadata = models.JSONField(default=dict)

    connection = models.ForeignKey(
        "connections.Connection",
        related_name="events",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    nodes = models.ManyToManyField(Node)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="events",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class TenantMeta:
        tenant_field_name = "workspace_id"


class Source(TenantModel):
    objects = SourceManager()

    tenant_id = "workspace_id"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    priority = models.IntegerField(default=0)

    workspace = models.ForeignKey(
        "workspaces.Workspace",
        related_name="sources",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    nodes = models.ManyToManyField(Node, related_name="data_sources")
    edges = models.ManyToManyField(Edge, related_name="data_sources")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "name"],
                name="Source name uniqueness",
            ),
        ]
        indexes = [
            models.Index(fields=["workspace", "name"]),
        ]

    def __str__(self):
        return self.name

    class TenantMeta:
        tenant_field_name = "workspace_id"

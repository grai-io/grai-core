import uuid
from abc import ABC, abstractmethod

from lineage.models import Edge, Node, NodeEmbeddings, Source
from pydantic import BaseModel, Field
from grai_schemas.serializers import GraiYamlSerializer
from django.db.models import Q
from channels.db import database_sync_to_async
from pgvector.django import MaxInnerProduct

from typing import Annotated, Any, Callable, Literal, ParamSpec, Type, TypeVar, Union
from connections.adapters.schemas import model_to_schema
import tiktoken
import openai
from grai_schemas.v1.edge import EdgeV1
from grAI.encoders import Embedder


T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")

RoleType = Union[Literal["user"], Literal["system"], Literal["assistant"]]


def filter_node_content(node: "Node") -> dict:
    from connections.adapters.schemas import model_to_schema

    spec_keys = ["name", "namespace", "metadata", "data_sources"]

    result: dict = model_to_schema(node, "NodeV1").spec.dict(exclude_none=True)
    result = {key: result[key] for key in spec_keys}
    result["metadata"] = result["metadata"]["grai"]
    return result


class API(ABC):
    schema_model: BaseModel
    description: str
    id: str

    @abstractmethod
    def call(self, **kwargs) -> (Any, str):
        pass

    def serialize(self, result) -> str:
        if isinstance(result, str):
            return result

        return GraiYamlSerializer.dump(result)

    async def response(self, **kwargs) -> str:
        obj, message = await self.call(**kwargs)

        if message is None:
            result = self.serialize(obj)
        else:
            result = f"{self.serialize(obj)}\n{message}"

        return result

    def gpt_definition(self) -> dict:
        return {
            "type": "function",
            "function": {"name": self.id, "description": self.description, "parameters": self.schema_model.schema()},
        }


class NodeIdentifier(BaseModel):
    name: str = Field(description="The nodes name")
    namespace: str = Field(description="The nodes namespace")
    request_context: str = Field(description="A brief description of the relevant data needed from the node.")


class NodeLookupAPI(API):
    id = "node_lookup"
    description = "Lookup metadata about one or more nodes if you know precisely which node to lookup"
    schema_model = NodeIdentifier

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace

    @staticmethod
    def response_message(result_set: list) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching the query."
        else:
            message = None

        return message

    @database_sync_to_async
    def call(self, **kwargs) -> (list[Node], str | None):
        def reduce_response(response: Node) -> dict:
            try:
                parsed: dict = model_to_schema(response, "NodeV1").spec.dict()
            except:
                return {}

            spec_keys = ["name", "namespace", "display_name", "metadata", "data_sources"]

            reduced_response = {key: parsed[key] for key in spec_keys}
            reduced_response["metadata"] = reduced_response["metadata"]["grai"]
            return reduced_response

        validation = self.schema_model(**kwargs)
        query = Q(name=validation.name, namespace=validation.namespace)
        result_query = Node.objects.filter(workspace=self.workspace).filter(query).prefetch_related("data_sources")
        response_items = [reduce_response(node) for node in result_query.all()]

        return response_items, self.response_message(response_items)


class SourceIdentifier(BaseModel):
    name: str | None = Field(description="The name of the source to lookup or None to return all sources", default=None)


class SourceLookupAPI(API):
    id = "source_lookup"
    description = "Lookup metadata about one or more nodes if you know precisely which node to lookup"
    schema_model = SourceIdentifier

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace

    def response_message(self, result_set: list) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching the query."
        else:
            message = None

        return message

    @database_sync_to_async
    def call(self, **kwargs) -> (list[Node], str | None):
        def reduce_response(response: Node) -> dict:
            try:
                parsed: dict = model_to_schema(response, "SourceV1").spec.dict()
            except:
                parsed = {}

            return parsed

        validation = self.schema_model(**kwargs)
        query = Q()
        if validation.name is not None:
            query |= Q(name=validation.name)

        result_query = Source.objects.filter(workspace=self.workspace).filter(query)
        response_items = [reduce_response(source) for source in result_query.all()]

        return response_items, self.response_message(response_items)


class FuzzyMatchQuery(BaseModel):
    string: str = Field(description="The fuzzy string used to search amongst node names")


class FuzzyMatchNodesAPI(API):
    id = "node_fuzzy_lookup"
    description = "Performs a fuzzy search for nodes matching a name regardless of namespace"
    schema_model = FuzzyMatchQuery

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace

    @staticmethod
    def response_message(result_set: list[Node]) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching these query conditions."
        else:
            message = None

        return message

    @database_sync_to_async
    def call(self, string: str) -> (list, str | None):
        query = Q(name__contains=string) | Q(display_name__contains=string)
        result_set = Node.objects.filter(workspace=self.workspace).filter(query).order_by("-created_at").all()
        response_items = [
            {"name": node.name, "namespace": node.namespace, "display_name": node.display_name} for node in result_set
        ]

        return response_items, self.response_message(result_set)


class EdgeLookupSchema(BaseModel):
    source: NodeIdentifier = Field(description="The primary key of the source node on an edge")
    destination: NodeIdentifier = Field(description="The primary key of the destination node on an edge")
    request_context: str = Field(description="A brief description of the relevant data needed about the node.")


class EdgeLookupAPI(API):
    id = "edge_lookup"
    description = """
    This function Supports looking up edges from a data lineage graph. For example, a query with name=Test but no
    namespace value will return all edges explicitly named "Test" regardless of namespace.
    Edges are uniquely identified both by their (name, namespace), and by the (source, destination) nodes they connect.
    """
    schema_model = EdgeLookupSchema

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace

    @staticmethod
    def response_message(result_set: list[Edge]) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching these query conditions."
        else:
            message = None

        return message

    @database_sync_to_async
    def call(self, **kwargs) -> tuple[list[EdgeV1], str | None]:
        try:
            validation = self.schema_model(**kwargs)
        except Exception as e:
            return [], f"Invalid input. {e}"

        query = Q()
        query &= Q(source__name=validation.source.name, source__namespace=validation.source.namespace)
        query &= Q(
            destination__name=validation.destination.name, destination__namespace=validation.destination.namespace
        )

        results = Edge.objects.filter(workspace=self.workspace).filter(query).all()
        return model_to_schema(results, "EdgeV1"), self.response_message(results)


class NHopQuerySchema(BaseModel):
    name: str = Field(description="The name of the node to query for")
    namespace: str = Field(description="The namespace of the node to query for")
    n: int = Field(description="The number of hops to query for", default=1)
    request_context: str = Field(description="A brief description of the relevant data needed about the node.")


class NHopQueryAPI(API):
    id: str = "n_hop_query"
    description: str = """Query for a list of edges up to n hops in the graph from a node.
    Edges are identified (source, destination node, edge type) e.g.

    RESPONSE:
    (name1,namespace1),(name2,namespace2),edge_type
    ...
    """
    schema_model = NHopQuerySchema

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace

    @staticmethod
    def response_message(result_set: list[str]) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching these query conditions."
        else:
            message = None

        return message

    @staticmethod
    def filter(queryset: list[Edge], source_nodes: list[Node], dest_nodes: list[Node]) -> tuple[list[Node], list[Node]]:
        def get_id(node: Edge | Node) -> tuple[str, str]:
            return node.name, node.namespace

        source_ids: set[T] = {get_id(node) for node in source_nodes}
        dest_ids: set[T] = {get_id(node) for node in dest_nodes}
        query_hashes: set[tuple[T, T]] = {(get_id(node.source), get_id(node.destination)) for node in queryset}

        source_resp = [n.destination for n, hashes in zip(queryset, query_hashes) if hashes[0] in source_ids]
        dest_resp = [n.source for n, hashes in zip(queryset, query_hashes) if hashes[1] in dest_ids]
        return source_resp, dest_resp

    @database_sync_to_async
    def call(self, **kwargs) -> (list[dict], str | None):
        def filter_edge(edge: EdgeV1) -> dict:
            result = {
                "name": edge.spec.name,
                "namespace": edge.spec.namespace,
                "source": edge.spec.source,
                "destination": edge.spec.destination,
                "edge_type": edge.spec.metadata.grai.edge_type,
            }
            return result

        try:
            inp = self.schema_model(**kwargs)
        except Exception as e:
            return [], f"Invalid input: {e}"

        source_node = Node.objects.filter(workspace__id=self.workspace, name=inp.name, namespace=inp.namespace).first()
        if source_node is None:
            return [], self.response_message([])

        source_nodes = [source_node]
        dest_nodes = [source_node]

        return_edges = []
        for i in range(inp.n):
            query = Q(source__in=source_nodes) | Q(destination__in=dest_nodes)
            edges = Edge.objects.filter(query).prefetch_related("source", "destination").all()

            source_nodes, dest_nodes = self.filter(edges, source_nodes, dest_nodes)
            return_edges.extend(list(edges))

            if len(source_nodes) == 0 and len(dest_nodes) == 0:
                break

        results = set(model_to_schema(return_edges, "EdgeV1"))
        results = [filter_edge(item) for item in results]
        return results, self.response_message(return_edges)


class EmbeddingSearchSchema(BaseModel):
    search_term: str = Field(description="Search request string")
    limit: int = Field(description="number of results to return", default=10)


class EmbeddingSearchAPI(API):
    id: str = "embedding_search_api"
    description: str = (
        "Search for nodes matching any query. Results are returned in the following format:\n"
        "(node1 name, node1 namespace, node1 type)\n(node2 name, node2 namespace, node2 type)\n..."
    )
    schema_model = EmbeddingSearchSchema

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace

    @staticmethod
    def response_message(result_set: list) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching these query conditions."
        else:
            message = None

        return message

    @database_sync_to_async
    def nearest_neighbor_search(self, vector_query: list[int], limit=10) -> list[Node]:
        node_result = (
            NodeEmbeddings.objects.filter(node__workspace__id=self.workspace)
            .order_by(MaxInnerProduct("embedding", vector_query))
            .select_related("node")[:limit]
        )

        return [n.node for n in node_result]

    async def call(self, **kwargs) -> tuple[str, str | None]:
        try:
            inp = self.schema_model(**kwargs)
        except Exception as e:
            return f"Invalid input. {e}", None

        embedding_resp = await Embedder.get_embedding(inp.search_term)
        embedding = list(embedding_resp.data[0].embedding)

        neighbors = await self.nearest_neighbor_search(embedding, inp.limit)
        response = ((n.name, n.namespace, n.metadata["grai"]["node_type"]) for n in neighbors)
        response_str = "\n".join([", ".join(vals) for vals in response])

        return response_str, self.response_message(neighbors)


class LoadGraph(API):
    id = "load_graph"
    description = ""
    schema_model = BaseModel

    def __init__(self, workspace):
        self.workspace = workspace

    @database_sync_to_async
    def call(self):
        nodes = model_to_schema(Node.objects.filter(workspace=self.workspace).all(), "NodeV1")
        edges = model_to_schema(Edge.objects.filter(workspace=self.workspace).all(), "EdgeV1")

        return [*nodes, *edges], None


class InvalidApiSchema(BaseModel):
    pass


class InvalidAPI(API):
    id = "invalid_api_endpoint"
    description = "placeholder"
    schema_model = InvalidApiSchema

    def __init__(self, apis):
        self.function_string = ", ".join([f"`{api.id}`" for api in apis])

    @database_sync_to_async
    def call(self, *args, **kwargs) -> tuple[str, str | None]:
        return (
            f"Invalid API Endpoint. That function does not exist. The supported apis are {self.function_string}",
            None,
        )

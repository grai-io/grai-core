import copy
import json
import logging
import operator
import uuid
from abc import ABC, abstractmethod
from functools import partial, reduce
from itertools import accumulate
from typing import Annotated, Any, Callable, Literal, Type, TypeVar, Union

import openai
import tiktoken
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from grai_schemas.serializers import GraiYamlSerializer
from pydantic import BaseModel, Field

from connections.adapters.schemas import model_to_schema
from grAI.models import Message
from lineage.models import Edge, Node
from workspaces.models import Workspace

logging.basicConfig(level=logging.DEBUG)


MAX_RETURN_LIMIT = 20

T = TypeVar("T")
RoleType = Union[Literal["user"], Literal["system"], Literal["assistant"]]


class BaseMessage(BaseModel):
    role: str
    content: str
    token_length: int

    def representation(self) -> dict:
        return {"role": self.role, "content": self.content}

    def chunk_content(self, n_chunks: int = 2) -> list[str]:
        if self.token_length is None:
            raise ValueError("Cannot chunk content without a token length")

        chunk_size = self.token_length // n_chunks
        chunks = [self.content[i : i + chunk_size] for i in range(0, len(self.content), chunk_size)]
        return chunks


class UserMessage(BaseMessage):
    role: Literal["user"] = "user"


class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"


class AIMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"


class FunctionMessage(BaseMessage):
    role: Literal["function"] = "function"
    name: str

    def representation(self) -> dict:
        return {"role": self.role, "content": self.content, "name": self.name}


class ChatMessage(BaseModel):
    message: Union[UserMessage, SystemMessage, AIMessage, FunctionMessage]


class ChatMessages(BaseModel):
    messages: list[BaseMessage]

    def to_gpt(self) -> list[dict]:
        return [message.representation() for message in self.messages]

    def __getitem__(self, index):
        return self.messages[index]

    def __len__(self) -> int:
        return len(self.messages)

    def append(self, item):
        self.messages.append(item)

    def extend(self, items):
        self.messages.extend(items)

    def token_length(self) -> int:
        return sum(m.token_length for m in self.messages)


def get_token_limit(model_type: str) -> int:
    OPENAI_TOKEN_LIMITS = {"gpt-4": 8192, "gpt-3.5-turbo": 4096, "gpt-3.5-turbo-16k": 16385, "gpt-4-32k": 32768}

    if model_type in OPENAI_TOKEN_LIMITS:
        return OPENAI_TOKEN_LIMITS[model_type]
    elif model_type.endswith("k"):
        return int(model_type.split("-")[-1]) * 1024
    elif model_type.startswith("gpt-4"):
        return 8192
    elif model_type.startswith("gpt-3.5"):
        return 4096
    else:
        return 2049


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

    def response(self, **kwargs) -> str:
        logging.info(f"Calling {self.id} with {kwargs}")
        obj, message = self.call(**kwargs)

        logging.info(f"Building Response message for {self.id} with {kwargs}")
        if message is None:
            result = self.serialize(obj)
        else:
            result = f"{self.serialize(obj)}\n{message}"

        return result

    def gpt_definition(self) -> dict:
        return {"name": self.id, "description": self.description, "parameters": self.schema_model.schema()}


class SummaryModel(API):
    content: str


class Summarize(API):
    id = "Summarize API"
    description: "Summarize a conversation to manage token lengths"
    schema_model = SummaryModel

    def __init__(self, encoder):
        self.encoder = encoder

    def call(self, content: str) -> str:
        pass


class NodeIdentifier(BaseModel):
    name: str = Field(description="The name of the node to query for")
    namespace: str = Field(description="The namespace of the node to query for")


class NodeLookup(BaseModel):
    nodes: list[NodeIdentifier] = Field(description="A list of nodes to lookup")


class NodeLookupAPI(API):
    id = "node_lookup"
    description = "Lookup metadata about one or more nodes if you know precisely which node(s) to lookup"
    schema_model = NodeLookup

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace
        self.query_limit = MAX_RETURN_LIMIT

    def response_message(self, result_set: list[Node]) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching these query conditions."
        else:
            message = None

        return message

    def call(self, **kwargs) -> (list[Node], str | None):
        try:
            validation = self.schema_model(**kwargs)
        except:
            return [], "Invalid input. Please check your input and try again."
        q_objects = (Q(**node.dict(exclude_none=True)) for node in validation.nodes)
        query = reduce(operator.or_, q_objects)
        result_set = Node.objects.filter(workspace=self.workspace).filter(query).order_by("-created_at").all()
        response_items = model_to_schema(result_set[: self.query_limit], "NodeV1")
        return response_items, self.response_message(result_set)


class FuzzyMatchQuery(BaseModel):
    string: str = Field(description="The fuzzy string used to search amongst node names")


class FuzzyMatchNodesAPI(API):
    id = "node_fuzzy_lookup"
    description = "Performs a fuzzy search for nodes matching a name regardless of namespace"
    schema_model = FuzzyMatchQuery

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace
        self.query_limit = MAX_RETURN_LIMIT

    def response_message(self, result_set: list[Node]) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching these query conditions."
        else:
            message = None

        return message

    def call(self, string: str) -> (list, str | None):
        result_set = (
            Node.objects.filter(workspace=self.workspace).filter(name__contains=string).order_by("-created_at").all()
        )
        response_items = [{"name": node.name, "namespace": node.namespace} for node in result_set]

        return response_items, self.response_message(result_set)


class EdgeLookupSchema(BaseModel):
    source: uuid.UUID | None = Field(description="The primary key of the source node on an edge", default=None)
    destination: uuid.UUID | None = Field(
        description="The primary key of the destination node on an edge", default=None
    )


class MultiEdgeLookup(BaseModel):
    edges: list[EdgeLookupSchema] = Field(
        description="List of edges to lookup. Edges can be uniquely identified by a (name, namespace) tuple, or by a (source, destination) tuple of the nodes the edge connects"
    )


class EdgeLookupAPI(API):
    id = "edge_lookup"
    description = """
    This function Supports looking up edges from a data lineage graph. For example, a query with name=Test but no
    namespace value will return all edges explicitly named "Test" regardless of namespace.
    Edges are uniquely identified both by their (name, namespace), and by the (source, destination) nodes they connect.
    """
    schema_model = MultiEdgeLookup

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace
        self.query_limit = MAX_RETURN_LIMIT

    def response_message(self, result_set: list[Edge]) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching these query conditions."
        else:
            message = None

        return message

    def call(self, **kwargs) -> (list[Edge], str | None):
        validation = self.schema_model(**kwargs)
        q_objects = (Q(**node.dict(exclude_none=True)) for node in validation.edges)
        query = reduce(operator.or_, q_objects)
        result_set = Edge.objects.filter(workspace=self.workspace).filter(query).all()[: self.query_limit]
        return model_to_schema(result_set[: self.query_limit], "EdgeV1"), self.response_message(result_set)


class EdgeFuzzyLookupSchema(BaseModel):
    name__contains: str | None = Field(
        description="The name of the edge to lookup perform a fuzzy search on", default=None
    )
    namespace__contains: str | None = Field(
        description="The namespace of the edge to lookup perform a fuzzy search on", default=None
    )
    is_active: bool | None = Field(description="Whether or not the edge is active", default=True)


class MultiFuzzyEdgeLookup(BaseModel):
    edges: list[EdgeLookupSchema] = Field(
        description="List of edges to lookup. Edges can be uniquely identified by a (name, namespace) tuple, or by a (source, destination) tuple of the nodes the edge connects"
    )


class EdgeFuzzyLookupAPI(EdgeLookupAPI):
    id = "edge_fuzzy_lookup"
    description = """
    This function Supports looking up edges from a data lineage graph. For example, a query with name__contains=test
    but no namespace value will return all edges whose names contain the substring "test" regardless of namespace.
    Edges are uniquely identified both by their (name, namespace), and by the (source, destination) nodes they connect.
    """
    schema_model = MultiFuzzyEdgeLookup


class NodeEdgeSerializer:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def representation(self, path=None):
        items = [item.spec for item in (*self.nodes, *self.edges)]
        return GraiYamlSerializer.dump(items, path)

    def __str__(self):
        return self.representation()


class NHopQuerySchema(BaseModel):
    name: str = Field(description="The name of the node to query for")
    namespace: str = Field(description="The namespace of the node to query for")
    n: int = Field(description="The number of hops to query for", default=1)


class NHopQueryAPI(API):
    id: str = "n_hop_query"
    description: str = "query for nodes and edges within a specified number of hops from a given node"
    schema_model = NHopQuerySchema

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace

    def response_message(self, result_set: list[Edge | Node]) -> str | None:
        total_results = len(result_set)
        if total_results == 0:
            message = "No results found matching these query conditions."
        else:
            message = None

        return message

    def call(self, **kwargs) -> (list[Edge | Node], str | None):
        n = kwargs.get("n", None)
        if n is None:
            return [], "Invalid input, n is a required parameter"
        elif n < 1:
            return [], "Invalid input, n must be greater than 0"

        source_node = Node(workspace=Workspace(pk=self.workspace), name=kwargs["name"], namespace=kwargs["namespace"])
        query = Q(source=source_node) | Q(destination=source_node)
        hop_edges = list(Edge.objects.filter(workspace=self.workspace).filter(query).all())
        search_nodes = [e.source if e.destination == source_node else e.destination for e in hop_edges]

        return_nodes = search_nodes
        return_edges = hop_edges
        for i in range(kwargs["n"] - 1):
            source_edges = Edge.objects.filter(source__in=search_nodes).all()
            destination_edges = Edge.objects.filter(destination__in=search_nodes).all()

            search_nodes = [*[e.source for e in source_edges], *[e.destination for e in destination_edges]]
            return_nodes.extend(search_nodes)
            return_edges.extend(source_edges)
            return_edges.extend(destination_edges)

        nodes = set(model_to_schema(return_nodes, "NodeV1"))
        edges = set(model_to_schema(return_edges, "EdgeV1"))
        result = [item.spec for item in (*nodes, *edges)]
        return result, self.response_message(result)


class InvalidApiSchema(BaseModel):
    pass


class InvalidAPI(API):
    id = "invalid_api_endpoint"
    description = "placeholder"
    schema_model = InvalidApiSchema

    def __init__(self, apis):
        self.function_string = ", ".join([f"`{api.id}`" for api in apis])

    def call(self, *args, **kwargs):
        return f"Invalid API Endpoint. That function does not exist. The supported apis are {self.function_string}"

    def serialize(self, result):
        return result


class FakeEncoder:
    def encode(self, text):
        return [1, 2, 3, 4]


class BaseConversation:
    def __init__(
        self,
        chat_id: str,
        prompt: str,
        model_type: str = settings.OPENAI_PREFERRED_MODEL,
        user: str = str(uuid.uuid4()),
        functions: list = None,
        verbose=False,
    ):
        if functions is None:
            functions = []

        self.model_type = model_type
        self.token_limit = get_token_limit(self.model_type)
        self.encoder = tiktoken.encoding_for_model(self.model_type)
        # self.encoder = FakeEncoder()
        self.chat_id = chat_id
        self.cache_id = f"grAI:chat_id:{chat_id}"
        self.system_context = prompt
        self.user = user
        self.api_functions = {func.id: func for func in functions}
        self.verbose = verbose

        self.prompt_message = self.build_message(SystemMessage, content=self.system_context)
        self.hydrate_chat()

    def build_message(self, message_type: Type[T], content: str, **kwargs) -> T:
        return message_type(content=content, token_length=self.get_token_length(content), **kwargs)

    def get_token_length(self, message):
        return len(self.encoder.encode(message))

    @property
    def cached_messages(self) -> list[BaseMessage]:
        messages = [ChatMessage(message=message).message for message in cache.get(self.cache_id)]
        return messages

    @cached_messages.setter
    def cached_messages(self, values: list[BaseMessage]):
        cache.set(self.cache_id, [v.dict() for v in values])

    def hydrate_chat(self):
        logging.info(f"Hydrating chat history for conversations: {self.chat_id}")
        messages = cache.get(self.cache_id, None)

        if messages is None:
            logging.info(f"Loading chat history for chat {self.chat_id} from database")
            messages_iter = (
                {"role": m.role, "content": m.message, "token_length": len(self.encoder.encode(m.message))}
                for m in Message.objects.filter(chat_id=self.chat_id).order_by("-created_at").all()
            )
            messages_list = [ChatMessage(message=message).message for message in messages_iter]
            self.cached_messages = messages_list

    def summarize(self, messages: list[BaseMessage]) -> AIMessage:
        summary_prompt = """
        Please summarize this conversation encoding the most important information a future agent would need to continue
        working on the problem with me. Please insure you do not call any functions providing an exclusively
        text based summary of the conversation to this point with all relevant context for the next agent.
        """
        message = self.build_message(UserMessage, summary_prompt)
        summary_messages = ChatMessages(messages=[*messages, message])
        logging.info(f"Summarizing conversation for chat: {self.chat_id}")
        response = openai.ChatCompletion.create(
            model=self.model_type, user=self.user, messages=summary_messages.to_gpt()
        )

        # this is hacky for now
        summary_message = self.build_message(AIMessage, response.choices[0].message.content)
        return summary_message

    @property
    def functions(self):
        return [func.gpt_definition() for func in self.api_functions.values()]

    @property
    def model(self) -> Callable:
        if len(self.functions) > 0:
            model = partial(
                openai.ChatCompletion.create, model=self.model_type, user=self.user, functions=self.functions
            )
        else:
            model = partial(openai.ChatCompletion.create, model=self.model_type, user=self.user)
        return model

    def evaluate_summary(self, messages: ChatMessages) -> ChatMessages:
        model_limit = self.token_limit * 0.85

        requires_summary = messages.token_length() > model_limit
        while requires_summary:
            prev_accumulated_tokens = 0
            accumulated_tokens = 0
            i = 0
            for i, message in enumerate(messages.messages):
                accumulated_tokens += message.token_length
                if accumulated_tokens > model_limit:
                    break
                prev_accumulated_tokens = accumulated_tokens

            available_tokens = model_limit - prev_accumulated_tokens
            message = messages.messages[i]
            if i == len(messages) and accumulated_tokens < model_limit:
                requires_summary = False
            elif available_tokens >= message.token_length:
                summary = self.summarize(messages.messages[: (i + 1)])
                messages = [self.prompt_message, summary, *messages.messages[(i + 1) :]]
            else:
                encoding = self.encoder.encode(message)
                message_obj = copy.copy(message)
                next_message_obj = copy.copy(message)

                message_obj.content = self.encoder.decode(encoding[:available_tokens])
                message_obj.token_length = len(encoding[:available_tokens])
                next_message_obj.content = self.encoder.decode(encoding[available_tokens:])
                next_message_obj.token_length = len(encoding[available_tokens:])

                summary = self.summarize([*messages.messages[:i], message_obj])
                messages = [self.prompt_message, summary, next_message_obj, *messages.messages[i:]]

            messages = ChatMessages(messages=messages)
        return messages

    def request(self, user_input: str) -> str:
        logging.info(f"Responding to request for: {self.chat_id}")

        messages = ChatMessages(
            messages=[self.prompt_message, *self.cached_messages, self.build_message(UserMessage, content=user_input)]
        )

        result = None
        stop = False
        while not stop:
            messages = self.evaluate_summary(messages)
            response = self.model(messages=messages.to_gpt())

            if result:
                for choice in response.choices:
                    if result != choice:
                        result = choice
                        break
            else:
                result = response.choices[0]

            if stop := result.finish_reason == "stop":
                message = self.build_message(AIMessage, content=result.message.content)
                messages.append(message)
            elif result.finish_reason == "function_call":
                func_id = result.message.function_call.name
                func_kwargs = json.loads(result.message.function_call.arguments)
                api = self.api_functions.get(func_id, InvalidAPI(self.api_functions.values()))
                response = api.response(**func_kwargs)

                if isinstance(api, InvalidAPI):
                    message = self.build_message(SystemMessage, response)
                    messages.append(message)
                else:
                    message = self.build_message(FunctionMessage, content=response, name=func_id)
                    messages.append(message)
            elif result.finish_reason == "length":
                summary = self.summarize(messages[:-1])
                messages = ChatMessages(messages=[self.prompt_message, summary, messages[-1]])
            else:
                # valid values include length, content_filter, null
                raise NotImplementedError(f"No stop reason for {result.finish_reason}")

        self.cached_messages = messages.messages
        return result.message.content


def get_chat_conversation(
    chat_id: str | uuid.UUID, workspace: str | uuid.UUID, model_type: str = settings.OPENAI_PREFERRED_MODEL
):
    chat_prompt = """
    You are a helpful assistant with domain expertise about an organizations data and data infrastructure.

    * You know how to query for additional context and metadata about any data in the organization.
    * Unique pieces of data like a column in a database is identified by a (name, namespace) tuple or a unique uuid.
    * You can help users discover new data or identify and correct issues such as broken data pipelines, and BI dashboards.
    * Your responses must use Markdown syntax
    * When a user asks you a question about their data you should proactively look up additional context about the data.
    * Nodes contain a metadata field with extra context about the node.
    * Nodes and Edges are typed. You can identify the type under `metadata.grai.node_type` or `metadata.grai.edge_type`
    * If a Node has a type like `Column` with a `TableToColumn` Edge connecting to a `Table` node, the Column node represents a column in the table.
    * Node names for databases and datawarehouses are constructed following `{schema}.{table}.{column}` format e.g. a column named `id` in a table named `users` in a schema named `public` would be identified as `public.users.id`
    """
    functions = [
        NodeLookupAPI(workspace=workspace),
        # Todo: edge lookup is broken
        # EdgeLookupAPI(workspace=workspace),
        FuzzyMatchNodesAPI(workspace=workspace),
        NHopQueryAPI(workspace=workspace),
    ]

    conversation = BaseConversation(
        prompt=chat_prompt, model_type=model_type, functions=functions, chat_id=str(chat_id)
    )
    return conversation

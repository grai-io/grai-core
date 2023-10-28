import json
import uuid
from abc import ABC, abstractmethod
from functools import partial
from typing import Callable, Any

import openai
from django.conf import settings
from django.core.cache import cache
from grai_schemas.serializers import GraiYamlSerializer
from pydantic import BaseModel, Field
from lineage.models import Node, Edge
from grAI.models import Message
from django.db.models import Q
from functools import reduce
import operator
import logging
from connections.adapters.schemas import model_to_schema

logging.basicConfig(level=logging.DEBUG)


MAX_RETURN_LIMIT = 20


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
            return self.serialize(obj)
        else:
            return f"{self.serialize(obj)}\n{message}"

    def gpt_definition(self) -> dict:
        return {"name": self.id, "description": self.description, "parameters": self.schema_model.schema()}


class NodeLookupSchema(BaseModel):
    name: str | None = Field(description="The name of the node to lookup", default=None)
    name__contains: str | None = Field(
        description="The name of the node to lookup perform a fuzzy search on", default=None
    )
    namespace: str | None = Field(description="The namespace of the node to lookup", default=None)
    namespace__contains: str | None = Field(
        description="The namespace of the node to lookup perform a fuzzy search on", default=None
    )
    is_active: bool | None = Field(description="Whether or not the node is active", default=True)


class MultiNodeLookup(BaseModel):
    nodes: list[NodeLookupSchema] = Field(description="List of queries to perform")


class NodeLookupAPI(API):
    id = "node_lookup"
    description = f"""
    This function Supports looking up nodes from a data lineage graph. For example, a query with name=Test but no
    namespace value will return all nodes explicitly named "Test" regardless of namespace. If you're unable to find a
    named result you should use fuzzy search capabilities.
    The `__contains` suffix indicates that the field should be searched using a fuzzy search.
    """
    schema_model = MultiNodeLookup

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace
        self.query_limit = MAX_RETURN_LIMIT

    def call(self, **kwargs) -> (list[Node], str | None):
        validation = self.schema_model(**kwargs)
        q_objects = (Q(**node.dict(exclude_none=True)) for node in validation.nodes)
        query = reduce(operator.or_, q_objects)
        result_set = Node.objects.filter(workspace=self.workspace).filter(query).order_by("-created_at").all()
        total_results = len(result_set)
        if total_results > self.query_limit:
            message = f"Returned {self.query_limit} of {total_results} results. You might need to narrow your search."
        else:
            message = None
        return model_to_schema(result_set[: self.query_limit], "NodeV1"), message


class EdgeLookupSchema(BaseModel):
    name: str | None = Field(description="The name of the edge to lookup", default=None)
    name__contains: str | None = Field(
        description="The name of the edge to lookup perform a fuzzy search on", default=None
    )
    namespace: str | None = Field(description="The namespace of the edge to lookup", default=None)
    namespace__contains: str | None = Field(
        description="The namespace of the edge to lookup perform a fuzzy search on", default=None
    )
    is_active: bool | None = Field(description="Whether or not the edge is active", default=True)
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
    The `__contains` suffix indicates that the field should be searched using a fuzzy search. If you're unable to find a
    named result you should use fuzzy search capabilities. Edges are uniquely
    identified both by their (name, namespace), and by the (source, destination) nodes they connect.
    """
    schema_model = MultiEdgeLookup

    def __init__(self, workspace: str | uuid.UUID):
        self.workspace = workspace
        self.query_limit = MAX_RETURN_LIMIT

    def call(self, **kwargs) -> (list[Edge], str | None):
        validation = self.schema_model(**kwargs)
        q_objects = (Q(**node.dict(exclude_none=True)) for node in validation.nodes)
        query = reduce(operator.or_, q_objects)
        result_set = Edge.objects.filter(workspace=self.workspace).filter(query).all()[: self.query_limit]
        total_results = len(result_set)
        if total_results > self.query_limit:
            message = f"Returned {self.query_limit} of {total_results} results. You might need to narrow your search."
        else:
            message = None
        return model_to_schema(result_set[: self.query_limit], "EdgeV1"), message


class NodeEdgeSerializer:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def representation(self, path=None):
        items = [item.spec for item in (*self.nodes, *self.edges)]
        return GraiYamlSerializer.dump(items, path)

    def __str__(self):
        return self.representation()


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
        self.chat_id = chat_id
        self.cache_id = f"grAI:chat_id:{chat_id}"
        self.system_context = prompt
        self.user = user
        self.api_functions = {func.id: func for func in functions}
        self.verbose = verbose

        self.prompt_message = {"role": "system", "content": self.system_context}
        self.hydrate_chat()

    @property
    def cached_messages(self) -> list:
        return cache.get(self.cache_id)

    @cached_messages.setter
    def cached_messages(self, values):
        cache.set(self.cache_id, values)

    def hydrate_chat(self):
        logging.info(f"Hydrating chat history for conversations: {self.chat_id}")
        messages = cache.get(self.cache_id, None)

        if messages is None:
            logging.info(f"Loading chat history for chat {self.chat_id} from database")
            model_messages = Message.objects.filter(chat_id=self.chat_id).order_by("-created_at").all()
            messages = [{"role": m.role, "content": m.message} for m in model_messages]
            self.cached_messages = messages

    def summarize(self, messages):
        summary_prompt = """
        Please summarize this conversation encoding the most important information a future agent would need to continue
        working on the problem with me. Please insure you do not call any functions providing an exclusively
        text based summary of the conversation to this point with all relevant context for the next agent.
        """
        message = {"role": "user", "content": summary_prompt}

        logging.info(f"Summarizing conversation for chat: {self.chat_id}")
        response = openai.ChatCompletion.create(model=self.model_type, user=self.user, messages=[*messages, message])

        # this is hacky for now
        summary_message = {"role": "assistant", "content": response.choices[0].message.content}
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

    def request(self, user_input: str) -> str:
        logging.info(f"Responding to request for: {self.chat_id}")
        messages = [self.prompt_message, *self.cached_messages, {"role": "user", "content": user_input}]

        stop = False
        while not stop:
            try:
                response = self.model(messages=messages)
            except openai.InvalidRequestError:
                # If it hits the token limit try to summarize
                summary = self.summarize(messages[:-1])
                messages = [self.prompt_message, summary, messages[-1]]
                response = self.model(messages=messages)

            result = response.choices[0]

            if stop := result.finish_reason == "stop":
                messages.append({"role": "assistant", "content": result.message.content})
            elif result.finish_reason == "function_call":
                func_id = result.message.function_call.name
                func_kwargs = json.loads(result.message.function_call.arguments)
                api = self.api_functions.get(func_id, InvalidAPI(self.api_functions.values()))
                response = api.response(**func_kwargs)

                if isinstance(api, InvalidAPI):
                    messages.append({"role": "system", "content": response})
                else:
                    messages.append({"role": "function", "name": func_id, "content": response})
            elif result.finish_reason == "length":
                summary = self.summarize(messages[:-1])
                messages = [self.prompt_message, summary, messages[-1]]
            else:
                # valid values include length, content_filter, null
                raise NotImplementedError(f"No stop reason for {result.finish_reason}")

        self.cached_messages = messages
        return result.message.content


def get_chat_conversation(
    chat_id: str | uuid.UUID, workspace: str | uuid.UUID, model_type: str = settings.OPENAI_PREFERRED_MODEL
):
    chat_prompt = """
    You are a helpful assistant with domain expertise about an organizations data and data infrastructure.
    You know how to query for additional context and metadata about any data in the organization.
    Unique pieces of data like a column in a database is identified by a (name, namespace) tuple or a unique uuid.
    You can help users discover new data or identify and correct issues such as broken data pipelines,
    and BI dashboards.
    """
    functions = [NodeLookupAPI(workspace=workspace), EdgeLookupAPI(workspace=workspace)]

    conversation = BaseConversation(
        prompt=chat_prompt, model_type=model_type, functions=functions, chat_id=str(chat_id)
    )
    return conversation

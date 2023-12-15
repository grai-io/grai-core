import json
import logging
import uuid

from typing import Any, Callable, ParamSpec, TypeVar, Coroutine

from openai.types.chat import ChatCompletion
from openai.types.completion_usage import CompletionUsage
import openai

from grAI.utils import get_token_limit, chunker
import tiktoken
from django.conf import settings
from django.core.cache import cache
import asyncio
from workspaces.models import Workspace

from channels.db import database_sync_to_async

from grAI.models import Message
from grAI.chat_types import (
    UserMessage,
    SystemMessage,
    FunctionMessage,
    ChatMessages,
    UsageMessage,
    ChatMessage,
    SupportedMessageTypes,
    to_gpt,
)
from grAI.tools import (
    NodeLookupAPI,
    EmbeddingSearchAPI,
    NHopQueryAPI,
    InvalidAPI,
    EdgeLookupAPI,
    FuzzyMatchNodesAPI,
    SourceLookupAPI,
)
from grAI.summarization import ProgressiveSummarization, ToolSummarization, GraiSummarization
from grAI.utils import compute_total_tokens

logging.basicConfig(level=logging.DEBUG)


MAX_RETURN_LIMIT = 20

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")


class SummaryPrompt:
    def __init__(self, encoder: tiktoken.Encoding):
        prompt_str = """
        Please summarize this conversation encoding the most important information a future agent would need to continue
        working on the problem with me. Please insure your response is a
        text based summary of the conversation to this point with all relevant context for the next agent.
        """
        self.prompt = SystemMessage(content=prompt_str)
        self.token_usage = len(encoder.encode(prompt_str))


class BaseConversation:
    def __init__(
        self,
        chat_id: str,
        prompt: str,
        client: openai.AsyncOpenAI | None = None,
        model_type: str = settings.OPENAI_PREFERRED_MODEL,
        functions: list = None,
        verbose=False,
    ):
        if functions is None:
            functions = []

        if client is None:
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY, organization=settings.OPENAI_ORG_ID)

        self.client = client
        self.model_type = model_type
        self.encoder = tiktoken.encoding_for_model(self.model_type)
        # self.encoder = FakeEncoder()

        self.chat_id = chat_id
        self.cache_id = f"grAI:chat_id:{chat_id}"

        self.api_functions = {func.id: func for func in functions}
        self.invalid_api = InvalidAPI(self.api_functions.values())

        self.prompt_message = SystemMessage(content=prompt)

        self.base_tokens = self.get_base_tokens()
        self.max_model_tokens = get_token_limit(self.model_type)
        self.max_tokens = self.max_model_tokens - self.base_tokens

    def get_base_tokens(self) -> int:
        tool_strings = (json.dumps(func, indent=2) for func in self.functions())
        num_tool_tokens = sum(len(self.encoder.encode(tool)) for tool in tool_strings)
        num_prompt_tokens = len(self.encoder.encode(self.prompt_message.content))
        return int((num_tool_tokens + num_prompt_tokens) * 1.2)

    def functions(self):
        return [func.gpt_definition() for func in self.api_functions.values()]

    @property
    async def cached_messages(self) -> list[SupportedMessageTypes]:
        cache_result = cache.get(self.cache_id, None)

        if cache_result is None:
            return await self.hydrate_chat()
        else:
            return [ChatMessage(message=message).message for message in cache_result]

    @cached_messages.setter
    def cached_messages(self, values: list[SupportedMessageTypes]):
        cache.set(self.cache_id, [v.dict(exclude_none=True) for v in values])

    @database_sync_to_async
    def hydrate_chat(self) -> list[SupportedMessageTypes]:
        """
        Hydration doesn't currently capture function call context or summarization and will need to be updated to do so.
        """
        messages_iter = (
            ChatMessage(message={"role": m.role, "content": m.message}).message
            for m in Message.objects.filter(chat_id=self.chat_id).order_by("-created_at").all()
        )
        messages = [self.prompt_message, *messages_iter]
        self.cached_messages = messages
        return messages

    @property
    def model(self) -> Callable[[list[SupportedMessageTypes]], Coroutine[Any, Any, ChatCompletion]]:
        base_kwargs = {"model": self.model_type}
        if len(functions := self.functions()) > 0:
            base_kwargs |= {"tools": functions, "tool_choice": "auto"}

        async def inner(messages: list[SupportedMessageTypes]) -> ChatCompletion:
            try:
                response = await self.client.chat.completions.create(messages=to_gpt(messages), **base_kwargs)
            except openai.BadRequestError as e:
                # Just in case we hit a marginal difference from the calculation above.
                if e.code == "context_length_exceeded":
                    messages = await self.evaluate_summary(messages)
                    response = await self.client.chat.completions.create(messages=to_gpt(messages), **base_kwargs)
                else:
                    raise e

            return response

        return inner

    async def evaluate_summary(
        self, messages: list[SupportedMessageTypes], max_tokens: int | None = None
    ) -> list[SupportedMessageTypes]:
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        summarizer = GraiSummarization(model=self.model_type, client=self.client, max_tokens=max_tokens)
        results = await summarizer.call(messages)
        return [self.prompt_message, *results]

    async def request(self, user_input: str) -> str:
        original_messages: list[SupportedMessageTypes] = await self.cached_messages
        messages = original_messages.copy()

        user_query = UserMessage(content=user_input)
        messages.append(user_query)

        final_response: str | None = None
        while final_response is None:
            if compute_total_tokens(messages, self.encoder) > self.max_tokens:
                messages = await self.evaluate_summary(messages)

            response = await self.model(messages)
            response_choice = response.choices[0]

            if response_choice.finish_reason == "stop":
                final_response = response_choice.message.content
            elif response_choice.finish_reason == "length":
                messages = await self.evaluate_summary(messages)
            elif response_choice.finish_reason == "content_filter":
                final_response = "Warning: This message was filtered by the content filter."
            elif response_choice.finish_reason == "tool_calls":
                messages.append(response_choice.message)
                for i, tool_call in enumerate(response_choice.message.tool_calls):
                    func_id = tool_call.function.name
                    func_kwargs = json.loads(tool_call.function.arguments)
                    api = self.api_functions.get(func_id, self.invalid_api)
                    response = await api.response(**func_kwargs)
                    message = FunctionMessage(
                        content=response,
                        name=func_id,
                        tool_call_id=tool_call.id,
                        args=func_kwargs,
                    )
                    messages.append(message)
            else:
                logging.error(f"Encountered an unknown openai finish reason {response_choice.finish_reason}")
                final_response = response_choice.message.content

        self.cached_messages = messages
        return final_response


async def get_chat_conversation(
    chat_id: str | uuid.UUID, workspace: Workspace | uuid.UUID, model_type: str = settings.OPENAI_PREFERRED_MODEL
):
    chat_prompt = """
    You are a helpful assistant with domain expertise about an organizations data and data infrastructure.
    All of that context is embedded in a graph where nodes represent individual data concepts like a database column or
    table. Edges in the graph represent relationships between data such as where the data was sourced from.

    Rules you MUST follow:
    - Understand the context of a users request and what they are trying to accomplish.
    - If a user asks about specific data, like a column, you will need to exhaustively search for that data. If
    you're unable to find results you should look for related data using other available tools.
    - You will verify your responses are accurate and exists in their infrastructure.
    - Your responses use GitHub flavored Markdown syntax.

    Data Structure Notes:
    - Unique pieces of data like a column in a database is identified by a (name, namespace) tuple or a unique uuid.
    - Nodes contain a metadata field with extra context about the node.
    - Nodes and Edges are typed. You can identify the type under `metadata.grai.node_type` or `metadata.grai.edge_type`
    - If a Node has a type like `Column` with a `TableToColumn` Edge connecting to a `Table` node, the Column node
    represents a column in the table.
    - Node names for databases and datawarehouses are constructed following `{schema}.{table}.{column}` format e.g. a
    column named `id` in a table named `users` in a schema named `public` would be identified as `public.users.id`.
    - Naming conventions NEVER follow a `{namespace}.{name}` format. Namespace and name will ALWAYS be referred to as
    two separate fields. Do not assume a namespace is a schema or a database.
    """
    client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY, organization=settings.OPENAI_ORG_ID)

    if workspace.ai_enabled:
        search_func = EmbeddingSearchAPI(workspace=workspace.id)
    else:
        search_func = FuzzyMatchNodesAPI(workspace=workspace.id)

    functions = [
        NodeLookupAPI(workspace=workspace.id),
        EdgeLookupAPI(workspace=workspace.id),
        SourceLookupAPI(workspace=workspace.id),
        NHopQueryAPI(workspace=workspace.id),
        search_func,
    ]

    conversation = BaseConversation(
        prompt=chat_prompt, model_type=model_type, functions=functions, chat_id=str(chat_id), client=client
    )
    return conversation

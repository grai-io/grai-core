import copy
import json
import logging
import uuid

from typing import Annotated, Any, Callable, Literal, ParamSpec, Type, TypeVar, Union, Coroutine

from openai import AsyncStream
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.completion_usage import CompletionUsage
import openai
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from workspaces.models import Workspace
import tiktoken
from django.conf import settings
from django.core.cache import cache
from itertools import islice
import asyncio

from channels.db import database_sync_to_async

from grAI.models import Message
from grAI.chat_types import (
    BaseMessage,
    UserMessage,
    SystemMessage,
    AIMessage,
    FunctionMessage,
    ChatMessages,
    UsageMessage,
    ChatMessage,
    UsageMessageTypes,
    to_gpt,
)
from grAI.tools import (
    NodeLookupAPI,
    EdgeLookupAPI,
    FuzzyMatchNodesAPI,
    EmbeddingSearchAPI,
    NHopQueryAPI,
    InvalidAPI,
    LoadGraph,
)
from grAI.summarization import ProgressiveSummarization

logging.basicConfig(level=logging.DEBUG)


MAX_RETURN_LIMIT = 20

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")


def chunker(it, size):
    iterator = iter(it)
    while chunk := list(islice(iterator, size)):
        yield chunk


def get_token_limit(model_type: str) -> int:
    OPENAI_TOKEN_LIMITS = {
        "gpt-4": 8192,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16385,
        "gpt-4-32k": 32768,
        "gpt-4-1106-preview": 128000,
    }

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

        self.model_type = model_type
        self.token_limit = get_token_limit(self.model_type)

        # Margin reserved for model response
        self.model_limit = int(self.token_limit * 0.8)

        self.encoder = tiktoken.encoding_for_model(self.model_type)
        # self.encoder = FakeEncoder()
        self.chat_id = chat_id
        self.cache_id = f"grAI:chat_id:{chat_id}"
        self.system_context = prompt
        self.api_functions = {func.id: func for func in functions}
        self.invalid_api = InvalidAPI(self.api_functions.values())

        self.verbose = verbose

        self.summary_prompt: SummaryPrompt = SummaryPrompt(self.encoder)

        # I don't have a clean way to identify the initial token allocation for the tool prompt
        # without simply calling the api and seeing what the usage is.
        # https://community.openai.com/t/how-to-calculate-the-tokens-when-using-function-call/266573/40
        tool_prompt_token_allocation = 800
        self.baseline_usage: CompletionUsage = CompletionUsage(
            completion_tokens=0, prompt_tokens=tool_prompt_token_allocation, total_tokens=tool_prompt_token_allocation
        )
        self.prompt_message: UsageMessage = UsageMessage(
            message=SystemMessage(content=self.system_context),
            usage=self.baseline_usage,
        )

        if client is None:
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY, organization=settings.OPENAI_ORG_ID)
        self.client = client
        self.load_graph = False

    def functions(self):
        return [func.gpt_definition() for func in self.api_functions.values()]

    def build_message(
        self, message_type: Type[T], content: str, current_usage: CompletionUsage, **kwargs
    ) -> UsageMessage:
        message = message_type(content=content, **kwargs)
        encoding = self.encoder.encode(content)
        usage = CompletionUsage(
            completion_tokens=len(encoding),
            prompt_tokens=current_usage.total_tokens,
            total_tokens=current_usage.total_tokens + len(encoding),
        )
        return UsageMessage(message=message, usage=usage, encoding=encoding)

    @property
    def cached_messages(self) -> list[BaseMessage]:
        return [ChatMessage(message=message).message for message in cache.get(self.cache_id)]

    @cached_messages.setter
    def cached_messages(self, values: list[BaseMessage]):
        cache.set(self.cache_id, [v.dict(exclude_none=True) for v in values])

    @database_sync_to_async
    def hydrate_chat(self):
        """
        Hydration doesn't currently capture function call context or summarization and will need to be updated to do so.
        """
        logging.info(f"Hydrating chat history for conversations: {self.chat_id}")
        messages = cache.get(self.cache_id, None)

        if messages is None:
            logging.info(f"Loading chat history for chat {self.chat_id} from database")
            messages_iter = (
                {"role": m.role, "content": m.message}
                for m in Message.objects.filter(chat_id=self.chat_id).order_by("-created_at").all()
            )
            for item in messages_iter:
                encoding = self.encoder.encode(item["content"])
                usage = CompletionUsage(
                    completion_tokens=len(encoding),
                    prompt_tokens=usage.total_tokens,
                    total_tokens=usage.total_tokens + len(encoding),
                )
                usage_message = UsageMessage(message=item, usage=usage, encoding=encoding)
                chat_messages.append(usage_message)

            self.cached_messages = chat_messages

    @property
    def model(self) -> R:
        base_kwargs = {"model": self.model_type}
        if len(functions := self.functions()) > 0:
            base_kwargs |= {"tools": functions, "tool_choice": "auto"}

        def inner(messages: list = None, **kwargs) -> Coroutine[Any, Any, ChatCompletion]:
            if messages is None:
                messages = [self.prompt_message.message.representation()]
            else:
                messages = [self.prompt_message.message.representation(), *messages]

            return self.client.chat.completions.create(
                messages=messages,
                **base_kwargs,
                **kwargs,
            )

        return inner

    async def evaluate_summary(self, messages: ChatMessages) -> str:
        summarizer = ProgressiveSummarization(model=self.model, client=self.client)
        return await summarizer.call(messages.messages)

    async def request(self, user_input: str) -> str:
        messages = self.cached_messages
        messages.append(self.build_message(UserMessage, content=user_input, current_usage=messages[-1].usage))

        final_response: str | None = None
        while final_response is None:
            response = await self.model(messages=messages.to_gpt())
            response_choice = response.choices[0]
            messages.append(UsageMessage(usage=response.usage, message=response_choice.message))
            if messages.current_usage.total_tokens > self.model_limit:
                messages = await self.evaluate_summary(messages)

            if finish_reason := response_choice.finish_reason == "stop":
                final_response = response_choice.message.content
            elif finish_reason == "length":
                messages = await self.evaluate_summary(messages)
            elif tool_calls := response_choice.message.tool_calls:
                tool_responses = []
                for i, tool_call in enumerate(tool_calls):
                    func_id = tool_call.function.name
                    func_kwargs = json.loads(tool_call.function.arguments)
                    api = self.api_functions.get(func_id, self.invalid_api)
                    response = await api.response(**func_kwargs)
                    message = self.build_message(
                        FunctionMessage,
                        content=response,
                        name=func_id,
                        tool_call_id=tool_call.id,
                        current_usage=messages[-1].usage,
                        args=func_kwargs,
                    )
                    tool_responses.append(message)
                messages.extend(tool_responses.messages)
            else:
                final_response = response_choice.message.content

                # if message_tokens + tool_responses.current_usage.total_tokens > self.model_limit:
                #     for response in tool_responses.messages:
                #         tool_responses[-1] = await self.summarize_tool(messages[:-1], response)

                # idx = messages.index_over_token_limit(self.model_limit)
                # if idx != (len(messages) - 1):
                #     response_choice.message.tool_calls = response_choice.message.tool_calls[:idx]
                #     messages[tool_request_idx] = response_choice.message
                #     messages = ChatMessages(messages=messages.messages[:idx])

        self.cached_messages = messages
        return final_response

    async def summarize_tool(self, messages: ChatMessages | list[UsageMessage], message: UsageMessage):
        def create_question(chunk: str):
            return f"""
            Please summarize the following chunk of content.
            The chunk is:
            {chunk}
            """

        if isinstance(messages, list):
            messages = ChatMessages(messages=messages)

        assert isinstance(message.message, FunctionMessage)
        prompt = f"""
        You've requested a tool to help you with your problem, however the response from the tool was too long
        to fit in the context window. The tool response requested was {message.message.name} with arguments
        {message.message.args}. Please provide a brief description of the details you're looking for which a future
        agent will use to summarize the tool response. Ensure you do not actually call any tools in your response.
        """
        chunk_question = self.build_message(SystemMessage, prompt, messages.current_usage)
        chunk_messages = ChatMessages(messages=[*messages.messages, chunk_question])
        response = await self.model(messages=chunk_messages.to_gpt())
        while response.choices[0].message.tool_calls:
            reiteration = self.build_message(
                SystemMessage, "YOU MUST NOT CALL TOOLS OR FUNCTIONS", chunk_messages.current_usage
            )
            chunk_messages.append(reiteration)
            response = await self.model(messages=chunk_messages.to_gpt())

        summary_context = response.choices[0].message

        chunk_size = self.model_limit - response.usage.completion_tokens - 100
        content_chunk_iter = (self.encoder.decode(chunk) for chunk in chunker(message.encoding, chunk_size))
        content_message_iter = (create_question(summary_context) for content in content_chunk_iter)
        system_message_iter = (SystemMessage(content=content) for content in content_message_iter)

        callbacks = (
            self.client.chat.completions.create(model=self.model_type, messages=to_gpt([summary_context, message]))
            for message in system_message_iter
        )
        responses = [r.choices[0].message for r in await asyncio.gather(*[callback for callback in callbacks])]
        new_message = await self.client.chat.completions.create(
            model=self.model_type, messages=to_gpt([summary_context, *responses])
        )

        message = self.build_message(
            FunctionMessage,
            content=new_message.choices[0].message.content,
            name=message.message.name,
            tool_call_id=message.message.tool_call_id,
            current_usage=messages.current_usage,
            args=message.message.args,
        )
        return message


async def get_chat_conversation(
    chat_id: str | uuid.UUID, workspace: str | uuid.UUID, model_type: str = settings.OPENAI_PREFERRED_MODEL
):
    chat_prompt = """
    You are a helpful assistant with domain expertise about an organizations data and data infrastructure.
    All of that context is available in a queryable graph where nodes represent individual data concepts like a database column or table.
    Edges in the graph represent relationships between data such as where the data was sourced from.
    Before you can help the user, you need to understand the context of their request and what they are trying to accomplish.
    You should attempt to understand the context of the request and what the user is trying to accomplish.
    If a user asks about specific data like nodes and you're unable to find an answer you should attempt to find a similar node and explain why you think it's similar.
    You should verify any specific data references you provide to the user actually exist in their infrastructure.
    Your responses must use Markdown syntax.

    Data Structure Notes:
    * Unique pieces of data like a column in a database is identified by a (name, namespace) tuple or a unique uuid.
    * Nodes contain a metadata field with extra context about the node.
    * Nodes and Edges are typed. You can identify the type under `metadata.grai.node_type` or `metadata.grai.edge_type`
    * If a Node has a type like `Column` with a `TableToColumn` Edge connecting to a `Table` node, the Column node represents a column in the table.
    * Node names for databases and datawarehouses are constructed following `{schema}.{table}.{column}` format e.g. a column named `id` in a table named `users` in a schema named `public` would be identified as `public.users.id`

    """
    client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY, organization=settings.OPENAI_ORG_ID)

    functions = [
        NodeLookupAPI(workspace=workspace),
        # Todo: edge lookup is broken
        # EdgeLookupAPI(workspace=workspace),
        # FuzzyMatchNodesAPI(workspace=workspace),
        EmbeddingSearchAPI(workspace=workspace),
        NHopQueryAPI(workspace=workspace),
    ]

    # Use Embedding when enabled on workspace otherwise fuzzymatch

    conversation = BaseConversation(
        prompt=chat_prompt, model_type=model_type, functions=functions, chat_id=str(chat_id), client=client
    )
    await conversation.hydrate_chat()
    return conversation

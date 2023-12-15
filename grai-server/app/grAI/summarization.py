from grAI.utils import get_token_limit, chunker, tool_segments, ToolSegmentReturnType
from abc import ABC, abstractmethod
import tiktoken
from typing import Any, TypeVar, Coroutine
import openai
from openai import AsyncOpenAI
from django.conf import settings
from asyncio import gather
from grAI.chat_types import SupportedMessageTypes, SystemMessage, FunctionMessage, UserMessage
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat import ChatCompletion


R = TypeVar("R")


class ContentLengthError(Exception):
    pass


class BaseChat(ABC):
    def __init__(self, model: str, client: AsyncOpenAI | None = None, max_tokens: int | None = None):
        if client is None:
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY, organization=settings.OPENAI_ORG_ID)

        self.client = client
        self.model = model
        self.max_tokens = get_token_limit(self.model) if max_tokens is None else max_tokens

    async def completion(self, messages: list[dict] | dict) -> R:
        messages = [messages] if isinstance(messages, dict) else messages
        return self.client.chat.completions.create(model=self.model, messages=messages)

    @abstractmethod
    async def call(self, *args, **kwargs) -> Any:
        pass


class BaseSummarizer(ABC):
    def __init__(
        self,
        model: str,
        prompt_string: str,
        client: AsyncOpenAI | None = None,
        max_tokens: int | None = None,
    ):
        if client is None:
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY, organization=settings.OPENAI_ORG_ID)
        self.prompt_string = prompt_string
        self.client = client
        self.model = model
        self.max_tokens = get_token_limit(self.model) if max_tokens is None else max_tokens
        self.encoder = tiktoken.encoding_for_model(self.model)

    async def completion(self, messages: list[dict] | dict) -> ChatCompletion:
        messages = [messages] if isinstance(messages, dict) else messages
        return await self.client.chat.completions.create(model=self.model, messages=messages)

    def prompt(self, content: SupportedMessageTypes):
        return self.prompt_string.format(content=content.content, role=content.role)

    def query(self, content: SupportedMessageTypes) -> dict:
        return {"role": "system", "content": self.prompt(content)}

    @abstractmethod
    async def call(self, *args, **kwargs) -> Any:
        pass


DEFAULT_SUMMARIZER_PROMPT = """The following is a conversation between a user and an openai AI agent.
'{content}'
please distill the conversation such that a future agent can answer the user's question.
"""


class BasicSummarizer(BaseSummarizer):
    def __init__(
        self,
        model: str,
        client: AsyncOpenAI | None = None,
        prompt_string: str | None = DEFAULT_SUMMARIZER_PROMPT,
        max_tokens: int | None = None,
    ):
        super().__init__(prompt_string=prompt_string, model=model, client=client, max_tokens=max_tokens)

    async def call(self, input_obj: SupportedMessageTypes) -> str:
        query = self.query(input_obj)
        self.validate(query["content"])
        response = await self.completion(query)
        return response.choices[0].message.content

    def validate(self, content: str) -> list[int]:
        encoding = self.encoder.encode(content)
        if enc_size := len(encoding) < self.max_tokens:
            message = (
                f"The provided prompt is {enc_size} tokens long but the chosen model {self.model} only supports"
                f"a maximum of {self.max_tokens} tokens. Please reduce the prompt size."
            )
            raise ContentLengthError(message)

        return encoding


class ConversationSummarizer(BasicSummarizer):
    def __init__(
        self,
        model: str,
        prompt_string: str,
        client: AsyncOpenAI | None = None,
        max_tokens: int | None = None,
    ):
        super().__init__(prompt_string=prompt_string, model=model, client=client, max_tokens=max_tokens)

    def prompt(self, content: str | list[SupportedMessageTypes], **kwargs) -> str:
        if isinstance(content, list):
            content = self.prompt_content(content)
        return self.prompt_string.format(content=content, **kwargs)

    @staticmethod
    def prompt_content(input_obj: list[SupportedMessageTypes]) -> str:
        component_iter = (f"{inp.role}\n---\n{inp.content}" for inp in input_obj)
        content = "\n---\n".join(component_iter)
        return content

    def query(self, content: list[SupportedMessageTypes] | str, **kwargs) -> dict:
        prompt = self.prompt(content=content, **kwargs)
        return {"role": "system", "content": prompt}

    async def call(self, input_obj: list[SupportedMessageTypes] | str, **kwargs) -> str:
        query = self.query(input_obj, **kwargs)
        self.validate(query["content"])
        response = await self.completion(query)
        return response.choices[0].message.content


DEFAULT_REDUCE_PROMPT = DEFAULT_SUMMARIZER_PROMPT


class Reduce(ConversationSummarizer):
    def __init__(
        self,
        model: str,
        prompt_string: str = DEFAULT_REDUCE_PROMPT,
        client: AsyncOpenAI | None = None,
        max_tokens: int | None = None,
    ):
        super().__init__(prompt_string=prompt_string, model=model, client=client, max_tokens=max_tokens)

    async def call(self, items: list[SupportedMessageTypes], **kwargs) -> str:
        query = self.query(items, **kwargs)
        encoding = self.validate(query["content"])
        response = await self.completion(query)
        return response.choices[0].message.content

    def validate(self, content: str) -> list[int]:
        encoding = self.encoder.encode(content)
        if enc_size := len(encoding) < self.max_tokens:
            message = (
                f"The provided prompt is {enc_size} tokens long but the chosen model {self.model} only supports"
                f"a maximum of {self.max_tokens} tokens. Please reduce the prompt size."
            )
            raise ContentLengthError(message)
        return encoding


DEFAULT_MAP_PROMPT = DEFAULT_SUMMARIZER_PROMPT


class Map(ConversationSummarizer):
    def __init__(
        self,
        model: str,
        prompt_string: str = DEFAULT_MAP_PROMPT,
        client: AsyncOpenAI | None = None,
        max_tokens: int | None = None,
    ):
        super().__init__(prompt_string=prompt_string, model=model, client=client, max_tokens=max_tokens)

    async def call(self, items: list[SupportedMessageTypes], **kwargs) -> list[str]:
        encoding = self.encoder.encode(self.prompt_content(items))

        queries = (self.query(self.encoder.decode(chunk)) for chunk in chunker(encoding, self.max_tokens - 50))
        responses = await gather(*[self.completion(query) for query in queries])
        return [resp.choices[0].message.content for resp in responses]


class MapReduceSummarization(BaseChat):
    def __init__(self, *args, map: Map, reduce: Reduce, **kwargs):
        self.map = map
        self.reduce = reduce
        super().__init__(*args, **kwargs)

    async def call(self, items: list[SupportedMessageTypes], **kwargs) -> str:
        reduction: str | None = None
        while reduction is None:
            items = [SystemMessage(content=content) for content in await self.map.call(items, **kwargs)]

            try:
                reduction = await self.reduce.call(items, **kwargs)
            except ContentLengthError:
                pass

        return reduction


DEFAULT_PROGRESSIVE_PROMPT = DEFAULT_SUMMARIZER_PROMPT


class ProgressiveSummarization(ConversationSummarizer):
    def __init__(
        self,
        model: str,
        prompt_string: str = DEFAULT_PROGRESSIVE_PROMPT,
        client: AsyncOpenAI | None = None,
        max_tokens: int | None = None,
    ):
        super().__init__(prompt_string=prompt_string, model=model, client=client, max_tokens=max_tokens)

    async def call(self, items: list[SupportedMessageTypes], **kwargs) -> str:
        content = self.prompt(items, **kwargs)
        encoding = self.encoder.encode(content)
        while len(encoding) > self.max_tokens:
            query = self.query(self.encoder.decode(encoding[: self.max_tokens]), **kwargs)
            response = await self.completion(query)

            content = "\n".join([response.choices[0].message.content, self.encoder.decode(encoding[self.max_tokens :])])
            encoding = self.encoder.encode(self.prompt_string.format(content=content, **kwargs))

        return content


class ToolSummarization(BaseChat):
    def __init__(self, strategy: ProgressiveSummarization | MapReduceSummarization, **kwargs):
        self.strategy = strategy
        kwargs.setdefault("client", self.strategy.client)
        kwargs.setdefault("model", self.strategy.model)
        kwargs.setdefault("max_tokens", self.strategy.max_tokens)

        super().__init__(**kwargs)

    @staticmethod
    def tool_segments(items: list[SupportedMessageTypes]) -> ToolSegmentReturnType:
        return tool_segments(items)

    async def call(self, items: list[SupportedMessageTypes], **kwargs) -> str:
        if len(items) == 0:
            return ""

        segment: list[SupportedMessageTypes] = []
        for pre_tool_segment, tool_segment in self.tool_segments(items):
            content = await self.strategy.call([*segment, *pre_tool_segment], **kwargs)
            pre_tool_context = SystemMessage(content=content)

            if tool_segment is not None:
                tool_summary = await self.strategy.call([pre_tool_context, *tool_segment], **kwargs)
                segment = [SystemMessage(content=tool_summary)]
            else:
                segment = [pre_tool_context]

        return segment[0].content


DEFAULT_GRAI_PROMPT = """The following is a conversation between a user and an openai AI agent.
'{content}'
The user is attempting to answer the following question:
'{question}'
Please distill the conversation to it's essence including all information needed by a future agent to
answer the user's question.
"""


class GraiSummarization(BaseChat):
    def __init__(self, model: str, client: openai.AsyncOpenAI, max_tokens: int):
        self.progressive = ProgressiveSummarization(
            model=model, prompt_string=DEFAULT_GRAI_PROMPT, client=client, max_tokens=max_tokens
        )

        self.map_reduce = MapReduceSummarization(
            model=model,
            client=client,
            max_tokens=max_tokens,
            map=Map(model=model, client=client, max_tokens=max_tokens, prompt_string=DEFAULT_GRAI_PROMPT),
            reduce=Reduce(model=model, client=client, max_tokens=max_tokens, prompt_string=DEFAULT_GRAI_PROMPT),
        )

        question_request_prompt = """The following is a conversation between a user and an openai AI agent.
        '{content}'
        Please identify the problem the user needs help with. Your response MUST be written as if you were the user and
        end in a question mark."
        """

        self.conversation = ConversationSummarizer(
            model=model, client=client, max_tokens=max_tokens, prompt_string=question_request_prompt
        )
        self.tool = ToolSummarization(strategy=self.progressive)
        self.max_tokens = max_tokens
        super().__init__(model=model, client=client, max_tokens=max_tokens)

    @staticmethod
    def user_messages(items: list[SupportedMessageTypes]) -> int:
        i = 0

        for i, item in enumerate(items[::-1]):
            if item.role == "user":
                break
        idx = len(items) - i
        return idx

    async def get_question(self, items: list[SupportedMessageTypes]) -> UserMessage:
        last_user_message_idx = self.user_messages(items)
        encoding = self.conversation.encoder.encode(self.conversation.prompt(items[: last_user_message_idx + 1]))

        content = self.conversation.encoder.decode(encoding[-min(self.max_tokens, 1000) :])
        response = await self.conversation.completion({"role": "system", "content": content})

        return UserMessage(content=response.choices[0].message.content)

    async def call(self, items: list[SupportedMessageTypes]) -> list[SystemMessage | UserMessage]:
        user_question = await self.get_question(items)
        print(user_question)
        tool_max_tokens = self.tool.max_tokens
        self.tool.max_tokens = tool_max_tokens - len(self.tool.strategy.encoder.encode(user_question.content)) - 10
        summary = await self.tool.call(items, question=user_question.content)
        self.tool.max_tokens = tool_max_tokens

        responses = [SystemMessage(content=summary), user_question]
        return responses

    prompt = """
    You've requested a tool to help you with your problem, however the response from the tool was too long
    to fit in the context window. The tool response requested was {message.message.name} with arguments
    {message.message.args}. Please provide a brief description of the details you're looking for which a future
    agent will use to summarize the tool response. Ensure you do not actually call any tools in your response.
    """

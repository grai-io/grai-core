from grAI.utils import get_token_limit, chunker
from abc import ABC, abstractmethod
import tiktoken
from typing import Any, TypeVar
import openai
from openai import AsyncOpenAI
from django.conf import settings
from asyncio import gather
from grAI.chat_types import SupportedMessageTypes, SystemMessage, FunctionMessage
from openai.types.chat.chat_completion_message import ChatCompletionMessage

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
        *args,
        client: AsyncOpenAI | None = None,
        max_tokens: int | None = None,
        **kwargs,
    ):
        if client is None:
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY, organization=settings.OPENAI_ORG_ID)
        self.prompt_string = prompt_string
        self.client = client
        self.model = model
        self.max_tokens = get_token_limit(self.model) if max_tokens is None else max_tokens

    async def completion(self, messages: list[dict] | dict) -> R:
        messages = [messages] if isinstance(messages, dict) else messages
        return self.client.chat.completions.create(model=self.model, messages=messages)

    def prompt(self, content: SupportedMessageTypes):
        return self.prompt_string.format(content=content.content, role=content.role)

    def query(self, content: SupportedMessageTypes) -> dict:
        return {"role": "system", "content": self.prompt(content)}

    @abstractmethod
    async def call(self, *args, **kwargs) -> Any:
        pass


DEFAULT_SUMMARIZER_PROMPT = """Write a concise summary of the following:
"{content}"
CONCISE SUMMARY:"""


class BasicSummarizer(BaseSummarizer):
    def __init__(
        self,
        model: str,
        client: AsyncOpenAI | None = None,
        prompt_string: str | None = DEFAULT_SUMMARIZER_PROMPT,
        max_tokens: int | None = None,
    ):
        self.encoder = tiktoken.encoding_for_model(self.model)
        super().__init__(prompt_string=prompt_string, model=model, client=client, max_tokens=max_tokens)

    async def call(self, input_obj: SupportedMessageTypes):
        query = self.query(input_obj)
        self.validate(query["content"])
        return self.completion(query)

    def validate(self, content: str) -> list[int]:
        encoding = self.encoder.encode(content)
        if enc_size := len(encoding) < self.max_tokens:
            message = (
                f"The provided prompt is {enc_size} tokens long but the chosen model {self.model} only supports"
                f"a maximum of {self.max_tokens} tokens. Please reduce the prompt size."
            )
            raise ContentLengthError(message)

        return encoding


DEFAULT_REDUCE_PROMPT = """The following is a conversation
{content}
Take these and distill it into a final, consolidated summary of the main themes.
Helpful Answer:"""


class Reduce(BasicSummarizer):
    def __init__(self, *args, prompt_string: str = DEFAULT_REDUCE_PROMPT, **kwargs):
        super().__init__(*args, prompt_string=prompt_string, **kwargs)

    def prompt(self, input_obj: list[SupportedMessageTypes]) -> str:
        component_iter = (f"{inp.role}\n---\n{inp.content}" for inp in input_obj)
        content = "\n---".join(component_iter)
        return self.prompt_string.format(content=content)

    def query(self, content: list[SupportedMessageTypes]) -> dict:
        return {"role": "system", "content": self.prompt(content)}

    async def call(self, items: list[SupportedMessageTypes]) -> str:
        query = self.query(items)
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


DEFAULT_MAP_PROMPT = """The following is a set of documents
{content}
Based on this list of docs, please identify the main themes
Helpful Answer:"""


class Map(BasicSummarizer):
    def __init__(self, *args, prompt_string: str = DEFAULT_MAP_PROMPT, **kwargs):
        super().__init__(*args, prompt_string=prompt_string, **kwargs)

    def prompt(self, input_obj: list[SupportedMessageTypes]) -> str:
        component_iter = (f"{inp.role}\n---\n{inp.content}" for inp in input_obj)
        content = "\n---".join(component_iter)
        return self.prompt_string.format(content=content)

    def query(self, content: list[SupportedMessageTypes]) -> dict:
        return {"role": "system", "content": self.prompt(content)}

    async def call(self, items: list[SupportedMessageTypes]) -> list[str]:
        encoding = self.encoder.encode(self.prompt(items))

        queries = (self.query(self.encoder.decode(chunk)) for chunk in chunker(encoding, self.max_tokens - 50))
        responses = await gather(*[self.completion(query) for query in queries])
        return [resp.choices[0].message.content for resp in responses]


class MapReduceSummarization(BaseChat):
    def __init__(self, *args, map: Map, reduce: Reduce, **kwargs):
        self.map = map
        self.reduce = reduce
        super().__init__(*args, **kwargs)

    async def call(self, items: list[SupportedMessageTypes]) -> str:
        reduction: str | None = None
        while reduction is None:
            items = [SystemMessage(content=content) for content in await self.map.call(items)]

            try:
                reduction = await self.reduce.call(items)
            except ContentLengthError:
                pass

        return reduction


class ProgressiveSummarization(BasicSummarizer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prompt(self, input_obj: list[SupportedMessageTypes]) -> str:
        component_iter = (f"{inp.role}\n---\n{inp.content}" for inp in input_obj)
        content = "\n---".join(component_iter)
        return self.prompt_string.format(content=content)

    def query(self, content: list[SupportedMessageTypes] | str) -> dict:
        if isinstance(content, list):
            content = self.prompt(content)

        return {"role": "system", "content": content}

    async def call(self, items: list[SupportedMessageTypes]) -> str:
        content = self.prompt(items)
        encoding = self.encoder.encode(content)
        while len(encoding) > self.max_tokens:
            query = self.query(self.encoder.decode(encoding[: self.max_tokens]))
            response = await self.completion(query)

            content = "\n".join([response.choices[0].message.content, self.encoder.decode(encoding[self.max_tokens :])])
            encoding = self.encoder.encode(self.prompt_string.format(content=content))

        return content


ToolSegmentReturnType = tuple[list[SupportedMessageTypes], list[FunctionMessage] | None]


class ToolSummarization(BasicSummarizer):
    def __init__(self, *args, strategy: ProgressiveSummarization | MapReduceSummarization, **kwargs):
        self.strategy = strategy
        kwargs.setdefault("client", self.strategy.client)
        kwargs.setdefault("model", self.strategy.model)

        super().__init__(*args, **kwargs)

    def prompt(self, input_obj: list[SupportedMessageTypes]) -> str:
        component_iter = (f"{inp.role}\n---\n{inp.content}" for inp in input_obj)
        content = "\n---".join(component_iter)
        return self.prompt_string.format(content=content)

    def query(self, content: list[SupportedMessageTypes]) -> dict:
        return {"role": "system", "content": self.prompt(content)}

    def tool_segments(self, items: list[SupportedMessageTypes]) -> ToolSegmentReturnType:
        pre_tool_segment = []
        tool_segment: list | None = None
        for item in items:
            if tool_segment is None:
                if isinstance(item, ChatCompletionMessage) and item.tool_calls is not None:
                    tool_segment = []
                elif item.role == "tool":
                    raise ValueError("Encountered a tool response message without a preceding tool call message.")
                else:
                    pre_tool_segment.append(item)
            else:
                if item.role == "tool":
                    tool_segment.append(item)
                elif len(tool_segment) == 1:
                    raise ValueError("Encountered a tool call message without any subsequent tool responses.")
                else:
                    yield pre_tool_segment, tool_segment
                    pre_tool_segment = []
                    tool_segment = None

        return pre_tool_segment, tool_segment

    async def call(self, items: list[SupportedMessageTypes]) -> str:
        if len(items) == 0:
            return ""

        segment: list[SupportedMessageTypes] = []
        for pre_tool_segment, tool_segment in self.tool_segments(items):
            content = await self.strategy.call([*segment, *pre_tool_segment])
            pre_tool_context = SystemMessage(content=content)

            if tool_segment is not None:
                tool_summary = await self.strategy.call([pre_tool_context, *tool_segment])
                segment = [SystemMessage(content=tool_summary)]
            else:
                segment = [pre_tool_context]

        return segment[0].content


prompt = """
You've requested a tool to help you with your problem, however the response from the tool was too long
to fit in the context window. The tool response requested was {message.message.name} with arguments
{message.message.args}. Please provide a brief description of the details you're looking for which a future
agent will use to summarize the tool response. Ensure you do not actually call any tools in your response.
"""

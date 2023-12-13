from grAI.chat_implementations import get_token_limit, chunker
from abc import ABC, abstractmethod
import tiktoken
from typing import Any, TypeVar
import openai
from openai import AsyncOpenAI
from django.conf import settings
from asyncio import gather
from grAI.chat_types import SupportedMessageTypes, SystemMessage

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


class BaseSummarizer(ABC, BaseChat):
    def __init__(self, prompt_string: str, model: str, client: AsyncOpenAI | None = None):
        self.prompt_string = prompt_string
        super().__init__(model=model, client=client)

    def prompt(self, content: SupportedMessageTypes):
        return self.prompt_string.format(content=content.content, role=content.role)

    def query(self, content: SupportedMessageTypes) -> dict:
        return {"role": "system", "content": self.prompt(content)}


DEFAULT_SUMMARIZER_PROMPT = """Write a concise summary of the following:
"{content}"
CONCISE SUMMARY:"""


class BasicSummarizer(BaseSummarizer):
    def __init__(
        self, model: str, client: AsyncOpenAI | None = None, prompt_string: str | None = DEFAULT_SUMMARIZER_PROMPT
    ):
        self.encoder = tiktoken.encoding_for_model(self.model)
        super().__init__(prompt_string=prompt_string, model=model, client=client)

    async def call(self, input_obj: SupportedMessageTypes):
        query = self.query(input_obj)
        self.validate(query["content"])
        return self.completion(query)

    def validate(self, content: str) -> list[int]:
        encoding = self.encoder.encode(content)
        if enc_size := len(encoding) < self.max_tokens:
            message = (
                f"The provided prompt is {enc_size} tokens long but the chosen model {self.model} only supports"
                f"a maximum of {self.num_tokens} tokens. Please reduce the prompt size."
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
        if enc_size := len(encoding) < self.num_tokens:
            message = (
                f"The provided prompt is {enc_size} tokens long but the chosen model {self.model} only supports"
                f"a maximum of {self.num_tokens} tokens. Please reduce the prompt size."
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

        queries = (self.query(self.encoder.decode(chunk)) for chunk in chunker(encoding, self.num_tokens - 50))
        responses = await gather(*[self.completion(query) for query in queries])
        return [resp.choices[0].message.content for resp in responses]


class MapReduce(BaseChat):
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
    def prompt(self, input_obj: list[SupportedMessageTypes]) -> str:
        component_iter = (f"{inp.role}\n---\n{inp.content}" for inp in input_obj)
        content = "\n---".join(component_iter)
        return self.prompt_string.format(content=content)

    def query(self, content: list[SupportedMessageTypes]) -> dict:
        return {"role": "system", "content": self.prompt(content)}

    async def call(self, items: list[SupportedMessageTypes]) -> str:
        content = self.prompt(items)
        encoding = self.encoder.encode(content)
        while len(encoding) > self.max_tokens:
            query = self.encoder.decode(encoding[: self.max_tokens])
            response = await self.completion(query)

            content = "\n".join([response.choices[0].message.content, self.encoder.decode(encoding[self.max_tokens :])])
            encoding = self.encoder.encode(self.prompt_string.format(content=content))

        return content

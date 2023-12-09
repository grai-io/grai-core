from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel
from typing import Any, Literal, Union
from multimethod import multimethod

RoleType = Union[Literal["user"], Literal["system"], Literal["assistant"]]


class BaseMessage(BaseModel):
    role: str
    content: str

    def representation(self) -> dict:
        return {"role": self.role, "content": self.content}


class UserMessage(BaseMessage):
    role: Literal["user"] = "user"


class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"


class AIMessage(BaseMessage):
    role: Literal["assistant"] = "assistant"


class FunctionMessage(BaseMessage):
    role: Literal["tool"] = "tool"
    name: str
    tool_call_id: str
    args: dict

    def representation(self) -> dict:
        return {"tool_call_id": self.tool_call_id, "role": self.role, "content": self.content, "name": self.name}


UsageMessageTypes = Union[UserMessage, SystemMessage, AIMessage, FunctionMessage, ChatCompletionMessage]


class ChatMessage(BaseModel):
    message: UsageMessageTypes


class UsageMessage(BaseModel):
    usage: CompletionUsage
    message: UsageMessageTypes
    encoding: list | None = None


@multimethod
def to_gpt(message: Any) -> dict | ChatCompletionMessage:
    raise Exception(f"Cannot convert {type(message)} to GPT format")


@to_gpt.register
def list_to_gpt(messages: list) -> list[dict]:
    return [to_gpt(message) for message in messages]


@to_gpt.register
def usage_message_to_gpt(message: UsageMessage) -> dict:
    return to_gpt(message.message)


@to_gpt.register
def dict_to_gpt(message: dict) -> dict:
    return message


@to_gpt.register
def base_message_to_gpt(message: BaseMessage) -> dict:
    return message.representation()


@to_gpt.register
def chat_completion_message_to_gpt(message: ChatCompletionMessage) -> ChatCompletionMessage:
    return message


class ChatMessages(BaseModel):
    messages: list[UsageMessage]

    def to_gpt(self) -> list[dict]:
        return to_gpt(self.messages)

    def __getitem__(self, index):
        return self.messages[index]

    def __len__(self) -> int:
        return len(self.messages)

    def __setitem__(self, key, value):
        self.messages[key] = value
        self.recompute_usage(key)

    def append(self, item):
        self.messages.append(item)
        self.recompute_usage(len(self.messages) - 1)

    def extend(self, items):
        self.messages.extend(items)
        self.recompute_usage(len(self.messages) - len(items))

    @property
    def current_usage(self) -> CompletionUsage:
        return self.messages[-1].usage

    def recompute_usage(self, from_index: int = 0):
        usage = self.messages[from_index].usage
        for message in self.messages[from_index + 1 :]:
            message.usage.prompt_tokens = usage.total_tokens
            message.usage.total_tokens = usage.total_tokens + message.usage.completion_tokens

    def index_over_token_limit(self, token_limit) -> int:
        for index, message in enumerate(self.messages):
            if message.usage.total_tokens > token_limit:
                return index
        return index

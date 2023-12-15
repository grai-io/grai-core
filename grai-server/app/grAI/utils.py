from itertools import islice
from multimethod import multimethod
import tiktoken
from typing import Any, Iterable
from grAI.chat_types import SupportedMessageTypes, BaseMessage, FunctionMessage
from openai.types.chat.chat_completion_message import ChatCompletionMessage

OPENAI_TOKEN_LIMITS = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-1106-preview": 128000,
}


def get_token_limit(model_type: str) -> int:
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


def chunker(it, size):
    iterator = iter(it)
    while chunk := list(islice(iterator, size)):
        yield chunk


def get_message_token_count(message, encoder) -> int:
    if message.content is not None:
        return len(encoder.encode(message.content))
    elif isinstance(message, ChatCompletionMessage) and message.tool_calls is not None:
        return sum(len(encoder.encode(call.json())) for call in message.tool_calls)
    else:
        raise ValueError("Message must have either content or tool_calls")


def compute_total_tokens(messages: list[SupportedMessageTypes], encoder: tiktoken.Encoding) -> int:
    return sum(get_message_token_count(message, encoder) for message in messages)


ToolSegmentReturnType = tuple[list[SupportedMessageTypes], list[FunctionMessage] | None]


def tool_segments(items: list[SupportedMessageTypes]) -> list[ToolSegmentReturnType]:
    pre_tool_segment: list = []
    tool_segment: list | None = None
    result = []
    for item in items:
        if tool_segment is None:
            if isinstance(item, ChatCompletionMessage) and item.tool_calls is not None:
                tool_segment = []
                # pre_tool_segment = []
            elif item.role == "tool":
                for stuff in result:
                    print(stuff)
                print("value error items")
                print(items)
                print("value error item")
                print(item)
                raise ValueError("Encountered a tool response message without a preceding tool call message.")
            else:
                pre_tool_segment.append(item)
        else:
            if item.role == "tool":
                tool_segment.append(item)
            elif len(tool_segment) == 0:
                raise ValueError(f"Encountered a tool call message without any subsequent tool responses.")
            else:
                result.append((pre_tool_segment, tool_segment))
                # yield pre_tool_segment, tool_segment
                if isinstance(item, ChatCompletionMessage) and item.tool_calls is not None:
                    tool_segment = []
                    pre_tool_segment = []
                else:
                    pre_tool_segment = [item]
                    tool_segment = None
    result.append((pre_tool_segment, tool_segment))
    return result
    # yield pre_tool_segment, tool_segment

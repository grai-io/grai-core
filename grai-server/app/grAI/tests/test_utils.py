from grAI.utils import tool_segments
from grAI.chat_types import SystemMessage, AIMessage, FunctionMessage, UserMessage
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
import pytest


example_tool_call = ChatCompletionMessageToolCall(
    id="tool_call_1", function={"arguments": "", "name": ""}, type="function"
)
chat_completion = ChatCompletionMessage(content=None, role="assistant", tool_calls=[example_tool_call])

example_tool_call2 = ChatCompletionMessageToolCall(
    id="tool_call_2", function={"arguments": "", "name": ""}, type="function"
)
chat_completion2 = ChatCompletionMessage(content=None, role="assistant", tool_calls=[example_tool_call2])


class TestToolSegmentation:
    def test_no_tools(self):
        messages = [
            UserMessage(content="Hello"),
            AIMessage(content="How are you?"),
            UserMessage(content="I'm good, how are you?"),
            AIMessage(content="I'm good too!"),
        ]
        result = list(tool_segments(messages))
        assert len(result) == 1
        assert result[0][0] == messages
        assert result[0][1] is None

    def test_no_tools_all_message_types(self):
        messages = [
            SystemMessage(content="Hello"),
            UserMessage(content="Hello"),
            AIMessage(content="How are you?"),
            UserMessage(content="I'm good, how are you?"),
            ChatCompletionMessage(content="I'm good too!", role="assistant"),
        ]
        result = list(tool_segments(messages))
        assert len(result) == 1
        assert result[0][0] == messages
        assert result[0][1] is None

    def test_messages_with_tools(self):
        messages = [
            SystemMessage(content="Hello"),
            UserMessage(content="Hello"),
            chat_completion,
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_1", args={}),
        ]
        result = list(tool_segments(messages))
        assert len(result) == 1
        assert result[0][0] == messages[0:2]
        assert result[0][1] == [messages[-1]]

    def test_messages_with_tools_multiple(self):
        messages = [
            SystemMessage(content="Hello"),
            UserMessage(content="Hello"),
            chat_completion,
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_1", args={}),
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_2", args={}),
        ]
        result = list(tool_segments(messages))
        assert len(result) == 1
        assert result[0][0] == messages[0:2]
        assert result[0][1] == messages[-2:]

    def test_messages_with_tools_multiple2(self):
        messages = [
            SystemMessage(content="Hello"),
            UserMessage(content="Hello"),
            chat_completion,
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_1", args={}),
            chat_completion2,
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_2", args={}),
        ]
        list(tool_segments(messages))

    def test_messages_with_multiple_tool_segments(self):
        messages = [
            SystemMessage(content="Hello 1"),
            UserMessage(content="Hello 1"),
            chat_completion,
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_1", args={}),
            SystemMessage(content="Hello 2"),
            UserMessage(content="Hello 2"),
            chat_completion,
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_2", args={}),
        ]
        result = list(tool_segments(messages))
        assert len(result) == 2
        assert result[0][0] == messages[0:2]
        assert result[0][1] == [messages[3]]
        assert result[1][0] == messages[4:6]
        assert result[1][1] == [messages[-1]]

    def test_message_starts_with_completion(self):
        messages = [
            chat_completion,
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_1", args={}),
            SystemMessage(content="Hello 1"),
            UserMessage(content="Hello 1"),
        ]
        result = list(tool_segments(messages))
        assert len(result) == 2
        assert result[0][0] == []
        assert result[0][1] == [messages[1]]
        assert result[1][0] == messages[2:]
        assert result[1][1] is None

    @pytest.mark.xfail(strict=True)
    def test_message_starting_with_tool(self):
        messages = [
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_1", args={}),
            SystemMessage(content="Hello 1"),
            UserMessage(content="Hello 1"),
            chat_completion,
        ]
        result = list(tool_segments(messages))

    @pytest.mark.xfail(strict=True)
    def test_message_starting_with_tool_completion(self):
        messages = [
            chat_completion,
            SystemMessage(content="Hello 1"),
            UserMessage(content="Hello 1"),
        ]
        result = list(tool_segments(messages))

    @pytest.mark.xfail(strict=True)
    def test_message_with_tool_without_completion(self):
        messages = [
            SystemMessage(content="Hello 1"),
            UserMessage(content="Hello 1"),
            FunctionMessage(content="I'm good too!", role="tool", name="test", tool_call_id="tool_call_1", args={}),
        ]
        result = list(tool_segments(messages))

    @pytest.mark.xfail(strict=True)
    def test_message_with_completion_without_tool(self):
        messages = [
            SystemMessage(content="Hello 1"),
            UserMessage(content="Hello 1"),
            chat_completion,
            SystemMessage(content="Hello 1"),
            UserMessage(content="Hello 1"),
        ]
        result = list(tool_segments(messages))

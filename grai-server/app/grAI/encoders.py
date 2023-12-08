import tiktoken
import openai
from typing import TypeVar

R = TypeVar("R")


class OpenAIEmbedder:
    def __init__(self, model: str, context_window: int):
        self.model = model
        self.model_context_window = context_window
        self.encoder = tiktoken.encoding_for_model(self.model)

        self.heuristic_max_length = self.model_context_window * 4 * 0.85

    def get_encoding(self, content: str) -> list[int]:
        return self.encoder.encode(content)

    def decode(self, encoding: list[int]) -> str:
        return self.encoder.decode(encoding)

    def get_max_length_content(self, content: str) -> str:
        content_length = len(content)

        # Heuristic estimate of the max length of content that can be encoded
        if len(content) < self.heuristic_max_length:
            return content

        encoded = self.get_encoding(content)
        if len(encoded) < self.model_context_window:
            return content
        else:
            return self.decode(encoded[: self.model_context_window])

    def get_embedding(self, content: str) -> R:
        content = self.get_max_length_content(content)
        return openai.embedding.create(input=content, model=self.model)

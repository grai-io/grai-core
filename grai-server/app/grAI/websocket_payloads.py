import uuid
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ValidationError, validator


class ChatErrorMessages(Enum):
    MISSING_OPENAI = (
        "OpenAI is currently disabled. In order to use AI components please enable ChatGPT on this instance of " "Grai"
    )
    WORKSPACE_AI_NOT_ENABLED = (
        "AI enabled chat has been disabled for your workspace. Please contact an administrator if you wish to "
        "enable these features."
    )


class ChatEvent(BaseModel):
    type: Literal["chat.message"] = "chat.message"
    message: str
    chat_id: str

    @validator("chat_id")
    def chat_id_is_uuid(cls, v):
        return v if v == "" else str(uuid.uuid4())

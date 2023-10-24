from pydantic import BaseModel
from abc import ABC, abstractmethod
from grai_schemas.serializers import GraiYamlSerializer
import uuid
from functools import partial
import openai
import json
from django.conf import settings
from django.core.cache import cache
from grAI.models import Message, MessageActions


class API(ABC):
    schema_model: BaseModel
    description: str
    id: str

    @abstractmethod
    def call(self, **kwargs):
        pass

    def serialize(self, result) -> str:
        if isinstance(result, str):
            return result

        return GraiYamlSerializer.dump(result)

    def response(self, **kwargs) -> str:
        return self.serialize(self.call(**kwargs))

    def gpt_definition(self) -> dict:
        return {"name": self.id, "description": self.description, "parameters": self.schema_model.schema()}


class InvalidApiSchema(BaseModel):
    pass


class InvalidAPI(API):
    id = "invalid_api_endpoint"
    description = "placeholder"
    schema_model = InvalidApiSchema

    def __init__(self, apis):
        self.function_string = ", ".join([f"`{api.id}`" for api in apis])

    def call(self, *args, **kwargs):
        return f"Invalid API Endpoint. That function does not exist. The supported apis are {self.function_string}"

    def serialize(self, result):
        return result


class BaseConversation:
    def __init__(
        self,
        chat_id: str,
        prompt: str,
        model_type: str = settings.OPENAI_PREFERRED_MODEL,
        user: str = str(uuid.uuid4()),
        functions: list = None,
        verbose=False,
    ):
        if functions is None:
            functions = []

        self.model_type = model_type
        self.chat_id = chat_id
        self.cache_id = f"grAI:chat_id:{chat_id}"
        self.system_context = prompt
        self.user = user
        self.api_functions = {func.id: func for func in functions}
        self.verbose = verbose

        self.prompt_message = {"role": "system", "content": self.system_context}
        self.hydrate_chat()

    @property
    def messages(self) -> list:
        return cache.get(self.cache_id)

    @messages.setter
    def messages(self, values):
        cache.aset(self.cache_id, values)

    def hydrate_chat(self):
        messages = cache.get_or_set(self.cache_id, [])
        if len(messages) == 0:
            model_messages = Message.objects.filter(chat_id=self.chat_id).order("-created_at").all()

            most_recent_summary_idx = None
            for i, message in enumerate(model_messages):
                if message.action == MessageActions.SUMMARIZE:
                    most_recent_summary_idx = i

            if most_recent_summary_idx is not None:
                model_messages = model_messages[most_recent_summary_idx:]

            messages = [{"role": m.role, "content": m.message} for m in model_messages]

        cache.aset(self.cache_id, messages)

    def summarize(self, messages):
        summary_prompt = """
        Please summarize this conversation encoding the most important information a future agent would need to continue working on the problem with me. Please insure you do not call any functions
        and only provide a text based summary of the conversation to this point.
        """
        message = {"role": "user", "content": summary_prompt}
        summary_messages = [*messages, message]

        model = partial(openai.ChatCompletion.create, model=self.model_type, user=self.user)
        response = model(messages=summary_messages)

        # this is hacky for now
        summary_message = {"role": "assistant", "content": response.choices[0].message.content}
        return summary_message

    @property
    def functions(self):
        return [func.gpt_definition() for func in self.api_functions.values()]

    @property
    def model(self):
        if len(self.functions) > 0:
            model = partial(
                openai.ChatCompletion.create, model=self.model_type, user=self.user, functions=self.functions
            )
        else:
            model = partial(openai.ChatCompletion.create, model=self.model_type, user=self.user)
        return model

    def build_messages(self, messages):
        return [self.prompt_message, messages]

    def request(self, user_input: str) -> str:
        messages = cache.get(self.cache_id)
        new_messages = [{"role": "user", "content": user_input}]

        stop = False
        while not stop:
            try:
                response = self.model(messages=self.build_messages(messages))
            except openai.InvalidRequestError:
                # If it hits the token limit try to summarize
                summary = self.summarize(messages[:-1])
                messages = [summary, messages[-1]]
                response = self.model(messages=self.build_messages(messages))

            result = response.choices[0]

            if stop := result.finish_reason == "stop":
                new_messages.append({"role": "assistant", "content": result.message.content})
            elif result.finish_reason == "function_call":
                func_id = result.message.function_call.name
                func_kwargs = json.loads(result.message.function_call.arguments)
                api = self.api_functions.get(func_id, InvalidAPI(self.api_functions.values()))
                response = api.response(**func_kwargs)

                if isinstance(api, InvalidAPI):
                    self.messages.append({"role": "system", "content": response})
                else:
                    self.messages.append({"role": "function", "name": func_id, "content": response})
            elif result.finish_reason == "length":
                self.messages = self.summarize(self.messages[:-1])
            else:
                # valid values include length, content_filter, null
                raise NotImplementedError(f"No stop reason for {result.finish_reason}")

        return result.message.content


def get_chat_conversation(model_type: str = settings.OPENAI_PREFERRED_MODEL):
    chat_prompt = """
    You are a helpful assistant with domain expertise about an organizations data and data infrastructure. You know how to query for additional context and metadata about any data in the organization.
    Unique pieces of data like a column in a database is identified by a (name, namespace) tuple or a unique uuid. You can help users discover new data or identify and correct issues such as broken data pipelines, and BI dashboards.
    """
    functions = []

    conversation = BaseConversation(prompt=chat_prompt, model_type=model_type, functions=functions)
    return conversation

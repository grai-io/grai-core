from pydantic import BaseModel
from abc import ABC, abstractmethod
from grai_schemas.serializers import GraiYamlSerializer
import uuid
from functools import partial
import openai
import json
from django.conf import settings


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
        prompt: str,
        model_type: str = settings.OPENAI_PREFERRED_MODEL,
        user: str = str(uuid.uuid4()),
        functions: list = None,
        verbose=False,
    ):
        if functions is None:
            functions = []

        self.model_type = model_type
        self.system_context = prompt
        self.user = user
        self.api_functions = {func.id: func for func in functions}
        self.verbose = verbose

        self.messages = [
            {"role": "system", "content": self.system_context},
        ]
        self.raw_responses = []

    def summarize(self, messages):
        if self.verbose:
            print("LOGGING: Attempting to summarize content")

        summary_prompt = """
        Please summarize this conversation encoding the most important information a future agent would need to continue working on the problem with me. Please insure you do not call any functions
        and only provide a text based summary of the conversation to this point.
        """
        message = {"role": "user", "content": summary_prompt}
        summary_messages = [*messages, message]

        model = partial(openai.ChatCompletion.create, model=self.model_type, user=self.user)
        response = model(messages=summary_messages)

        self.raw_responses.append(response)

        # this is hacky for now
        summary_message = {"role": "assistant", "content": response.choices[0].message.content}
        messages = [messages[0], summary_message, messages[-1]]

        return messages

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

    def call_model(self) -> str:
        if self.verbose:
            print(f"LOGGING: Calling model with {len(self.messages)} messages")

        try:
            response = self.model(messages=self.messages)
            self.raw_responses.append(response)
        except openai.InvalidRequestError:
            if self.verbose:
                print("LOGGING: Text was too long... probably")
            self.messages = self.summarize(self.messages[:-1])
            response = self.model(messages=self.messages)

        return response

    def request(self, user_input: str) -> str:
        if not settings.HAS_OPENAI:
            message = (
                "OpenAI is currently disabled. In order to use AI components please enable ChatGPT for your "
                "organization."
            )
            return message

        self.messages.append({"role": "user", "content": user_input})
        stop = False
        while not stop:
            response = self.call_model()
            result = response.choices[0]

            if stop := result.finish_reason == "stop":
                if self.verbose:
                    print(f"LOGGING: Responded with: {result.message.content}")
                self.messages.append({"role": "assistant", "content": result.message.content})
            elif result.finish_reason == "function_call":
                if self.verbose:
                    print(f"LOGGING: Requested function {result.message.function_call.name}")

                func_id = result.message.function_call.name
                func_kwargs = json.loads(result.message.function_call.arguments)
                api = self.api_functions.get(func_id, InvalidAPI(self.api_functions.values()))
                response = api.response(**func_kwargs)

                if isinstance(api, InvalidAPI):
                    self.messages.append({"role": "system", "content": response})
                else:
                    self.messages.append({"role": "function", "name": func_id, "content": response})
            elif result.finish_reason == "length":
                print("LOGGING: Stopped for length, summarizing.")
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

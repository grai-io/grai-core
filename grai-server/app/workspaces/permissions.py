from rest_framework_api_key.permissions import BaseHasAPIKey, KeyParser, APIKey

from .models import WorkspaceAPIKey


class BearerKeyParser(KeyParser):
    keyword = "Bearer"


class BearerApiKey(BaseHasAPIKey):
    model = APIKey
    key_parser = BearerKeyParser()


class HasWorkspaceAPIKey(BaseHasAPIKey):
    model = WorkspaceAPIKey

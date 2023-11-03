from rest_framework_api_key.permissions import BaseHasAPIKey, KeyParser, HasAPIKey

from .models import WorkspaceAPIKey


class BearerKeyParser(KeyParser):
    keyword = "Bearer"


class HasBearerApiKey(HasAPIKey):
    model = HasAPIKey
    key_parser = BearerKeyParser()


class HasBearerWorkspaceAPIKey(BaseHasAPIKey):
    model = WorkspaceAPIKey
    key_parser = BearerKeyParser()


class HasWorkspaceAPIKey(BaseHasAPIKey):
    model = WorkspaceAPIKey

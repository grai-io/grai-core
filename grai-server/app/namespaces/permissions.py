from rest_framework_api_key.permissions import BaseHasAPIKey

from .models import ServiceAPIKey


class HasServiceAPIKey(BaseHasAPIKey):
    model = ServiceAPIKey

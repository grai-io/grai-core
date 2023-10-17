from django.urls import path
from strawberry.django.views import AsyncGraphQLView

from .schema import schema

urlpatterns = [
    path("", AsyncGraphQLView.as_view(schema=schema)),
]

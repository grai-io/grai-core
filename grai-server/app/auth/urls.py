from django.urls import path
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.authtoken import views
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from common.permissions.multitenant import Multitenant
from workspaces.permissions import HasWorkspaceAPIKey


class TenPerSecondUserThrottle(UserRateThrottle):
    rate = "10/sec"


@api_view(["GET"])
@throttle_classes([TenPerSecondUserThrottle])
@authentication_classes(
    [
        SessionAuthentication,
        TokenAuthentication,
        BasicAuthentication,
        JWTAuthentication,
    ]
)
@permission_classes([(HasWorkspaceAPIKey | IsAuthenticated) & Multitenant])
def check_authentication(request):
    return Response({"message": "Authenticated!"})


urlpatterns = [
    path("api-token/", views.obtain_auth_token),
    path("is-authenticated/", check_authentication),
]

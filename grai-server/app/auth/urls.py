from django.urls import path
from rest_framework.authtoken import views
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from workspaces.permissions import HasWorkspaceAPIKey


class OncePerSecondUserThrottle(UserRateThrottle):
    rate = "1/sec"


@api_view(["GET"])
@throttle_classes([OncePerSecondUserThrottle])
@permission_classes([HasWorkspaceAPIKey | IsAuthenticated])
def check_authentication(request):
    return Response({"message": "Authenticated!"})


urlpatterns = [
    path("api-token/", views.obtain_auth_token),
    path("is-authenticated/", check_authentication),
]

from django.urls import path
from rest_framework import routers

from .views import WorkspaceViewSet, MembershipViewSet

app_name = "workspaces"

router = routers.SimpleRouter()
router.register("workspaces", WorkspaceViewSet, basename="workspaces")
router.register("memberships", MembershipViewSet, basename="memberships")

urlpatterns = router.urls

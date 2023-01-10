from django.urls import path
from rest_framework import routers

from .views import ConnectionViewSet, ConnectorViewSet

app_name = "connections"

router = routers.SimpleRouter()
router.register("connections", ConnectionViewSet, basename="connections")
router.register("connectors", ConnectorViewSet, basename="connectors")

urlpatterns = router.urls

from django.urls import path

from rest_framework import routers

from .views import ConnectionViewSet, ConnectorViewSet, RunViewSet

app_name = "connections"

router = routers.SimpleRouter()
router.register("connections", ConnectionViewSet, basename="connections")
router.register("connectors", ConnectorViewSet, basename="connectors")
router.register("runs", RunViewSet, basename="runs")


urlpatterns = router.urls

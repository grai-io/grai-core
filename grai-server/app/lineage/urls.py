from django.urls import path

from rest_framework import routers

from .views import EdgeViewSet, NodeViewSet, SourceViewSet

app_name = "graph"

router = routers.SimpleRouter()
router.register("nodes", NodeViewSet, basename="nodes")
router.register("edges", EdgeViewSet, basename="edges")
router.register("sources", SourceViewSet, basename="sources")

urlpatterns = router.urls

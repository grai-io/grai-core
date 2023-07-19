from django.urls import include, path
from rest_framework_nested import routers

from .views import (
    EdgeViewSet,
    NodeViewSet,
    SourceEdgeViewSet,
    SourceNodeViewSet,
    SourceViewSet,
)

app_name = "graph"

router = routers.SimpleRouter()
router.register(r"nodes", NodeViewSet, basename="nodes")
router.register(r"edges", EdgeViewSet, basename="edges")
router.register(r"sources", SourceViewSet, basename="sources")

source_router = routers.NestedSimpleRouter(router, r"sources", lookup="source")
source_router.register(r"nodes", SourceNodeViewSet, basename="source-nodes")
source_router.register(r"edges", SourceEdgeViewSet, basename="source-edges")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(source_router.urls)),
]

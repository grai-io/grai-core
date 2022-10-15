from django.urls import path
from rest_framework import routers

from health.views import HealthViewSet

router = routers.SimpleRouter()
router.register("can-authenticate", HealthViewSet, basename="health")

urlpatterns = router.urls

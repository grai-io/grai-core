from django.urls import path
from health.views import HealthViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register("can-authenticate", HealthViewSet, basename="health")

urlpatterns = router.urls

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from strawberry.django.views import AsyncGraphQLView

from api.schema import schema

from .views import index

spectacular_settings = {
    "SCHEMA_PATH_PREFIX": "/api/v1/",
}


urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    # path("api/v1/health/", include("health.urls"), name="health"),
    path("api/v1/auth/jwttoken/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/v1/auth/jwttoken/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/v1/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/auth/", include("auth.urls"), name="auth"),
    path("api/v1/lineage/", include("lineage.urls"), name="lineage"),
    path("api/v1/", include("connections.urls"), name="connections"),
    path("api/v1/", include("workspaces.urls"), name="workspaces"),
    path("graphql/", AsyncGraphQLView.as_view(schema=schema)),
    # OpenAPI 3 docs w/ Swagger
    path(
        "api/v1/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema", template_name="swagger-ui.html"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("health/", include("health_check.urls"), name="health"),
]

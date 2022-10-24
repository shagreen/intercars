import os

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from intercars.views import Healthcheck

SchemaView = get_schema_view(
    openapi.Info(
        title="Intercars Backend API",
        default_version=os.getenv("API_VERSION", "N/A"),
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    url=settings.SWAGGER_BASE_URL,
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("healthcheck/", Healthcheck.as_view()),
    path('bank/', include("bank.urls")),
    path('users/', include("users.urls")),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

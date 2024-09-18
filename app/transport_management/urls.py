"""
URL configuration for transport_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from service_areas.views import ServiceAreaViewSet, find_service_areas
from providers.views import ProviderViewSet

# Create the DefaultRouter
router = DefaultRouter()
router.register(r"serviceareas", ServiceAreaViewSet)
router.register(r"providers", ProviderViewSet)

# Schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Mozio API",
        default_version="v1",
        description="API documentation for the Mozio project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@mozio.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Define your URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger and ReDoc documentation paths
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Custom view for service areas lat/lng query
    path("api/serviceareas/latlng/", find_service_areas, name="servicearea-latlng"),
    # REST API router URLs
    path("api/", include(router.urls)),
]

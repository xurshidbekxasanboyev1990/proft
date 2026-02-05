"""
URL patterns for swagger/OpenAPI documentation.
"""

from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

app_name = 'swagger'

urlpatterns = [
    # OpenAPI Schema (JSON/YAML)
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI
    path('', SpectacularSwaggerView.as_view(url_name='swagger:schema'), name='swagger-ui'),
    
    # ReDoc UI (alternative documentation)
    path('redoc/', SpectacularRedocView.as_view(url_name='swagger:schema'), name='redoc'),
]

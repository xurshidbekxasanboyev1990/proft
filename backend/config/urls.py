"""
URL configuration for proft project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('auth/', include('apps.hemis_auth.urls', namespace='hemis_auth')),
    path('accounts/', include('allauth.urls')),
    
    # API Endpoints
    path('api/accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('api/portfolios/', include('apps.portfolios.urls', namespace='portfolios')),
    path('api/assignments/', include('apps.assignments.urls', namespace='assignments')),
    path('api/analytics/', include('apps.analytics.urls', namespace='analytics')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

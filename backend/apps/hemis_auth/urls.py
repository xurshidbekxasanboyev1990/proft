"""
URL patterns for Hemis OAuth 2.0 authentication.
"""

from django.urls import path
from . import views

app_name = 'hemis_auth'

urlpatterns = [
    # Hemis OAuth 2.0 flow
    path('hemis/login/', views.HemisLoginView.as_view(), name='login'),
    path('hemis/callback/', views.HemisCallbackView.as_view(), name='callback'),
    path('hemis/logout/', views.HemisLogoutView.as_view(), name='logout'),
    
    # Auth utilities
    path('status/', views.AuthStatusView.as_view(), name='status'),
    path('csrf/', views.CSRFTokenView.as_view(), name='csrf'),
    
    # Development login (DEBUG mode only)
    path('dev-login/', views.DevLoginView.as_view(), name='dev_login'),
]

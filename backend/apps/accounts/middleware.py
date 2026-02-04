"""
Role-based access control middleware.
"""

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


class RoleBasedAccessMiddleware:
    """
    Middleware to enforce role-based access control.
    """
    
    # URLs that don't require authentication
    PUBLIC_URLS = [
        '/auth/',
        '/admin/login/',
        '/accounts/login/',
        '/accounts/signup/',
        '/static/',
        '/media/',
    ]
    
    # URLs restricted by role
    ROLE_RESTRICTED_URLS = {
        'superadmin': [
            '/api/accounts/users/',  # User management
        ],
        'admin': [
            '/api/portfolios/approve/',
            '/api/portfolios/reject/',
        ],
    }
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if URL is public
        if self._is_public_url(request.path):
            return self.get_response(request)
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            # For API requests, return JSON response
            if request.path.startswith('/api/'):
                return JsonResponse({
                    'error': 'Authentication required',
                    'code': 'UNAUTHORIZED'
                }, status=401)
            # For other requests, redirect to login
            return redirect(f"{reverse('hemis_auth:login')}?next={request.path}")
        
        # Log user access
        logger.debug(f"User {request.user.username} accessing {request.path}")
        
        return self.get_response(request)
    
    def _is_public_url(self, path):
        """Check if the URL is public."""
        for public_url in self.PUBLIC_URLS:
            if path.startswith(public_url):
                return True
        return False

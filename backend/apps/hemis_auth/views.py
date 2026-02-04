"""
Views for Hemis OAuth 2.0 authentication.
"""

import secrets
import logging
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings

from .backends import HemisOAuth2Client
from apps.accounts.models import UserActivity
from apps.accounts.views import get_client_ip

logger = logging.getLogger(__name__)


class HemisLoginView(View):
    """
    Initiate Hemis OAuth 2.0 login flow.
    GET /auth/hemis/login/
    """
    
    def get(self, request):
        # Generate state for CSRF protection
        state = secrets.token_urlsafe(32)
        request.session['hemis_oauth_state'] = state
        
        # Store the next URL if provided
        next_url = request.GET.get('next', '/dashboard/')
        request.session['hemis_oauth_next'] = next_url
        
        # Get authorization URL
        client = HemisOAuth2Client()
        auth_url = client.get_authorization_url(state=state)
        
        logger.info(f"Redirecting to Hemis OAuth 2.0: {auth_url}")
        
        return redirect(auth_url)


class HemisCallbackView(View):
    """
    Handle Hemis OAuth 2.0 callback.
    GET /auth/hemis/callback/
    """
    
    def get(self, request):
        # Check for errors
        error = request.GET.get('error')
        if error:
            error_description = request.GET.get('error_description', 'Unknown error')
            logger.error(f"Hemis OAuth error: {error} - {error_description}")
            return JsonResponse({
                'error': error,
                'error_description': error_description
            }, status=400)
        
        # Get authorization code
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'error': 'No authorization code provided'}, status=400)
        
        # Verify state (CSRF protection)
        state = request.GET.get('state')
        stored_state = request.session.get('hemis_oauth_state')
        
        if not state or state != stored_state:
            logger.warning("Invalid OAuth state parameter")
            return JsonResponse({'error': 'Invalid state parameter'}, status=400)
        
        # Clear state from session
        del request.session['hemis_oauth_state']
        
        # Exchange code for token
        client = HemisOAuth2Client()
        token_response = client.exchange_code_for_token(code)
        
        if not token_response:
            return JsonResponse({'error': 'Failed to exchange code for token'}, status=400)
        
        access_token = token_response.get('access_token')
        refresh_token = token_response.get('refresh_token')
        
        if not access_token:
            return JsonResponse({'error': 'No access token in response'}, status=400)
        
        # Get user info
        user_info = client.get_user_info(access_token)
        
        if not user_info:
            return JsonResponse({'error': 'Failed to get user info'}, status=400)
        
        # Extract hemis_id
        hemis_id = user_info.get('id') or user_info.get('hemis_id') or user_info.get('sub')
        
        if not hemis_id:
            logger.error(f"No hemis_id in user info: {user_info}")
            return JsonResponse({'error': 'No user ID in response'}, status=400)
        
        # Authenticate user
        user = authenticate(
            request,
            hemis_id=str(hemis_id),
            access_token=access_token,
            user_data=user_info
        )
        
        if not user:
            return JsonResponse({'error': 'Authentication failed'}, status=400)
        
        # Update refresh token
        if refresh_token:
            user.hemis_refresh_token = refresh_token
            user.save()
        
        # Login user
        login(request, user, backend='apps.hemis_auth.backends.HemisOAuth2Backend')
        
        # Log activity
        UserActivity.objects.create(
            user=user,
            action=UserActivity.ACTION_LOGIN,
            description='Logged in via Hemis OAuth 2.0',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        logger.info(f"User {user.username} logged in via Hemis OAuth 2.0")
        
        # Redirect to next URL or dashboard
        next_url = request.session.pop('hemis_oauth_next', '/dashboard/')
        
        # For Vue.js frontend, you might want to redirect to frontend URL
        frontend_url = settings.CORS_ALLOWED_ORIGINS[0] if settings.CORS_ALLOWED_ORIGINS else 'http://localhost:3000'
        
        # If the request expects JSON (API call), return JSON response
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'full_name': user.get_full_name(),
                },
                'redirect_url': next_url
            })
        
        return redirect(next_url)


class HemisLogoutView(View):
    """
    Logout user.
    POST /auth/hemis/logout/
    """
    
    @method_decorator(csrf_protect)
    def post(self, request):
        if request.user.is_authenticated:
            # Log activity
            UserActivity.objects.create(
                user=request.user,
                action=UserActivity.ACTION_LOGOUT,
                description='Logged out',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            logger.info(f"User {request.user.username} logged out")
            
            logout(request)
        
        return JsonResponse({'message': 'Logged out successfully'})
    
    def get(self, request):
        """Also allow GET for browser-based logout."""
        if request.user.is_authenticated:
            UserActivity.objects.create(
                user=request.user,
                action=UserActivity.ACTION_LOGOUT,
                description='Logged out',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            logout(request)
        
        return redirect('/')


class AuthStatusView(View):
    """
    Check authentication status.
    GET /auth/status/
    """
    
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'role': request.user.role,
                    'role_display': request.user.get_role_display(),
                    'full_name': request.user.get_full_name(),
                    'hemis_id': request.user.hemis_id,
                    'permissions': {
                        'can_manage_users': request.user.can_manage_users,
                        'can_approve_portfolios': request.user.can_approve_portfolios,
                        'can_manage_all_portfolios': request.user.can_manage_all_portfolios,
                    }
                }
            })
        else:
            return JsonResponse({
                'authenticated': False,
                'user': None
            })


class CSRFTokenView(View):
    """
    Get CSRF token for frontend.
    GET /auth/csrf/
    """
    
    def get(self, request):
        from django.middleware.csrf import get_token
        return JsonResponse({
            'csrfToken': get_token(request)
        })

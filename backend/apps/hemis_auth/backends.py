"""
Hemis OAuth 2.0 authentication backend.
"""

import requests
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)
User = get_user_model()


class HemisOAuth2Backend(BaseBackend):
    """
    Custom authentication backend for Hemis OAuth 2.0.
    """
    
    def authenticate(self, request, hemis_id=None, access_token=None, user_data=None, **kwargs):
        """
        Authenticate user via Hemis OAuth 2.0.
        
        Args:
            hemis_id: Unique ID from Hemis system
            access_token: OAuth 2.0 access token
            user_data: User data from Hemis userinfo endpoint
        """
        if not hemis_id:
            return None
        
        try:
            # Try to find existing user
            user = User.objects.get(hemis_id=hemis_id)
            
            # Update tokens
            if access_token:
                user.hemis_access_token = access_token
                user.hemis_token_expires_at = timezone.now() + timedelta(hours=1)
            
            # Update user data from Hemis if provided
            if user_data:
                self._update_user_from_hemis(user, user_data)
            
            user.save()
            logger.info(f"User {user.username} authenticated via Hemis OAuth 2.0")
            return user
            
        except User.DoesNotExist:
            # Create new user
            if not user_data:
                logger.warning(f"Cannot create user without user_data for hemis_id: {hemis_id}")
                return None
            
            user = self._create_user_from_hemis(hemis_id, access_token, user_data)
            logger.info(f"New user {user.username} created via Hemis OAuth 2.0")
            return user
        
        except Exception as e:
            logger.error(f"Error authenticating Hemis user: {e}")
            return None
    
    def get_user(self, user_id):
        """Get user by ID."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def _create_user_from_hemis(self, hemis_id, access_token, user_data):
        """Create a new user from Hemis data."""
        username = user_data.get('username') or user_data.get('login') or f"hemis_{hemis_id}"
        email = user_data.get('email', '')
        
        # Ensure unique username
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        
        user = User.objects.create(
            username=username,
            email=email,
            hemis_id=hemis_id,
            hemis_access_token=access_token,
            hemis_token_expires_at=timezone.now() + timedelta(hours=1),
            role='teacher',  # Default role for new users from Hemis
            first_name=user_data.get('first_name', user_data.get('firstname', '')),
            last_name=user_data.get('last_name', user_data.get('lastname', '')),
            department=user_data.get('department', user_data.get('faculty', '')),
            position=user_data.get('position', user_data.get('employee_type', '')),
        )
        
        # Set unusable password since they authenticate via Hemis
        user.set_unusable_password()
        user.save()
        
        return user
    
    def _update_user_from_hemis(self, user, user_data):
        """Update existing user with data from Hemis."""
        if user_data.get('email'):
            user.email = user_data['email']
        if user_data.get('first_name') or user_data.get('firstname'):
            user.first_name = user_data.get('first_name', user_data.get('firstname', ''))
        if user_data.get('last_name') or user_data.get('lastname'):
            user.last_name = user_data.get('last_name', user_data.get('lastname', ''))
        if user_data.get('department') or user_data.get('faculty'):
            user.department = user_data.get('department', user_data.get('faculty', ''))
        if user_data.get('position') or user_data.get('employee_type'):
            user.position = user_data.get('position', user_data.get('employee_type', ''))


class HemisOAuth2Client:
    """
    Client for Hemis OAuth 2.0 API.
    """
    
    def __init__(self):
        self.config = settings.HEMIS_OAUTH2
        self.client_id = self.config['CLIENT_ID']
        self.client_secret = self.config['CLIENT_SECRET']
        self.authorization_url = self.config['AUTHORIZATION_URL']
        self.token_url = self.config['TOKEN_URL']
        self.userinfo_url = self.config['USERINFO_URL']
        self.redirect_uri = self.config['REDIRECT_URI']
        self.scope = self.config.get('SCOPE', 'openid profile email')
    
    def get_authorization_url(self, state=None):
        """
        Generate the authorization URL for Hemis OAuth 2.0.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            Authorization URL string
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': self.scope,
        }
        
        if state:
            params['state'] = state
        
        query_string = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{self.authorization_url}?{query_string}"
    
    def exchange_code_for_token(self, code):
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from Hemis
            
        Returns:
            Token response dict or None on error
        """
        try:
            response = requests.post(
                self.token_url,
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': self.redirect_uri,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Token exchange failed: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Token exchange request error: {e}")
            return None
    
    def get_user_info(self, access_token):
        """
        Get user info from Hemis using access token.
        
        Args:
            access_token: OAuth 2.0 access token
            
        Returns:
            User info dict or None on error
        """
        try:
            response = requests.get(
                self.userinfo_url,
                headers={
                    'Authorization': f'Bearer {access_token}'
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"User info request failed: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"User info request error: {e}")
            return None
    
    def refresh_token(self, refresh_token):
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: OAuth 2.0 refresh token
            
        Returns:
            New token response dict or None on error
        """
        try:
            response = requests.post(
                self.token_url,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Token refresh failed: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Token refresh request error: {e}")
            return None

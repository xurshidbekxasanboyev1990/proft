"""
Custom OpenAPI schema extensions for drf-spectacular.
"""

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object


class SessionAuthenticationScheme(OpenApiAuthenticationExtension):
    """Session authentication scheme for Swagger."""
    target_class = 'rest_framework.authentication.SessionAuthentication'
    name = 'sessionAuth'
    
    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'sessionid',
            'description': 'Session-based authentication using cookies'
        }


class HemisOAuthScheme(OpenApiAuthenticationExtension):
    """Hemis OAuth2 authentication scheme for Swagger."""
    target_class = 'apps.hemis_auth.backends.HemisOAuth2Backend'
    name = 'hemisOAuth2'
    
    def get_security_definition(self, auto_schema):
        return {
            'type': 'oauth2',
            'flows': {
                'authorizationCode': {
                    'authorizationUrl': '/auth/hemis/login/',
                    'tokenUrl': '/auth/hemis/callback/',
                    'scopes': {
                        'openid': 'OpenID Connect',
                        'profile': 'User profile',
                        'email': 'User email',
                    }
                }
            },
            'description': 'Hemis OAuth 2.0 authentication'
        }

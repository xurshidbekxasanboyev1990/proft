"""
App configuration for hemis_auth app.
"""

from django.apps import AppConfig


class HemisAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hemis_auth'
    verbose_name = 'Hemis Authentication'

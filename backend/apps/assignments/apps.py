"""
App configuration for assignments app.
"""

from django.apps import AppConfig


class AssignmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.assignments'
    verbose_name = 'Assignments'

    def ready(self):
        """Import signals when app is ready."""
        import apps.assignments.signals  # noqa

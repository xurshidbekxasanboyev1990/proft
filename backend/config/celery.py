"""
Celery configuration for proft project.
"""

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('proft')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    # Check deadline reminders every hour
    'check-deadline-reminders-hourly': {
        'task': 'apps.assignments.tasks.check_deadline_reminders',
        'schedule': crontab(minute=0),  # Every hour at minute 0
    },
    # Update overdue assignments every 30 minutes
    'update-overdue-assignments': {
        'task': 'apps.assignments.tasks.update_overdue_assignments',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
    # Refresh dashboard cache every 5 minutes
    'refresh-dashboard-cache': {
        'task': 'apps.analytics.tasks.refresh_dashboard_cache',
        'schedule': crontab(minute='*/5'),
    },
    # Cleanup expired cache daily
    'cleanup-expired-cache-daily': {
        'task': 'apps.analytics.tasks.cleanup_expired_cache',
        'schedule': crontab(hour=3, minute=0),  # 03:00 AM
    },
    # Cleanup old reports weekly
    'cleanup-old-reports-weekly': {
        'task': 'apps.analytics.tasks.cleanup_old_reports',
        'schedule': crontab(hour=4, minute=0, day_of_week='sunday'),
    },
    # Generate monthly report on 1st day of month
    'generate-monthly-report': {
        'task': 'apps.analytics.tasks.generate_monthly_report',
        'schedule': crontab(hour=6, minute=0, day_of_month='1'),
    },
    # Generate yearly report on Jan 1st
    'generate-yearly-report': {
        'task': 'apps.analytics.tasks.generate_yearly_report',
        'schedule': crontab(hour=6, minute=0, day_of_month='1', month_of_year='1'),
    },
}

app.conf.timezone = 'Asia/Tashkent'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

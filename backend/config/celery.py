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
}

app.conf.timezone = 'Asia/Tashkent'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

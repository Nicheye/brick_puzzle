import os
from celery import Celery
from celery.schedules import crontab
import logging


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendmusic.settings')

logging.basicConfig(level=logging.DEBUG)
app = Celery('backendmusic')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
FORKED_BY_MULTIPROCESSING = 1
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'run-periodic-task': {
        'task': 'prompts.tasks.regenerate_grid',
        'schedule': crontab(minute='*/30'),  # Run every 5 minutes
    },
}
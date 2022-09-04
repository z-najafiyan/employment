import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employment.settings')

app = Celery('employment')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "announcement_task": {
         'task': 'employer.tasks.announcement_task',
            'schedule': 86400   # 24 hours
    },


}

app.autodiscover_tasks()

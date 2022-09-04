import datetime

from celery import shared_task

from employer.models import Announcement
from datetime import date


@shared_task
def announcement_task():

    files = Announcement.objects.filter(status_name="active")
    for item in files:
        new_data = datetime.datetime.now()
        d0 = date(item.creation_date.year, item.creation_date.month, item.creation_date.day)
        d1 = date(new_data.year, new_data.month, new_data.day)
        delta = d1 - d0
        if delta >= 60:
            item.status_name = "closed"
            item.save()

    return True

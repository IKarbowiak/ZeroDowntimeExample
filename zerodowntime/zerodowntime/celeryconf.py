import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zerodowntime.settings")

app = Celery("zerodowntime")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

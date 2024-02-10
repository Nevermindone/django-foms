from celery import Celery
from django.conf import settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("FOMS", backend=settings.REDIS_URL, broker=settings.RABBIT_URL)
app.autodiscover_tasks()

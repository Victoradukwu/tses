import os

from celery.app.base import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("tses_app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

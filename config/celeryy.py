"""Module for celery instance for 'top_api' project."""
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(
    "config",
    broker="redis://127.0.0.1:6379",
    backend="redis://127.0.0.1:6379",
    include=["service.tasks"],
)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

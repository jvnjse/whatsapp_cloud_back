# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whatsapp_back.settings")

# create a Celery instance and configure it with the Django settings
celery_app = Celery("whatsapp_back")

# Load task modules from all registered Django app configs.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
celery_app.autodiscover_tasks()

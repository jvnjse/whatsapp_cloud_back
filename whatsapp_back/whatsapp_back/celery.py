from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whatsapp_back.settings")


celery_app = Celery("whatsapp_back")

celery_app.config_from_object("django.conf:settings", namespace="CELERY")


celery_app.autodiscover_tasks()

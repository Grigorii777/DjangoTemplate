import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
app = Celery('myproject')               # create Celery app
app.config_from_object('django.conf:settings', namespace='CELERY')  # read CELERY_* from settings
app.autodiscover_tasks()                # auto-load tasks.py in apps

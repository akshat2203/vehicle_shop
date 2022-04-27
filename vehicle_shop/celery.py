import os
from celery import Celery
from django.core.mail import EmailMessage

# Celery Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_shop.settings')
BASE_REDIS_URL = 'redis://localhost:6379'

app = Celery('vehicle_shop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

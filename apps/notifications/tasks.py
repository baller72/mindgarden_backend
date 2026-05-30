from celery import shared_task
from django.contrib.auth import get_user_model
from .services import create_journal_reminder, create_breathing_reminder, create_daily_encouragement
from datetime import datetime, time

User = get_user_model()

@shared_task
def send_journal_reminders():
    for user in User.objects.filter(is_active=True):
        create_journal_reminder(user)

@shared_task
def send_breathing_reminders():
    for user in User.objects.filter(is_active=True):
        create_breathing_reminder(user)

@shared_task
def send_daily_encouragements():
    for user in User.objects.filter(is_active=True):
        create_daily_encouragement(user)
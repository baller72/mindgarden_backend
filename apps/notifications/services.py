from .models import Notification, NotificationPreference
from django.utils import timezone
from datetime import timedelta

def create_journal_reminder(user):
    pref, _ = NotificationPreference.objects.get_or_create(user=user)
    if pref.journal_reminder:
        Notification.objects.create(
            user=user,
            message="N'oubliez pas d'écrire dans votre journal aujourd'hui",
            notification_type="reminder"
        )

def create_breathing_reminder(user):
    pref = NotificationPreference.objects.get(user=user)
    if pref.breathing_reminder:
        Notification.objects.create(
            user=user,
            message="Prenez une pause respiration de 2 minutes 🧘",
            notification_type="reminder"
        )

def create_daily_encouragement(user):
    pref = NotificationPreference.objects.get(user=user)
    if pref.daily_encouragement:
        messages = [
            "Chaque petit pas compte. Continuez !",
            "Vous faites de votre mieux, c'est suffisant.",
            "Prenez soin de vous aujourd'hui."
        ]
        import random
        msg = random.choice(messages)
        Notification.objects.create(
            user=user,
            message=msg,
            notification_type="encouragement"
        )
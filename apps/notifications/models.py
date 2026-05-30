from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=50)  # 'reminder', 'encouragement'
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.message[:30]}"

class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    journal_reminder = models.BooleanField(default=True)
    breathing_reminder = models.BooleanField(default=True)
    daily_encouragement = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences for {self.user.email}"
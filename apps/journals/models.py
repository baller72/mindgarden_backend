from django.db import models
from django.conf import settings

class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journals')
    text = models.TextField(blank=True, default='')
    audio_file = models.FileField(upload_to='journals/audio/', blank=True, null=True)
    transcription = models.TextField(blank=True, default='')
    mood = models.CharField(max_length=50, blank=True, default='')
    stress_score = models.IntegerField(null=True, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Journal {self.id} by {self.user.email}"
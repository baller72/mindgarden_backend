from django.db import models
from django.conf import settings

class EmotionAnalysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emotion_analyses')
    journal_entry = models.ForeignKey('journals.JournalEntry', on_delete=models.CASCADE, related_name='emotion_analysis')
    stress_score = models.IntegerField(default=0)
    sadness_score = models.IntegerField(default=0)
    anxiety_score = models.IntegerField(default=0)
    positivity_score = models.IntegerField(default=0)
    emotion = models.CharField(max_length=100, blank=True)
    recommendation = models.CharField(max_length=100, blank=True)
    critical_flags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis {self.id} for Entry {self.journal_entry_id}"
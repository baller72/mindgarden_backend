from django.db import models

class BreathingExercise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_seconds = models.IntegerField()
    rhythm = models.CharField(max_length=100)  # ex: "4-7-8"
    audio_guide = models.FileField(upload_to='breathing/audio/', blank=True, null=True)
    category = models.CharField(max_length=100)  # ex: "relaxation", "stress"
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
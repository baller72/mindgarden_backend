from rest_framework import serializers
from .models import JournalEntry

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'transcription', 'mood', 'stress_score', 'sentiment_score')

class JournalEntryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ('text', 'mood')
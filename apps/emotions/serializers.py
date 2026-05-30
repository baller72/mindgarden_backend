from rest_framework import serializers
from .models import EmotionAnalysis

class EmotionAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionAnalysis
        fields = '__all__'
        read_only_fields = ('id', 'user', 'journal_entry', 'created_at')
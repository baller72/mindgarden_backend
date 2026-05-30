from rest_framework import serializers
from .models import BreathingExercise

class BreathingExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreathingExercise
        fields = '__all__'
from rest_framework import generics, permissions
from .models import BreathingExercise
from .serializers import BreathingExerciseSerializer

class BreathingExerciseListView(generics.ListAPIView):
    queryset = BreathingExercise.objects.filter(is_active=True)
    serializer_class = BreathingExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

class BreathingExerciseDetailView(generics.RetrieveAPIView):
    queryset = BreathingExercise.objects.filter(is_active=True)
    serializer_class = BreathingExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]
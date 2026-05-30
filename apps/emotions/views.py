from rest_framework import viewsets, permissions
from .models import EmotionAnalysis
from .serializers import EmotionAnalysisSerializer

class EmotionAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmotionAnalysis.objects.all()
    serializer_class = EmotionAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return EmotionAnalysis.objects.filter(user=self.request.user).order_by('-created_at')
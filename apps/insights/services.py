from apps.emotions.models import EmotionAnalysis
from django.utils import timezone
from datetime import timedelta
from apps.ai.services import aggregate_emotions

def get_weekly_insights(user):
    today = timezone.now().date()
    start = today - timedelta(days=7)
    analyses = EmotionAnalysis.objects.filter(
        user=user, 
        created_at__date__gte=start,
        created_at__date__lte=today
    )
    return aggregate_emotions(analyses)

def get_monthly_insights(user):
    today = timezone.now().date()
    start = today - timedelta(days=30)
    analyses = EmotionAnalysis.objects.filter(
        user=user,
        created_at__date__gte=start,
        created_at__date__lte=today
    )
    return aggregate_emotions(analyses)
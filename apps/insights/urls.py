from django.urls import path
from .views import WeeklyInsightsView, MonthlyInsightsView

urlpatterns = [
    path('weekly/', WeeklyInsightsView.as_view(), name='insights_weekly'),
    path('monthly/', MonthlyInsightsView.as_view(), name='insights_monthly'),
]
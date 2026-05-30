from django.urls import path
from .views import BreathingExerciseListView, BreathingExerciseDetailView

urlpatterns = [
    path('exercises/', BreathingExerciseListView.as_view(), name='breathing-list'),
    path('exercises/<int:pk>/', BreathingExerciseDetailView.as_view(), name='breathing-detail'),
]
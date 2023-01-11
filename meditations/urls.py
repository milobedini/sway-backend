from django.urls import path
from .views import MeditationDetailView, MeditationListView, LatestMeditationView

urlpatterns = [
    path('<int:pk>/', MeditationDetailView.as_view()),
    path('', MeditationListView.as_view()),
    path('latest/', LatestMeditationView.as_view()),
]

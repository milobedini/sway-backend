from django.urls import path
from .views import MeditationDetailView, MeditationListView, LatestMeditationView, MeditationSearchView

urlpatterns = [
    path('<int:pk>/', MeditationDetailView.as_view()),
    path('', MeditationListView.as_view()),
    path('latest/', LatestMeditationView.as_view()),
    path('search/', MeditationSearchView.as_view())
]

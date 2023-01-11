from django.urls import path
from articles.views import ArticleDetailView, ArticleListView
urlpatterns = [
    path('<int:pk>/', ArticleDetailView.as_view()),
    path('', ArticleListView.as_view()),
]

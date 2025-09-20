"""
URL configuration for recommendations app.
"""
from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('status/', views.recommendations_status, name='recommendations-status'),
    # Recommendation endpoints will be added here
    # path('', views.RecommendationsView.as_view(), name='recommendations'),
    # path('trending/', views.TrendingMoviesView.as_view(), name='trending'),
    # path('popular/', views.PopularMoviesView.as_view(), name='popular'),
]

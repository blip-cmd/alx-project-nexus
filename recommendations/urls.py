"""
URL configuration for recommendations app.
"""
from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    # Status endpoint
    path('status/', views.recommendations_status, name='recommendations-status'),
    
    # User recommendations
    path('for-me/', views.UserRecommendationsView.as_view(), name='user-recommendations'),
    
    # Trending and discovery
    path('trending/', views.TrendingMoviesView.as_view(), name='trending-movies'),
    
    # Similar movies
    path('movies/<int:movie_id>/similar/', views.SimilarMoviesView.as_view(), name='similar-movies'),
]

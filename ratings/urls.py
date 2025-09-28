"""
URL configura    # Movie-specific rating endpoints
    path('movies/<uuid:movie_id>/rate/', views.RateMovieView.as_view(), name='rate-movie'),
    path('movies/<uuid:movie_id>/favorite/', views.ToggleFavoriteView.as_view(), name='toggle-favorite'),
    path('movies/<uuid:movie_id>/watch/', views.AddToWatchHistoryView.as_view(), name='add-to-watchlist'),
    path('movies/<uuid:movie_id>/unwatch/', views.RemoveFromWatchHistoryView.as_view(), name='remove-from-watchlist'),
    
    # Movie rating analytics
    path('movies/<uuid:movie_id>/ratings/', views.MovieRatingsView.as_view(), name='movie-ratings'),
    path('movies/<uuid:movie_id>/stats/', views.MovieRatingStatsView.as_view(), name='movie-rating-stats'),ratings app.
"""
from django.urls import path
from . import views

app_name = 'ratings'

urlpatterns = [
    # Status endpoint
    path('status/', views.ratings_status, name='ratings-status'),
    
    # User rating endpoints
    path('my-ratings/', views.UserRatingsView.as_view(), name='user-ratings'),
    path('my-favorites/', views.UserFavoritesView.as_view(), name='user-favorites'),
    path('my-watchlist/', views.UserWatchHistoryView.as_view(), name='user-watchlist'),
    path('my-stats/', views.UserStatsView.as_view(), name='user-stats'),
    
    # Movie-specific rating endpoints
    path('movies/<int:movie_id>/rate/', views.RateMovieView.as_view(), name='rate-movie'),
    path('movies/<int:movie_id>/favorite/', views.ToggleFavoriteView.as_view(), name='toggle-favorite'),
    path('movies/<int:movie_id>/watch/', views.AddToWatchHistoryView.as_view(), name='add-to-watchlist'),
    path('movies/<int:movie_id>/unwatch/', views.RemoveFromWatchHistoryView.as_view(), name='remove-from-watchlist'),
    
    # Movie rating lists and stats
    path('movies/<int:movie_id>/ratings/', views.MovieRatingsView.as_view(), name='movie-ratings'),
    path('movies/<int:movie_id>/stats/', views.MovieRatingStatsView.as_view(), name='movie-rating-stats'),
]

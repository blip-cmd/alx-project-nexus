"""
URL configuration for ratings app.
"""
from django.urls import path
from . import views

app_name = 'ratings'

urlpatterns = [
    path('status/', views.ratings_status, name='ratings-status'),
    # Rating endpoints will be added here
    # path('', views.RatingListView.as_view(), name='rating-list'),
    # path('create/', views.RatingCreateView.as_view(), name='rating-create'),
    # path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    # path('watch-history/', views.WatchHistoryView.as_view(), name='watch-history'),
]

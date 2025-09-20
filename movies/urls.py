"""
URL configuration for movies app.
"""
from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('status/', views.movie_status, name='movie-status'),
    # Movie endpoints will be added here
    # path('', views.MovieListView.as_view(), name='movie-list'),
    # path('<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    # path('genres/', views.GenreListView.as_view(), name='genre-list'),
    # path('search/', views.MovieSearchView.as_view(), name='movie-search'),
]

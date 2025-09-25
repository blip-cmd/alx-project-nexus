"""
URL configuration for movies app.
"""
from django.urls import path
from . import views
from . import seed_api

app_name = 'movies'

urlpatterns = [
    # Status endpoint
    path('status/', views.movie_status, name='movie-status'),
    
    # Movie endpoints
    path('', views.MovieListView.as_view(), name='movie-list'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('create/', views.MovieCreateView.as_view(), name='movie-create'),
    path('<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),
    
    # Special movie lists
    path('popular/', views.PopularMoviesView.as_view(), name='popular-movies'),
    path('trending/', views.TrendingMoviesView.as_view(), name='trending-movies'),
    path('top-rated/', views.TopRatedMoviesView.as_view(), name='top-rated-movies'),
    
    # Genre endpoints
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    path('genres/create/', views.GenreCreateView.as_view(), name='genre-create'),
    path('genres/<int:pk>/update/', views.GenreUpdateView.as_view(), name='genre-update'),
    path('genres/<int:pk>/delete/', views.GenreDeleteView.as_view(), name='genre-delete'),
    path('genres/<int:genre_id>/movies/', views.GenreMoviesView.as_view(), name='genre-movies'),
    
    # Tag endpoints
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag-detail'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag-create'),
    path('tags/<int:pk>/update/', views.TagUpdateView.as_view(), name='tag-update'),
    path('tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag-delete'),
    path('tags/<int:tag_id>/movies/', views.TagMoviesView.as_view(), name='tag-movies'),
    
    # Admin data seeding endpoints (for production)
    path('admin/seed-data/', seed_api.seed_database, name='admin-seed-data'),
    path('admin/database-stats/', seed_api.database_stats, name='admin-db-stats'),
]

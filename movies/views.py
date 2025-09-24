"""
Views for movies app.
"""
from rest_framework import status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.core.cache import cache
from django.conf import settings

from .models import Movie, Genre, Tag
from .serializers import (
    MovieListSerializer, MovieDetailSerializer, MovieCreateUpdateSerializer,
    GenreSerializer, GenreCreateUpdateSerializer,
    TagSerializer, TagCreateUpdateSerializer
)
from movie_recommendation_project.cache_utils import MovieCacheManager, cache_view_result


class MoviePagination(PageNumberPagination):
    """
    Custom pagination for movies.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def movie_status(request):
    """
    API endpoint for checking movies app status.
    """
    movie_count = Movie.objects.count()
    genre_count = Genre.objects.count()
    tag_count = Tag.objects.count()
    
    return Response({
        'message': 'Movies app is working!',
        'stats': {
            'total_movies': movie_count,
            'total_genres': genre_count,
            'total_tags': tag_count,
        }
    }, status=status.HTTP_200_OK)


class MovieListView(ListAPIView):
    """
    API endpoint for listing movies with filtering, searching, and sorting.
    """
    serializer_class = MovieListSerializer
    pagination_class = MoviePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Search fields
    search_fields = ['title', 'description', 'genres__name', 'tags__name']
    
    # Ordering fields
    ordering_fields = ['title', 'release_date', 'imdb_rating', 'popularity_score', 'created_at']
    ordering = ['-popularity_score']  # Default ordering
    
    # Filter fields
    filterset_fields = {
        'release_date': ['year', 'year__gte', 'year__lte'],
        'imdb_rating': ['gte', 'lte'],
        'popularity_score': ['gte', 'lte'],
        'duration': ['gte', 'lte'],
        'genres': ['exact'],
        'tags': ['exact'],
    }
    
    def get_queryset(self):
        """
        Get movies queryset with optimized queries.
        """
        queryset = Movie.objects.select_related().prefetch_related(
            'genres', 'tags', 'ratings', 'favorited_by'
        ).all()
        
        # Filter by genre names
        genre_names = self.request.query_params.getlist('genre_name')
        if genre_names:
            queryset = queryset.filter(genres__name__in=genre_names)
            
        # Filter by tag names
        tag_names = self.request.query_params.getlist('tag_name')
        if tag_names:
            queryset = queryset.filter(tags__name__in=tag_names)
            
        # Filter by rating range
        min_rating = self.request.query_params.get('min_user_rating')
        max_rating = self.request.query_params.get('max_user_rating')
        if min_rating or max_rating:
            # Annotate with average rating
            queryset = queryset.annotate(avg_rating=Avg('ratings__rating'))
            if min_rating:
                queryset = queryset.filter(avg_rating__gte=float(min_rating))
            if max_rating:
                queryset = queryset.filter(avg_rating__lte=float(max_rating))
                
        return queryset.distinct()


class MovieDetailView(RetrieveAPIView):
    """
    API endpoint for retrieving a specific movie's details.
    """
    queryset = Movie.objects.select_related().prefetch_related(
        'genres', 'tags', 'ratings', 'favorited_by', 'watched_by'
    ).all()
    serializer_class = MovieDetailSerializer


class MovieCreateView(CreateAPIView):
    """
    API endpoint for creating movies (admin only).
    """
    queryset = Movie.objects.all()
    serializer_class = MovieCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        """
        Save the movie instance.
        """
        serializer.save()


class MovieUpdateView(UpdateAPIView):
    """
    API endpoint for updating movies (admin only).
    """
    queryset = Movie.objects.all()
    serializer_class = MovieCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class MovieDeleteView(DestroyAPIView):
    """
    API endpoint for deleting movies (admin only).
    """
    queryset = Movie.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        movie_title = instance.title
        self.perform_destroy(instance)
        return Response({
            'message': f'Movie "{movie_title}" deleted successfully'
        }, status=status.HTTP_200_OK)


class PopularMoviesView(ListAPIView):
    """
    API endpoint for popular movies with caching.
    """
    serializer_class = MovieListSerializer
    pagination_class = MoviePagination
    
    def get_queryset(self):
        """
        Get popular movies ordered by popularity score with caching.
        """
        # Generate cache key based on query parameters
        limit = int(self.request.GET.get('limit', 50))
        filters = {k: v for k, v in self.request.GET.items() 
                  if k not in ['page', 'page_size', 'limit']}
        
        # Try to get from cache using MovieCacheManager
        try:
            cached_movies = MovieCacheManager.get_popular_movies(limit=limit, **filters)
            # Convert to queryset for compatibility with serializer
            movie_ids = [movie.id for movie in cached_movies]
            return Movie.objects.filter(id__in=movie_ids).order_by('-popularity_score')
        except Exception:
            # Fallback to direct query if caching fails
            return Movie.objects.select_related().prefetch_related(
                'genres', 'tags', 'ratings', 'favorited_by'
            ).order_by('-popularity_score')[:limit]


class TrendingMoviesView(ListAPIView):
    """
    API endpoint for trending movies with caching.
    """
    serializer_class = MovieListSerializer
    pagination_class = MoviePagination
    
    def get_queryset(self):
        """
        Get trending movies with caching.
        """
        period = self.request.GET.get('period', 'weekly')
        limit = int(self.request.GET.get('limit', 20))
        
        # Try to get from cache using MovieCacheManager
        try:
            cached_movies = MovieCacheManager.get_trending_movies(period=period, limit=limit)
            # Convert to queryset for compatibility with serializer
            movie_ids = [movie.id for movie in cached_movies]
            return Movie.objects.filter(id__in=movie_ids).order_by('-popularity_score', '-imdb_rating')
        except Exception:
            # Fallback to direct query if caching fails
            from django.utils import timezone
            from datetime import timedelta
            
            # Get movies with recent activity
            if period == 'daily':
                recent_date = timezone.now() - timedelta(days=1)
            elif period == 'monthly':
                recent_date = timezone.now() - timedelta(days=30)
            else:  # weekly
                recent_date = timezone.now() - timedelta(weeks=1)
            
            return Movie.objects.select_related().prefetch_related(
                'genres', 'tags', 'ratings', 'favorited_by'
            ).annotate(
                recent_ratings=Count('ratings', filter=Q(ratings__rated_at__gte=recent_date)),
                recent_favorites=Count('favorited_by', filter=Q(favorited_by__favorited_at__gte=recent_date))
            ).filter(
            Q(recent_ratings__gt=0) | Q(recent_favorites__gt=0)
        ).order_by('-recent_ratings', '-recent_favorites')[:30]


class TopRatedMoviesView(ListAPIView):
    """
    API endpoint for top-rated movies.
    """
    serializer_class = MovieListSerializer
    pagination_class = MoviePagination
    
    def get_queryset(self):
        """
        Get top-rated movies by user ratings.
        """
        return Movie.objects.select_related().prefetch_related(
            'genres', 'tags', 'ratings', 'favorited_by'
        ).annotate(
            avg_rating=Avg('ratings__score'),
            rating_count=Count('ratings')
        ).filter(
            rating_count__gte=5  # At least 5 ratings
        ).order_by('-avg_rating')[:50]


# Genre Views
class GenreListView(ListAPIView):
    """
    API endpoint for listing all genres.
    """
    queryset = Genre.objects.annotate(movie_count=Count('movies')).all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'movie_count']
    ordering = ['name']


class GenreDetailView(RetrieveAPIView):
    """
    API endpoint for retrieving a specific genre's details.
    """
    queryset = Genre.objects.annotate(movie_count=Count('movies')).all()
    serializer_class = GenreSerializer


class GenreCreateView(CreateAPIView):
    """
    API endpoint for creating genres (admin only).
    """
    queryset = Genre.objects.all()
    serializer_class = GenreCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class GenreUpdateView(UpdateAPIView):
    """
    API endpoint for updating genres (admin only).
    """
    queryset = Genre.objects.all()
    serializer_class = GenreCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class GenreDeleteView(DestroyAPIView):
    """
    API endpoint for deleting genres (admin only).
    """
    queryset = Genre.objects.all()
    permission_classes = [permissions.IsAdminUser]


class GenreMoviesView(ListAPIView):
    """
    API endpoint for listing movies in a specific genre.
    """
    serializer_class = MovieListSerializer
    pagination_class = MoviePagination
    
    def get_queryset(self):
        """
        Get movies for a specific genre.
        """
        genre_id = self.kwargs['genre_id']
        return Movie.objects.select_related().prefetch_related(
            'genres', 'tags', 'ratings', 'favorited_by'
        ).filter(genres__id=genre_id).order_by('-popularity_score')


# Tag Views
class TagListView(ListAPIView):
    """
    API endpoint for listing all tags.
    """
    queryset = Tag.objects.annotate(movie_count=Count('movies')).all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'movie_count']
    ordering = ['name']


class TagDetailView(RetrieveAPIView):
    """
    API endpoint for retrieving a specific tag's details.
    """
    queryset = Tag.objects.annotate(movie_count=Count('movies')).all()
    serializer_class = TagSerializer


class TagCreateView(CreateAPIView):
    """
    API endpoint for creating tags (admin only).
    """
    queryset = Tag.objects.all()
    serializer_class = TagCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class TagUpdateView(UpdateAPIView):
    """
    API endpoint for updating tags (admin only).
    """
    queryset = Tag.objects.all()
    serializer_class = TagCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class TagDeleteView(DestroyAPIView):
    """
    API endpoint for deleting tags (admin only).
    """
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAdminUser]


class TagMoviesView(ListAPIView):
    """
    API endpoint for listing movies with a specific tag.
    """
    serializer_class = MovieListSerializer
    pagination_class = MoviePagination
    
    def get_queryset(self):
        """
        Get movies for a specific tag.
        """
        tag_id = self.kwargs['tag_id']
        return Movie.objects.select_related().prefetch_related(
            'genres', 'tags', 'ratings', 'favorited_by'
        ).filter(tags__id=tag_id).order_by('-popularity_score')

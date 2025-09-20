"""
Views for ratings app.
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404

from .models import Rating, Favorite, WatchHistory
from movies.models import Movie
from .serializers import (
    RatingSerializer, RatingCreateUpdateSerializer,
    FavoriteSerializer, WatchHistorySerializer,
    UserStatsSerializer, MovieRatingStatsSerializer
)


class RatingPagination(PageNumberPagination):
    """
    Custom pagination for ratings.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def ratings_status(request):
    """
    API endpoint for checking ratings app status.
    """
    rating_count = Rating.objects.count()
    favorite_count = Favorite.objects.count()
    watch_history_count = WatchHistory.objects.count()
    
    return Response({
        'message': 'Ratings app is working!',
        'stats': {
            'total_ratings': rating_count,
            'total_favorites': favorite_count,
            'total_watch_history': watch_history_count,
        }
    }, status=status.HTTP_200_OK)


# Rating Views
class UserRatingsView(ListAPIView):
    """
    API endpoint for listing current user's ratings.
    """
    serializer_class = RatingSerializer
    pagination_class = RatingPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get ratings for the current user.
        """
        return Rating.objects.filter(user=self.request.user).select_related('movie').order_by('-created_at')


class MovieRatingsView(ListAPIView):
    """
    API endpoint for listing ratings of a specific movie.
    """
    serializer_class = RatingSerializer
    pagination_class = RatingPagination
    
    def get_queryset(self):
        """
        Get ratings for a specific movie.
        """
        movie_id = self.kwargs['movie_id']
        return Rating.objects.filter(movie_id=movie_id).select_related('user', 'movie').order_by('-created_at')


class RateMovieView(APIView):
    """
    API endpoint for rating a movie.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, movie_id):
        """
        Rate a movie.
        """
        movie = get_object_or_404(Movie, id=movie_id)
        
        # Check if user already rated this movie
        existing_rating = Rating.objects.filter(user=request.user, movie=movie).first()
        
        serializer = RatingCreateUpdateSerializer(data=request.data, instance=existing_rating)
        
        if serializer.is_valid():
            if existing_rating:
                # Update existing rating
                rating = serializer.save()
                message = 'Rating updated successfully'
            else:
                # Create new rating
                rating = serializer.save(user=request.user, movie=movie)
                message = 'Rating created successfully'
                
            return Response({
                'message': message,
                'rating': RatingSerializer(rating).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, movie_id):
        """
        Get current user's rating for a movie.
        """
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            
        movie = get_object_or_404(Movie, id=movie_id)
        rating = Rating.objects.filter(user=request.user, movie=movie).first()
        
        if rating:
            return Response(RatingSerializer(rating).data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No rating found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, movie_id):
        """
        Delete user's rating for a movie.
        """
        movie = get_object_or_404(Movie, id=movie_id)
        rating = Rating.objects.filter(user=request.user, movie=movie).first()
        
        if rating:
            rating.delete()
            return Response({'message': 'Rating deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No rating found'}, status=status.HTTP_404_NOT_FOUND)


# Favorite Views
class UserFavoritesView(ListAPIView):
    """
    API endpoint for listing current user's favorite movies.
    """
    serializer_class = FavoriteSerializer
    pagination_class = RatingPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get favorites for the current user.
        """
        return Favorite.objects.filter(user=self.request.user).select_related('movie').order_by('-created_at')


class ToggleFavoriteView(APIView):
    """
    API endpoint for adding/removing a movie from favorites.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, movie_id):
        """
        Toggle favorite status for a movie.
        """
        movie = get_object_or_404(Movie, id=movie_id)
        favorite = Favorite.objects.filter(user=request.user, movie=movie).first()
        
        if favorite:
            # Remove from favorites
            favorite.delete()
            return Response({
                'message': 'Removed from favorites',
                'is_favorited': False
            }, status=status.HTTP_200_OK)
        else:
            # Add to favorites
            favorite = Favorite.objects.create(user=request.user, movie=movie)
            return Response({
                'message': 'Added to favorites',
                'is_favorited': True,
                'favorite': FavoriteSerializer(favorite).data
            }, status=status.HTTP_201_CREATED)


# Watch History Views
class UserWatchHistoryView(ListAPIView):
    """
    API endpoint for listing current user's watch history.
    """
    serializer_class = WatchHistorySerializer
    pagination_class = RatingPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get watch history for the current user.
        """
        return WatchHistory.objects.filter(user=self.request.user).select_related('movie').order_by('-watched_at')


class AddToWatchHistoryView(APIView):
    """
    API endpoint for adding a movie to watch history.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, movie_id):
        """
        Add or update watch history for a movie.
        """
        movie = get_object_or_404(Movie, id=movie_id)
        progress_minutes = request.data.get('progress_minutes', 0)
        
        # Create or update watch history
        watch_history, created = WatchHistory.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'progress_minutes': progress_minutes}
        )
        
        message = 'Added to watch history' if created else 'Watch history updated'
        
        return Response({
            'message': message,
            'watch_history': WatchHistorySerializer(watch_history).data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class RemoveFromWatchHistoryView(APIView):
    """
    API endpoint for removing a movie from watch history.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, movie_id):
        """
        Remove movie from watch history.
        """
        movie = get_object_or_404(Movie, id=movie_id)
        watch_history = WatchHistory.objects.filter(user=request.user, movie=movie).first()
        
        if watch_history:
            watch_history.delete()
            return Response({'message': 'Removed from watch history'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Movie not found in watch history'}, status=status.HTTP_404_NOT_FOUND)


# Statistics Views
class UserStatsView(APIView):
    """
    API endpoint for getting user statistics.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get statistics for the current user.
        """
        user = request.user
        
        # Calculate stats
        ratings = Rating.objects.filter(user=user)
        favorites = Favorite.objects.filter(user=user)
        watch_history = WatchHistory.objects.filter(user=user)
        
        # Basic stats
        total_ratings = ratings.count()
        average_rating_given = ratings.aggregate(avg=Avg('rating'))['avg'] or 0
        total_favorites = favorites.count()
        total_watch_time = watch_history.aggregate(sum=Sum('progress_minutes'))['sum'] or 0
        
        # Favorite genres
        favorite_genres = list(
            favorites.values('movie__genres__name')
            .annotate(count=Count('movie__genres__name'))
            .order_by('-count')[:5]
            .values_list('movie__genres__name', flat=True)
        )
        
        # Most rated genre
        most_rated_genre = (
            ratings.values('movie__genres__name')
            .annotate(count=Count('movie__genres__name'))
            .order_by('-count')
            .first()
        )
        most_rated_genre_name = most_rated_genre['movie__genres__name'] if most_rated_genre else 'None'
        
        # Movies watched this month
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        movies_watched_this_month = watch_history.filter(watched_at__gte=current_month).count()
        
        stats = {
            'total_ratings': total_ratings,
            'average_rating_given': round(average_rating_given, 1),
            'total_favorites': total_favorites,
            'total_watch_time_minutes': total_watch_time,
            'favorite_genres': favorite_genres,
            'most_rated_genre': most_rated_genre_name,
            'movies_watched_this_month': movies_watched_this_month,
        }
        
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieRatingStatsView(APIView):
    """
    API endpoint for getting movie rating statistics.
    """
    def get(self, request, movie_id):
        """
        Get rating statistics for a specific movie.
        """
        movie = get_object_or_404(Movie, id=movie_id)
        ratings = Rating.objects.filter(movie=movie)
        
        # Basic stats
        total_ratings = ratings.count()
        average_rating = ratings.aggregate(avg=Avg('rating'))['avg'] or 0
        
        # Rating distribution
        rating_distribution = {}
        for i in range(1, 6):
            rating_distribution[str(i)] = ratings.filter(rating=i).count()
        
        # Recent ratings (last 10)
        recent_ratings = list(
            ratings.select_related('user')
            .order_by('-created_at')[:10]
            .values('user__username', 'rating', 'review', 'created_at')
        )
        
        stats = {
            'movie_id': movie.id,
            'movie_title': movie.title,
            'total_ratings': total_ratings,
            'average_rating': round(average_rating, 1),
            'rating_distribution': rating_distribution,
            'recent_ratings': recent_ratings,
        }
        
        serializer = MovieRatingStatsSerializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)

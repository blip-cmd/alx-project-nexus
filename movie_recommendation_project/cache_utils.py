# 🗄️ Movie Recommendation API - Caching Utilities

from django.core.cache import cache
from django.conf import settings
from django.db.models import QuerySet
from typing import Any, Optional, Callable
import json
import hashlib


class CacheManager:
    """
    Centralized cache management for the movie recommendation system.
    """
    
    @staticmethod
    def get_cache_key(prefix: str, *args, **kwargs) -> str:
        """
        Generate a consistent cache key from prefix and arguments.
        
        Args:
            prefix: Cache key prefix
            *args: Additional arguments to include in key
            **kwargs: Keyword arguments to include in key
            
        Returns:
            str: Generated cache key
        """
        # Create a hash of arguments for consistent key generation
        key_data = f"{prefix}:{':'.join(map(str, args))}"
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            kwargs_str = ':'.join(f"{k}={v}" for k, v in sorted_kwargs)
            key_data += f":{kwargs_str}"
        
        # Hash the key if it's too long
        if len(key_data) > 200:
            key_hash = hashlib.md5(key_data.encode()).hexdigest()
            key_data = f"{prefix}:{key_hash}"
        
        return key_data
    
    @staticmethod
    def get_timeout(cache_type: str) -> int:
        """
        Get cache timeout for a specific cache type.
        
        Args:
            cache_type: Type of cache (e.g., 'movies_popular', 'recommendations')
            
        Returns:
            int: Timeout in seconds
        """
        return getattr(settings, 'CACHE_TTL', {}).get(cache_type, 300)
    
    @staticmethod
    def cached_query(cache_key: str, query_func: Callable, timeout: Optional[int] = None) -> Any:
        """
        Cache the result of a database query.
        
        Args:
            cache_key: Key to store the result under
            query_func: Function that returns the query result
            timeout: Cache timeout in seconds
            
        Returns:
            Query result (from cache or fresh)
        """
        # Try to get from cache first
        result = cache.get(cache_key)
        if result is not None:
            return result
        
        # If not in cache, execute query and cache result
        result = query_func()
        
        # Serialize QuerySet to list for caching
        if isinstance(result, QuerySet):
            result = list(result)
        
        cache.set(cache_key, result, timeout or 300)
        return result
    
    @staticmethod
    def invalidate_pattern(pattern: str) -> None:
        """
        Invalidate all cache keys matching a pattern.
        
        Args:
            pattern: Pattern to match cache keys
        """
        # Note: This is a simplified implementation
        # In production, consider using Redis key patterns or cache tagging
        try:
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            keys = redis_conn.keys(f"*{pattern}*")
            if keys:
                redis_conn.delete(*keys)
        except Exception:
            # Fallback to clearing all cache if Redis operations fail
            cache.clear()


class MovieCacheManager(CacheManager):
    """
    Specialized cache manager for movie-related operations.
    """
    
    @classmethod
    def get_popular_movies(cls, limit: int = 20, **filters) -> Any:
        """
        Get popular movies with caching.
        """
        from movies.models import Movie
        
        cache_key = cls.get_cache_key('movies_popular', limit, **filters)
        timeout = cls.get_timeout('movies_popular')
        
        def query_func():
            queryset = Movie.objects.select_related().prefetch_related('genres', 'tags')
            
            # Apply filters
            for key, value in filters.items():
                if hasattr(Movie, key.split('__')[0]):
                    queryset = queryset.filter(**{key: value})
            
            return queryset.order_by('-popularity_score')[:limit]
        
        return cls.cached_query(cache_key, query_func, timeout)
    
    @classmethod
    def get_trending_movies(cls, period: str = 'weekly', limit: int = 20) -> Any:
        """
        Get trending movies with caching.
        """
        from movies.models import Movie
        from django.utils import timezone
        from datetime import timedelta
        
        cache_key = cls.get_cache_key('movies_trending', period, limit)
        timeout = cls.get_timeout('movies_trending')
        
        def query_func():
            now = timezone.now()
            
            # Calculate date threshold based on period
            if period == 'daily':
                date_threshold = now - timedelta(days=1)
            elif period == 'weekly':
                date_threshold = now - timedelta(weeks=1)
            elif period == 'monthly':
                date_threshold = now - timedelta(days=30)
            else:
                date_threshold = now - timedelta(weeks=1)
            
            return Movie.objects.select_related().prefetch_related('genres', 'tags').filter(
                created_at__gte=date_threshold
            ).order_by('-popularity_score', '-imdb_rating')[:limit]
        
        return cls.cached_query(cache_key, query_func, timeout)
    
    @classmethod
    def get_movie_stats(cls, movie_id: int) -> Any:
        """
        Get movie statistics with caching.
        """
        from django.db.models import Avg, Count
        from ratings.models import Rating
        
        cache_key = cls.get_cache_key('movie_stats', movie_id)
        timeout = cls.get_timeout('movie_stats')
        
        def query_func():
            stats = Rating.objects.filter(movie_id=movie_id).aggregate(
                average_rating=Avg('rating'),
                total_ratings=Count('id')
            )
            return {
                'average_rating': round(stats['average_rating'] or 0, 2),
                'total_ratings': stats['total_ratings']
            }
        
        return cls.cached_query(cache_key, query_func, timeout)
    
    @classmethod
    def invalidate_movie_cache(cls, movie_id: Optional[int] = None) -> None:
        """
        Invalidate movie-related cache.
        """
        patterns = ['movies_popular', 'movies_trending', 'movies_list']
        
        if movie_id:
            patterns.extend([f'movie_stats_{movie_id}', f'movie_{movie_id}'])
        
        for pattern in patterns:
            cls.invalidate_pattern(pattern)


class RecommendationCacheManager(CacheManager):
    """
    Specialized cache manager for recommendation operations.
    """
    
    @classmethod
    def get_user_recommendations(cls, user_id: int, algorithm: str = 'hybrid', 
                               limit: int = 10, **params) -> Any:
        """
        Get user recommendations with caching.
        """
        cache_key = cls.get_cache_key('recommendations', user_id, algorithm, limit, **params)
        timeout = cls.get_timeout('recommendations')
        
        def query_func():
            from recommendations.views import RecommendationEngine
            engine = RecommendationEngine()
            
            if algorithm == 'popularity':
                return engine.get_popularity_based_recommendations(limit, **params)
            elif algorithm == 'genre':
                return engine.get_genre_based_recommendations(user_id, limit, **params)
            elif algorithm == 'collaborative':
                return engine.get_collaborative_filtering_recommendations(user_id, limit)
            elif algorithm == 'content':
                return engine.get_content_based_recommendations(user_id, limit)
            else:  # hybrid
                return engine.get_hybrid_recommendations(user_id, limit, **params)
        
        return cls.cached_query(cache_key, query_func, timeout)
    
    @classmethod
    def get_similar_movies(cls, movie_id: int, method: str = 'combined', limit: int = 10) -> Any:
        """
        Get similar movies with caching.
        """
        cache_key = cls.get_cache_key('similar_movies', movie_id, method, limit)
        timeout = cls.get_timeout('recommendations')
        
        def query_func():
            from recommendations.views import RecommendationEngine
            engine = RecommendationEngine()
            return engine.get_similar_movies(movie_id, method, limit)
        
        return cls.cached_query(cache_key, query_func, timeout)
    
    @classmethod
    def invalidate_user_recommendations(cls, user_id: int) -> None:
        """
        Invalidate user-specific recommendation cache.
        """
        cls.invalidate_pattern(f'recommendations:{user_id}')


class UserCacheManager(CacheManager):
    """
    Specialized cache manager for user-related operations.
    """
    
    @classmethod
    def get_user_stats(cls, user_id: int) -> Any:
        """
        Get user statistics with caching.
        """
        cache_key = cls.get_cache_key('user_stats', user_id)
        timeout = cls.get_timeout('user_stats')
        
        def query_func():
            from django.db.models import Avg, Count
            from ratings.models import Rating, Favorite, WatchHistory
            
            # Get user rating statistics
            rating_stats = Rating.objects.filter(user_id=user_id).aggregate(
                total_ratings=Count('id'),
                average_rating=Avg('rating')
            )
            
            # Get favorites count
            favorites_count = Favorite.objects.filter(user_id=user_id).count()
            
            # Get watch history count
            watch_history_count = WatchHistory.objects.filter(user_id=user_id).count()
            
            return {
                'total_ratings': rating_stats['total_ratings'],
                'average_rating': round(rating_stats['average_rating'] or 0, 2),
                'total_favorites': favorites_count,
                'total_watched': watch_history_count
            }
        
        return cls.cached_query(cache_key, query_func, timeout)
    
    @classmethod
    def invalidate_user_cache(cls, user_id: int) -> None:
        """
        Invalidate user-specific cache.
        """
        patterns = [f'user_stats:{user_id}', f'recommendations:{user_id}']
        
        for pattern in patterns:
            cls.invalidate_pattern(pattern)


# Decorators for easy caching
def cache_view_result(cache_key_prefix: str, timeout: Optional[int] = None):
    """
    Decorator to cache view results.
    
    Args:
        cache_key_prefix: Prefix for the cache key
        timeout: Cache timeout in seconds
    """
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            # Generate cache key from request parameters
            cache_key = CacheManager.get_cache_key(
                cache_key_prefix,
                request.user.id if request.user.is_authenticated else 'anonymous',
                *args,
                **dict(request.GET.items())
            )
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # If not cached, execute view
            result = view_func(self, request, *args, **kwargs)
            
            # Cache the result
            cache.set(cache_key, result, timeout or 300)
            return result
        
        return wrapper
    return decorator


# Cache invalidation signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender='movies.Movie')
@receiver(post_delete, sender='movies.Movie')
def invalidate_movie_cache_on_change(sender, instance, **kwargs):
    """Invalidate movie cache when movies are created, updated, or deleted."""
    MovieCacheManager.invalidate_movie_cache(instance.id)


@receiver(post_save, sender='ratings.Rating')
@receiver(post_delete, sender='ratings.Rating')
def invalidate_rating_cache_on_change(sender, instance, **kwargs):
    """Invalidate caches when ratings change."""
    MovieCacheManager.invalidate_movie_cache(instance.movie.id)
    UserCacheManager.invalidate_user_cache(instance.user.id)
    RecommendationCacheManager.invalidate_user_recommendations(instance.user.id)


@receiver(post_save, sender='ratings.Favorite')
@receiver(post_delete, sender='ratings.Favorite')
def invalidate_favorite_cache_on_change(sender, instance, **kwargs):
    """Invalidate caches when favorites change."""
    UserCacheManager.invalidate_user_cache(instance.user.id)
    RecommendationCacheManager.invalidate_user_recommendations(instance.user.id)


@receiver(post_save, sender='ratings.WatchHistory')
@receiver(post_delete, sender='ratings.WatchHistory')
def invalidate_watch_history_cache_on_change(sender, instance, **kwargs):
    """Invalidate caches when watch history changes."""
    UserCacheManager.invalidate_user_cache(instance.user.id)
    RecommendationCacheManager.invalidate_user_recommendations(instance.user.id)

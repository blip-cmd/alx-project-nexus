"""
Views for recommendations app.
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from datetime import timedelta
from collections import Counter
import random

from movies.models import Movie, Genre, Tag
from ratings.models import Rating, Favorite, WatchHistory
from .serializers import (
    RecommendationSerializer, RecommendationRequestSerializer,
    TrendingMoviesSerializer, SimilarMoviesSerializer
)
from movie_recommendation_project.cache_utils import RecommendationCacheManager, MovieCacheManager


class RecommendationPagination(PageNumberPagination):
    """
    Custom pagination for recommendations.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recommendations_status(request):
    """
    API endpoint for checking recommendations app status.
    """
    total_movies = Movie.objects.count()
    total_ratings = Rating.objects.count()
    
    return Response({
        'message': 'Recommendations app is working!',
        'stats': {
            'total_movies': total_movies,
            'total_ratings': total_ratings,
            'algorithms_available': ['popularity', 'genre', 'collaborative', 'content', 'hybrid']
        }
    }, status=status.HTTP_200_OK)


class RecommendationEngine:
    """
    Core recommendation engine with multiple algorithms.
    """
    
    @staticmethod
    def popularity_based(user=None, limit=10, min_rating=0.0):
        """
        Get popular movies based on ratings and favorites.
        """
        movies = Movie.objects.annotate(
            avg_rating=Avg('ratings__rating'),
            rating_count=Count('ratings'),
            favorite_count=Count('favorites')
        ).filter(
            rating_count__gte=1,
            imdb_rating__gte=min_rating
        ).order_by('-popularity_score', '-avg_rating')[:limit]
        
        recommendations = []
        for movie in movies:
            recommendations.append({
                'movie': movie,
                'score': movie.popularity_score,
                'reason': f'Popular movie with {movie.rating_count} ratings',
                'algorithm': 'popularity'
            })
        
        return recommendations
    
    @staticmethod
    def genre_based(user, limit=10, min_rating=0.0):
        """
        Recommend movies based on user's favorite genres.
        """
        if not user or not user.is_authenticated:
            return RecommendationEngine.popularity_based(limit=limit, min_rating=min_rating)
        
        # Get user's favorite genres from ratings and favorites
        user_ratings = Rating.objects.filter(user=user, rating__gte=4)
        user_favorites = Favorite.objects.filter(user=user)
        
        # Count genre preferences
        genre_scores = Counter()
        
        for rating in user_ratings:
            for genre in rating.movie.genres.all():
                genre_scores[genre.id] += rating.rating
                
        for favorite in user_favorites:
            for genre in favorite.movie.genres.all():
                genre_scores[genre.id] += 5  # Weight favorites highly
        
        if not genre_scores:
            return RecommendationEngine.popularity_based(limit=limit, min_rating=min_rating)
        
        # Get top genres
        top_genres = [genre_id for genre_id, _ in genre_scores.most_common(5)]
        
        # Get movies from these genres, excluding already rated ones
        rated_movie_ids = user_ratings.values_list('movie_id', flat=True)
        favorite_movie_ids = user_favorites.values_list('movie_id', flat=True)
        excluded_ids = set(rated_movie_ids) | set(favorite_movie_ids)
        
        movies = Movie.objects.filter(
            genres__id__in=top_genres,
            imdb_rating__gte=min_rating
        ).exclude(
            id__in=excluded_ids
        ).annotate(
            avg_rating=Avg('ratings__rating'),
            rating_count=Count('ratings')
        ).order_by('-popularity_score', '-avg_rating').distinct()[:limit]
        
        recommendations = []
        for movie in movies:
            matching_genres = [g.name for g in movie.genres.all() if g.id in top_genres]
            recommendations.append({
                'movie': movie,
                'score': movie.popularity_score,
                'reason': f'Based on your interest in {", ".join(matching_genres[:2])}',
                'algorithm': 'genre'
            })
        
        return recommendations
    
    @staticmethod
    def collaborative_filtering(user, limit=10, min_rating=0.0):
        """
        Collaborative filtering based on similar users.
        """
        if not user or not user.is_authenticated:
            return RecommendationEngine.popularity_based(limit=limit, min_rating=min_rating)
        
        # Get user's ratings
        user_ratings = Rating.objects.filter(user=user)
        if user_ratings.count() < 3:
            return RecommendationEngine.genre_based(user, limit=limit, min_rating=min_rating)
        
        user_movie_ratings = {r.movie_id: r.rating for r in user_ratings}
        
        # Find similar users based on common movie ratings
        similar_users = []
        for other_user_rating in Rating.objects.exclude(user=user).select_related('user'):
            other_user = other_user_rating.user
            if other_user.id in [u[0] for u in similar_users]:
                continue
                
            other_ratings = {r.movie_id: r.rating for r in Rating.objects.filter(user=other_user)}
            
            # Calculate similarity score
            common_movies = set(user_movie_ratings.keys()) & set(other_ratings.keys())
            if len(common_movies) >= 2:
                similarity = sum(
                    1 - abs(user_movie_ratings[movie_id] - other_ratings[movie_id]) / 4
                    for movie_id in common_movies
                ) / len(common_movies)
                
                if similarity > 0.5:  # Threshold for similarity
                    similar_users.append((other_user.id, similarity))
        
        if not similar_users:
            return RecommendationEngine.genre_based(user, limit=limit, min_rating=min_rating)
        
        # Get recommendations from similar users
        similar_user_ids = [user_id for user_id, _ in sorted(similar_users, key=lambda x: x[1], reverse=True)[:10]]
        
        recommended_movies = Rating.objects.filter(
            user_id__in=similar_user_ids,
            rating__gte=4
        ).exclude(
            movie_id__in=user_movie_ratings.keys()
        ).values('movie').annotate(
            avg_score=Avg('rating'),
            count=Count('rating')
        ).filter(
            count__gte=2,
            movie__imdb_rating__gte=min_rating
        ).order_by('-avg_score', '-count')[:limit]
        
        recommendations = []
        for item in recommended_movies:
            movie = Movie.objects.get(id=item['movie'])
            recommendations.append({
                'movie': movie,
                'score': item['avg_score'],
                'reason': f'Recommended by {item["count"]} similar users',
                'algorithm': 'collaborative'
            })
        
        return recommendations
    
    @staticmethod
    def content_based(user, limit=10, min_rating=0.0):
        """
        Content-based filtering using movie features.
        """
        if not user or not user.is_authenticated:
            return RecommendationEngine.popularity_based(limit=limit, min_rating=min_rating)
        
        # Get user's highly rated movies
        user_favorites = Rating.objects.filter(user=user, rating__gte=4)
        if not user_favorites.exists():
            return RecommendationEngine.genre_based(user, limit=limit, min_rating=min_rating)
        
        # Analyze user preferences
        preferred_genres = Counter()
        preferred_tags = Counter()
        preferred_decades = Counter()
        
        for rating in user_favorites:
            movie = rating.movie
            
            # Genre preferences
            for genre in movie.genres.all():
                preferred_genres[genre.id] += rating.rating
            
            # Tag preferences
            for tag in movie.tags.all():
                preferred_tags[tag.id] += rating.rating
            
            # Decade preferences
            decade = (movie.release_date.year // 10) * 10
            preferred_decades[decade] += rating.rating
        
        # Get candidate movies
        rated_movie_ids = Rating.objects.filter(user=user).values_list('movie_id', flat=True)
        
        candidate_movies = Movie.objects.exclude(
            id__in=rated_movie_ids
        ).filter(
            imdb_rating__gte=min_rating
        ).prefetch_related('genres', 'tags')
        
        # Score movies based on content similarity
        scored_movies = []
        for movie in candidate_movies:
            score = 0
            reasons = []
            
            # Genre similarity
            for genre in movie.genres.all():
                if genre.id in preferred_genres:
                    score += preferred_genres[genre.id] * 0.4
                    reasons.append(f"{genre.name}")
            
            # Tag similarity
            for tag in movie.tags.all():
                if tag.id in preferred_tags:
                    score += preferred_tags[tag.id] * 0.3
            
            # Decade similarity
            decade = (movie.release_date.year // 10) * 10
            if decade in preferred_decades:
                score += preferred_decades[decade] * 0.3
            
            if score > 0:
                reason = f"Similar to your preferences: {', '.join(reasons[:2])}"
                scored_movies.append({
                    'movie': movie,
                    'score': score,
                    'reason': reason,
                    'algorithm': 'content'
                })
        
        # Sort by score and return top recommendations
        scored_movies.sort(key=lambda x: x['score'], reverse=True)
        return scored_movies[:limit]
    
    @staticmethod
    def hybrid_recommendations(user, limit=10, min_rating=0.0):
        """
        Hybrid approach combining multiple algorithms.
        """
        if not user or not user.is_authenticated:
            return RecommendationEngine.popularity_based(limit=limit, min_rating=min_rating)
        
        # Get recommendations from different algorithms
        popularity_recs = RecommendationEngine.popularity_based(user, limit=limit//2, min_rating=min_rating)
        genre_recs = RecommendationEngine.genre_based(user, limit=limit//2, min_rating=min_rating)
        
        # Try collaborative and content-based if user has enough data
        user_rating_count = Rating.objects.filter(user=user).count()
        if user_rating_count >= 5:
            collaborative_recs = RecommendationEngine.collaborative_filtering(user, limit=limit//3, min_rating=min_rating)
            content_recs = RecommendationEngine.content_based(user, limit=limit//3, min_rating=min_rating)
        else:
            collaborative_recs = []
            content_recs = []
        
        # Combine and deduplicate recommendations
        all_recs = popularity_recs + genre_recs + collaborative_recs + content_recs
        seen_movies = set()
        final_recs = []
        
        for rec in all_recs:
            if rec['movie'].id not in seen_movies:
                seen_movies.add(rec['movie'].id)
                rec['algorithm'] = 'hybrid'
                final_recs.append(rec)
                
                if len(final_recs) >= limit:
                    break
        
        return final_recs


class UserRecommendationsView(APIView):
    """
    API endpoint for getting personalized recommendations with caching.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get personalized recommendations for the user with caching.
        """
        serializer = RecommendationRequestSerializer(data=request.query_params)
        
        if serializer.is_valid():
            algorithm = serializer.validated_data['algorithm']
            limit = serializer.validated_data['limit']
            min_rating = serializer.validated_data['min_rating']
            
            # Try to get from cache first
            try:
                recommendations = RecommendationCacheManager.get_user_recommendations(
                    user_id=request.user.id,
                    algorithm=algorithm,
                    limit=limit,
                    min_rating=min_rating
                )
                
                # If recommendations is a queryset, convert to list
                if hasattr(recommendations, 'values'):
                    recommendations = list(recommendations)
                
                return Response({
                    'algorithm_used': algorithm,
                    'total_recommendations': len(recommendations),
                    'recommendations': RecommendationSerializer(recommendations, many=True).data,
                    'cached': True
                }, status=status.HTTP_200_OK)
                
            except Exception:
                # Fallback to direct computation if caching fails
                engine = RecommendationEngine()
                
                if algorithm == 'popularity':
                    recommendations = engine.get_popularity_based_recommendations(
                        limit=limit, min_rating=min_rating
                    )
                elif algorithm == 'genre':
                    recommendations = engine.get_genre_based_recommendations(
                        request.user.id, limit=limit, min_rating=min_rating
                    )
                elif algorithm == 'collaborative':
                    recommendations = engine.get_collaborative_filtering_recommendations(
                        request.user.id, limit=limit
                    )
                elif algorithm == 'content':
                    recommendations = engine.get_content_based_recommendations(
                        request.user.id, limit=limit
                    )
                else:  # hybrid
                    recommendations = engine.get_hybrid_recommendations(
                        request.user.id, limit=limit, min_rating=min_rating
                    )
                
                return Response({
                    'algorithm_used': algorithm,
                    'total_recommendations': len(recommendations),
                    'recommendations': RecommendationSerializer(recommendations, many=True).data,
                    'cached': False
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrendingMoviesView(APIView):
    """
    API endpoint for trending movies.
    """
    def get(self, request):
        """
        Get trending movies based on recent activity.
        """
        serializer = TrendingMoviesSerializer(data=request.query_params)
        
        if serializer.is_valid():
            period = serializer.validated_data['period']
            limit = serializer.validated_data['limit']
            
            # Calculate date threshold
            now = timezone.now()
            if period == 'daily':
                threshold = now - timedelta(days=1)
            elif period == 'weekly':
                threshold = now - timedelta(days=7)
            else:  # monthly
                threshold = now - timedelta(days=30)
            
            # Get trending movies
            trending_movies = Movie.objects.annotate(
                recent_ratings=Count('ratings', filter=Q(ratings__created_at__gte=threshold)),
                recent_favorites=Count('favorites', filter=Q(favorites__created_at__gte=threshold)),
                recent_watches=Count('watch_history', filter=Q(watch_history__watched_at__gte=threshold)),
                trend_score=F('recent_ratings') + F('recent_favorites') * 2 + F('recent_watches')
            ).filter(
                trend_score__gt=0
            ).order_by('-trend_score', '-popularity_score')[:limit]
            
            recommendations = []
            for movie in trending_movies:
                recommendations.append({
                    'movie': movie,
                    'score': movie.trend_score,
                    'reason': f'Trending in the last {period.replace("ly", "")}',
                    'algorithm': 'trending'
                })
            
            return Response({
                'period': period,
                'total_trending': len(recommendations),
                'recommendations': RecommendationSerializer(recommendations, many=True).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SimilarMoviesView(APIView):
    """
    API endpoint for finding movies similar to a given movie.
    """
    def get(self, request, movie_id):
        """
        Get movies similar to the specified movie.
        """
        try:
            target_movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'detail': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SimilarMoviesSerializer(data=request.query_params)
        
        if serializer.is_valid():
            method = serializer.validated_data['method']
            limit = serializer.validated_data['limit']
            
            similar_movies = []
            
            if method in ['genre', 'combined']:
                # Genre-based similarity
                target_genres = target_movie.genres.all()
                genre_similar = Movie.objects.filter(
                    genres__in=target_genres
                ).exclude(
                    id=movie_id
                ).annotate(
                    common_genres=Count('genres', filter=Q(genres__in=target_genres))
                ).order_by('-common_genres', '-popularity_score')[:limit]
                
                for movie in genre_similar:
                    common_genre_names = [g.name for g in movie.genres.all() if g in target_genres]
                    similar_movies.append({
                        'movie': movie,
                        'score': movie.common_genres,
                        'reason': f'Shares genres: {", ".join(common_genre_names[:2])}',
                        'algorithm': 'genre_similarity'
                    })
            
            if method in ['tags', 'combined']:
                # Tag-based similarity
                target_tags = target_movie.tags.all()
                if target_tags.exists():
                    tag_similar = Movie.objects.filter(
                        tags__in=target_tags
                    ).exclude(
                        id=movie_id
                    ).annotate(
                        common_tags=Count('tags', filter=Q(tags__in=target_tags))
                    ).order_by('-common_tags', '-popularity_score')[:limit//2]
                    
                    for movie in tag_similar:
                        if movie.id not in [sm['movie'].id for sm in similar_movies]:
                            common_tag_names = [t.name for t in movie.tags.all() if t in target_tags]
                            similar_movies.append({
                                'movie': movie,
                                'score': movie.common_tags,
                                'reason': f'Similar themes: {", ".join(common_tag_names[:2])}',
                                'algorithm': 'tag_similarity'
                            })
            
            # Sort by score and limit results
            similar_movies.sort(key=lambda x: x['score'], reverse=True)
            similar_movies = similar_movies[:limit]
            
            return Response({
                'target_movie': {
                    'id': target_movie.id,
                    'title': target_movie.title,
                },
                'method_used': method,
                'total_similar': len(similar_movies),
                'similar_movies': RecommendationSerializer(similar_movies, many=True).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

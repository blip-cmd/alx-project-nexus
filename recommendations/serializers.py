"""
Serializers for recommendations app.
"""
from rest_framework import serializers
from movies.models import Movie
from movies.serializers import MovieListSerializer


class RecommendationSerializer(serializers.Serializer):
    """
    Serializer for movie recommendations.
    """
    movie = MovieListSerializer(read_only=True)
    score = serializers.FloatField(read_only=True)
    reason = serializers.CharField(read_only=True)
    algorithm = serializers.CharField(read_only=True)


class RecommendationRequestSerializer(serializers.Serializer):
    """
    Serializer for recommendation requests.
    """
    ALGORITHM_CHOICES = [
        ('popularity', 'Popularity-based'),
        ('genre', 'Genre-based'),
        ('collaborative', 'Collaborative filtering'),
        ('content', 'Content-based'),
        ('hybrid', 'Hybrid approach'),
    ]
    
    algorithm = serializers.ChoiceField(
        choices=ALGORITHM_CHOICES,
        default='hybrid',
        help_text="Algorithm to use for recommendations"
    )
    limit = serializers.IntegerField(
        default=10,
        min_value=1,
        max_value=50,
        help_text="Number of recommendations to return"
    )
    exclude_rated = serializers.BooleanField(
        default=True,
        help_text="Exclude movies the user has already rated"
    )
    exclude_watched = serializers.BooleanField(
        default=False,
        help_text="Exclude movies the user has already watched"
    )
    min_rating = serializers.FloatField(
        default=0.0,
        min_value=0.0,
        max_value=10.0,
        help_text="Minimum IMDB rating for recommended movies"
    )


class TrendingMoviesSerializer(serializers.Serializer):
    """
    Serializer for trending movies.
    """
    period = serializers.ChoiceField(
        choices=[
            ('daily', 'Last 24 hours'),
            ('weekly', 'Last 7 days'),
            ('monthly', 'Last 30 days'),
        ],
        default='weekly'
    )
    limit = serializers.IntegerField(default=20, min_value=1, max_value=100)


class SimilarMoviesSerializer(serializers.Serializer):
    """
    Serializer for finding similar movies.
    """
    method = serializers.ChoiceField(
        choices=[
            ('genre', 'Genre similarity'),
            ('tags', 'Tag similarity'),
            ('rating', 'Rating similarity'),
            ('combined', 'Combined approach'),
        ],
        default='combined'
    )
    limit = serializers.IntegerField(default=10, min_value=1, max_value=30)

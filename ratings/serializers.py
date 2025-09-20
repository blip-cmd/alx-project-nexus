"""
Serializers for ratings app.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rating, Favorite, WatchHistory
from movies.models import Movie


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for movie ratings.
    """
    user = serializers.StringRelatedField(read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_poster = serializers.URLField(source='movie.poster_image', read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'user', 'movie', 'movie_title', 'movie_poster', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        
    def validate_rating(self, value):
        """
        Validate rating is between 1 and 5.
        """
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
        
    def validate_movie(self, value):
        """
        Validate movie exists.
        """
        if not Movie.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Movie does not exist.")
        return value
        
    def create(self, validated_data):
        """
        Create a new rating or update existing one.
        """
        user = self.context['request'].user
        movie = validated_data['movie']
        
        # Check if rating already exists
        rating, created = Rating.objects.update_or_create(
            user=user,
            movie=movie,
            defaults={
                'rating': validated_data['rating'],
                'review': validated_data.get('review', '')
            }
        )
        
        return rating


class RatingCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating ratings.
    """
    class Meta:
        model = Rating
        fields = ['movie', 'rating', 'review']
        
    def validate_rating(self, value):
        """
        Validate rating is between 1 and 5.
        """
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for user favorites.
    """
    user = serializers.StringRelatedField(read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_poster = serializers.URLField(source='movie.poster_image', read_only=True)
    movie_release_date = serializers.DateField(source='movie.release_date', read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'movie', 'movie_title', 'movie_poster', 'movie_release_date', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class WatchHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for watch history.
    """
    user = serializers.StringRelatedField(read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_poster = serializers.URLField(source='movie.poster_image', read_only=True)
    movie_duration = serializers.IntegerField(source='movie.duration', read_only=True)
    
    class Meta:
        model = WatchHistory
        fields = ['id', 'user', 'movie', 'movie_title', 'movie_poster', 'movie_duration', 'watched_at', 'progress_minutes']
        read_only_fields = ['id', 'user', 'watched_at']
        
    def validate_progress_minutes(self, value):
        """
        Validate progress is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Progress cannot be negative.")
        return value


class UserStatsSerializer(serializers.Serializer):
    """
    Serializer for user statistics.
    """
    total_ratings = serializers.IntegerField()
    average_rating_given = serializers.FloatField()
    total_favorites = serializers.IntegerField()
    total_watch_time_minutes = serializers.IntegerField()
    favorite_genres = serializers.ListField()
    most_rated_genre = serializers.CharField()
    movies_watched_this_month = serializers.IntegerField()


class MovieRatingStatsSerializer(serializers.Serializer):
    """
    Serializer for movie rating statistics.
    """
    movie_id = serializers.IntegerField()
    movie_title = serializers.CharField()
    total_ratings = serializers.IntegerField()
    average_rating = serializers.FloatField()
    rating_distribution = serializers.DictField()
    recent_ratings = serializers.ListField()

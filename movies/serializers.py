"""
Serializers for movies app.
"""
from rest_framework import serializers
from .models import Movie, Genre, Tag


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for Genre model.
    """
    movie_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'movie_count']
        
    def get_movie_count(self, obj):
        """
        Get the count of movies in this genre.
        """
        return obj.movies.count()


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """
    movie_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'movie_count']
        
    def get_movie_count(self, obj):
        """
        Get the count of movies with this tag.
        """
        return obj.movies.count()


class MovieListSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model in list views (minimal data).
    """
    genres = GenreSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'release_date', 'duration',
            'poster_image', 'imdb_rating', 'popularity_score',
            'genres', 'tags', 'average_rating', 'rating_count',
            'is_favorited'
        ]
        
    def get_average_rating(self, obj):
        """
        Get the average user rating for this movie.
        """
        ratings = obj.ratings.all()
        if ratings:
            return round(sum(r.rating for r in ratings) / len(ratings), 1)
        return 0.0
        
    def get_rating_count(self, obj):
        """
        Get the total number of ratings for this movie.
        """
        return obj.ratings.count()
        
    def get_is_favorited(self, obj):
        """
        Check if the current user has favorited this movie.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False


class MovieDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model in detail views (full data).
    """
    genres = GenreSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    in_watchlist = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_date', 'duration',
            'poster_image', 'trailer_url', 'imdb_rating', 'popularity_score',
            'created_at', 'updated_at', 'genres', 'tags',
            'average_rating', 'rating_count', 'user_rating',
            'is_favorited', 'in_watchlist'
        ]
        
    def get_average_rating(self, obj):
        """
        Get the average user rating for this movie.
        """
        ratings = obj.ratings.all()
        if ratings:
            return round(sum(r.rating for r in ratings) / len(ratings), 1)
        return 0.0
        
    def get_rating_count(self, obj):
        """
        Get the total number of ratings for this movie.
        """
        return obj.ratings.count()
        
    def get_user_rating(self, obj):
        """
        Get the current user's rating for this movie.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = obj.ratings.filter(user=request.user).first()
            return rating.rating if rating else None
        return None
        
    def get_is_favorited(self, obj):
        """
        Check if the current user has favorited this movie.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False
        
    def get_in_watchlist(self, obj):
        """
        Check if the current user has this movie in their watch history.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.watch_history.filter(user=request.user).exists()
        return False


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating movies (admin only).
    """
    genre_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'release_date', 'duration',
            'poster_image', 'trailer_url', 'imdb_rating',
            'popularity_score', 'genre_ids', 'tag_ids'
        ]
        
    def validate_duration(self, value):
        """
        Validate movie duration is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Duration must be positive.")
        return value
        
    def validate_imdb_rating(self, value):
        """
        Validate IMDB rating is between 0 and 10.
        """
        if not (0 <= value <= 10):
            raise serializers.ValidationError("IMDB rating must be between 0 and 10.")
        return value
        
    def validate_popularity_score(self, value):
        """
        Validate popularity score is between 0 and 100.
        """
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Popularity score must be between 0 and 100.")
        return value
        
    def create(self, validated_data):
        """
        Create a new movie with genres and tags.
        """
        genre_ids = validated_data.pop('genre_ids', [])
        tag_ids = validated_data.pop('tag_ids', [])
        
        movie = Movie.objects.create(**validated_data)
        
        if genre_ids:
            genres = Genre.objects.filter(id__in=genre_ids)
            movie.genres.set(genres)
            
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            movie.tags.set(tags)
            
        return movie
        
    def update(self, instance, validated_data):
        """
        Update a movie with genres and tags.
        """
        genre_ids = validated_data.pop('genre_ids', None)
        tag_ids = validated_data.pop('tag_ids', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update genres if provided
        if genre_ids is not None:
            genres = Genre.objects.filter(id__in=genre_ids)
            instance.genres.set(genres)
            
        # Update tags if provided
        if tag_ids is not None:
            tags = Tag.objects.filter(id__in=tag_ids)
            instance.tags.set(tags)
            
        return instance


class GenreCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating genres.
    """
    class Meta:
        model = Genre
        fields = ['name', 'description']
        
    def validate_name(self, value):
        """
        Validate genre name is unique.
        """
        if Genre.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A genre with this name already exists.")
        return value


class TagCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating tags.
    """
    class Meta:
        model = Tag
        fields = ['name']
        
    def validate_name(self, value):
        """
        Validate tag name is unique.
        """
        if Tag.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A tag with this name already exists.")
        return value

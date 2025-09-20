"""
Models for movies app.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    """
    Movie genre model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'genres'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    Movie tag model for additional categorization.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tags'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    """
    Movie model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)
    poster_image = models.URLField(blank=True, help_text="URL to poster image")
    trailer_url = models.URLField(blank=True, help_text="URL to trailer video")
    imdb_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="IMDB rating (0.0-10.0)"
    )
    popularity_score = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.0,
        help_text="Calculated popularity score"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Many-to-many relationships
    genres = models.ManyToManyField(Genre, through='MovieGenre', related_name='movies')
    tags = models.ManyToManyField(Tag, through='MovieTag', related_name='movies')
    
    class Meta:
        db_table = 'movies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['release_date']),
            models.Index(fields=['popularity_score']),
            models.Index(fields=['imdb_rating']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.release_date.year if self.release_date else 'Unknown'})"
    
    @property
    def average_rating(self):
        """Calculate average user rating."""
        from ratings.models import Rating
        ratings = Rating.objects.filter(movie=self)
        if ratings.exists():
            return ratings.aggregate(avg_rating=models.Avg('score'))['avg_rating']
        return None
    
    @property
    def total_ratings(self):
        """Get total number of ratings."""
        from ratings.models import Rating
        return Rating.objects.filter(movie=self).count()

class MovieGenre(models.Model):
    """
    Through model for Movie-Genre many-to-many relationship.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'movie_genres'
        unique_together = ('movie', 'genre')

class MovieTag(models.Model):
    """
    Through model for Movie-Tag many-to-many relationship.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'movie_tags'
        unique_together = ('movie', 'tag')

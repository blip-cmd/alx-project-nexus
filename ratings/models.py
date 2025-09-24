"""
Models for ratings app.
"""
import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Rating(models.Model):
    """
    User rating for movies.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='ratings')
    score = models.DecimalField(
        max_digits=2, 
        decimal_places=1,
        validators=[MinValueValidator(Decimal('0.5')), MaxValueValidator(Decimal('5.0'))],
        help_text="Rating score (0.5-5.0 stars)"
    )
    review = models.TextField(blank=True, help_text="Optional review text")
    rated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ratings'
        unique_together = ('user', 'movie')
        ordering = ['-rated_at']
        indexes = [
            models.Index(fields=['user', 'movie']),
            models.Index(fields=['movie', 'score']),
            models.Index(fields=['rated_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} rated {self.movie.title}: {self.score} stars"

class Favorite(models.Model):
    """
    User's favorite movies.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='favorited_by')
    favorited_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'favorites'
        unique_together = ('user', 'movie')
        ordering = ['-favorited_at']
        indexes = [
            models.Index(fields=['user', 'favorited_at']),
            models.Index(fields=['movie']),
        ]
    
    def __str__(self):
        return f"{self.user.username} favorited {self.movie.title}"

class WatchHistory(models.Model):
    """
    User's movie watch history.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='watched_by')
    watched_at = models.DateTimeField(auto_now_add=True)
    watch_duration = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Duration watched in minutes"
    )
    completed = models.BooleanField(default=False, help_text="Whether the movie was watched completely")
    
    class Meta:
        db_table = 'watch_history'
        ordering = ['-watched_at']
        indexes = [
            models.Index(fields=['user', 'watched_at']),
            models.Index(fields=['movie']),
            models.Index(fields=['watched_at']),
        ]
    
    def __str__(self):
        status = "completed" if self.completed else "partial"
        return f"{self.user.username} watched {self.movie.title} ({status})"

"""
Models for recommendations app.
"""
import uuid
from django.db import models
from django.contrib.auth.models import User

class RecommendationEngine(models.Model):
    """
    Model to track different recommendation algorithms and their performance.
    """
    ALGORITHM_CHOICES = [
        ('popularity', 'Popularity Based'),
        ('genre', 'Genre Based'),
        ('collaborative', 'Collaborative Filtering'),
        ('content', 'Content Based'),
        ('hybrid', 'Hybrid Approach'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    algorithm_type = models.CharField(max_length=20, choices=ALGORITHM_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    version = models.CharField(max_length=20, default='1.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'recommendation_engines'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.algorithm_type})"

class UserRecommendation(models.Model):
    """
    Personalized movie recommendations for users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='recommended_to')
    engine = models.ForeignKey(RecommendationEngine, on_delete=models.CASCADE, related_name='recommendations')
    score = models.DecimalField(
        max_digits=5, 
        decimal_places=4,
        help_text="Recommendation confidence score (0.0-1.0)"
    )
    reason = models.TextField(blank=True, help_text="Explanation for the recommendation")
    created_at = models.DateTimeField(auto_now_add=True)
    clicked = models.BooleanField(default=False)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_recommendations'
        unique_together = ('user', 'movie', 'engine')
        ordering = ['-score', '-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['movie']),
            models.Index(fields=['score']),
        ]
    
    def __str__(self):
        return f"Recommend {self.movie.title} to {self.user.username} (score: {self.score})"

class TrendingMovie(models.Model):
    """
    Model to track trending movies based on various metrics.
    """
    TRENDING_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='trending_periods')
    period = models.CharField(max_length=10, choices=TRENDING_PERIOD_CHOICES)
    rank = models.PositiveIntegerField()
    score = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Trending score based on views, ratings, etc."
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'trending_movies'
        unique_together = ('movie', 'period', 'date')
        ordering = ['period', 'rank']
        indexes = [
            models.Index(fields=['period', 'date', 'rank']),
            models.Index(fields=['movie', 'period']),
        ]
    
    def __str__(self):
        return f"{self.movie.title} - {self.period} trend #{self.rank}"

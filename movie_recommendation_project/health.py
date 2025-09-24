from django.http import JsonResponse
from django.contrib.auth.models import User
from movies.models import Movie
from ratings.models import Rating
from django.db import connection

def health_check(request):
    """Simple health check endpoint for deployment monitoring."""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Get basic stats
        stats = {
            'status': 'healthy',
            'database': 'connected',
            'users': User.objects.count(),
            'movies': Movie.objects.count(),
            'ratings': Rating.objects.count(),
        }
        
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)
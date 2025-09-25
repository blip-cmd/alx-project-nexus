"""
API endpoints for database seeding operations.
Useful for production environments without shell access.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from django.core.management import call_command
from django.contrib.auth.models import User
from movies.models import Movie, Genre, Tag
from ratings.models import Rating, Favorite
import io
import sys

@api_view(['POST'])
@permission_classes([IsAdminUser])
def seed_database(request):
    """
    Seed the database with sample data.
    Only admin users can trigger this.
    """
    try:
        # Get parameters from request
        movies_count = request.data.get('movies', 50)
        users_count = request.data.get('users', 5)
        
        # Capture the command output
        output = io.StringIO()
        
        # Run the seeding command
        call_command('seed_data', 
                    movies=movies_count, 
                    users=users_count,
                    stdout=output)
        
        # Get current stats
        stats = {
            'genres': Genre.objects.count(),
            'tags': Tag.objects.count(),
            'movies': Movie.objects.count(),
            'users': User.objects.count(),
            'ratings': Rating.objects.count(),
            'favorites': Favorite.objects.count(),
        }
        
        return Response({
            'success': True,
            'message': 'Database seeding completed successfully',
            'stats': stats,
            'output': output.getvalue()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Seeding failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def database_stats(request):
    """
    Get database statistics.
    """
    stats = {
        'genres': Genre.objects.count(),
        'tags': Tag.objects.count(),
        'movies': Movie.objects.count(),
        'users': User.objects.count(),
        'ratings': Rating.objects.count(),
        'favorites': Favorite.objects.count(),
        'is_empty': Movie.objects.count() == 0
    }
    
    return Response({
        'database_stats': stats,
        'needs_seeding': stats['movies'] == 0
    })

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def clear_sample_data(request):
    """
    Clear sample data from database (keep admin users).
    Only admin users can trigger this.
    """
    try:
        # Delete sample users (non-admin)
        users_deleted = User.objects.filter(is_superuser=False).count()
        User.objects.filter(is_superuser=False).delete()
        
        # Delete all movies, which will cascade delete ratings and favorites
        movies_deleted = Movie.objects.count()
        Movie.objects.all().delete()
        
        # Delete all genres and tags
        genres_deleted = Genre.objects.count()
        tags_deleted = Tag.objects.count()
        Genre.objects.all().delete()
        Tag.objects.all().delete()
        
        return Response({
            'success': True,
            'message': 'Sample data cleared successfully',
            'deleted': {
                'users': users_deleted,
                'movies': movies_deleted,
                'genres': genres_deleted,
                'tags': tags_deleted
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Clear operation failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
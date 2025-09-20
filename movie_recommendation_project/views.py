"""
Main project views.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root endpoint providing links to all available endpoints.
    """
    return Response({
        'message': 'Welcome to Movie Recommendation API',
        'version': '1.0.0',
        'endpoints': {
            'authentication': request.build_absolute_uri('/api/auth/'),
            'movies': request.build_absolute_uri('/api/movies/'),
            'recommendations': request.build_absolute_uri('/api/recommendations/'),
            'ratings': request.build_absolute_uri('/api/ratings/'),
            'admin': request.build_absolute_uri('/admin/'),
        },
        'status_endpoints': {
            'auth_status': request.build_absolute_uri('/api/auth/status/'),
            'movies_status': request.build_absolute_uri('/api/movies/status/'),
            'recommendations_status': request.build_absolute_uri('/api/recommendations/status/'),
            'ratings_status': request.build_absolute_uri('/api/ratings/status/'),
        }
    }, status=status.HTTP_200_OK)

def home_view(request):
    """
    Simple home page view.
    """
    context = {
        'project_name': 'Movie Recommendation App',
        'version': '1.0.0',
        'api_root': '/api/',
    }
    return render(request, 'home.html', context)

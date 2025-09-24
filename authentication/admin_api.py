"""
Admin management views for situations where shell access isn't available.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.conf import settings
import os

@api_view(['POST'])
@permission_classes([AllowAny])
def create_admin_user(request):
    """
    Create an admin user via API endpoint.
    This is only enabled in specific conditions for security.
    """
    # Security checks
    if settings.DEBUG is False and not os.getenv('ENABLE_ADMIN_CREATION_API'):
        return Response({
            'error': 'Admin creation API is disabled'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Check if any superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        return Response({
            'error': 'Admin user already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get data from request
    username = request.data.get('username', 'admin')
    email = request.data.get('email', 'admin@movierecommendations.com')
    password = request.data.get('password')
    
    # Require password to be provided
    if not password:
        return Response({
            'error': 'Password is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        return Response({
            'success': 'Admin user created successfully',
            'username': username,
            'email': email
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Failed to create admin user: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def admin_status(request):
    """
    Check if admin user exists.
    """
    admin_exists = User.objects.filter(is_superuser=True).exists()
    
    return Response({
        'admin_exists': admin_exists,
        'total_users': User.objects.count(),
        'api_enabled': settings.DEBUG or bool(os.getenv('ENABLE_ADMIN_CREATION_API'))
    })
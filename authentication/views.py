"""
Views for authentication app.
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def auth_status(request):
    """
    API endpoint for checking authentication status.
    This is a placeholder view.
    """
    return Response({
        'message': 'Authentication app is working!',
        'authenticated': request.user.is_authenticated,
        'user': str(request.user) if request.user.is_authenticated else None
    }, status=status.HTTP_200_OK)

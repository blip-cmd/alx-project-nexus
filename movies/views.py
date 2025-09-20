"""
Views for movies app.
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def movie_status(request):
    """
    API endpoint for checking movies app status.
    This is a placeholder view.
    """
    return Response({
        'message': 'Movies app is working!',
        'endpoint': 'Movies API'
    }, status=status.HTTP_200_OK)

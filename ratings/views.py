"""
Views for ratings app.
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def ratings_status(request):
    """
    API endpoint for checking ratings app status.
    This is a placeholder view.
    """
    return Response({
        'message': 'Ratings app is working!',
        'endpoint': 'Ratings API'
    }, status=status.HTTP_200_OK)

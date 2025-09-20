"""
Views for recommendations app.
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def recommendations_status(request):
    """
    API endpoint for checking recommendations app status.
    This is a placeholder view.
    """
    return Response({
        'message': 'Recommendations app is working!',
        'endpoint': 'Recommendations API'
    }, status=status.HTTP_200_OK)

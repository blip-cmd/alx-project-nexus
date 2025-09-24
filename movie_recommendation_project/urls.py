"""
URL configuration for movie_recommendation_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views
from .health import health_check

# Swagger/OpenAPI Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Recommendation API",
        default_version='v1',
        description="""
        🎬 **Movie Recommendation System API**
        
        A comprehensive REST API for a movie recommendation system built with Django REST Framework.
        
        ## Features
        - **Authentication**: JWT-based user authentication and authorization
        - **Movie Catalog**: Browse, search, and filter movies with detailed information
        - **User Interactions**: Rate movies, manage favorites, and track watch history
        - **Recommendations**: Advanced recommendation algorithms including collaborative filtering and content-based recommendations
        - **Caching**: Redis-based caching for improved performance
        
        ## Authentication
        This API uses JWT (JSON Web Token) authentication. To access protected endpoints:
        1. Register a new user or login with existing credentials
        2. Include the access token in the Authorization header: `Authorization: Bearer <your_token>`
        
        ## Rate Limiting
        API endpoints are rate-limited to ensure fair usage and system stability.
        
        ## Pagination
        List endpoints support pagination with `page` and `page_size` parameters.
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@movierecommendations.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/', views.api_root, name='api-root'),
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/movies/', include('movies.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/ratings/', include('ratings.urls')),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

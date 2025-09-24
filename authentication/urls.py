"""
URL configuration for authentication app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .admin_api import create_admin_user, admin_status

app_name = 'authentication'

urlpatterns = [
    # Auth status endpoint
    path('status/', views.auth_status, name='auth-status'),
    
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    
    # Password reset endpoints
    path('password/reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Admin management (for deployment without shell access)
    path('admin/status/', admin_status, name='admin-status'),
    path('admin/create/', create_admin_user, name='admin-create'),
]

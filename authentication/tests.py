"""
Tests for authentication app.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticationTestCase(TestCase):
    """
    Test case for authentication endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        self.test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'securepassword123',
            'password_confirm': 'securepassword123'
        }
        
    def test_user_registration(self):
        """
        Test user registration endpoint.
        """
        response = self.client.post('/api/auth/register/', self.test_user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['email'], 'test@example.com')
        
        # Verify user was created in database
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        
    def test_user_registration_duplicate_username(self):
        """
        Test registration with duplicate username.
        """
        # Create first user
        self.client.post('/api/auth/register/', self.test_user_data, format='json')
        
        # Try to create second user with same username
        duplicate_data = self.test_user_data.copy()
        duplicate_data['email'] = 'another@example.com'
        
        response = self.client.post('/api/auth/register/', duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        
    def test_user_registration_password_mismatch(self):
        """
        Test registration with password mismatch.
        """
        data = self.test_user_data.copy()
        data['password_confirm'] = 'differentpassword'
        
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_login(self):
        """
        Test user login endpoint.
        """
        # Create user first
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123',
            first_name='Test',
            last_name='User'
        )
        
        login_data = {
            'username': 'testuser',
            'password': 'securepassword123'
        }
        
        response = self.client.post('/api/auth/login/', login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        
    def test_user_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        
        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post('/api/auth/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_profile_access(self):
        """
        Test accessing user profile with valid token.
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123',
            first_name='Test',
            last_name='User'
        )
        
        # Generate token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Access profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/auth/profile/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        
    def test_user_profile_access_unauthorized(self):
        """
        Test accessing user profile without token.
        """
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_token_refresh(self):
        """
        Test token refresh functionality.
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        
        response = self.client.post(
            '/api/auth/token/refresh/', 
            {'refresh': refresh_token}, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
    def test_user_profile_update(self):
        """
        Test updating user profile.
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123',
            first_name='Test',
            last_name='User'
        )
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Update profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        response = self.client.put('/api/auth/profile/', update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'], 'Updated')
        self.assertEqual(response.data['user']['last_name'], 'Name')
        self.assertEqual(response.data['user']['email'], 'updated@example.com')
        
        # Verify in database
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Name')
        self.assertEqual(user.email, 'updated@example.com')
        
    def test_password_change(self):
        """
        Test password change functionality.
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpassword123'
        )
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Change password
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        password_data = {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword123',
            'new_password_confirm': 'newpassword123'
        }
        
        response = self.client.post('/api/auth/password/change/', password_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password was changed
        user.refresh_from_db()
        self.assertTrue(user.check_password('newpassword123'))
        self.assertFalse(user.check_password('oldpassword123'))
        
    def test_auth_status_endpoint(self):
        """
        Test auth status endpoint.
        """
        response = self.client.get('/api/auth/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('authenticated', response.data)
        self.assertEqual(response.data['authenticated'], False)


class AuthenticationIntegrationTestCase(TestCase):
    """
    Integration tests for complete authentication flow.
    """
    
    def setUp(self):
        self.client = APIClient()
        
    def test_complete_authentication_flow(self):
        """
        Test complete registration -> login -> profile access -> logout flow.
        """
        # 1. Register user
        registration_data = {
            'username': 'integrationuser',
            'email': 'integration@example.com',
            'first_name': 'Integration',
            'last_name': 'Test',
            'password': 'securepassword123',
            'password_confirm': 'securepassword123'
        }
        
        reg_response = self.client.post('/api/auth/register/', registration_data, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)
        
        # 2. Login with registered user
        login_data = {
            'username': 'integrationuser',
            'password': 'securepassword123'
        }
        
        login_response = self.client.post('/api/auth/login/', login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']
        
        # 3. Access protected profile endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_response = self.client.get('/api/auth/profile/')
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['username'], 'integrationuser')
        
        # 4. Refresh token
        self.client.credentials()  # Remove auth header
        refresh_response = self.client.post(
            '/api/auth/token/refresh/', 
            {'refresh': refresh_token}, 
            format='json'
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
        
        # 5. Use new access token
        new_access_token = refresh_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_access_token}')
        profile_response2 = self.client.get('/api/auth/profile/')
        self.assertEqual(profile_response2.status_code, status.HTTP_200_OK)

"""
Simple authentication test using requests.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_auth_endpoints():
    """
    Test authentication endpoints with real HTTP requests.
    """
    print("🧪 Testing Authentication Endpoints")
    print("=" * 50)
    
    # Test auth status
    print("\n0. Testing Auth Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/status/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Auth status endpoint working!")
            print(f"Response: {response.json()}")
        else:
            print("❌ Auth status failed!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Test registration
    print("\n1. Testing User Registration...")
    registration_data = {
        'username': 'testuser123',
        'email': 'test123@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'securepassword123',
        'password_confirm': 'securepassword123'
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register/", 
            json=registration_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print("✅ Registration successful!")
            registration_response = response.json()
            print(f"User ID: {registration_response['user']['id']}")
            print(f"Username: {registration_response['user']['username']}")
        else:
            print("❌ Registration failed!")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration request failed: {e}")
        return
    
    # Test login
    print("\n2. Testing User Login...")
    login_data = {
        'username': 'testuser123',
        'password': 'securepassword123'
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login/", 
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login successful!")
            login_response = response.json()
            access_token = login_response['tokens']['access']
            refresh_token = login_response['tokens']['refresh']
            print("🔑 Tokens generated successfully")
        else:
            print("❌ Login failed!")
            print(f"Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login request failed: {e}")
        return
    
    # Test protected endpoint (profile)
    print("\n3. Testing Protected Endpoint (Profile)...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/profile/",
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Profile access successful!")
            profile_data = response.json()
            print(f"Profile: {profile_data['username']} ({profile_data['email']})")
        else:
            print("❌ Profile access failed!")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Profile request failed: {e}")
    
    # Test token refresh
    print("\n4. Testing Token Refresh...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/token/refresh/", 
            json={'refresh': refresh_token},
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Token refresh successful!")
            refresh_response = response.json()
            new_access_token = refresh_response['access']
            print("🔄 New access token generated")
        else:
            print("❌ Token refresh failed!")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Token refresh request failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication testing completed!")

if __name__ == '__main__':
    test_auth_endpoints()

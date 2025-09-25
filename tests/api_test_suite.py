#!/usr/bin/env python3
"""
🧪 Movie Recommendation API - Automated Test Suite
Comprehensive testing script for all API endpoints with results logging.
"""

import requests
import json
import time
from datetime import datetime
import sys
import os

class APITester:
    def __init__(self, base_url="http://127.0.0.1:8000", output_file="test_results.txt"):
        self.base_url = base_url
        self.output_file = output_file
        self.session = requests.Session()
        self.test_results = []
        self.access_token = None
        self.test_user_data = {
            "username": "test_api_user",
            "email": "test_api@example.com",
            "first_name": "API",
            "last_name": "Tester",
            "password": "securepass123",
            "password_confirm": "securepass123"
        }
        
        # Initialize output file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(f"🧪 Movie Recommendation API Test Results\n")
            f.write(f"=" * 60 + "\n")
            f.write(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Base URL: {self.base_url}\n\n")

    def log_result(self, test_name, status, details, response_data=None):
        """Log test result to both console and file."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        
        result = {
            'timestamp': timestamp,
            'test_name': test_name,
            'status': status,
            'details': details,
            'response_data': response_data
        }
        self.test_results.append(result)
        
        # Console output
        print(f"{status_icon} [{timestamp}] {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
        if response_data and isinstance(response_data, dict):
            print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
        print()
        
        # File output
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(f"{status_icon} [{timestamp}] {test_name}: {status}\n")
            if details:
                f.write(f"   Details: {details}\n")
            if response_data:
                f.write(f"   Response: {json.dumps(response_data, indent=2)}\n")
            f.write("-" * 60 + "\n\n")

    def make_request(self, method, endpoint, data=None, headers=None, auth=False):
        """Make HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"
        
        # Add authorization header if needed
        if auth and self.access_token:
            if headers is None:
                headers = {}
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        # Set content type for POST/PUT requests
        if data and not headers:
            headers = {'Content-Type': 'application/json'}
        elif data and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers, timeout=10)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            return response
        except requests.exceptions.RequestException as e:
            return None, str(e)

    def test_server_health(self):
        """Test if the server is running and accessible."""
        self.log_result("Server Health Check", "INFO", "Testing server connectivity...")
        
        response = self.make_request('GET', '/')
        if response and response.status_code == 200:
            self.log_result("Home Page Access", "PASS", f"Status Code: {response.status_code}")
        else:
            self.log_result("Home Page Access", "FAIL", f"Could not access home page. Server may not be running.")
            return False
        return True

    def test_api_root(self):
        """Test API root endpoint."""
        response = self.make_request('GET', '/api/')
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.log_result("API Root", "PASS", f"Status: {response.status_code}", data)
                return True
            except json.JSONDecodeError:
                self.log_result("API Root", "FAIL", "Response is not valid JSON")
        else:
            status_code = response.status_code if response else "No response"
            self.log_result("API Root", "FAIL", f"Status Code: {status_code}")
        return False

    def test_authentication_endpoints(self):
        """Test authentication related endpoints."""
        # Test auth status
        response = self.make_request('GET', '/api/auth/status/')
        if response and response.status_code == 200:
            self.log_result("Auth Status", "PASS", f"Status: {response.status_code}", response.json())
        else:
            self.log_result("Auth Status", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        # Test user registration
        response = self.make_request('POST', '/api/auth/register/', self.test_user_data)
        if response and response.status_code in [201, 400]:  # 400 might mean user already exists
            if response.status_code == 201:
                self.log_result("User Registration", "PASS", "New user created successfully", response.json())
            else:
                # Check if user already exists
                error_data = response.json()
                if 'username' in error_data and 'already exists' in str(error_data):
                    self.log_result("User Registration", "WARN", "User already exists, proceeding with login")
                else:
                    self.log_result("User Registration", "FAIL", f"Registration failed: {error_data}")
        else:
            self.log_result("User Registration", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        # Test user login
        login_data = {
            "username": self.test_user_data["username"],
            "password": self.test_user_data["password"]
        }
        response = self.make_request('POST', '/api/auth/login/', login_data)
        if response and response.status_code == 200:
            data = response.json()
            if 'access' in data:
                self.access_token = data['access']
                self.log_result("User Login", "PASS", "Login successful, token obtained", data)
                return True
            else:
                self.log_result("User Login", "FAIL", "No access token in response", data)
        else:
            self.log_result("User Login", "FAIL", f"Status: {response.status_code if response else 'No response'}")
        return False

    def test_movies_endpoints(self):
        """Test movie related endpoints."""
        # Test movies list
        response = self.make_request('GET', '/api/movies/')
        if response and response.status_code == 200:
            data = response.json()
            self.log_result("Movies List", "PASS", f"Status: {response.status_code}, Count: {len(data.get('results', data))}", data)
        else:
            self.log_result("Movies List", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        # Test movies with search
        response = self.make_request('GET', '/api/movies/?search=action')
        if response and response.status_code == 200:
            self.log_result("Movies Search", "PASS", f"Search functionality works", response.json())
        else:
            self.log_result("Movies Search", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        # Test genres
        response = self.make_request('GET', '/api/movies/genres/')
        if response and response.status_code == 200:
            data = response.json()
            self.log_result("Genres List", "PASS", f"Status: {response.status_code}, Count: {len(data.get('results', data))}", data)
        else:
            self.log_result("Genres List", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        # Test tags
        response = self.make_request('GET', '/api/movies/tags/')
        if response and response.status_code == 200:
            data = response.json()
            self.log_result("Tags List", "PASS", f"Status: {response.status_code}, Count: {len(data.get('results', data))}", data)
        else:
            self.log_result("Tags List", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        # Test popular movies
        response = self.make_request('GET', '/api/movies/popular/')
        if response and response.status_code == 200:
            self.log_result("Popular Movies", "PASS", f"Status: {response.status_code}", response.json())
        else:
            self.log_result("Popular Movies", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        # Test trending movies
        response = self.make_request('GET', '/api/movies/trending/')
        if response and response.status_code == 200:
            self.log_result("Trending Movies", "PASS", f"Status: {response.status_code}", response.json())
        else:
            self.log_result("Trending Movies", "FAIL", f"Status: {response.status_code if response else 'No response'}")

    def test_ratings_endpoints(self):
        """Test rating related endpoints."""
        # Test ratings status
        response = self.make_request('GET', '/api/ratings/status/')
        if response and response.status_code == 200:
            self.log_result("Ratings Status", "PASS", f"Status: {response.status_code}", response.json())
        else:
            self.log_result("Ratings Status", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        if self.access_token:
            # Test user's ratings (authenticated)
            response = self.make_request('GET', '/api/ratings/my-ratings/', auth=True)
            if response and response.status_code == 200:
                self.log_result("My Ratings", "PASS", f"Status: {response.status_code}", response.json())
            else:
                self.log_result("My Ratings", "FAIL", f"Status: {response.status_code if response else 'No response'}")

            # Test user's favorites (authenticated)
            response = self.make_request('GET', '/api/ratings/my-favorites/', auth=True)
            if response and response.status_code == 200:
                self.log_result("My Favorites", "PASS", f"Status: {response.status_code}", response.json())
            else:
                self.log_result("My Favorites", "FAIL", f"Status: {response.status_code if response else 'No response'}")

            # Test user stats (authenticated)
            response = self.make_request('GET', '/api/ratings/my-stats/', auth=True)
            if response and response.status_code == 200:
                self.log_result("User Stats", "PASS", f"Status: {response.status_code}", response.json())
            else:
                self.log_result("User Stats", "FAIL", f"Status: {response.status_code if response else 'No response'}")

    def test_recommendations_endpoints(self):
        """Test recommendation related endpoints."""
        # Test recommendations status
        response = self.make_request('GET', '/api/recommendations/status/')
        if response and response.status_code == 200:
            self.log_result("Recommendations Status", "PASS", f"Status: {response.status_code}", response.json())
        else:
            self.log_result("Recommendations Status", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        # Test trending movies
        response = self.make_request('GET', '/api/recommendations/trending/')
        if response and response.status_code == 200:
            self.log_result("Trending Recommendations", "PASS", f"Status: {response.status_code}", response.json())
        else:
            self.log_result("Trending Recommendations", "FAIL", f"Status: {response.status_code if response else 'No response'}")

        if self.access_token:
            # Test personalized recommendations (authenticated)
            response = self.make_request('GET', '/api/recommendations/for-me/', auth=True)
            if response and response.status_code == 200:
                self.log_result("Personal Recommendations", "PASS", f"Status: {response.status_code}", response.json())
            else:
                self.log_result("Personal Recommendations", "FAIL", f"Status: {response.status_code if response else 'No response'}")

            # Test different recommendation algorithms
            algorithms = ['popularity', 'genre', 'collaborative', 'content', 'hybrid']
            for algorithm in algorithms:
                response = self.make_request('GET', f'/api/recommendations/for-me/?algorithm={algorithm}', auth=True)
                if response and response.status_code == 200:
                    self.log_result(f"Recommendation Algorithm ({algorithm})", "PASS", f"Status: {response.status_code}")
                else:
                    self.log_result(f"Recommendation Algorithm ({algorithm})", "FAIL", f"Status: {response.status_code if response else 'No response'}")

    def test_admin_endpoints(self):
        """Test admin related endpoints."""
        response = self.make_request('GET', '/admin/')
        if response and response.status_code in [200, 302]:  # 302 = redirect to login
            self.log_result("Admin Panel Access", "PASS", f"Admin panel accessible (Status: {response.status_code})")
        else:
            self.log_result("Admin Panel Access", "FAIL", f"Status: {response.status_code if response else 'No response'}")

    def test_error_handling(self):
        """Test error handling for invalid requests."""
        # Test 404 endpoint
        response = self.make_request('GET', '/api/nonexistent/')
        if response and response.status_code == 404:
            self.log_result("404 Error Handling", "PASS", "Correctly returns 404 for non-existent endpoint")
        else:
            self.log_result("404 Error Handling", "FAIL", f"Expected 404, got {response.status_code if response else 'No response'}")

        # Test unauthorized access
        response = self.make_request('GET', '/api/ratings/my-ratings/')  # Should require auth
        if response and response.status_code == 401:
            self.log_result("Unauthorized Access Handling", "PASS", "Correctly returns 401 for unauthorized access")
        else:
            self.log_result("Unauthorized Access Handling", "WARN", f"Expected 401, got {response.status_code if response else 'No response'}")

    def run_all_tests(self):
        """Run all test suites."""
        print(f"🧪 Starting Movie Recommendation API Test Suite")
        print(f"📍 Testing: {self.base_url}")
        print(f"📝 Results will be saved to: {self.output_file}")
        print("=" * 60)
        
        # Check if server is running
        if not self.test_server_health():
            self.log_result("Test Suite", "FAIL", "Server is not accessible. Please start the Django server first.")
            return False

        # Run test suites
        self.test_api_root()
        self.test_authentication_endpoints()
        self.test_movies_endpoints()
        self.test_ratings_endpoints()
        self.test_recommendations_endpoints()
        self.test_admin_endpoints()
        self.test_error_handling()

        # Generate summary
        self.generate_summary()
        return True

    def generate_summary(self):
        """Generate test summary."""
        total_tests = len(self.test_results)
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed = len([r for r in self.test_results if r['status'] == 'FAIL'])
        warnings = len([r for r in self.test_results if r['status'] == 'WARN'])
        
        summary = f"""
🏁 TEST SUMMARY
{'=' * 60}
Total Tests: {total_tests}
✅ Passed: {passed}
❌ Failed: {failed}
⚠️  Warnings: {warnings}

Success Rate: {(passed / total_tests * 100):.1f}%
Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        print(summary)
        
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(summary)
            f.write("\n" + "=" * 60 + "\n")
            f.write("🔍 DETAILED RESULTS ABOVE\n")
            f.write("💡 Tips:\n")
            f.write("- If server health check failed, start Django server: python manage.py runserver\n")
            f.write("- If many endpoints return empty data, create sample data: python manage.py create_sample_data\n")
            f.write("- If authentication tests fail, check user registration and login endpoints\n")
            f.write("- For detailed API documentation, visit: http://127.0.0.1:8000/api/\n")

def py_test():
    """Main test function that can be called directly."""
    # Check if server is likely running
    try:
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        print("✅ Server appears to be running. Starting tests...")
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server at http://127.0.0.1:8000/")
        print("💡 Please start the Django server first:")
        print("   python manage.py runserver")
        return False
    
    # Run tests
    tester = APITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    # Allow custom base URL from command line
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "test_results.txt"
    
    tester = APITester(base_url, output_file)
    success = tester.run_all_tests()
    
    if success:
        print(f"\n📊 Test results saved to: {output_file}")
        print("🎉 Test suite completed!")
    else:
        print("\n💥 Test suite failed to complete!")
        sys.exit(1)
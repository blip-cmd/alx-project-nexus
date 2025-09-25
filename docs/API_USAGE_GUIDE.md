# 🌐 API Usage Guide - Movie Recommendation API

## 🚀 Quick Access

### **🌍 Live API**
- **Base URL**: https://movie-recommendation-api-0thd.onrender.com/
- **Documentation**: https://movie-recommendation-api-0thd.onrender.com/swagger/
- **Admin Panel**: https://movie-recommendation-api-0thd.onrender.com/admin/

### **🏠 Local Development**
- **Base URL**: http://127.0.0.1:8000/
- **Documentation**: http://127.0.0.1:8000/swagger/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 📋 API Endpoints Overview

### **🔐 Authentication**
```http
POST /api/auth/register/     # User registration
POST /api/auth/login/        # User login  
POST /api/auth/refresh/      # Refresh JWT token
POST /api/auth/logout/       # User logout
```

### **🎬 Movies**
```http
GET    /api/movies/          # List all movies (paginated)
GET    /api/movies/{id}/     # Get specific movie details
GET    /api/movies/popular/  # Get popular movies
GET    /api/movies/trending/ # Get trending movies
GET    /api/movies/search/   # Search movies by title/genre
```

### **⭐ Ratings**
```http
GET    /api/ratings/         # User's ratings
POST   /api/ratings/         # Rate a movie
PUT    /api/ratings/{id}/    # Update rating
DELETE /api/ratings/{id}/    # Remove rating
```

### **💡 Recommendations**
```http
GET    /api/recommendations/ # Get personalized recommendations
GET    /api/recommendations/similar/{movie_id}/ # Similar movies
```

### **👤 User Profile**
```http
GET    /api/profile/         # Get user profile
PUT    /api/profile/         # Update profile
GET    /api/profile/favorites/ # User's favorite movies
POST   /api/profile/favorites/ # Add to favorites
```

---

## 🔐 Authentication Flow

### **1. User Registration**
```bash
# Request
curl -X POST https://movie-recommendation-api-0thd.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com", 
    "password": "securepassword123"
  }'

# Response
{
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### **2. User Login**
```bash
# Request
curl -X POST https://movie-recommendation-api-0thd.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepassword123"
  }'

# Response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### **3. Using Authentication Token**
```bash
# Include in all authenticated requests
curl -X GET https://movie-recommendation-api-0thd.onrender.com/api/profile/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

## 🎬 Movie API Examples

### **Get All Movies (Paginated)**
```bash
# Request
curl -X GET "https://movie-recommendation-api-0thd.onrender.com/api/movies/?page=1&page_size=10"

# Response
{
  "count": 150,
  "next": "https://movie-recommendation-api-0thd.onrender.com/api/movies/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "The Shawshank Redemption",
      "description": "Two imprisoned men bond over years...",
      "release_date": "1994-09-23",
      "duration": 142,
      "imdb_rating": 9.3,
      "poster_url": "https://example.com/poster1.jpg",
      "genres": ["Drama"],
      "tags": ["prison", "friendship", "hope"]
    }
  ]
}
```

### **Search Movies**
```bash
# Search by title
curl -X GET "https://movie-recommendation-api-0thd.onrender.com/api/movies/search/?q=shawshank"

# Filter by genre
curl -X GET "https://movie-recommendation-api-0thd.onrender.com/api/movies/?genre=drama"

# Filter by year
curl -X GET "https://movie-recommendation-api-0thd.onrender.com/api/movies/?release_year=1994"
```

### **Get Movie Details**
```bash
# Request
curl -X GET "https://movie-recommendation-api-0thd.onrender.com/api/movies/1/"

# Response
{
  "id": 1,
  "title": "The Shawshank Redemption",
  "description": "Two imprisoned men bond over years, finding solace and eventual redemption through acts of common decency.",
  "release_date": "1994-09-23",
  "duration": 142,
  "imdb_rating": 9.3,
  "popularity_score": 95.5,
  "poster_url": "https://example.com/poster1.jpg",
  "trailer_url": "https://youtube.com/watch?v=6hB3S9bIaco",
  "genres": [
    {"id": 1, "name": "Drama", "description": "Drama films"}
  ],
  "tags": ["prison", "friendship", "hope", "redemption"],
  "average_rating": 9.2,
  "total_ratings": 1247
}
```

---

## ⭐ Rating API Examples

### **Rate a Movie**
```bash
# Request (Authentication required)
curl -X POST https://movie-recommendation-api-0thd.onrender.com/api/ratings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "movie": 1,
    "rating": 5,
    "review": "Absolutely fantastic movie!"
  }'

# Response
{
  "id": 15,
  "user": 1,
  "movie": 1,
  "rating": 5,
  "review": "Absolutely fantastic movie!",
  "created_at": "2025-09-25T14:30:00Z"
}
```

### **Get User's Ratings**
```bash
# Request (Authentication required)
curl -X GET https://movie-recommendation-api-0thd.onrender.com/api/ratings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response
{
  "count": 5,
  "results": [
    {
      "id": 15,
      "movie": {
        "id": 1,
        "title": "The Shawshank Redemption",
        "poster_url": "https://example.com/poster1.jpg"
      },
      "rating": 5,
      "review": "Absolutely fantastic movie!",
      "created_at": "2025-09-25T14:30:00Z"
    }
  ]
}
```

---

## 💡 Recommendations API Examples

### **Get Personalized Recommendations**
```bash
# Request (Authentication required)
curl -X GET https://movie-recommendation-api-0thd.onrender.com/api/recommendations/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response
{
  "recommendations": [
    {
      "movie": {
        "id": 25,
        "title": "The Green Mile",
        "description": "The lives of guards on Death Row are affected by one of their charges...",
        "imdb_rating": 8.6,
        "poster_url": "https://example.com/poster25.jpg"
      },
      "reason": "Because you liked Drama movies like The Shawshank Redemption",
      "confidence": 0.87
    }
  ],
  "total": 10
}
```

### **Get Similar Movies**
```bash
# Request
curl -X GET "https://movie-recommendation-api-0thd.onrender.com/api/recommendations/similar/1/"

# Response
{
  "similar_movies": [
    {
      "id": 25,
      "title": "The Green Mile",
      "similarity_score": 0.92,
      "poster_url": "https://example.com/poster25.jpg"
    }
  ],
  "total": 5
}
```

---

## 👤 User Profile API Examples

### **Get User Profile**
```bash
# Request (Authentication required)
curl -X GET https://movie-recommendation-api-0thd.onrender.com/api/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response
{
  "id": 1,
  "username": "moviefan",
  "email": "fan@example.com",
  "first_name": "Movie",
  "last_name": "Fan", 
  "date_joined": "2025-09-01T10:00:00Z",
  "favorite_genres": ["Drama", "Action"],
  "total_ratings": 15,
  "average_rating_given": 4.2
}
```

### **Add Movie to Favorites**
```bash
# Request (Authentication required)
curl -X POST https://movie-recommendation-api-0thd.onrender.com/api/profile/favorites/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"movie": 1}'

# Response
{
  "id": 5,
  "movie": {
    "id": 1,
    "title": "The Shawshank Redemption"
  },
  "added_at": "2025-09-25T14:35:00Z"
}
```

---

## 🔧 API Features

### **Pagination**
```bash
# All list endpoints support pagination
GET /api/movies/?page=2&page_size=5

# Response includes pagination info
{
  "count": 150,
  "next": "http://api/movies/?page=3&page_size=5",
  "previous": "http://api/movies/?page=1&page_size=5",
  "results": [...]
}
```

### **Filtering & Searching**
```bash
# Movies can be filtered by:
GET /api/movies/?genre=action
GET /api/movies/?release_year=2023
GET /api/movies/?imdb_rating__gte=8.0
GET /api/movies/?search=avengers

# Combine filters
GET /api/movies/?genre=action&release_year=2023&search=marvel
```

### **Sorting**
```bash
# Sort movies by various fields
GET /api/movies/?ordering=-imdb_rating     # Highest rated first
GET /api/movies/?ordering=release_date     # Oldest first
GET /api/movies/?ordering=-release_date    # Newest first
GET /api/movies/?ordering=title            # Alphabetical
```

---

## ❌ Error Handling

### **Common HTTP Status Codes**
- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

### **Error Response Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "rating": ["Rating must be between 1 and 5"]
    }
  }
}
```

---

## 📊 Rate Limiting

### **Current Limits**
- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour
- **Admin users**: 5000 requests per hour

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1632567890
```

---

## 🧪 Testing the API

### **Using cURL**
```bash
# Test registration
curl -X POST https://movie-recommendation-api-0thd.onrender.com/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'
```

### **Using Postman**
1. Import the API collection from `/swagger/`
2. Set up environment variables for base URL and tokens
3. Use the built-in authentication flow

### **Using Python requests**
```python
import requests

# Base configuration
BASE_URL = "https://movie-recommendation-api-0thd.onrender.com"
headers = {"Content-Type": "application/json"}

# Register user
response = requests.post(f"{BASE_URL}/api/auth/register/", 
    headers=headers,
    json={
        "username": "pythonuser",
        "email": "python@example.com", 
        "password": "pythonpass123"
    }
)
tokens = response.json()

# Use access token for authenticated requests
auth_headers = {
    **headers,
    "Authorization": f"Bearer {tokens['access']}"
}

# Get movies
movies = requests.get(f"{BASE_URL}/api/movies/", headers=auth_headers)
print(movies.json())
```

---

## 📚 Additional Resources

### **Documentation**
- **Interactive API Docs**: Visit `/swagger/` when server is running
- **ReDoc Documentation**: Visit `/redoc/` for alternative format  
- **Admin Interface**: Visit `/admin/` for data management

### **Code Examples**
- Check `tests/` directory for comprehensive API usage examples
- See `docs/` directory for additional guides
- Review Django app views for implementation details

---

**🎉 Happy API testing! The Movie Recommendation API is ready for integration!**
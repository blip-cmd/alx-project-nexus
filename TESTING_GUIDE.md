# 🧪 Movie Recommendation API - Testing Guide

This document provides comprehensive testing commands and procedures for the Movie Recommendation API.

## 📋 Prerequisites

1. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

2. **Create a superuser for admin testing:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Install testing tools:**
   ```bash
   pip install httpie  # For command-line testing
   # Or use curl, Postman, or any HTTP client
   ```

## 🔐 Phase 3: Authentication Testing

### User Registration
```bash
# Register a new user
http POST localhost:8000/api/auth/register/ \
  username=testuser \
  email=test@example.com \
  first_name=Test \
  last_name=User \
  password=securepassword123 \
  password_confirm=securepassword123

# Expected: 201 Created with user data and JWT tokens
```

### User Login
```bash
# Login with credentials
http POST localhost:8000/api/auth/login/ \
  username=testuser \
  password=securepassword123

# Expected: 200 OK with user data and JWT tokens
# Save the access token for authenticated requests
```

### Protected Endpoints
```bash
# Get user profile (requires authentication)
http GET localhost:8000/api/auth/profile/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"

# Update user profile
http PUT localhost:8000/api/auth/profile/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  first_name=Updated \
  last_name=Name \
  email=updated@example.com

# Change password
http POST localhost:8000/api/auth/password/change/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  old_password=securepassword123 \
  new_password=newsecurepassword123 \
  new_password_confirm=newsecurepassword123
```

### Token Management
```bash
# Refresh access token
http POST localhost:8000/api/auth/token/refresh/ \
  refresh=YOUR_REFRESH_TOKEN

# Logout (blacklist token)
http POST localhost:8000/api/auth/logout/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  refresh_token=YOUR_REFRESH_TOKEN
```

## 🎬 Phase 4: Movie Catalog Testing

### Movie CRUD Operations
```bash
# List all movies (public)
http GET localhost:8000/api/movies/

# Get movie details
http GET localhost:8000/api/movies/1/

# Search movies
http GET localhost:8000/api/movies/ search=="action comedy"

# Filter movies by genre
http GET localhost:8000/api/movies/ genre_name==Action

# Filter by rating range
http GET localhost:8000/api/movies/ imdb_rating__gte==7.0

# Sort movies
http GET localhost:8000/api/movies/ ordering="-release_date"

# Get popular movies
http GET localhost:8000/api/movies/popular/

# Get trending movies
http GET localhost:8000/api/movies/trending/

# Get top-rated movies
http GET localhost:8000/api/movies/top-rated/
```

### Admin Movie Management (requires admin user)
```bash
# Create a movie (admin only)
http POST localhost:8000/api/movies/create/ \
  Authorization:"Bearer ADMIN_ACCESS_TOKEN" \
  title="Test Movie" \
  description="A test movie" \
  release_date=2024-01-01 \
  duration=120 \
  imdb_rating=7.5 \
  popularity_score=80 \
  genre_ids:='[1,2]' \
  tag_ids:='[1,3]'

# Update a movie (admin only)
http PUT localhost:8000/api/movies/1/update/ \
  Authorization:"Bearer ADMIN_ACCESS_TOKEN" \
  title="Updated Movie Title"

# Delete a movie (admin only)
http DELETE localhost:8000/api/movies/1/delete/ \
  Authorization:"Bearer ADMIN_ACCESS_TOKEN"
```

### Genre Management
```bash
# List genres
http GET localhost:8000/api/movies/genres/

# Get genre details
http GET localhost:8000/api/movies/genres/1/

# Get movies in a genre
http GET localhost:8000/api/movies/genres/1/movies/

# Create genre (admin only)
http POST localhost:8000/api/movies/genres/create/ \
  Authorization:"Bearer ADMIN_ACCESS_TOKEN" \
  name="New Genre" \
  description="Description of the new genre"
```

### Tag Management
```bash
# List tags
http GET localhost:8000/api/movies/tags/

# Get tag details
http GET localhost:8000/api/movies/tags/1/

# Get movies with a tag
http GET localhost:8000/api/movies/tags/1/movies/

# Create tag (admin only)
http POST localhost:8000/api/movies/tags/create/ \
  Authorization:"Bearer ADMIN_ACCESS_TOKEN" \
  name="New Tag"
```

## ⭐ Phase 5: User Interactions Testing

### Rating System
```bash
# Rate a movie
http POST localhost:8000/api/ratings/movies/1/rate/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  rating:=4 \
  review="Great movie!"

# Get user's rating for a movie
http GET localhost:8000/api/ratings/movies/1/rate/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"

# Update rating
http POST localhost:8000/api/ratings/movies/1/rate/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  rating:=5 \
  review="Updated: Excellent movie!"

# Delete rating
http DELETE localhost:8000/api/ratings/movies/1/rate/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"

# Get user's all ratings
http GET localhost:8000/api/ratings/my-ratings/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"

# Get all ratings for a movie
http GET localhost:8000/api/ratings/movies/1/ratings/

# Get movie rating statistics
http GET localhost:8000/api/ratings/movies/1/stats/
```

### Favorites System
```bash
# Add/remove from favorites (toggle)
http POST localhost:8000/api/ratings/movies/1/favorite/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"

# Get user's favorites
http GET localhost:8000/api/ratings/my-favorites/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"
```

### Watch History
```bash
# Add to watch history
http POST localhost:8000/api/ratings/movies/1/watch/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  progress_minutes:=45

# Get user's watch history
http GET localhost:8000/api/ratings/my-watchlist/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"

# Remove from watch history
http DELETE localhost:8000/api/ratings/movies/1/unwatch/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"
```

### User Statistics
```bash
# Get user statistics
http GET localhost:8000/api/ratings/my-stats/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"
```

## 🧠 Phase 6: Recommendation Engine Testing

### Personalized Recommendations
```bash
# Get hybrid recommendations (default)
http GET localhost:8000/api/recommendations/for-me/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"

# Get popularity-based recommendations
http GET localhost:8000/api/recommendations/for-me/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  algorithm==popularity \
  limit:=15

# Get genre-based recommendations
http GET localhost:8000/api/recommendations/for-me/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  algorithm==genre \
  min_rating:=7.0

# Get collaborative filtering recommendations
http GET localhost:8000/api/recommendations/for-me/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  algorithm==collaborative

# Get content-based recommendations
http GET localhost:8000/api/recommendations/for-me/ \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  algorithm==content
```

### Trending Movies
```bash
# Get trending movies (weekly)
http GET localhost:8000/api/recommendations/trending/

# Get daily trending
http GET localhost:8000/api/recommendations/trending/ \
  period==daily \
  limit:=10

# Get monthly trending
http GET localhost:8000/api/recommendations/trending/ \
  period==monthly \
  limit:=25
```

### Similar Movies
```bash
# Get movies similar to a specific movie
http GET localhost:8000/api/recommendations/movies/1/similar/

# Get genre-based similarity
http GET localhost:8000/api/recommendations/movies/1/similar/ \
  method==genre \
  limit:=15

# Get tag-based similarity
http GET localhost:8000/api/recommendations/movies/1/similar/ \
  method==tags

# Get combined similarity
http GET localhost:8000/api/recommendations/movies/1/similar/ \
  method==combined \
  limit:=20
```

## 🔧 Database and Setup Testing

### Check App Status
```bash
# Check all app statuses
http GET localhost:8000/api/auth/status/
http GET localhost:8000/api/movies/status/
http GET localhost:8000/api/ratings/status/
http GET localhost:8000/api/recommendations/status/
```

### Database Population
```bash
# Create sample data (run these in Django shell: python manage.py shell)
# See create_sample_data.py for sample data creation script
```

## 🧪 Comprehensive Integration Testing

### Full User Journey Test
```bash
# 1. Register user
http POST localhost:8000/api/auth/register/ \
  username=journeyuser \
  email=journey@example.com \
  first_name=Journey \
  last_name=User \
  password=testpassword123 \
  password_confirm=testpassword123

# 2. Login
http POST localhost:8000/api/auth/login/ \
  username=journeyuser \
  password=testpassword123

# 3. Browse movies
http GET localhost:8000/api/movies/

# 4. Rate some movies
http POST localhost:8000/api/ratings/movies/1/rate/ \
  Authorization:"Bearer TOKEN" \
  rating:=5 \
  review="Love this movie!"

# 5. Add to favorites
http POST localhost:8000/api/ratings/movies/1/favorite/ \
  Authorization:"Bearer TOKEN"

# 6. Get recommendations
http GET localhost:8000/api/recommendations/for-me/ \
  Authorization:"Bearer TOKEN"

# 7. Check user stats
http GET localhost:8000/api/ratings/my-stats/ \
  Authorization:"Bearer TOKEN"
```

## 📊 Performance Testing

### Load Testing Commands
```bash
# Use Apache Bench for basic load testing
ab -n 100 -c 10 http://localhost:8000/api/movies/

# Use wrk for more advanced testing
wrk -t12 -c400 -d30s http://localhost:8000/api/movies/

# Test with authentication
# Create a file with auth headers and use tools like wrk or hey
```

## 🐛 Error Testing

### Test Error Scenarios
```bash
# Test invalid authentication
http GET localhost:8000/api/ratings/my-ratings/ \
  Authorization:"Bearer invalid_token"

# Test nonexistent resources
http GET localhost:8000/api/movies/99999/

# Test invalid data
http POST localhost:8000/api/ratings/movies/1/rate/ \
  Authorization:"Bearer TOKEN" \
  rating:=10  # Should fail (max is 5)

# Test unauthorized operations
http POST localhost:8000/api/movies/create/ \
  Authorization:"Bearer USER_TOKEN"  # Should fail (admin only)
```

## 📝 Testing Checklist

### Authentication ✅
- [ ] User registration works
- [ ] User login works
- [ ] JWT tokens are generated
- [ ] Token refresh works
- [ ] Password change works
- [ ] Profile update works
- [ ] Logout/token blacklisting works

### Movies ✅
- [ ] Movie list retrieval works
- [ ] Movie detail retrieval works
- [ ] Movie search works
- [ ] Movie filtering works
- [ ] Movie sorting works
- [ ] Popular movies endpoint works
- [ ] Trending movies endpoint works
- [ ] Top-rated movies endpoint works
- [ ] Genre CRUD works (admin)
- [ ] Tag CRUD works (admin)
- [ ] Movie CRUD works (admin)

### Ratings & Interactions ✅
- [ ] Movie rating works
- [ ] Rating updates work
- [ ] Rating deletion works
- [ ] Favorites toggle works
- [ ] Watch history tracking works
- [ ] User statistics work
- [ ] Movie rating statistics work

### Recommendations ✅
- [ ] Personalized recommendations work
- [ ] Different algorithms work
- [ ] Trending movies work
- [ ] Similar movies work
- [ ] Recommendation parameters work

### Error Handling ✅
- [ ] Authentication errors handled
- [ ] Invalid data errors handled
- [ ] Permission errors handled
- [ ] Not found errors handled
- [ ] Rate limiting works (if implemented)

## 🚀 Automation Scripts

Create test scripts in `tests/` directory:

1. `test_auth.py` - Authentication flow tests
2. `test_movies.py` - Movie CRUD and filtering tests
3. `test_ratings.py` - Rating and interaction tests
4. `test_recommendations.py` - Recommendation algorithm tests
5. `test_integration.py` - Full user journey tests

Run all tests:
```bash
python manage.py test
```

## 📈 Monitoring

Monitor these metrics during testing:
- Response times
- Database query counts
- Memory usage
- Error rates
- Cache hit rates (when implemented)

Use Django Debug Toolbar for development monitoring:
```bash
pip install django-debug-toolbar
# Add to INSTALLED_APPS and middleware
```

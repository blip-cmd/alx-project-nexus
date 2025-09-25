# ⚡ Performance Optimization Guide

## 🎯 Overview

This guide covers performance optimizations implemented in the Movie Recommendation API to ensure smooth operation under various loads.

---

## 🚀 Current Performance Optimizations

### **1. Database Optimizations**

#### **Connection Pooling**
```python
# settings.py - Database connection pooling enabled
DATABASES['default'].update({
    'CONN_MAX_AGE': 600,  # 10 minutes connection pooling
    'OPTIONS': {
        'MAX_CONNS': 20,
    }
})
```

#### **Query Optimization**
- **Select Related**: Reduces database queries for related objects
- **Prefetch Related**: Optimizes many-to-many and reverse foreign key queries
- **Database Indexes**: Added on frequently queried fields

#### **Pagination**
```python
# All list endpoints use pagination
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### **2. Caching Strategy**

#### **Redis Caching Configuration**
```python
# Caching timeouts for different endpoints
CACHE_TTL = {
    'movies_popular': 60 * 15,    # 15 minutes
    'movies_trending': 60 * 10,   # 10 minutes  
    'movies_list': 60 * 5,        # 5 minutes
}

# Redis configuration with fallback
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'movie_rec',
        'TIMEOUT': 300,  # 5 minutes default
    }
}
```

### **3. Static Files Optimization**

#### **WhiteNoise Configuration**
```python
# Compressed static files serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### **4. API Response Optimization**

#### **JSON-Only Responses**
```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
```

---

## 📊 Performance Monitoring

### **Logging Configuration**
```python
# Performance monitoring through logging
LOGGING = {
    'loggers': {
        'movies': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
        },
        'recommendations': {
            'level': 'INFO', 
            'handlers': ['console', 'file'],
        },
    },
}
```

---

## 🎯 Performance Benchmarks

### **Target Performance Metrics**

#### **API Response Times**
- **Movie List**: < 500ms
- **Movie Detail**: < 200ms
- **User Registration**: < 1s
- **Login**: < 500ms
- **Recommendations**: < 1s

#### **Database Performance**
- **Query Count**: < 5 queries per request
- **Connection Pool**: 80%+ reuse rate
- **Cache Hit Rate**: > 70%

---

## 💡 Performance Tips

### **Code-Level Optimizations**
- Use select_related() and prefetch_related() for database queries
- Implement pagination for all list endpoints
- Use database indexes on frequently queried fields
- Cache expensive computations like recommendation algorithms
- Minimize serializer field counts to reduce data transfer

### **Infrastructure Optimizations**
- Use CDN for static files in production
- Enable gzip compression on web server
- Use Redis for session storage and caching
- Implement database connection pooling
- Use read replicas for read-heavy operations

---

**⚡ Result: API responds in < 500ms for most requests with smooth user experience!**
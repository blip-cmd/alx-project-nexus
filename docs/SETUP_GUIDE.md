# 🛠️ Complete Setup Guide - Movie Recommendation API

## 📋 Table of Contents
- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)  
- [Development Setup](#-development-setup)
- [Database Setup](#-database-setup)
- [Environment Configuration](#-environment-configuration)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### **Manual Setup**
```bash
# 1. Clone and navigate
git clone https://github.com/blip-cmd/alx-project-nexus.git
cd alx-project-nexus

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Windows Command Prompt  
venv\Scripts\activate.bat
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup database
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

---

## 📋 Prerequisites

### **Required**
- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Virtual Environment** (venv) - Included with Python 3.3+

### **Optional (for Production)**
- **PostgreSQL** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis** - [Download Redis](https://redis.io/download)
- **Docker** - [Download Docker](https://www.docker.com/get-started)

### **Verify Installation**
```bash
python --version    # Should be 3.11+
pip --version       # Should be latest
git --version       # Any recent version
```

---

## 🔧 Development Setup

### **Step 1: Environment Setup**
```bash
# Create project directory
mkdir movie-recommendation-api
cd movie-recommendation-api

# Clone repository
git clone https://github.com/blip-cmd/alx-project-nexus.git .

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
source venv/bin/activate     # Linux/Mac

# Verify activation
which python    # Should point to venv/Scripts/python
```

### **Step 2: Dependencies**
```bash
# Install all dependencies
pip install -r requirements.txt

# Verify critical packages
pip show django djangorestframework
```

### **Step 3: Environment Variables**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# Minimum required for development:
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost
```

---

## 🗄️ Database Setup

### **Development (SQLite - Default)**
```bash
# Create database and run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com  
# Password: [choose secure password]

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### **Production (PostgreSQL)**
```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update .env file
DATABASE_URL=postgresql://username:password@localhost:5432/movie_db

# Run migrations
python manage.py migrate
```

---

## ⚙️ Environment Configuration

### **Development (.env)**
```bash
# Basic Configuration
DEBUG=True
SECRET_KEY=django-insecure-development-key-change-in-production
ALLOWED_HOSTS=127.0.0.1,localhost,testserver

# Database (SQLite for development)
# DATABASE_URL is optional for development

# Caching (optional)
REDIS_URL=redis://127.0.0.1:6379/1

# Security
CORS_ALLOW_ALL_ORIGINS=True
```

### **Production (.env)**
```bash
# Basic Configuration  
DEBUG=False
SECRET_KEY=super-secure-secret-key-for-production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Caching
REDIS_URL=redis://redis-host:6379/0

# Security
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourfrontend.com
```

---

## 🧪 Testing

### **Run All Tests**
```bash
# Using the test runner
python tests/run_tests.py

# Or Windows batch file
tests/test_api.bat

# Or Django's built-in testing
python manage.py test
```

### **Test Individual Components**
```bash
# Test specific app
python manage.py test movies

# Test specific file
python manage.py test authentication.tests

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### **API Testing**
```bash
# Test live API endpoints
python tests/live_api_test.py

# Test database connection
python tests/test_db_connection.py

# Test deployment readiness
python tests/test_deployment.py
```

---

## 🚀 Deployment

### **Render (Recommended)**
1. **Connect Repository**: Link your GitHub repo to Render
2. **Environment Variables**: Set in Render dashboard
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn movie_recommendation_project.wsgi:application`

### **Railway**
1. **Connect Repository**: Link GitHub repo
2. **Set Environment Variables** in Railway dashboard
3. **Deploy automatically** on push to main branch

### **Docker Deployment**
```bash
# Build image
docker build -t movie-recommendation-api .

# Run container
docker run -p 8000:8000 movie-recommendation-api
```

---

## 🛠️ Troubleshooting

### **Common Issues**

#### **"ModuleNotFoundError: No module named 'rest_framework_simplejwt'"**
```bash
# Solution: Activate virtual environment and reinstall
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### **"django.db.utils.OperationalError: no such table"**
```bash
# Solution: Run migrations
python manage.py migrate
```

#### **"Permission denied" on Windows**
```bash
# Solution: Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **Server won't start - "Port already in use"**
```bash
# Solution: Use different port
python manage.py runserver 8001
```

#### **"CORS error" in frontend**
```bash
# Solution: Update CORS settings in settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Your frontend URL
]
```

### **Performance Issues**

#### **Slow API responses**
1. **Enable caching**: Install and configure Redis
2. **Database optimization**: Add database indexes
3. **Pagination**: Ensure API endpoints use pagination

#### **Memory issues**
1. **Check DEBUG setting**: Set `DEBUG=False` in production
2. **Database connections**: Ensure proper connection pooling
3. **Static files**: Use WhiteNoise for static file serving

---

## 📞 Getting Help

### **Resources**
- **Documentation**: Check `docs/` directory
- **API Docs**: Visit `/swagger/` endpoint when server is running  
- **Admin Panel**: Visit `/admin/` for data management

### **Support**
- **Issues**: Create GitHub issue for bugs
- **Questions**: Check existing issues or create discussion
- **Contributions**: Follow contributing guidelines

---

## ✅ Verification Checklist

### **Development Setup Complete**
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list` shows Django, DRF, etc.)
- [ ] Environment variables configured (`.env` file exists)
- [ ] Database migrated (`python manage.py showmigrations` shows [X])
- [ ] Server runs without errors (`python manage.py runserver`)
- [ ] Admin panel accessible (`http://127.0.0.1:8000/admin/`)
- [ ] API documentation loads (`http://127.0.0.1:8000/swagger/`)

### **Production Deployment Complete**  
- [ ] Environment variables set in hosting platform
- [ ] Database connected and migrated
- [ ] Static files served correctly
- [ ] HTTPS enabled
- [ ] CORS configured for frontend domain
- [ ] Performance monitoring enabled

---

**🎉 Congratulations! Your Movie Recommendation API is ready!**

For detailed API usage, see the Swagger documentation at `/swagger/` when your server is running.
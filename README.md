# 🎬 Movie Recommendation App – ALX Project Nexus

## 🚀 Quick Start

### 🌐 **Live Demo**
- **API Base URL**: https://movie-recommendation-api-0thd.onrender.com/
- **API Documentation**: https://movie-recommendation-api-0thd.onrender.com/swagger/
- **Admin Panel**: https://movie-recommendation-api-0thd.onrender.com/admin/
- **📊 Project Presentation Slides**: https://gamma.app/docs/Movie-Recommendation-API-dn7fg6o9xgloikb
- **📊 Project Demo**: https://youtube.com/demovideoincoming

### ⚡ **Local Development Setup**

#### **Prerequisites**
- Python 3.11+ installed
- Git installed
- Virtual environment support

#### **Simple Setup**
```bash
# Clone the repository
git clone https://github.com/blip-cmd/alx-project-nexus.git
cd alx-project-nexus

# Create and activate virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Windows Command Prompt
venv\Scripts\activate.bat
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### **🌐 Access Your Local Server**
- **API Base**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/

---

## 📌 Project Objective
To build a scalable, secure, and feature-rich backend application that delivers personalized movie recommendations based on user preferences, ratings, and viewing history. This project demonstrates mastery of backend engineering principles and serves as a portfolio-grade showcase for professional opportunities.

---

## 🌟 Core Features

- **🔐 User Authentication**  
  Secure login and registration using JWT for stateless session management.

- **🎞️ Movie Catalog**  
  Browse, search, and filter movies by genre, popularity, and release date.

- **⭐ User Ratings & Favorites**  
  Users can rate movies and mark favorites to personalize their experience.

- **🧠 Recommendation Engine**  
  Suggests movies based on user interactions—starting with genre/popularity-based logic and extendable to collaborative filtering.

- **🛠️ Admin Panel**  
  Django Admin interface for managing movie data and user accounts.

---

## 🧱 Technical Highlights

- **📊 Database Design**  
  Normalized ERD with models for Users, Movies, Genres, Ratings, Watch History, and Tags. Designed for relational integrity and query efficiency.

- **⚡ Caching**  
  Redis integration to cache popular movie queries and reduce database load.

- **🔗 API Design**  
  RESTful endpoints using Django REST Framework with pagination, filtering, and auto-generated Swagger documentation.

- **🚀 Deployment**  
  Dockerized application hosted on Railway or Render for public access and CI/CD integration.

- **🔐 Security**  
  JWT-based authentication, role-based access control, and secure password hashing.

---

## 🧰 Tech Stack & Purpose

| Technology            | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| **Python**            | Core programming language for backend logic                             |
| **Django**            | Web framework for rapid development and ORM-based data modeling         |
| **Django REST Framework** | Building RESTful APIs with serializers, viewsets, and routers         |
| **PostgreSQL**        | Relational database for structured and normalized data                  |
| **Redis**             | In-memory caching for performance optimization                          |
| **Docker**            | Containerization for consistent development and deployment environments |
| **JWT (JSON Web Tokens)** | Stateless authentication and secure session management               |
| **Swagger / Postman** | API documentation and testing                                           |
| **Railway / Render**  | Cloud hosting for deployment and public access                          |
| **GitHub Actions**    | CI/CD pipeline for automated testing and deployment                     |

---

## 📂 Project Structure

```
alx-project-nexus/
├── 📁 authentication/           # User authentication & management
│   ├── models.py                # User models and authentication logic
│   ├── serializers.py           # User data serialization
│   ├── views.py                 # Authentication endpoints
│   └── urls.py                  # Authentication URL patterns
├── 📁 movies/                   # Movie catalog & management
│   ├── models.py                # Movie, Genre, Tag models
│   ├── serializers.py           # Movie data serialization
│   ├── views.py                 # Movie CRUD operations
│   └── urls.py                  # Movie API endpoints
├── 📁 ratings/                  # User ratings system
│   ├── models.py                # Rating and review models
│   ├── serializers.py           # Rating data serialization
│   └── views.py                 # Rating management endpoints
├── 📁 recommendations/          # Recommendation engine
│   ├── models.py                # Recommendation models
│   ├── views.py                 # Recommendation algorithms
│   └── urls.py                  # Recommendation endpoints
├── 📁 movie_recommendation_project/ # Django project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI application entry point
├── 📁 static/                   # Static files (CSS, JS, images)
├── 📁 templates/                # HTML templates
├── 📁 scripts/                  # Setup & build scripts
│   ├── build.sh                 # Production build script
│   ├── setup.ps1                # Windows development setup
│   └── setup.py                 # Python setup configuration
├── 📁 tests/                    # Testing suite
│   ├── api_test_suite.py        # Comprehensive API tests
│   ├── run_tests.py             # Test runner script
│   ├── test_auth_live.py        # Authentication testing
│   ├── test_db_connection.py    # Database connectivity tests
│   └── test_deployment.py       # Deployment verification tests
├── 📁 docs/                     # Documentation & design files
│   ├── API_USAGE_GUIDE.md       # Complete API usage documentation
│   ├── PERFORMANCE_GUIDE.md     # Performance optimization guide
│   ├── SETUP_GUIDE.md           # Detailed setup instructions
│   ├── ERD.png                  # Database design diagram
│   ├── ERD.txt                  # Database schema documentation
│   └── TODO.md                  # Development roadmap
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── render.yaml                  # Render deployment configuration
├── .env.example                 # Environment variables template
└── README.md                    # Project documentation (this file)
```

---

## 🎯 Why This Project Matters

This app simulates a real-world backend system for a streaming platform, demonstrating your ability to:

- Architect scalable and maintainable APIs
- Handle sensitive user data securely
- Optimize performance with caching and efficient queries
- Collaborate effectively with frontend teams
- Apply backend engineering principles in a production-like environment

---

## 🧱 What the Backend Is Building

### 1. **User Management System**
- Handles user registration, login, and authentication using JWT
- Stores user profiles securely with hashed passwords
- Manages user sessions and access control

### 2. **Movie Catalog API**
- CRUD operations for movies, genres, and tags
- Endpoints to browse, search, and filter movies by genre, popularity, and release date
- Admin access to manage movie data via Django Admin

### 3. **User Interaction Tracking**
- Stores user ratings for movies (1–5 stars or similar)
- Tracks watch history and favorite movies
- These interactions feed into the recommendation logic

### 4. **Recommendation Engine**
- Suggests movies based on:
  - Genre preferences
  - Popularity trends
  - User rating patterns
- Can be extended to collaborative filtering or content-based algorithms

### 5. **Optimized Data Layer**
- Normalized relational database schema using Django ORM
- Efficient queries for filtering, sorting, and aggregating movie data
- Redis caching for high-traffic endpoints (e.g., trending movies)

### 6. **RESTful API Interface**
- Clean, versioned endpoints for frontend consumption
- Pagination, filtering, and sorting support
- Swagger or Postman documentation for easy integration

### 7. **Deployment & Hosting**
- Dockerized backend for portability
- Hosted on Railway or Render with CI/CD pipelines
- Environment variables and secrets managed securely

---

## Getting Started

To get a local copy up and running, follow these steps (to be updated as the project progresses).

### Prerequisites

- Python 3.x
- pip
- PostgreSQL
- Redis (for caching)
- Docker (optional, for containerization)

### Installation (To Be Updated)

1. Clone the repository:
   ```bash
   git clone https://github.com/blip-cmd/alx-project-nexus.git
   ```
2. Navigate to the project directory:
   ```bash
   cd alx-project-nexus
   ```
3. Install dependencies (requirements file and details will be added as development begins):
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database and environment variables as needed (instructions will follow).

---

## 📚 Documentation & Guides

This project includes comprehensive documentation to help you get started and understand the system:

### **🚀 Setup & Development**
- **[Complete Setup Guide](docs/SETUP_GUIDE.md)** - Detailed installation and configuration instructions
- **[Performance Guide](docs/PERFORMANCE_GUIDE.md)** - Optimization strategies and monitoring

### **🌐 API Documentation**
- **[API Usage Guide](docs/API_USAGE_GUIDE.md)** - Complete API endpoint documentation with examples
- **[Interactive API Docs](https://movie-recommendation-api-0thd.onrender.com/swagger/)** - Swagger UI for testing
- **[ReDoc Documentation](https://movie-recommendation-api-0thd.onrender.com/redoc/)** - Alternative API documentation format

### **📊 Database & Architecture**
- **[Entity Relationship Diagram](docs/ERD.png)** - Visual database schema
- **[Database Schema](docs/ERD.txt)** - Text-based schema documentation
- **[Development Roadmap](docs/TODO.md)** - Project tasks and progress tracking

### **🧪 Testing**
- **[Testing Guide](docs/TESTING_GUIDE.md)** - How to run and write tests
- **Automated Test Suite** - Located in `tests/` directory

---

## ✅ Development Challenges & Solutions

- **Challenge**: Designing a flexible schema for user preferences and ratings  
	**Solution**: Created normalized models with many-to-many relationships and indexed queries for performance.

- **Challenge**: Ensuring fast response times for popular endpoints  
	**Solution**: Integrated Redis to cache frequently accessed movie data.

- **Challenge**: Building a scalable recommendation engine  
	**Solution**: Started with genre-based filtering and laid groundwork for collaborative filtering using user ratings.

- **Challenge**: Syncing with frontend collaborators  
	**Solution**: Shared API specs early via Discord and used Postman collections for testing.

---

## ✅ Best Practices & Personal Takeaways

- Write modular, readable, and well-documented code
- Use Git strategically: branches, commits, pull requests
- Prioritize API clarity and consistency
- Secure authentication flows with token-based access
- Embrace CI/CD for professional-grade workflows
- Collaborate early and often—communication is key

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## 📄 License

This project is licensed under the MIT License.

---

## 🚀 Final Thoughts

Project Nexus will be a transformative experience. It challenges me to apply backend engineering principles in a real-world context, collaborate across teams, and deliver a professional-grade application. This repository stands as a testament to my growth and readiness for backend engineering roles in the global tech landscape.
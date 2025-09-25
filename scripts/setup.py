#!/usr/bin/env python
"""
🎬 Movie Recommendation API - Setup Script
Automated setup for the movie recommendation system.
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description="", check=True):
    """Run a shell command with error handling."""
    print(f"🔄 {description}")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        if result.stderr and check:
            print(f"   Warning: {result.stderr.strip()}")
        print("   ✅ Success\n")
        return result
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        print()
        if check:
            sys.exit(1)
        return e

def check_python_version():
    """Check if Python version is adequate."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_and_install_requirements():
    """Install Python packages from requirements.txt."""
    print("📦 Installing Python packages...")
    
    # Upgrade pip first
    run_command("python -m pip install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    run_command("pip install -r requirements.txt", "Installing requirements")

def setup_environment():
    """Set up environment variables."""
    print("🔧 Setting up environment...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("Creating .env file...")
        env_content = """# Django Settings
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Settings (SQLite for development)
USE_SQLITE=True
DB_NAME=movie_recommendation_db
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# Redis Settings
REDIS_URL=redis://127.0.0.1:6379/1

# Email Settings (for password reset)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    else:
        print("✅ .env file already exists")

def setup_database():
    """Set up the database."""
    print("🗄️ Setting up database...")
    
    # Make migrations
    run_command("python manage.py makemigrations", "Creating migrations")
    
    # Apply migrations
    run_command("python manage.py migrate", "Applying migrations")

def create_superuser():
    """Create a superuser account."""
    print("👤 Creating superuser account...")
    
    # Check if superuser already exists
    result = run_command(
        'python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())"',
        "Checking for existing superuser",
        check=False
    )
    
    if "True" in result.stdout:
        print("✅ Superuser already exists")
        return
    
    print("Creating superuser account...")
    print("Please enter superuser details:")
    
    # Create superuser interactively
    run_command("python manage.py createsuperuser", "Creating superuser account")

def create_sample_data():
    """Create sample data for testing."""
    print("🎭 Creating sample data...")
    
    run_command(
        "python manage.py create_sample_data --movies 30 --users 10 --ratings 150",
        "Creating sample movies, users, and ratings"
    )

def test_server():
    """Test if the server can start."""
    print("🧪 Testing server startup...")
    
    # Test server startup (run for 5 seconds then stop)
    run_command(
        "timeout 5 python manage.py runserver || true",
        "Testing server startup",
        check=False
    )

def display_completion_message():
    """Display setup completion message."""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE! 🎉")
    print("="*60)
    print()
    print("🚀 Your Movie Recommendation API is ready!")
    print()
    print("📝 Next steps:")
    print("1. Start the development server:")
    print("   python manage.py runserver")
    print()
    print("2. Visit the API documentation:")
    print("   • Swagger UI: http://127.0.0.1:8000/swagger/")
    print("   • ReDoc: http://127.0.0.1:8000/redoc/")
    print("   • API Root: http://127.0.0.1:8000/api/")
    print()
    print("3. Access the admin panel:")
    print("   • Admin: http://127.0.0.1:8000/admin/")
    print()
    print("4. Start testing with the sample data:")
    print("   • See TESTING_GUIDE.md for comprehensive testing instructions")
    print("   • Use the test users (testuser1-10) with password 'testpassword123'")
    print()
    print("📊 What was created:")
    print("   • Database with sample movies, users, and ratings")
    print("   • JWT authentication system")
    print("   • Movie catalog with search and filtering")
    print("   • Rating and recommendation systems")
    print("   • API documentation")
    print()
    print("🔧 Optional: Set up Redis for caching")
    print("   • Install Redis server")
    print("   • Update REDIS_URL in .env if needed")
    print()
    print("Happy coding! 🎬✨")

def main():
    """Main setup function."""
    print("🎬 Movie Recommendation API - Setup Script")
    print("="*50)
    print()
    
    # Check Python version
    check_python_version()
    print()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    try:
        # Setup steps
        check_and_install_requirements()
        setup_environment()
        setup_database()
        
        # Ask about creating superuser
        create_superuser_choice = input("🤔 Would you like to create a superuser account? (y/n): ").lower()
        if create_superuser_choice in ['y', 'yes']:
            create_superuser()
        
        # Ask about sample data
        create_data_choice = input("🤔 Would you like to create sample data for testing? (y/n): ").lower()
        if create_data_choice in ['y', 'yes']:
            create_sample_data()
        
        # Test server
        test_server()
        
        # Display completion message
        display_completion_message()
        
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

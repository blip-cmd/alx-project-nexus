# 🎬 Movie Recommendation API - Windows Setup Script
# PowerShell script for automated setup on Windows

Write-Host "🎬 Movie Recommendation API - Setup Script" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Yellow
Write-Host ""

# Function to run commands with error handling
function Run-Command {
    param(
        [string]$Command,
        [string]$Description = "",
        [bool]$CheckErrors = $true
    )
    
    Write-Host "🔄 $Description" -ForegroundColor Cyan
    Write-Host "   Command: $Command" -ForegroundColor Gray
    
    try {
        if ($CheckErrors) {
            Invoke-Expression $Command
            if ($LASTEXITCODE -ne 0) {
                throw "Command failed with exit code $LASTEXITCODE"
            }
        } else {
            Invoke-Expression $Command | Out-Null
        }
        Write-Host "   ✅ Success`n" -ForegroundColor Green
    }
    catch {
        Write-Host "   ❌ Error: $_`n" -ForegroundColor Red
        if ($CheckErrors) {
            exit 1
        }
    }
}

# Check Python version
Write-Host "🐍 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python (\d+)\.(\d+)") {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "❌ Python 3.8 or higher is required. Found: $pythonVersion" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Install packages
Write-Host "📦 Installing Python packages..." -ForegroundColor Yellow
Run-Command "python -m pip install --upgrade pip" "Upgrading pip"
Run-Command "pip install -r requirements.txt" "Installing requirements"

# Setup environment
Write-Host "🔧 Setting up environment..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Cyan
    $envContent = @"
# Django Settings
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
"@
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ Created .env file" -ForegroundColor Green
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}
Write-Host ""

# Setup database
Write-Host "🗄️ Setting up database..." -ForegroundColor Yellow
Run-Command "python manage.py makemigrations" "Creating migrations"
Run-Command "python manage.py migrate" "Applying migrations"

# Check for existing superuser
Write-Host "👤 Checking for superuser..." -ForegroundColor Yellow
$hasSuperuser = python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())"
if ($hasSuperuser -match "True") {
    Write-Host "✅ Superuser already exists" -ForegroundColor Green
} else {
    $createSuperuser = Read-Host "🤔 Would you like to create a superuser account? (y/n)"
    if ($createSuperuser -eq "y" -or $createSuperuser -eq "yes") {
        Write-Host "Creating superuser account..." -ForegroundColor Cyan
        python manage.py createsuperuser
    }
}
Write-Host ""

# Create sample data
$createData = Read-Host "🤔 Would you like to create sample data for testing? (y/n)"
if ($createData -eq "y" -or $createData -eq "yes") {
    Write-Host "🎭 Creating sample data..." -ForegroundColor Yellow
    Run-Command "python manage.py create_sample_data --movies 30 --users 10 --ratings 150" "Creating sample movies, users, and ratings"
}

# Test server startup
Write-Host "🧪 Testing server startup..." -ForegroundColor Yellow
$serverTest = Start-Job -ScriptBlock { python manage.py runserver 2>&1 }
Start-Sleep -Seconds 3
Stop-Job $serverTest
$testOutput = Receive-Job $serverTest
Remove-Job $serverTest

if ($testOutput -match "Starting development server") {
    Write-Host "✅ Server test successful" -ForegroundColor Green
} else {
    Write-Host "⚠️ Server test completed (check for any errors above)" -ForegroundColor Yellow
}
Write-Host ""

# Display completion message
Write-Host "=" * 60 -ForegroundColor Yellow
Write-Host "🎉 SETUP COMPLETE! 🎉" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 Your Movie Recommendation API is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Start the development server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Visit the API documentation:" -ForegroundColor White
Write-Host "   • Swagger UI: http://127.0.0.1:8000/swagger/" -ForegroundColor Gray
Write-Host "   • ReDoc: http://127.0.0.1:8000/redoc/" -ForegroundColor Gray
Write-Host "   • API Root: http://127.0.0.1:8000/api/" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Access the admin panel:" -ForegroundColor White
Write-Host "   • Admin: http://127.0.0.1:8000/admin/" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Start testing with the sample data:" -ForegroundColor White
Write-Host "   • See TESTING_GUIDE.md for comprehensive testing instructions" -ForegroundColor Gray
Write-Host "   • Use the test users (testuser1-10) with password 'testpassword123'" -ForegroundColor Gray
Write-Host ""
Write-Host "📊 What was created:" -ForegroundColor Cyan
Write-Host "   • Database with sample movies, users, and ratings" -ForegroundColor Gray
Write-Host "   • JWT authentication system" -ForegroundColor Gray
Write-Host "   • Movie catalog with search and filtering" -ForegroundColor Gray
Write-Host "   • Rating and recommendation systems" -ForegroundColor Gray
Write-Host "   • API documentation" -ForegroundColor Gray
Write-Host ""
Write-Host "🔧 Optional: Set up Redis for caching" -ForegroundColor Yellow
Write-Host "   • Install Redis server" -ForegroundColor Gray
Write-Host "   • Update REDIS_URL in .env if needed" -ForegroundColor Gray
Write-Host ""
Write-Host "Happy coding! 🎬✨" -ForegroundColor Green

# Keep window open
Write-Host ""
Write-Host "Press Enter to continue..." -ForegroundColor Yellow
Read-Host

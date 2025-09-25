@echo off
REM 🧪 Movie Recommendation API - Windows Test Runner
echo 🎬 Movie Recommendation API Test Suite
echo =====================================

REM Check if virtual environment exists
if not exist "..\venv\" (
    echo ❌ Virtual environment not found!
    echo 💡 Create it with: python -m venv venv (from project root)
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call ..\venv\Scripts\activate.bat

REM Check if Django server is running
echo 🔍 Checking if Django server is running...
curl -s http://127.0.0.1:8000/ >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Django server doesn't seem to be running
    echo 💡 Please start it in another terminal with: python manage.py runserver
    echo.
    echo 🤔 Do you want to continue anyway? (y/n)
    set /p choice=
    if /i not "%choice%"=="y" (
        echo ❌ Test cancelled
        pause
        exit /b 1
    )
)

REM Run the tests
echo 🧪 Running API tests...
echo.
python run_tests.py

REM Show results
echo.
echo 📄 Test results saved to: test_results.txt
echo.
echo 🔍 Opening results file...
type test_results.txt | more

echo.
echo ✅ Test execution completed!
pause
@echo off
REM 🎬 Movie Recommendation API - Quick Access (Windows)
echo.
echo 🎬 Movie Recommendation API - Quick Access
echo =============================================
echo.
echo Choose an action:
echo [1] 🛠️  Setup Development Environment
echo [2] 🧪  Run API Tests
echo [3] 🏗️  Build for Production
echo [4] 📖  Open Documentation Folder
echo [5] 🚪  Exit
echo.
set /p choice="Select option (1-5): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto tests
if "%choice%"=="3" goto build
if "%choice%"=="4" goto docs
if "%choice%"=="5" goto exit
goto invalid

:setup
echo 🛠️  Running setup script...
powershell -ExecutionPolicy Bypass -File "scripts\setup.ps1"
pause
goto menu

:tests
echo 🧪  Running API tests...
cd tests
python run_tests.py
cd ..
pause
goto menu

:build
echo 🏗️  Building for production...
bash scripts\build.sh
pause
goto menu

:docs
echo 📖  Opening documentation folder...
explorer docs
pause
goto menu

:invalid
echo ❌ Invalid choice! Please select 1-5.
pause

:menu
cls
goto start

:exit
echo 👋 Goodbye!
exit /b 0

:start
goto menu
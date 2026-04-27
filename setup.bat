@echo off
REM Quick setup script for RPK Trading System (Windows)

echo.
echo ========================================
echo RPK Algorithmic Trading System
echo Setup Script (Windows)
echo ========================================

REM Check Python version
python --version
echo.

REM Navigate to backend
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed

REM Return to root
cd ..

echo.
echo ========================================
echo Setup complete!
echo.
echo To start the application:
echo.
echo 1. Backend (Flask API):
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python run.py
echo.
echo 2. Frontend (Web Interface):
echo    cd frontend
echo    Open index.html in your browser
echo.
echo API will be at: http://localhost:5000
echo ========================================
pause

@echo off
echo ========================================
echo CarRent AI Chatbot - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file - PLEASE EDIT IT TO ADD YOUR OPENAI API KEY!
) else (
    echo .env file already exists
)

echo [5/5] Initializing database...
python database.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo IMPORTANT: Edit .env file and add your OpenAI API key
echo.
echo To start the application:
echo   1. Run: venv\Scripts\activate.bat
echo   2. Run: python app.py
echo   3. Open browser to: http://localhost:5000
echo.
pause

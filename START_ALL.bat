@echo off
REM Krishna RAG - Complete System Starter (Backend + Frontend)
REM Starts both backend and frontend servers with one click

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo     Krishna RAG - Bhagavad Gita AI Assistant
echo     Complete System Launcher
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python found
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo [*] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [*] Installing dependencies...
pip install -q -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [✓] Dependencies installed

REM Check Gemini API Key
echo.
if "%GEMINI_API_KEY%"=="" (
    echo [!] GEMINI_API_KEY not set - will use pretrained answers
) else (
    echo [✓] GEMINI_API_KEY found
)

echo.
echo ================================================================
echo   Starting Backend and Frontend...
echo ================================================================
echo.

REM Start Backend in a new window
echo [*] Starting Backend (Port 8000)...
start "Krishna RAG - Backend" cmd /k "cd backend && python main.py"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start Frontend in a new window
echo [*] Starting Frontend (Port 3000)...
start "Krishna RAG - Frontend" cmd /k "cd frontend && python -m http.server 3000"

REM Wait for frontend to start
timeout /t 2 /nobreak

echo.
echo ================================================================
echo   ✓ Krishna RAG System Started Successfully!
echo ================================================================
echo.
echo   FRONTEND:  http://localhost:3000
echo   BACKEND:   http://localhost:8000
echo   API DOCS:  http://localhost:8000/docs
echo.
echo   FEATURES:
echo   - 50 Pretrained Q&A Pairs (instant responses)
echo   - Gemini API Integration
echo   - RAG with Vector Search
echo   - All responses prefixed with "Krishna says:"
echo.
echo   HOW TO USE:
echo   1. Open http://localhost:3000 in your browser
echo   2. Type your question about the Bhagavad Gita
echo   3. Get instant answers or AI-generated responses
echo.
echo   EXAMPLE QUESTIONS:
echo   - "What is the purpose of meditation?"
echo   - "How can I handle stress?"
echo   - "Tell me about karma yoga"
echo.
echo ================================================================
echo.
echo   System is running. Both terminal windows will stay open.
echo   Close either window to stop that service.
echo.
pause

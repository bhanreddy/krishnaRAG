@echo off
REM Krishna RAG - Backend Server Starter

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo     Krishna RAG - Backend Server
echo     Gemini API + 50 Pretrained Q&A Answers
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python found
python --version

REM Create and activate venv
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [*] Installing dependencies...
pip install -q -r requirements.txt >nul 2>&1

echo [✓] Ready to start

echo.
echo ================================================================
echo   Backend Configuration:
echo ================================================================
echo   URL:      http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   
echo   FEATURES:
echo   ✓ 50 Pretrained Q&A (instant <100ms)
echo   ✓ Gemini API Integration
echo   ✓ RAG with Vector Search
echo   ✓ "Krishna says:" prefix on all answers
echo.
if "%GEMINI_API_KEY%"=="" (
    echo   NOTE: GEMINI_API_KEY not set
    echo   System will use pretrained answers for common topics
) else (
    echo   ✓ Gemini API Key configured
)
echo ================================================================
echo.
echo [*] Starting Backend Server...
echo.

cd backend
python main.py

pause


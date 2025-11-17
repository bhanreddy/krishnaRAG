@echo off
REM GitaRAG - Quick Start Script for Windows

echo.
echo ================================================
echo     GitaRAG - Bhagavad Gita AI Assistant
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1] Checking Python version...
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo [2] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo.
echo [3] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo [4] Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Check if Ollama is running
echo.
echo [5] Checking Ollama service...
for /f %%i in ('curl -s http://localhost:11434/api/tags ^| findstr "models" 2^>nul') do set OLLAMA_OK=1

if not defined OLLAMA_OK (
    echo WARNING: Ollama service not detected at http://localhost:11434
    echo Please ensure:
    echo   1. Ollama is installed from https://ollama.ai/download
    echo   2. Ollama is running (ollama serve)
    echo   3. A model is pulled (ollama pull mistral)
    echo.
    echo Do you want to continue anyway? (y/n)
    set /p CONTINUE=
    if /i not "%CONTINUE%"=="y" (
        pause
        exit /b 1
    )
)

REM Start the application
echo.
echo [6] Starting GitaRAG Backend...
echo.
echo ================================================
echo   Backend will start on: http://localhost:8000
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo ================================================
echo.

cd backend
python main.py

pause

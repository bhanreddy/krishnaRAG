@echo off
REM Krishna RAG - Frontend Server Starter

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo     Krishna RAG - Frontend Server
echo     Bhagavad Gita AI Assistant
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

echo.
echo ================================================================
echo   Frontend Configuration:
echo ================================================================
echo   URL:              http://localhost:3000
echo   Backend URL:      http://localhost:8000
echo.
echo   IMPORTANT: Backend must be running!
echo   Run start_backend.bat in another window first.
echo.
echo   Or use START_ALL.bat to launch both at once!
echo ================================================================
echo.
echo [*] Starting Frontend Server...
echo.

cd frontend
python -m http.server 3000

pause


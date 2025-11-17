@echo off
REM GitaRAG - Frontend Quick Start

echo.
echo ================================================
echo     GitaRAG - Frontend Server
echo ================================================
echo.

cd frontend

REM Check if Python is available for simple server
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not available
    pause
    exit /b 1
)

echo Starting frontend server on http://localhost:3000
echo Press Ctrl+C to stop
echo.

python -m http.server 3000

pause

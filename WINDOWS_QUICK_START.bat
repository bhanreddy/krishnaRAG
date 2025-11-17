@echo off
REM ============================================================
REM     GitaRAG - How to Use (Windows Quick Start)
REM ============================================================

cls
echo.
echo ============================================================
echo     GITAGRAG - BHAGAVAD GITA AI ASSISTANT
echo     How to Use - Windows Step by Step
echo ============================================================
echo.

echo.
echo STEP 1: INSTALL OLLAMA
echo ============================================================
echo.
echo.
echo TO VERIFY: Open PowerShell and type: ollama --version
echo Should show a version number if installed correctly.
echo.
pause

cls
echo.
echo STEP 2: DOWNLOAD AN AI MODEL
echo ============================================================
echo.
echo Open PowerShell and type ONE of these:
echo.
echo   ollama pull mistral          (RECOMMENDED - Fast & Good)
echo   ollama pull llama2           (Alternative)
echo   ollama pull neural-chat      (Alternative - Fast)
echo.
echo Copy and paste the command above.
echo Wait 2-5 minutes while it downloads (~4GB).
echo.
echo TO VERIFY: Type: ollama list
echo Should show your model in the list.
echo.
pause

cls
echo.
echo STEP 3: SETUP PYTHON ENVIRONMENT
echo ============================================================
echo.
echo 3a. Open PowerShell
echo     - Press Win+R
echo     - Type: powershell
echo     - Press Enter
echo.
echo 3b. Navigate to project:
echo     cd "c:\Users\reddy\Desktop\Capestone Project"
echo.
echo 3c. Create virtual environment:
echo     python -m venv venv
echo     Wait 30 seconds...
echo.
echo 3d. Activate environment:
echo     venv\Scripts\Activate.ps1
echo     (You should see (venv) appear in the terminal)
echo.
echo 3e. Install dependencies:
echo     pip install -r requirements.txt
echo     Wait 2-3 minutes...
echo.
pause

cls
echo.
echo STEP 4: START THE BACKEND SERVER
echo ============================================================
echo.
echo 4a. Make sure you see (venv) in terminal
echo.
echo 4b. Navigate to backend:
echo     cd backend
echo.
echo 4c. Start the server:
echo     python main.py
echo.
echo WAIT FOR THIS MESSAGE:
echo   "Uvicorn running on http://0.0.0.0:8000"
echo.
echo IMPORTANT: KEEP THIS TERMINAL OPEN!
echo Do NOT close it while using the app.
echo.
pause

cls
echo.
echo STEP 5: START THE FRONTEND SERVER
echo ============================================================
echo.
echo 5a. Open a NEW PowerShell window (don't close the first one!)
echo     - Press Win+R
echo     - Type: powershell
echo     - Press Enter
echo.
echo 5b. Navigate to project:
echo     cd "c:\Users\reddy\Desktop\Capestone Project"
echo.
echo 5c. Navigate to frontend:
echo     cd frontend
echo.
echo 5d. Start web server:
echo     python -m http.server 3000
echo.
echo WAIT FOR THIS MESSAGE:
echo   "Serving HTTP on 0.0.0.0 port 3000"
echo.
echo IMPORTANT: KEEP THIS TERMINAL OPEN TOO!
echo Now you have TWO terminals open - both needed.
echo.
pause

cls
echo.
echo STEP 6: OPEN IN BROWSER
echo ============================================================
echo.
echo 6a. Open your web browser (Chrome, Firefox, Edge, etc)
echo.
echo 6b. Type in the address bar:
echo     http://localhost:3000
echo.
echo 6c. Press Enter
echo.
echo YOU SHOULD SEE:
echo   - Beautiful page with OM symbol (🕉️)
echo   - Question input box
echo   - "Ask AI" button
echo   - Modern gradient design
echo.
pause

cls
echo.
echo STEP 7: ASK YOUR FIRST QUESTION!
echo ============================================================
echo.
echo 7a. Click in the question box
echo.
echo 7b. Type a question, for example:
echo     What is the meaning of yoga?
echo.
echo 7c. Click "Ask AI" button
echo.
echo 7d. Wait 10-15 seconds for answer
echo.
echo YOU SHOULD SEE:
echo   - 🧠 AI Answer section
echo   - 📚 Retrieved Passages section
echo   - Actual Gita verses
echo.
echo TRY THESE QUESTIONS:
echo   - What does Krishna teach about duty?
echo   - Explain the concept of dharma
echo   - What is enlightenment?
echo   - Who is Arjuna?
echo.
pause

cls
echo.
echo ============================================================
echo     ALL SET! YOU'RE READY TO GO!
echo ============================================================
echo.
echo WHAT'S RUNNING NOW:
echo   ✓ Ollama (LLM Service)      - Port 11434
echo   ✓ Backend (FastAPI)         - Port 8000 (Terminal 1)
echo   ✓ Frontend (Web Server)     - Port 3000 (Terminal 2)
echo   ✓ Browser                   - http://localhost:3000
echo.
echo IMPORTANT REMINDERS:
echo   - Keep BOTH terminals open while using
echo   - Don't close them or the app stops
echo   - Questions take 10-15 seconds to answer
echo   - Ollama should be running
echo.
echo TROUBLESHOOTING:
echo   "Connection refused?" → Check both terminals are open
echo   "LLM not available?" → Start Ollama (check taskbar)
echo   "Port in use?" → Try: python -m http.server 5000
echo.
echo STOP THE APP:
echo   - Press Ctrl+C in each terminal
echo   - Close browser
echo.
echo TO RESTART:
echo   - Start backend again (Step 4)
echo   - Start frontend again (Step 5)
echo   - Refresh browser
echo.
echo NEED HELP?
echo   Read: HOW_TO_USE.md (full version)
echo   Read: SETUP_GUIDE.md (detailed guide)
echo   Read: QUICK_REFERENCE.md (quick help)
echo.
echo 🙏 Enjoy exploring the Bhagavad Gita! ✨
echo.
echo ============================================================
pause

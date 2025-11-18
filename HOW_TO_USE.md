# 🚀 GitaRAG - How to Use (Step-by-Step)

## ⚡ Quick Start in 5 Minutes

---

## STEP 1️⃣: Configure Google Gemini

### What is Google Gemini?
Google Gemini (Generative Language API) is Google's hosted LLM service. This project now uses the Gemini API via the `google-generativeai` SDK. You must provide a valid API key in the environment variable `GEMINI_API_KEY`.

### Quick setup
1. Obtain a Gemini API key from Google Cloud and set it in your environment:

```powershell
setx GEMINI_API_KEY "<YOUR_GEMINI_API_KEY>"
# Restart your shell after setting the env var
```

2. Install Python dependencies and the SDK:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Verify the backend can contact Gemini by starting the backend and calling `/llm/status` or `/llm/test` (see API docs).

---

## STEP 2️⃣: Download an AI Model

### What is a Model?
A model is the AI brain. Think of it like installing a smart assistant.

### Popular Options:

**Option A: Mistral (RECOMMENDED) ⭐**
- Fast and accurate
- 7 billion parameters
- Best for beginners
```bash
ollama pull mistral
```

**Option B: Llama2**
- Popular and capable
- 7 billion parameters
```bash
ollama pull llama2
```

**Option C: Neural-Chat**
- Optimized for conversation
- Fast responses
```bash
ollama pull neural-chat
```

### How to Pull:

1. Open **PowerShell** (Windows) or **Terminal** (Mac/Linux)
2. Type this command:
```bash
ollama pull mistral
```
3. Wait 2-5 minutes while it downloads (about 4GB)
4. You'll see progress bars
5. When done, you'll see: ✅ "success"

### ✅ Verify Model Downloaded:
```bash
ollama list
```

Should show your model in the list. ✅

---

## STEP 3️⃣: Setup Python Environment

### What is Virtual Environment?
A isolated Python workspace for this project. Keeps dependencies organized.

### Steps:

#### **Step 3a: Open Terminal**

**Windows:**
- Press `Win + R`
- Type `cmd` or `powershell`
- Press Enter

**Mac/Linux:**
- Open Terminal application

#### **Step 3b: Navigate to Project**

```bash
cd "c:\Users\reddy\Desktop\Capestone Project"
```

Or use File Explorer to navigate there, then right-click and "Open in Terminal"

#### **Step 3c: Create Virtual Environment**

```bash
python -m venv venv
```

Wait a few seconds... ✅ Done when you see nothing printed

#### **Step 3d: Activate Virtual Environment**

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

✅ You'll see `(venv)` appear at the start of your terminal line

#### **Step 3e: Install Dependencies**

```bash
pip install -r requirements.txt
```

Wait 2-3 minutes while packages install...

You'll see lots of text. When done, you should see ✅ "Successfully installed..."

---

## STEP 4️⃣: Start the Backend

### What is Backend?
The server that handles your questions and connects to the AI.

### Steps:

1. Make sure terminal shows `(venv)` at the start
2. Navigate to backend folder:
```bash
cd backend
```

3. Start the server:
```bash
python main.py
```

### ✅ Success Signs:
You should see:
```
✓ LLM Service Connected: mistral at http://localhost:11434
✓ Application startup complete
✓ Uvicorn running on http://0.0.0.0:8000
```

**KEEP THIS TERMINAL OPEN** ← Important! Don't close it.

---

## STEP 5️⃣: Start the Frontend

### What is Frontend?
The beautiful web interface where you ask questions.

### Steps:

1. **Open a NEW terminal** (don't close the backend one!)

**Windows:**
- Press `Win + R`, type `cmd`, press Enter

**Mac/Linux:**
- Open a new Terminal window

2. Navigate to project:
```bash
cd "c:\Users\reddy\Desktop\Capestone Project"
```

3. Navigate to frontend:
```bash
cd frontend
```

4. Start web server:
```bash
python -m http.server 3000
```

### ✅ Success Signs:
You should see:
```
Serving HTTP on 0.0.0.0 port 3000...
```

**KEEP THIS TERMINAL OPEN** ← Important!

---

## STEP 6️⃣: Open in Browser

### Final Step!

1. Open your web browser (Chrome, Firefox, Edge, Safari)
2. Type in address bar:
```
http://localhost:3000
```
3. Press Enter

### ✅ You Should See:
- Beautiful Gita page with OM symbol 🕉️
- Question input box
- "Ask AI" button
- Modern gradient design

---

## STEP 7️⃣: Ask Your First Question!

### Try These Questions:

**Example 1:** Click in the textarea and type:
```
What is the meaning of yoga?
```

Then click **Ask AI** button.

Wait 10-15 seconds...

You'll see:
- 🧠 AI Answer
- 📚 Retrieved Passages (with the actual Gita verses)

**Example 2:**
```
What does Krishna teach about duty?
```

**Example 3:**
```
Explain the concept of dharma
```

---

## 🎯 Visual Diagram

```
┌─────────────────────────────────────┐
│  Your Computer                      │
├─────────────────────────────────────┤
│                                     │
│  Terminal 1: Backend (Port 8000)    │
│  ✅ python main.py                  │
│                                     │
│  Terminal 2: Frontend (Port 3000)   │
│  ✅ python -m http.server 3000      │
│                                     │
│  Browser: http://localhost:3000     │
│  ✅ Ask Questions Here              │
│                                     │
│  Ollama: LLM Service (Port 11434)   │
│  ✅ Running in background           │
│                                     │
└─────────────────────────────────────┘
```

---

## 📋 Troubleshooting Quick Fixes

### ❌ "LLM service not available"

**Solution:**
```bash
ollama serve
```

Or check if Ollama is running (look for Ollama icon in taskbar/menu)

### ❌ "Connection refused" or "Cannot connect to server"

**Solution:** Make sure BOTH terminals are open:
- Terminal 1: Backend running
- Terminal 2: Frontend running
- Ollama: Running (check taskbar)

### ❌ "Port already in use"

**Solution:** Try different ports:
```bash
# Frontend on port 5000 instead
python -m http.server 5000
# Then open: http://localhost:5000
```

### ❌ "Module not found" or import error

**Solution:** Make sure virtual environment is activated:
```bash
venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate   # Mac/Linux
```

See `SETUP_GUIDE.md` for more troubleshooting.

---

## 📊 What Happens Inside

```
1. You Type a Question
   ↓
2. Frontend sends to Backend
   ↓
3. Backend searches for relevant passages (FAISS)
   ↓
4. Backend sends passages to Ollama (LLM)
   ↓
5. Ollama/Mistral generates answer
   ↓
6. Backend returns answer + sources
   ↓
7. Frontend displays beautifully
   ↓
8. You read the wisdom! 🙏
```

---

## ⏱️ Time Estimates

| Step | Time |
|------|------|
| 1. Install Ollama | 2 minutes |
| 2. Download Model | 5 minutes |
| 3. Python Setup | 3 minutes |
| 4. Backend Start | 1 minute |
| 5. Frontend Start | 1 minute |
| 6. Open Browser | 30 seconds |
| **TOTAL** | **~12 minutes** |

Then each question takes 10-15 seconds for answer.

---

## 🎓 Understanding the Setup

### Why Multiple Terminals?

- **Terminal 1 (Backend):** Handles your questions
  - Port 8000
  - Receives questions from browser
  - Sends questions to Ollama
  - Returns answers
  - **DON'T CLOSE THIS**

- **Terminal 2 (Frontend):** Serves web page
  - Port 3000
  - Shows the beautiful interface
  - Sends requests to backend
  - **DON'T CLOSE THIS**

- **Ollama (Background):** AI Brain
  - Port 11434
  - Generates answers
  - Runs in background
  - Usually auto-starts

### Why Keep Them Open?

Once you close a terminal:
- That service stops
- Your application stops working
- You'll see "Connection refused" errors

---

## 🔄 Restarting (If Something Goes Wrong)

1. Close all terminals
2. Close browser
3. Make sure Ollama is running
4. Start backend again (Step 4)
5. Start frontend again (Step 5)
6. Refresh browser (F5)

---

## ✅ Success Checklist

- [ ] Ollama installed
- [ ] Model downloaded (`ollama list` shows it)
- [ ] Python virtual environment created
- [ ] Virtual environment activated (shows `(venv)`)
- [ ] Dependencies installed
- [ ] Backend running (see "Uvicorn running")
- [ ] Frontend running (see "Serving HTTP")
- [ ] Browser shows beautiful interface
- [ ] Questions get answers!

---

## 🎉 You're All Set!

Now you have a complete Bhagavad Gita AI Assistant running on your computer!

### Next Steps:

1. **Explore** - Ask different questions
2. **Try Models** - `ollama pull llama2` and switch
3. **Customize** - Edit prompts in code
4. **Share** - Show friends your creation
5. **Learn** - Read documentation files

---

## 📚 Need More Help?

| Question | Answer |
|----------|--------|
| How do I stop the servers? | Press `Ctrl + C` in each terminal |
| How do I use different models? | `ollama pull llama2` then `set LLM_MODEL=llama2` |
| Can I change settings? | Yes, edit files in `backend/` |
| Is my data safe? | Yes, everything runs locally |
| Can I share this? | Yes, it's open source |

---

## 🙏 Final Notes

- Everything runs on YOUR computer
- No data sent to internet
- No API keys needed
- Completely private
- Completely free

**Enjoy the wisdom of the Bhagavad Gita!** ✨

---

## 📞 Quick Reference

```bash
# Activate environment
venv\Scripts\Activate.ps1

# Start backend (Terminal 1)
cd backend && python main.py

# Start frontend (Terminal 2)
cd frontend && python -m http.server 3000

# Open in browser
http://localhost:3000

# Stop either service
Ctrl + C
```

---

**You're ready to go! 🚀**

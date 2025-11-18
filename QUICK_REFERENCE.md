# GitaRAG - Quick Reference Card

## 🚀 One-Minute Setup

```powershell
# 1. Configure Google Gemini API key
setx GEMINI_API_KEY "<YOUR_GEMINI_API_KEY>"
# Restart your shell after setting the env var

# 2. Setup Python (one time)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. Run backend
cd backend
python main.py

# 4. Run frontend (new terminal)
cd frontend
python -m http.server 3000

# 5. Open browser
# http://localhost:3000
```

---

## 📚 Documentation Map

| What? | Where? |
|-------|--------|
| **Getting Started** | `README.md` |
| **Installation Help** | `SETUP_GUIDE.md` |
| **API Reference** | `API_DOCUMENTATION.md` |
| **Code Examples** | `API_EXAMPLES.md` |
| **System Design** | `ARCHITECTURE.md` |
| **Technical Details** | `IMPLEMENTATION_SUMMARY.md` |
| **Project Status** | `STATUS.md` |

---

## 🔌 API Endpoints

```
GET  http://localhost:8000/health
GET  http://localhost:8000/llm/status
GET  http://localhost:8000/llm/models
POST http://localhost:8000/llm/test
POST http://localhost:8000/build_index
POST http://localhost:8000/search
POST http://localhost:8000/query
```

---

## 🎯 Quick API Calls

### Health Check
```bash
curl http://localhost:8000/health
```

### Search
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"question":"What is yoga?","top_k":3}'
```

### Get Answer
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Explain dharma","top_k":3}'
```

---

## 🐍 Python Usage

```python
import requests

# Query the API
response = requests.post('http://localhost:8000/query', json={
    "question": "What is the meaning of yoga?",
    "top_k": 3,
    "temperature": 0.7,
    "max_tokens": 512
})

# Get result
data = response.json()
print(f"Question: {data['question']}")
print(f"Answer: {data['answer']}")
print(f"Sources: {len(data['retrieved'])} passages")
```

---

## 🔧 Configuration

### Change Model / Provider
This project uses Google Gemini via `gemini_llm.py`. To change which model is used, update the model name inside `backend/gemini_llm.py` or add environment-based configuration. Use `/llm/models` to see the models available to your API key.

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| LLM not available | Ensure `GEMINI_API_KEY` is set and valid; check `/llm/status` |
| Slow responses | Reduce `max_tokens` to 256 |
| Connection refused | Check backend is running |
| API not responding | Check network connectivity and API key permissions |

See `SETUP_GUIDE.md` for detailed troubleshooting.

---

## 📊 Performance

| Operation | Time |
|-----------|------|
| Search | <1 second |
| Generate | 5-15 seconds |
| Full Query | 6-16 seconds |
| Build Index | 2-5 minutes |

---

## 📁 Key Files

```
backend/main.py           - FastAPI server
backend/local_llm.py      - LLM client
backend/rag_engine.py     - RAG engine

frontend/index.html       - Web interface
frontend/app.js          - JavaScript logic
frontend/styles.css      - Beautiful design

requirements.txt         - Dependencies
start_backend.bat        - Backend launcher
start_frontend.bat       - Frontend launcher
```

---

## ✨ Features

- ✅ Semantic search
- ✅ AI answer generation
- ✅ Multiple LLM support
- ✅ Beautiful UI
- ✅ Mobile responsive
- ✅ Local & private
- ✅ Production ready

---

## 🎯 Example Questions

- "What is karma?"
- "Explain dharma"
- "What is yoga?"
- "Who is Arjuna?"
- "What is enlightenment?"
- "What does Krishna teach about duty?"
- "Explain the nature of the soul"

---

## 📞 Quick Help

**Issue?** Check `SETUP_GUIDE.md`  
**API Question?** Check `API_DOCUMENTATION.md`  
**Code Example?** Check `API_EXAMPLES.md`  
**System Design?** Check `ARCHITECTURE.md`  

---

## ✅ Checklist

- [ ] `GEMINI_API_KEY` set
- [ ] Python venv created
- [ ] Dependencies installed
- [ ] Python venv created
- [ ] Dependencies installed
- [ ] Backend running (`python main.py`)
- [ ] Frontend running (`python -m http.server 3000`)
- [ ] Browser open (`http://localhost:3000`)

---

## 🎉 You're All Set!

Everything is ready to use. Just follow the Quick Setup above!

**Happy exploring the Bhagavad Gita! 🙏✨**

---

## 📚 More Information

- Full Setup → `SETUP_GUIDE.md`
- API Details → `API_DOCUMENTATION.md`
- Code Examples → `API_EXAMPLES.md`
- Architecture → `ARCHITECTURE.md`

---

**Version:** 1.0.0  
**Status:** Ready to Use ✅  
**Date:** November 17, 2025

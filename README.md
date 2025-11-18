# 🙏 GitaRAG - Bhagavad Gita AI Assistant

> Explore the wisdom of the Bhagavad Gita with AI-powered Q&A

## Overview

GitaRAG is a modern, intelligent question-answering system for the Bhagavad Gita that combines:

- **RAG (Retrieval-Augmented Generation)**: Semantic search to find relevant passages
- **LLM Integration**: Uses Google Gemini via the `GEMINI_API_KEY` and the `google-generativeai` SDK
- **Beautiful Web UI**: Modern, responsive interface with smooth animations
- **Zero Privacy Concerns**: Everything runs locally on your machine

## ✨ Key Features

✅ **Semantic Search** - Find relevant Gita passages using AI embeddings  
✅ **AI-Powered Answers** - Get thoughtful, context-aware responses  
✅ **Multiple LLM Support** - Works with Mistral, Llama2, Neural-Chat, and more  
✅ **Beautiful UI** - Modern design with gradient animations  
✅ **Fast & Responsive** - Optimized for quick responses  
✅ **Privacy-First** - Runs completely locally, no data sent anywhere  
✅ **Open Source** - Free to use and modify  

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- Google Gemini API access and `GEMINI_API_KEY` environment variable
- 4GB RAM minimum

### Installation

1. **Set your Google Gemini API key**
```powershell
setx GEMINI_API_KEY "<YOUR_GEMINI_API_KEY>"
# Restart your shell after setting the env var
```
2. **Install Python dependencies**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. **Setup Python environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **Run backend**
```bash
cd backend
python main.py
```

4. **Run frontend (new terminal)**
```bash
cd frontend
python -m http.server 3000
```

5. **Open browser**
```
http://localhost:3000
```

## 📚 Usage Examples

### Web Interface
Open `http://localhost:3000` and ask questions about the Bhagavad Gita

### API (curl)
```bash
# Get AI answer
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does Krishna teach about duty?",
    "top_k": 3
  }'
```

### Python
```python
import requests

response = requests.post('http://localhost:8000/query', json={
    "question": "Explain the concept of dharma",
    "top_k": 3
})

print(response.json()['answer'])
```

## 📖 Documentation

- **`HOW_TO_USE.md`** ⭐ **START HERE** - Clear step-by-step guide
- **`WINDOWS_QUICK_START.bat`** - Interactive Windows guide
- **`QUICK_REFERENCE.md`** - Quick API reference
- **`SETUP_GUIDE.md`** - Detailed installation
- **`API_DOCUMENTATION.md`** - Complete API reference
- **`API_EXAMPLES.md`** - Code examples
- **`ARCHITECTURE.md`** - System design
- **`IMPLEMENTATION_SUMMARY.md`** - Technical details

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS) 
    ↓ REST API
FastAPI Backend
    ↓
RAG Engine (FAISS + Embeddings)
    ↓
Local LLM (Ollama: Mistral, Llama2, etc.)
```

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check service status |
| `/llm/status` | GET | Check LLM connection |
| `/llm/models` | GET | List available models |
| `/build_index` | POST | Build search index |
| `/search` | POST | Search passages |
| `/query` | POST | Get AI answer |

## ⚙️ Configuration

### Change LLM / Model
This project now uses Google Gemini models via the `google-generativeai` SDK. To change the model used by the backend, set the model name in `backend/gemini_llm.py` or via the environment variable used by your deployment (if you add such support). The `gemini_llm.py` includes fallback logic and will list available models for your account.

## 🚨 Troubleshooting

### LLM Service Not Available
If the backend reports the LLM is not available, verify:
- You have set the `GEMINI_API_KEY` environment variable and restarted your shell.
- Your machine has internet access to reach Google's Generative Language API.
- The key is valid and has access to the requested models.

Use the `/llm/status` and `/llm/models` endpoints to debug available models and connection status.

### Slow Responses
- Use faster model: `neural-chat`
- Reduce `max_tokens` to 256
- Reduce `top_k` to 2

See `SETUP_GUIDE.md` for detailed troubleshooting.

## 📊 Performance

| Operation | Time |
|-----------|------|
| Search | 500ms - 1s |
| Generate Answer | 5-15s |
| Index Build | 2-5 min |

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI server
│   ├── local_llm.py        # LLM client
│   ├── rag_engine.py       # RAG engine
│   ├── app/
│   │   ├── llm.py
│   │   ├── rag.py
│   │   └── utils.py
│   └── data/corpus/
│       └── geetha_verses.txt
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── requirements.txt
```

## 💡 Example Questions

- "What is the meaning of yoga?"
- "Explain the concept of dharma"
- "What does Krishna teach about duty?"
- "What is the path to liberation?"
- "Explain the nature of the soul"

## 🎯 Use Cases

- **Educational** - Study and understand Gita concepts
- **Research** - Find relevant passages quickly
- **Spiritual** - Get guidance and wisdom
- **Content** - Create articles and materials

## 🔧 Dependencies

- FastAPI 0.121.2
- sentence-transformers 2.2.2
- faiss-cpu 1.7.3
- torch 2.0.1
- transformers 4.57.1
- requests 2.32.5

## 📞 Support

1. Check `SETUP_GUIDE.md` for setup issues
2. Review `API_DOCUMENTATION.md` for API questions
3. See `API_EXAMPLES.md` for code examples
4. Check error logs in backend terminal

## 🙏 Acknowledgments

- Bhagavad Gita - Ancient sacred text
-- Google Gemini (Generative Language API)
- FastAPI - Modern Python web framework
- Sentence Transformers - Semantic embeddings
- FAISS - Efficient vector search

---

**Happy exploring! 🙏✨**

Start by running the backend and frontend, then open http://localhost:3000
   pip install -r requirements.txt
   ```
3. Start the backend
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   Backend will run at http://127.0.0.1:8000

4. Serve the frontend (simple option)
   ```bash
   cd frontend
   python -m http.server 3000
   ```
   Open http://127.0.0.1:3000 in your browser.

## Notes and customization
- For better quality generative answers, install and configure a local LLM like `llama-cpp-python` with a local GGML model, or use a larger transformers model.
- Expand `backend/data/corpus/geetha_verses.txt` with the full text divided by lines or separators. Then call the `/build_index` endpoint.
- File `backend/app/llm.py` contains a fallback generator that uses `transformers` if `llama_cpp` is not available.
- This project is a demo and not production hardened. For production: add auth, rate limits, caching, and model management.

## Endpoints
- `GET /health` - health check
- `POST /build_index` - build the FAISS index from the corpus file (reads `backend/data/corpus/geetha_verses.txt`)
- `POST /query` - JSON `{ "question": "your question", "top_k": 3 }` returns retrieved contexts and a generated answer

---
Enjoy building! If you want the full zip with additional features (Next.js frontend, Dockerfile, full corpus), tell me and I'll add them.

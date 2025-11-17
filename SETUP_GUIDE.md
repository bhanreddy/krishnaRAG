# GitaRAG - Setup and Installation Guide

## Overview

GitaRAG is an AI-powered Q&A system for the Bhagavad Gita that combines:
- **RAG (Retrieval-Augmented Generation)**: Uses semantic search to find relevant passages
- **Local LLM Integration**: Uses Ollama or other local LLM services for intelligent answers
- **Modern UI**: Beautiful, responsive web interface

## Architecture

```
Frontend (React/Vanilla JS)
    ↓
FastAPI Backend
    ↓
RAG Engine (FAISS + Embeddings)
    ↓
Local LLM Service (Ollama/LM Studio/etc)
```

## Prerequisites

- **Python 3.8+**
- **Node.js** (for frontend development - optional)
- **Ollama or other local LLM service**
- **At least 4GB RAM** for embeddings model
- **Internet connection** (first run to download models)

## Installation Steps

### 1. Install Ollama (Local LLM Service)

#### Windows
1. Download from: https://ollama.ai/download
2. Run the installer
3. Start Ollama: It will run in background automatically

#### macOS
```bash
brew install ollama
```

#### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

### 2. Pull a Model in Ollama

Open terminal/PowerShell and run:

```bash
# Pull Mistral (Recommended - balanced, fast)
ollama pull mistral

# Or pull another model:
ollama pull llama2
ollama pull neural-chat
ollama pull dolphin-mixtral
```

Check if running:
```bash
curl http://localhost:11434/api/tags
```

### 3. Setup Python Environment

#### Option A: Using venv (Recommended)
```bash
cd "c:\Users\reddy\Desktop\Capestone Project"

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using Conda
```bash
conda create -n gitagrag python=3.10
conda activate gitagrag
pip install -r requirements.txt
```

### 4. Prepare Data

Ensure the corpus file exists:
```
backend/data/corpus/geetha_verses.txt
```

The file should contain Bhagavad Gita verses separated by blank lines.

### 5. Run the Backend

```bash
# From project root
cd backend

# Start server (with virtual env activated)
python main.py
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
GitaRAG Backend Starting
================================================
✓ LLM Service Connected: mistral at http://localhost:11434
  Available models: mistral, llama2, neural-chat
================================================
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6. Run the Frontend

In a new terminal:

```bash
cd frontend
# Serve with Python (simple)
python -m http.server 3000

# Or use Node.js
npx http-server -p 3000

# Or open directly in browser
# file:///c:/Users/reddy/Desktop/Capestone Project/frontend/index.html
```

Access at: `http://localhost:3000`

## API Endpoints

### Health Check
```
GET /health
```

### List Available Models
```
GET /llm/models
```

### Build Index (Creates FAISS index from corpus)
```
POST /build_index
Response: {
  "status": "index_built",
  "documents_indexed": 700,
  "message": "Successfully indexed 700 passages..."
}
```

### Search Only (Without Generation)
```
POST /search
Request: {
  "question": "What is dharma?",
  "top_k": 3
}
Response: {
  "question": "What is dharma?",
  "retrieved": [...],
  "passage_count": 3
}
```

### Full RAG Query (Search + Generate)
```
POST /query
Request: {
  "question": "What is the meaning of yoga?",
  "top_k": 3,
  "temperature": 0.7,
  "max_tokens": 512
}
Response: {
  "question": "What is the meaning of yoga?",
  "answer": "According to the Bhagavad Gita...",
  "retrieved": ["Passage 1", "Passage 2", "Passage 3"],
  "passage_count": 3
}
```

### LLM Status
```
GET /llm/status
Response: {
  "llm_available": true,
  "llm_api_url": "http://localhost:11434",
  "llm_model": "mistral",
  "available_models": ["mistral", "llama2"],
  "rag_engine_ready": true
}
```

### Test LLM
```
POST /llm/test
Response: {
  "success": true,
  "prompt": "What is the Bhagavad Gita?",
  "response": "The Bhagavad Gita is...",
  "model": "mistral"
}
```

## Configuration

### Environment Variables

Create a `.env` file in backend directory:

```env
# LLM Configuration
LLM_MODEL=mistral
LLM_API_URL=http://localhost:11434

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Model Configuration
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
```

### Changing LLM Model

Edit `main.py` or set environment variable:
```bash
set LLM_MODEL=llama2
python main.py
```

## Troubleshooting

### Error: "LLM service not available"

1. **Check if Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```
   Should return JSON with available models.

2. **Start Ollama:**
   ```bash
   ollama serve
   ```

3. **Change API URL:**
   ```python
   # In main.py, change:
   llm_api_url='http://your-server:11434'
   ```

### Error: "Model not found"

1. **List installed models:**
   ```bash
   ollama list
   ```

2. **Pull model:**
   ```bash
   ollama pull mistral
   ```

### Error: "FAISS index error"

1. **Delete existing index:**
   ```bash
   rm -r backend/data/faiss_index.faiss
   ```

2. **Rebuild index:**
   ```bash
   curl -X POST http://localhost:8000/build_index
   ```

### Slow Responses

1. **Reduce top_k:** Try with fewer passages
2. **Reduce max_tokens:** Generate shorter answers
3. **Use faster model:** Try `neural-chat` or `dolphin-mixtral`
4. **Add GPU support:** Configure CUDA with torch

## Performance Tips

1. **Use GPU acceleration:**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Use smaller embedding model:**
   ```python
   embeddings_model='all-MiniLM-L6-v2'  # Already optimal
   ```

3. **Use faster LLM model:**
   ```bash
   ollama pull neural-chat  # Faster than mistral
   ```

4. **Batch queries:** Process multiple queries together

## File Structure

```
Capestone Project/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── local_llm.py           # LLM client integration
│   ├── rag_engine.py          # Enhanced RAG engine
│   ├── app/
│   │   ├── llm.py            # LLM wrapper for app
│   │   ├── rag.py            # RAG wrapper for app
│   │   └── utils.py          # Utilities
│   └── data/
│       └── corpus/
│           └── geetha_verses.txt
├── frontend/
│   ├── index.html            # Main page
│   ├── app.js               # Frontend logic
│   ├── styles.css           # Modern UI
│   ├── components/
│   └── pages/
├── requirements.txt          # Python dependencies
└── SETUP_GUIDE.md           # This file
```

## Next Steps

1. **Build the index:** `POST /build_index`
2. **Try a query:** Use frontend or `curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question":"What is karma?"}'`
3. **Experiment with different models:** Try llama2, neural-chat, etc.
4. **Add your own corpus:** Replace geetha_verses.txt with different content

## Additional Resources

- **Ollama**: https://ollama.ai/
- **Mistral Model**: https://huggingface.co/mistralai/Mistral-7B
- **FastAPI**: https://fastapi.tiangolo.com/
- **FAISS**: https://github.com/facebookresearch/faiss
- **Sentence Transformers**: https://huggingface.co/sentence-transformers

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify Ollama is running
3. Check logs for error messages
4. Ensure all dependencies are installed

Happy exploring! 🙏✨

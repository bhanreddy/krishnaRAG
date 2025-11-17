# GitaRAG API Documentation

## Base URL
```
http://localhost:8000
```

## Overview

GitaRAG provides RESTful endpoints for:
- **Index Management**: Build and manage FAISS index
- **Search & Retrieval**: Find relevant Bhagavad Gita passages
- **RAG Queries**: Get AI-generated answers with context
- **LLM Management**: Check and test LLM service
- **System Status**: Monitor service health

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

Check if the API is running and services are available.

**Response:**
```json
{
  "status": "ok",
  "service": "GitaRAG",
  "rag_engine_ready": true
}
```

**cURL:**
```bash
curl http://localhost:8000/health
```

---

### 2. Build Index

**Endpoint:** `POST /build_index`

Create FAISS semantic search index from the Bhagavad Gita corpus.

**Request:** None

**Response:**
```json
{
  "status": "index_built",
  "documents_indexed": 700,
  "message": "Successfully indexed 700 passages from Bhagavad Gita"
}
```

**Time Required:** ~2-5 minutes (first time)

**cURL:**
```bash
curl -X POST http://localhost:8000/build_index
```

**Python:**
```python
import requests
response = requests.post('http://localhost:8000/build_index')
print(response.json())
```

---

### 3. Search Passages

**Endpoint:** `POST /search`

Search for relevant passages without generating answers.

**Request Body:**
```json
{
  "question": "What is dharma?",
  "top_k": 3
}
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| question | string | required | Search query |
| top_k | integer | 3 | Number of results |

**Response:**
```json
{
  "question": "What is dharma?",
  "retrieved": [
    "Verse 1 content...",
    "Verse 2 content...",
    "Verse 3 content..."
  ],
  "passage_count": 3
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is dharma?",
    "top_k": 3
  }'
```

**Python:**
```python
import requests

response = requests.post(
    'http://localhost:8000/search',
    json={
        "question": "What is dharma?",
        "top_k": 3
    }
)
print(response.json())
```

---

### 4. Full RAG Query

**Endpoint:** `POST /query`

Complete RAG pipeline: retrieve passages + generate answer with AI.

**Request Body:**
```json
{
  "question": "What is the meaning of yoga according to the Gita?",
  "top_k": 3,
  "temperature": 0.7,
  "max_tokens": 512
}
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| question | string | required | Your question |
| top_k | integer | 3 | Passages to retrieve |
| temperature | float | 0.7 | LLM randomness (0.0-1.0) |
| max_tokens | integer | 512 | Max response length |

**Response:**
```json
{
  "question": "What is the meaning of yoga?",
  "answer": "According to the Bhagavad Gita, yoga is the union of individual consciousness with universal consciousness...",
  "retrieved": [
    "Chapter 6, Verse 1: Performing prescribed duties...",
    "Chapter 2, Verse 48: Yoga is the equilibrium...",
    "Chapter 6, Verse 23: That which is called yoga..."
  ],
  "passage_count": 3
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the meaning of yoga?",
    "top_k": 3,
    "temperature": 0.7,
    "max_tokens": 512
  }'
```

**Python:**
```python
import requests

response = requests.post(
    'http://localhost:8000/query',
    json={
        "question": "What is the meaning of yoga?",
        "top_k": 5,
        "temperature": 0.5,
        "max_tokens": 256
    }
)

data = response.json()
print(f"Question: {data['question']}")
print(f"Answer: {data['answer']}")
print(f"Passages: {len(data['retrieved'])}")
```

---

### 5. LLM Status

**Endpoint:** `GET /llm/status`

Check LLM service availability and status.

**Response:**
```json
{
  "llm_available": true,
  "llm_api_url": "http://localhost:11434",
  "llm_model": "mistral",
  "available_models": [
    "mistral",
    "llama2",
    "neural-chat"
  ],
  "rag_engine_ready": true
}
```

**cURL:**
```bash
curl http://localhost:8000/llm/status
```

---

### 6. Test LLM

**Endpoint:** `POST /llm/test`

Test LLM with a sample prompt.

**Response:**
```json
{
  "success": true,
  "prompt": "What is the Bhagavad Gita? Answer in one sentence.",
  "response": "The Bhagavad Gita is an ancient Hindu scripture that contains dialogue between Lord Krishna and the warrior Arjuna...",
  "model": "mistral"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8000/llm/test
```

**Python:**
```python
import requests

response = requests.post('http://localhost:8000/llm/test')
print(response.json())
```

---

### 7. List Models

**Endpoint:** `GET /llm/models`

List all available LLM models.

**Response:**
```json
{
  "available": true,
  "models": [
    "mistral:latest",
    "llama2:latest",
    "neural-chat:latest",
    "dolphin-mixtral:latest"
  ],
  "api_url": "http://localhost:11434"
}
```

**cURL:**
```bash
curl http://localhost:8000/llm/models
```

---

## Error Handling

### Error Responses

**4xx Client Errors:**
```json
{
  "detail": "Question cannot be empty"
}
```

**5xx Server Errors:**
```json
{
  "detail": "RAG Engine not initialized"
}
```

### Common Errors

| Status | Error | Solution |
|--------|-------|----------|
| 400 | "Question cannot be empty" | Provide a non-empty question |
| 500 | "RAG Engine not initialized" | Backend not started properly |
| 500 | "LLM service not available" | Start Ollama: `ollama serve` |
| 500 | "Index build failed" | Check corpus file exists |

---

## Request Examples

### Example 1: Simple Search

```bash
# Find passages about karma
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is karma?",
    "top_k": 2
  }'
```

### Example 2: Get AI Answer

```bash
# Get AI analysis of dharma
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain the concept of dharma in the Gita",
    "top_k": 5,
    "temperature": 0.5,
    "max_tokens": 1024
  }'
```

### Example 3: Python Integration

```python
import requests

API_URL = "http://localhost:8000"

# Check health
health = requests.get(f"{API_URL}/health")
print("Status:", health.status_code)

# Build index
build_resp = requests.post(f"{API_URL}/build_index")
print("Index built:", build_resp.json())

# Query with AI
query = {
    "question": "What does Krishna teach about duty?",
    "top_k": 3,
    "temperature": 0.7,
    "max_tokens": 512
}

response = requests.post(f"{API_URL}/query", json=query)
result = response.json()

print(f"Question: {result['question']}")
print(f"Answer: {result['answer']}")
print(f"Sources: {len(result['retrieved'])} passages")
```

### Example 4: JavaScript Frontend

```javascript
const API_URL = 'http://localhost:8000';

async function askQuestion(question) {
  try {
    const response = await fetch(`${API_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question: question,
        top_k: 3,
        temperature: 0.7,
        max_tokens: 512
      })
    });

    if (!response.ok) {
      throw new Error('Query failed');
    }

    const data = await response.json();
    console.log('Answer:', data.answer);
    console.log('Sources:', data.retrieved);
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}

// Usage
askQuestion("What is the path to liberation?");
```

---

## Performance Considerations

### Response Times (Approximate)

| Operation | Time |
|-----------|------|
| Health check | <10ms |
| Search (3 passages) | 500-1000ms |
| Query with AI (512 tokens) | 5-15 seconds |
| Build index (first time) | 2-5 minutes |

### Optimization Tips

1. **Reduce max_tokens** for faster responses
2. **Reduce top_k** for faster retrieval
3. **Use faster model**: `neural-chat` instead of `mistral`
4. **Enable GPU** for LLM inference

---

## Configuration

### Environment Variables

Set these in `.env` file or as system variables:

```env
# LLM Configuration
LLM_MODEL=mistral
LLM_API_URL=http://localhost:11434

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### Change LLM Model

To use a different model:

```bash
# Pull model
ollama pull llama2

# Set environment variable
set LLM_MODEL=llama2

# Restart backend
python backend/main.py
```

---

## Advanced Features

### Chat Mode (Future)

```python
# Coming soon: Full chat history with context
POST /chat
{
  "messages": [
    {"role": "user", "content": "What is moksha?"},
    {"role": "assistant", "content": "..."}
  ],
  "top_k": 3
}
```

### Batch Queries

```python
# Process multiple questions efficiently
queries = [
  "What is karma?",
  "Explain dharma",
  "What is yoga?"
]

for q in queries:
  response = requests.post(f"{API_URL}/query", 
    json={"question": q})
```

---

## API Reference Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Check API status |
| GET | `/llm/status` | Check LLM service |
| GET | `/llm/models` | List available models |
| POST | `/llm/test` | Test LLM connection |
| POST | `/build_index` | Build search index |
| POST | `/search` | Search passages |
| POST | `/query` | Full RAG query |

---

## Support & Troubleshooting

For detailed troubleshooting, see `SETUP_GUIDE.md`

Common issues:
- **LLM not available**: Check Ollama is running
- **Slow responses**: Reduce max_tokens or use faster model
- **Index errors**: Rebuild index with `/build_index`

Happy querying! 🙏✨

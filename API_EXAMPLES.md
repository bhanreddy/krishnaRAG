# GitaRAG - API Usage Examples

## Quick Reference

### cURL Examples

#### 1. Check Service Health
```bash
curl http://localhost:8000/health
```

#### 2. Check LLM Status
```bash
curl http://localhost:8000/llm/status
```

#### 3. Build Index (do this first!)
```bash
curl -X POST http://localhost:8000/build_index
```

#### 4. Search for Passages
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is karma?",
    "top_k": 3
  }'
```

#### 5. Get AI Answer (Full RAG)
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does Krishna teach about duty?",
    "top_k": 3,
    "temperature": 0.7,
    "max_tokens": 512
  }'
```

---

## Python Examples

### Basic Setup
```python
import requests
import json

API_BASE = "http://localhost:8000"

def print_response(response):
    print(json.dumps(response.json(), indent=2))
```

### 1. Health Check
```python
resp = requests.get(f"{API_BASE}/health")
print_response(resp)

# Output:
# {
#   "status": "ok",
#   "service": "GitaRAG",
#   "rag_engine_ready": true
# }
```

### 2. Check LLM Connection
```python
resp = requests.get(f"{API_BASE}/llm/status")
data = resp.json()

print(f"LLM Available: {data['llm_available']}")
print(f"Model: {data['llm_model']}")
print(f"API URL: {data['llm_api_url']}")
print(f"Available Models: {', '.join(data['available_models'])}")
```

### 3. Build Index
```python
print("Building index... This may take a few minutes...")
resp = requests.post(f"{API_BASE}/build_index")
data = resp.json()

print(f"Status: {data['status']}")
print(f"Documents indexed: {data['documents_indexed']}")
print(f"Message: {data['message']}")
```

### 4. Simple Search
```python
question = "What is the nature of the soul?"

resp = requests.post(f"{API_BASE}/search", json={
    "question": question,
    "top_k": 3
})

data = resp.json()
print(f"Question: {data['question']}")
print(f"Passages found: {data['passage_count']}\n")

for i, passage in enumerate(data['retrieved'], 1):
    print(f"Passage {i}:")
    print(passage[:200] + "...\n")
```

### 5. Full RAG Query
```python
question = "Explain the concept of yoga in the Gita"

resp = requests.post(f"{API_BASE}/query", json={
    "question": question,
    "top_k": 5,
    "temperature": 0.7,
    "max_tokens": 1024
})

data = resp.json()

print("=" * 60)
print(f"QUESTION: {data['question']}")
print("=" * 60)
print(f"\nAI ANSWER:\n{data['answer']}")
print(f"\nRETRIEVED {data['passage_count']} PASSAGES:")
print("-" * 60)

for i, passage in enumerate(data['retrieved'], 1):
    print(f"\n[Passage {i}]\n{passage}\n")
```

### 6. Test LLM
```python
resp = requests.post(f"{API_BASE}/llm/test")
data = resp.json()

print(f"Test successful: {data['success']}")
print(f"Model: {data['model']}")
print(f"Response: {data['response']}")
```

### 7. List Available Models
```python
resp = requests.get(f"{API_BASE}/llm/models")
data = resp.json()

print(f"Service available: {data['available']}")
print(f"API URL: {data['api_url']}")
print(f"Available models:")
for model in data['models']:
    print(f"  - {model}")
```

---

## JavaScript/Fetch Examples

### Basic Setup
```javascript
const API_BASE = 'http://localhost:8000';

async function apiCall(endpoint, method = 'GET', data = null) {
  const options = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
    }
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, options);
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return await response.json();
}
```

### 1. Health Check
```javascript
const health = await apiCall('/health');
console.log('Service status:', health.status);
```

### 2. Search Passages
```javascript
async function searchPassages(question) {
  const result = await apiCall('/search', 'POST', {
    question: question,
    top_k: 3
  });

  console.log(`Found ${result.passage_count} passages:`);
  result.retrieved.forEach((passage, i) => {
    console.log(`\n[${i + 1}] ${passage.substring(0, 100)}...`);
  });

  return result;
}

// Usage
await searchPassages("What is dharma?");
```

### 3. Get AI Answer
```javascript
async function getAnswer(question) {
  try {
    const result = await apiCall('/query', 'POST', {
      question: question,
      top_k: 5,
      temperature: 0.7,
      max_tokens: 512
    });

    console.log('Question:', result.question);
    console.log('Answer:', result.answer);
    console.log('Sources:', result.passage_count);

    return result;
  } catch (error) {
    console.error('Error getting answer:', error);
  }
}

// Usage
await getAnswer("What is the path to liberation?");
```

### 4. Build Index
```javascript
async function buildIndex() {
  console.log('Building index...');
  
  const result = await apiCall('/build_index', 'POST');
  
  console.log(`✓ Index built!`);
  console.log(`Documents indexed: ${result.documents_indexed}`);
  
  return result;
}

// Usage
await buildIndex();
```

### 5. Complete Workflow
```javascript
async function completeWorkflow() {
  try {
    // 1. Check health
    console.log('Checking service...');
    const health = await apiCall('/health');
    console.log('✓ Service is running');

    // 2. Check LLM
    console.log('Checking LLM...');
    const status = await apiCall('/llm/status');
    console.log(`✓ LLM available: ${status.llm_available}`);

    // 3. Build index if needed
    console.log('Building index...');
    const index = await apiCall('/build_index', 'POST');
    console.log(`✓ Index built with ${index.documents_indexed} documents`);

    // 4. Ask question
    const question = "What is the meaning of yoga?";
    console.log(`\nAsking: "${question}"`);
    
    const answer = await apiCall('/query', 'POST', {
      question: question,
      top_k: 3,
      temperature: 0.7,
      max_tokens: 512
    });

    console.log('\n=== RESULTS ===');
    console.log('Answer:', answer.answer);
    console.log('Sources:', answer.passage_count);

  } catch (error) {
    console.error('Error:', error);
  }
}

// Run workflow
completeWorkflow();
```

---

## Different Question Types

### Philosophy Questions
```python
questions = [
    "What is the nature of reality according to the Gita?",
    "Explain the concept of Brahman",
    "What does the Gita teach about the self?"
]

for q in questions:
    resp = requests.post(f"{API_BASE}/query", json={"question": q})
    data = resp.json()
    print(f"Q: {q}\nA: {data['answer']}\n")
```

### Action/Duty Questions
```python
questions = [
    "What does Krishna teach about duty (dharma)?",
    "How should one approach work according to the Gita?",
    "What is the difference between duty and desire?"
]

for q in questions:
    resp = requests.post(f"{API_BASE}/query", json={"question": q})
    print(resp.json()['answer'])
```

### Meditation/Practice Questions
```python
questions = [
    "What techniques does the Gita recommend for meditation?",
    "How does yoga lead to enlightenment?",
    "What is the path of devotion?"
]

for q in questions:
    resp = requests.post(f"{API_BASE}/query", json={"question": q})
    print(resp.json()['answer'])
```

### Character/Story Questions
```python
questions = [
    "Who was Arjuna and what was his dilemma?",
    "What was Krishna's role in the Gita?",
    "Explain the context of the Gita's teaching"
]

for q in questions:
    resp = requests.post(f"{API_BASE}/query", json={"question": q})
    print(resp.json()['answer'])
```

---

## Performance Testing

### Measure Response Time
```python
import time

def measure_query_time(question):
    start = time.time()
    resp = requests.post(f"{API_BASE}/query", json={"question": question})
    elapsed = time.time() - start
    
    print(f"Question: {question}")
    print(f"Response time: {elapsed:.2f}s")
    print(f"Status code: {resp.status_code}")
    return elapsed

# Test multiple questions
times = []
for q in ["What is karma?", "Explain dharma", "What is yoga?"]:
    t = measure_query_time(q)
    times.append(t)

print(f"\nAverage time: {sum(times)/len(times):.2f}s")
```

### Batch Processing
```python
import concurrent.futures

questions = [
    "What is karma?",
    "Explain dharma",
    "What is yoga?",
    "Who is Arjuna?",
    "What is enlightenment?"
]

def query_gita(question):
    resp = requests.post(f"{API_BASE}/query", 
                        json={"question": question})
    return resp.json()

# Process in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(query_gita, questions))

for result in results:
    print(f"Q: {result['question']}")
    print(f"A: {result['answer'][:100]}...\n")
```

---

## Error Handling

### Proper Error Handling in Python
```python
def safe_query(question):
    try:
        resp = requests.post(
            f"{API_BASE}/query",
            json={"question": question},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to backend")
        print("Is the backend running? (python main.py)")
    
    except requests.exceptions.Timeout:
        print("Error: Request timeout")
        print("The query is taking too long")
    
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e.response.status_code}")
        print(e.response.json().get('detail', 'Unknown error'))
    
    except Exception as e:
        print(f"Unexpected error: {e}")

# Usage
result = safe_query("What is yoga?")
if result:
    print(result['answer'])
```

### Error Handling in JavaScript
```javascript
async function safeQuery(question) {
  try {
    const response = await fetch(`${API_BASE}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question: question,
        top_k: 3
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API error');
    }

    const data = await response.json();
    return data;

  } catch (error) {
    if (error instanceof TypeError) {
      console.error('Connection error - is backend running?');
    } else {
      console.error('Error:', error.message);
    }
    return null;
  }
}

// Usage
const result = await safeQuery("What is dharma?");
if (result) {
  console.log(result.answer);
}
```

---

## Tips & Best Practices

### Do's ✅
- ✅ Check service health first
- ✅ Build index before querying
- ✅ Use reasonable timeouts
- ✅ Handle errors gracefully
- ✅ Limit concurrent requests
- ✅ Cache results when possible

### Don'ts ❌
- ❌ Don't send empty questions
- ❌ Don't use extremely high max_tokens (>2048)
- ❌ Don't send rapid requests without delay
- ❌ Don't ignore API errors
- ❌ Don't assume LLM is always available

---

## Debugging

### Check What's Running
```bash
# Check backend
curl http://localhost:8000/health

# Check LLM
curl http://localhost:8000/llm/status

# Check models
curl http://localhost:8000/llm/models
```

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now all requests will show detailed logs
resp = requests.post(f"{API_BASE}/query", ...)
```

### Inspect API Response
```python
resp = requests.post(f"{API_BASE}/query", json={...})

print(f"Status: {resp.status_code}")
print(f"Headers: {resp.headers}")
print(f"Body: {resp.text}")
```

---

Ready to integrate! 🚀

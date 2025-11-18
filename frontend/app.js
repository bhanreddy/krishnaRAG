const API = 'http://127.0.0.1:8000';
const API_TIMEOUT = 5000; // 5 second timeout

// Character counter
const questionInput = document.getElementById('question');
const charCount = document.getElementById('charCount');

questionInput.addEventListener('input', () => {
  charCount.textContent = questionInput.value.length;
});

// Ask button
document.getElementById('ask').addEventListener('click', async () => {
  const q = questionInput.value.trim();
  if (!q) {
    alert('Please enter a question');
    return;
  }

  const askBtn = document.getElementById('ask');
  const loading = document.getElementById('loading');
  const response = document.getElementById('response');

  // Show loading, hide response
  loading.classList.remove('hidden');
  response.classList.add('hidden');
  askBtn.disabled = true;

  try {
    // Add timeout to fetch
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

    const res = await fetch(API + '/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q, top_k: 3, temperature: 0.7, max_tokens: 512 }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!res.ok) {
      const t = await res.text();
      throw new Error(t);
    }

    const j = await res.json();
    
    // Display answer (now with "Krishna says:" prefix)
    const answer = j.answer || '(no answer)';
    document.getElementById('answer').textContent = answer;
    
    // Display response metadata with proper styling
    const metadata = document.getElementById('metadata');
    metadata.innerHTML = '';
    if (j.passage_count > 0) {
      metadata.className = 'metadata-info rag-retrieved';
      metadata.textContent = `Context: ${j.passage_count} passage(s) retrieved`;
    } else {
      metadata.className = 'metadata-info pretrained';
      metadata.textContent = 'Pretrained Answer (instant response)';
    }

    const retrieved = document.getElementById('retrieved');
    retrieved.innerHTML = '';

    const snippets = j.retrieved || [];
    document.getElementById('snippetCount').textContent = snippets.length;

    if (snippets.length > 0) {
      snippets.forEach((txt, i) => {
        const d = document.createElement('div');
        d.className = 'snippet';
        d.style.animationDelay = (i * 0.1) + 's';
        d.innerHTML = '<strong>Passage ' + (i + 1) + '</strong><pre>' + 
                      txt.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre>';
        retrieved.appendChild(d);
      });
    }

    loading.classList.add('hidden');
    response.classList.remove('hidden');
  } catch (error) {
    if (error.name === 'AbortError') {
      alert('Request timeout. Make sure the backend is running at ' + API);
    } else {
      alert('Error: ' + error.message + '\n\nMake sure backend is running: python backend/main.py');
    }
    loading.classList.add('hidden');
  } finally {
    askBtn.disabled = false;
  }
});

// Build Index button
document.getElementById('build').addEventListener('click', async () => {
  const buildBtn = document.getElementById('build');
  const loading = document.getElementById('loading');
  const response = document.getElementById('response');

  loading.classList.remove('hidden');
  response.classList.add('hidden');
  buildBtn.disabled = true;

  try {
    const res = await fetch(API + '/build_index', { method: 'POST' });
    if (!res.ok) {
      const t = await res.text();
      throw new Error(t);
    }
    const j = await res.json();
    alert('✅ Index built successfully!\nDocuments indexed: ' + (j.documents_indexed || 0));
    loading.classList.add('hidden');
  } catch (error) {
    alert('❌ Error: ' + error.message);
    loading.classList.add('hidden');
  } finally {
    buildBtn.disabled = false;
  }
});

// Copy button functionality
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('copy-btn')) {
    const answerText = document.getElementById('answer').textContent;
    navigator.clipboard.writeText(answerText).then(() => {
      e.target.textContent = '✓';
      setTimeout(() => {
        e.target.textContent = '📋';
      }, 2000);
    });
  }
});

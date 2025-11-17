const API = 'http://127.0.0.1:8000';

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
    const res = await fetch(API + '/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q, top_k: 3 })
    });

    if (!res.ok) {
      const t = await res.text();
      throw new Error(t);
    }

    const j = await res.json();
    document.getElementById('answer').textContent = j.answer || '(no answer)';

    const retrieved = document.getElementById('retrieved');
    retrieved.innerHTML = '';

    const snippets = j.retrieved || [];
    document.getElementById('snippetCount').textContent = snippets.length;

    snippets.forEach((txt, i) => {
      const d = document.createElement('div');
      d.className = 'snippet';
      d.style.animationDelay = (i * 0.1) + 's';
      d.innerHTML = '<strong>Passage ' + (i + 1) + '</strong><pre>' + 
                    txt.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</pre>';
      retrieved.appendChild(d);
    });

    loading.classList.add('hidden');
    response.classList.remove('hidden');
  } catch (error) {
    alert('Error: ' + error.message);
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

"""
Enhanced RAG Engine for Bhagavad Gita
Integrates with Google Gemini API for context-aware answers
"""
import os
import json
from typing import List, Dict, Optional, Tuple
import logging
from gemini_llm import get_gemini_client

logger = logging.getLogger(__name__)


class BhagavadGitaRAGEngine:
    """RAG Engine optimized for Bhagavad Gita Q&A"""
    
    # Bhagavad Gita specific system prompts
    GITA_SYSTEM_PROMPT = """You are a knowledgeable guide to the Bhagavad Gita, the sacred Hindu scripture. 
Your role is to:
1. Answer questions accurately using only the provided passages from the Gita
2. Explain concepts clearly and thoughtfully
3. Provide context about the teachings
4. If the answer isn't in the provided context, say "This specific answer isn't in the provided passages"
5. Be respectful and reverent of the spiritual nature of the text

Always ground your answers in the actual text provided."""

    GITA_QUERY_TEMPLATE = """Based on the following passages from the Bhagavad Gita, answer the question clearly and accurately.

Passages:
{context}

Question: {question}

Please provide a thoughtful answer based on the Gita teachings:"""

    def __init__(
        self,
        corpus_path: str = 'data/corpus/geetha_verses.txt',
        gemini_api_key: str = None,
        embeddings_model: str = 'all-MiniLM-L6-v2',
        use_gemini: bool = True
    ):
        """
        Initialize Bhagavad Gita RAG Engine with Gemini API
        
        Args:
            corpus_path: Path to Gita verses corpus
            gemini_api_key: Google Gemini API key
            embeddings_model: Model for generating embeddings
            use_gemini: Whether to use Gemini API
        """
        self.corpus_path = corpus_path
        self.gemini_api_key = gemini_api_key
        self.embeddings_model = embeddings_model
        self.use_gemini = use_gemini
        
        # Import here to avoid hard dependency
        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            self.SentenceTransformer = SentenceTransformer
            self.faiss = faiss
            self.embeddings_available = True
        except ImportError:
            logger.warning("sentence_transformers or faiss not available")
            self.embeddings_available = False
        
        # Initialize embeddings model
        if self.embeddings_available:
            self.embeddings = self.SentenceTransformer(embeddings_model)
        
        # Initialize Gemini client
        self.gemini_client = None
        if use_gemini:
            try:
                self.gemini_client = get_gemini_client(api_key=gemini_api_key)
                logger.info("Gemini client initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize Gemini client: {e}")
                self.gemini_client = None
        
        self.corpus: List[str] = []
        self.index = None
        self.id_to_text: Dict[int, str] = {}
        self.verses_metadata: Dict[int, Dict] = {}
    
    def load_corpus(self) -> int:
        """
        Load Bhagavad Gita corpus from file
        
        Returns:
            Number of verses/passages loaded
        """
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Corpus not found: {self.corpus_path}")
        
        with open(self.corpus_path, 'r', encoding='utf-8') as f:
            raw = f.read().strip()
        
        # Split by blank lines to get individual verses/passages
        passages = [p.strip() for p in raw.split('\n\n') if p.strip()]
        
        self.corpus = passages
        logger.info(f"Loaded {len(passages)} passages from Bhagavad Gita")
        
        return len(passages)
    
    def build_embeddings_index(self) -> int:
        """
        Build FAISS index for semantic search
        
        Returns:
            Number of verses indexed
        """
        if not self.embeddings_available:
            raise RuntimeError("sentence_transformers/faiss not available")
        
        if not self.corpus:
            self.load_corpus()
        
        logger.info(f"Building embeddings for {len(self.corpus)} passages...")
        
        # Generate embeddings
        embeddings = self.embeddings.encode(
            self.corpus,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # Create FAISS index
        dim = embeddings.shape[1]
        index = self.faiss.IndexFlatIP(dim)
        
        # Normalize for cosine similarity
        self.faiss.normalize_L2(embeddings)
        index.add(embeddings)
        
        self.index = index
        self.id_to_text = {i: text for i, text in enumerate(self.corpus)}
        
        logger.info(f"Index built with {len(self.corpus)} passages")
        
        return len(self.corpus)
    
    def search_passages(
        self,
        query: str,
        top_k: int = 3
    ) -> List[str]:
        """
        Search for relevant passages using semantic similarity
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant passages
        """
        if not self.embeddings_available:
            raise RuntimeError("Embeddings not available")
        
        if self.index is None:
            self.build_embeddings_index()
        
        # Encode query
        query_embedding = self.embeddings.encode(
            [query],
            convert_to_numpy=True
        )
        self.faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for idx in indices[0]:
            if idx >= 0 and idx in self.id_to_text:
                results.append(self.id_to_text[int(idx)])
        
        return results
    
    def generate_answer(
        self,
        query: str,
        retrieved_passages: List[str],
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> str:
        """
        Generate answer using Gemini API and retrieved context
        
        Args:
            query: User question
            retrieved_passages: Passages retrieved from corpus
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated answer
        """
        if not self.gemini_client or not self.gemini_client.is_available():
            return self._fallback_answer(retrieved_passages)
        
        # Build context from passages
        context = "\n\n---\n\n".join(retrieved_passages)
        
        # Create prompt
        prompt = self.GITA_QUERY_TEMPLATE.format(
            context=context,
            question=query
        )
        
        try:
            # Generate using Gemini API
            answer = self.gemini_client.generate(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return answer.strip()
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return self._fallback_answer(retrieved_passages)
    
    def _fallback_answer(self, passages: List[str]) -> str:
        """Fallback answer when LLM unavailable"""
        if not passages:
            return "Unable to find relevant passages and LLM service is unavailable."
        
        return f"""Unable to generate AI response. Here are relevant passages from the Bhagavad Gita:

{passages[0][:500]}"""
    
    def answer_question(
        self,
        question: str,
        top_k: int = 3,
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> Dict[str, any]:
        """
        Complete RAG pipeline: search + answer generation
        
        Args:
            question: User question
            top_k: Number of passages to retrieve
            max_tokens: Max tokens for answer
            temperature: Sampling temperature
            
        Returns:
            Dict with retrieved passages and generated answer
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        # Search for relevant passages
        retrieved = self.search_passages(question, top_k=top_k)
        
        # Generate answer
        answer = self.generate_answer(
            question,
            retrieved,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return {
            "question": question,
            "retrieved_passages": retrieved,
            "answer": answer,
            "passage_count": len(retrieved)
        }
    
    def chat_mode(
        self,
        messages: List[Dict[str, str]],
        top_k: int = 3,
        max_tokens: int = 512,
        temperature: float = 0.7
    ) -> str:
        """
        Chat mode with Gita context (if LLM supports chat)
        
        Args:
            messages: Chat history with 'role' and 'content'
            top_k: Passages to retrieve for context
            max_tokens: Max tokens for response
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        if not self.llm_client:
            raise RuntimeError("LLM client not available")
        
        # Extract last user message for context retrieval
        last_message = messages[-1]["content"] if messages else ""
        
        if last_message:
            # Add Gita context to system message
            messages_with_context = messages.copy()
            retrieved = self.search_passages(last_message, top_k=top_k)
            context = "\n\n".join(retrieved)
            
            system_msg = {
                "role": "system",
                "content": f"{self.GITA_SYSTEM_PROMPT}\n\nRelevant passages:\n{context}"
            }
            
            messages_with_context.insert(0, system_msg)
        else:
            messages_with_context = messages
        
        try:
            response = self.llm_client.chat(
                messages=messages_with_context,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response
        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise
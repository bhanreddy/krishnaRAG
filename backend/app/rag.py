"""
App RAG Module - FastAPI integration layer
Imports and wraps the enhanced RAG engine
"""
import sys
import os
from typing import List, Dict, Optional

# Add parent directory to path to import local_llm
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_engine import BhagavadGitaRAGEngine
import logging

logger = logging.getLogger(__name__)


class RAGEngine:
    """
    FastAPI-compatible RAG wrapper
    Provides backward compatibility while using enhanced engine
    """
    
    def __init__(
        self,
        corpus_path: str = 'data/corpus/geetha_verses.txt',
        model_name: str = 'all-MiniLM-L6-v2',
        index_path: str = 'data/faiss_index.faiss',
        gemini_api_key: str = None,
        use_gemini: bool = True
    ):
        """
        Initialize RAG Engine for app using Gemini API
        
        Args:
            corpus_path: Path to Gita corpus
            model_name: Embedding model name
            index_path: Path to save/load FAISS index
            gemini_api_key: Google Gemini API key
            use_gemini: Use Gemini API for generation
        """
        self.corpus_path = corpus_path
        self.model_name = model_name
        self.index_path = index_path
        
        # Initialize enhanced RAG engine with Gemini
        self.engine = BhagavadGitaRAGEngine(
            corpus_path=corpus_path,
            gemini_api_key=gemini_api_key,
            embeddings_model=model_name,
            use_gemini=use_gemini
        )
        
        # Try to load existing index
        self._load_index()
    
    def _load_index(self) -> bool:
        """Load existing FAISS index if available"""
        try:
            if os.path.exists(self.index_path):
                self.engine.load_corpus()
                # The index will be rebuilt if needed in search
                logger.info(f"Corpus loaded from {self.corpus_path}")
                return True
        except Exception as e:
            logger.warning(f"Could not load index: {e}")
        return False
    
    def build_index(self) -> int:
        """
        Build FAISS index from corpus
        
        Returns:
            Number of documents indexed
        """
        try:
            count = self.engine.build_embeddings_index()
            logger.info(f"Index built: {count} documents")
            return count
        except Exception as e:
            logger.error(f"Error building index: {e}")
            raise
    
    def search(self, question: str, top_k: int = 3) -> List[str]:
        """
        Search for relevant passages
        
        Args:
            question: Search query
            top_k: Number of results
            
        Returns:
            List of relevant passages
        """
        try:
            passages = self.engine.search_passages(question, top_k=top_k)
            return passages
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise
    
    def query(self, question: str, top_k: int = 3) -> Dict:
        """
        Full RAG query: search + generate
        
        Args:
            question: User question
            top_k: Number of passages to retrieve
            
        Returns:
            Dict with question, retrieved passages, and answer
        """
        try:
            result = self.engine.answer_question(
                question,
                top_k=top_k,
                max_tokens=512,
                temperature=0.7
            )
            return result
        except Exception as e:
            logger.error(f"Error in query: {e}")
            raise

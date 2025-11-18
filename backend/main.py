"""
GitaRAG - Bhagavad Gita RAG Demo Backend
Integrates RAG with local LLM for intelligent Q&A
"""
from fastapi import FastAPI, HTTPException

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import logging

from app.rag import RAGEngine
from app.llm import generate_answer, answer_bhagavad_gita_question, get_llm_status, is_greeting, add_krishna_says
from app.pretrained_qa import get_pretrained_answer
from gemini_llm import get_gemini_client, test_gemini_connection

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define lifespan handler before FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize on startup and handle shutdown"""
    logger.info("=" * 50)
    logger.info("GitaRAG Backend Starting with Gemini API")
    logger.info("=" * 50)
    
    # Check Gemini connection
    global engine
    try:
        client = get_gemini_client(api_key=GEMINI_API_KEY)
        if client.is_available():
            logger.info(f"✓ Gemini API Connected: {client.model_name}")
            logger.info(f"  Available models: {client.list_models()}")
        else:
            logger.warning("✗ Gemini API Connection Failed")
    except Exception as e:
        logger.warning(f"✗ Gemini API Error: {str(e)}")
        logger.warning("  Make sure Gemini API key is set and service is available")
    
    logger.info("=" * 50)
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("GitaRAG Backend Shutting Down")

# Initialize FastAPI
app = FastAPI(
    title="KrishnaRAG - Bhagavad Gita AI Assistant",
    description="AI-powered Q&A system for Bhagavad Gita using RAG + Local LLM",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup API Key
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyBT49gqX6QXI9QdPBusoGU76wq8YzCGKb8')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not set!")

# Get absolute paths
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.path.join(BACKEND_DIR, "data", "corpus", "geetha_verses.txt")
FAISS_INDEX_PATH = os.path.join(BACKEND_DIR, "data", "faiss_index.faiss")

logger.info(f"Using corpus path: {CORPUS_PATH}")
logger.info(f"Corpus exists: {os.path.exists(CORPUS_PATH)}")

# Initialize RAG Engine lazily (on first use) to avoid startup delays
engine = None
engine_initialized = False

def get_rag_engine():
    """Lazy initialization of RAG engine"""
    global engine, engine_initialized
    if not engine and not engine_initialized:
        try:
            logger.info("Initializing RAG Engine on first use...")
            engine = RAGEngine(
                corpus_path=CORPUS_PATH,
                index_path=FAISS_INDEX_PATH,
                gemini_api_key=GEMINI_API_KEY,
                use_gemini=True
            )
            engine_initialized = True
            logger.info("RAG Engine initialized successfully with Gemini API")
        except Exception as e:
            logger.warning(f"Failed to initialize RAG Engine: {e}")
            engine_initialized = True
    return engine


# Request/Response Models
class QueryRequest(BaseModel):
    question: str
    top_k: int = 3
    temperature: float = 0.7
    max_tokens: int = 512


class QueryResponse(BaseModel):
    question: str
    answer: str
    retrieved: List[str]
    passage_count: int


class BuildIndexResponse(BaseModel):
    status: str
    documents_indexed: int
    message: str


class LLMStatusResponse(BaseModel):
    llm_available: bool
    llm_api_url: str
    llm_model: str
    available_models: List[str]
    rag_engine_ready: bool


# Health Check Endpoint
@app.get('/health')
async def health():
    """Check API health and service status"""
    return {
        "status": "ok",
        "service": "GitaRAG",
        "rag_engine_ready": get_rag_engine() is not None
    }


# Build Index Endpoint
@app.post('/build_index', response_model=BuildIndexResponse)
async def build_index():
    """
    Build FAISS index from Bhagavad Gita corpus
    
    Returns:
        Build status and document count
    """
    rag_engine = get_rag_engine()
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")
    
    try:
        count = rag_engine.build_index()
        return BuildIndexResponse(
            status="index_built",
            documents_indexed=count,
            message=f"Successfully indexed {count} passages from Bhagavad Gita"
        )
    except Exception as e:
        logger.error(f"Error building index: {e}")
        raise HTTPException(status_code=500, detail=f"Index build failed: {str(e)}")


# Query Endpoint (Simple Retrieval)
@app.post('/search')
async def search(req: QueryRequest):
    """
    Search for relevant passages without generation
    
    Args:
        req: Query request with question and top_k
        
    Returns:
        List of relevant passages
    """
    rag_engine = get_rag_engine()
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")
    
    if not req.question or req.question.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        docs = rag_engine.search(req.question, top_k=req.top_k)
        return {
            "question": req.question,
            "retrieved": docs,
            "passage_count": len(docs)
        }
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Query Endpoint (Full RAG Pipeline)
@app.post('/query', response_model=QueryResponse)
async def query(req: QueryRequest):
    """
    Full RAG pipeline: retrieve relevant passages + generate answer with local LLM
    Falls back to predefined answers if LLM unavailable
    
    Args:
        req: Query request
        
    Returns:
        Question, retrieved passages, and AI-generated answer
    """
    if not req.question or req.question.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Check for greetings first
    is_greeting_query, greeting_response = is_greeting(req.question)
    if is_greeting_query:
        return QueryResponse(
            question=req.question,
            answer=greeting_response,
            retrieved=[],
            passage_count=0
        )
    
    # Check for pretrained answers from 50 human problems database (works without Gemini!)
    has_pretrained, pretrained_answer = get_pretrained_answer(req.question)
    if has_pretrained:
        return QueryResponse(
            question=req.question,
            answer=add_krishna_says(pretrained_answer),
            retrieved=[],
            passage_count=0
        )
    
    # If no predefined answer, try RAG + LLM
    rag_engine = get_rag_engine()
    if not rag_engine:
        return QueryResponse(
            question=req.question,
            answer="🙏 Krishna says: I apologize, but the RAG engine is not initialized. Please try asking about yoga, dharma, karma, moksha, or other Bhagavad Gita concepts which have predefined answers.",
            retrieved=[],
            passage_count=0
        )
    
    try:
        # Search for relevant passages
        docs = rag_engine.search(req.question, top_k=req.top_k)
        
        if not docs:
            return QueryResponse(
                question=req.question,
                answer="No relevant passages found in the Bhagavad Gita corpus for your question.",
                retrieved=[],
                passage_count=0
            )
        
        # Build context from retrieved passages
        context_text = "\n\n---\n\n".join(docs)
        
        # Generate answer using answer_bhagavad_gita_question which handles pretrained answers
        answer = answer_bhagavad_gita_question(
            question=req.question,
            retrieved_context=context_text,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            gemini_api_key=GEMINI_API_KEY
        )
        
        return QueryResponse(
            question=req.question,
            answer=answer,
            retrieved=docs,
            passage_count=len(docs)
        )
    
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


# LLM Status Endpoint
@app.get('/llm/status', response_model=LLMStatusResponse)
async def llm_status():
    """Check Gemini API status and availability"""
    try:
        client = get_gemini_client(api_key=GEMINI_API_KEY)
        is_available = client.is_available()
        
        return LLMStatusResponse(
            llm_available=is_available,
            llm_api_url="https://generativelanguage.googleapis.com/",
            llm_model="gemini-pro",
            available_models=client.list_models(),
            rag_engine_ready=engine is not None
        )
    except Exception as e:
        logger.error(f"Error checking Gemini status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# LLM Test Endpoint
@app.post('/llm/test')
async def test_llm():
    """Test Gemini with a sample prompt"""
    try:
        client = get_gemini_client(api_key=GEMINI_API_KEY)
        
        if not client.is_available():
            raise HTTPException(status_code=503, detail="Gemini API not available")
        
        test_prompt = "What is the Bhagavad Gita? Answer in one sentence."
        
        response = client.generate(
            prompt=test_prompt,
            max_tokens=100,
            temperature=0.7
        )
        
        return {
            "success": True,
            "prompt": test_prompt,
            "response": response,
            "model": client.model_name
        }
    except Exception as e:
        logger.error(f"LLM test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# List Models Endpoint
@app.get('/llm/models')
async def list_models():
    """List available Gemini models"""
    try:
        client = get_gemini_client(api_key=GEMINI_API_KEY)
        models = client.list_models()
        
        return {
            "available": client.is_available(),
            "models": models,
            "api_url": "https://generativelanguage.googleapis.com/",
            "provider": "Google Gemini"
        }
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

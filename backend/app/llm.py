"""
LLM Module - Generates answers using Google Gemini API with pretrained Q&A fallback
Integrates Gemini API with pretrained answers for common questions about human problems
"""
import logging
import re
from typing import Optional, Tuple, List

from gemini_llm import get_gemini_client
from app.pretrained_qa import get_pretrained_answer

logger = logging.getLogger(__name__)

# Reusable greeting patterns (fast responses without calling Gemini)
GREETINGS = {
    r"\b(hi|hello|hey|greetings|namaste|namaskar|pranaam)\b": "🙏 Namaste! Welcome to the Bhagavad Gita AI Assistant. How can I help you today?",
    r"\b(how are you|how are ya|how're you|how do you do|how you doing)\b": "🙏 I'm here and ready to help you explore the Bhagavad Gita.",
    r"\b(bye|goodbye|farewell|see you|take care)\b": "🙏 Farewell — may the wisdom of the Gita guide you.",
}


def is_greeting(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check if text is a greeting and return predefined response
    
    Args:
        text: User's input text
        
    Returns:
        Tuple of (is_greeting, response_text)
    """
    if not text:
        return False, None
    
    t = text.strip().lower()
    for pattern, resp in GREETINGS.items():
        if re.search(pattern, t, re.IGNORECASE):
            return True, resp
    return False, None


def add_krishna_says(answer: str) -> str:
    """
    Add 'Krishna says:' prefix to answer if not already present
    
    Args:
        answer: The answer text
        
    Returns:
        Answer with Krishna says prefix
    """
    if not answer:
        return answer
    
    # If already has Krishna says, return as is
    if answer.strip().startswith("🙏 Krishna says:") or answer.strip().startswith("Krishna says:"):
        return answer
    
    # Add Krishna says prefix
    return f"🙏 Krishna says:\n\n{answer}"


def generate_answer(
    prompt: str,
    context: str = "",
    max_tokens: int = 256,
    temperature: float = 0.7,
    gemini_api_key: Optional[str] = None,
) -> str:
    """
    Generic generator that uses the Gemini client.
    Returns generated text or a sensible fallback when Gemini is unavailable.
    
    Args:
        prompt: The prompt to send to Gemini
        context: Additional context (used for fallback)
        max_tokens: Maximum tokens in response
        temperature: Temperature for generation
        gemini_api_key: Gemini API key
        
    Returns:
        Generated answer from Gemini or fallback
    """
    try:
        client = get_gemini_client(api_key=gemini_api_key)
        if not client.is_available():
            logger.warning("Gemini not available — returning fallback context")
            return _fallback_answer(context)

        answer = client.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return add_krishna_says(answer)
    except Exception as e:
        logger.error(f"generate_answer error: {e}")
        return _fallback_answer(context)


def answer_bhagavad_gita_question(
    question: str,
    retrieved_context: str = "",
    max_tokens: int = 512,
    temperature: float = 0.7,
    gemini_api_key: Optional[str] = None,
) -> str:
    """
    Compose a Gita-aware prompt and generate an answer via Gemini.
    First checks for pretrained answers to avoid Gemini calls when possible.
    
    Args:
        question: User's question
        retrieved_context: Context from RAG retrieval
        max_tokens: Maximum tokens
        temperature: Generation temperature
        gemini_api_key: Gemini API key
        
    Returns:
        Answer from pretrained database or Gemini
    """
    # First check for pretrained answer - these cover 50 human problems
    has_pretrained, pretrained_answer = get_pretrained_answer(question)
    if has_pretrained:
        logger.info(f"Using pretrained answer for: {question[:50]}")
        return add_krishna_says(pretrained_answer)
    
    # Fall back to Gemini + RAG for other questions
    system_instruction = (
        "You are a knowledgeable guide to the Bhagavad Gita. "
        "Answer accurately using the provided passages, be respectful and concise."
    )

    prompt = f"{system_instruction}\n\nRelevant passages:\n{retrieved_context}\n\nQuestion: {question}\n\nAnswer:"

    return generate_answer(
        prompt=prompt,
        context=retrieved_context,
        max_tokens=max_tokens,
        temperature=temperature,
        gemini_api_key=gemini_api_key,
    )


def chat_with_gita(
    user_message: str,
    chat_history: Optional[List[dict]] = None,
    retrieved_context: str = "",
    gemini_api_key: Optional[str] = None,
    max_tokens: int = 512,
    temperature: float = 0.7,
) -> str:
    """
    Simple chat wrapper that formats messages and calls Gemini chat/generate.
    Checks pretrained answers first for quick responses.
    
    Args:
        user_message: Current user message
        chat_history: Previous chat messages
        retrieved_context: Context from RAG
        gemini_api_key: Gemini API key
        max_tokens: Maximum tokens
        temperature: Generation temperature
        
    Returns:
        Chat response
    """
    # First check for pretrained answer - these handle 50 human problems
    has_pretrained, pretrained_answer = get_pretrained_answer(user_message)
    if has_pretrained:
        logger.info(f"Using pretrained answer in chat for: {user_message[:50]}")
        return add_krishna_says(pretrained_answer)
    
    try:
        client = get_gemini_client(api_key=gemini_api_key)
        if not client.is_available():
            return _fallback_answer(retrieved_context)

        messages = chat_history or []
        messages.append({"role": "user", "content": user_message})

        # Prepend a system message with context
        system_msg = {
            "role": "system",
            "content": (
                "You are a Bhagavad Gita guide. Use the passages below to answer the user's questions.\n\n"
                f"Relevant passages:\n{retrieved_context}"
            ),
        }

        messages_with_system = [system_msg] + messages

        answer = client.chat(messages=messages_with_system, max_tokens=max_tokens, temperature=temperature)
        return add_krishna_says(answer)
    except Exception as e:
        logger.error(f"chat_with_gita error: {e}")
        return _fallback_answer(retrieved_context)


def get_llm_status(gemini_api_key: Optional[str] = None) -> dict:
    """
    Return a status dict compatible with the API's LLMStatusResponse model.
    
    Args:
        gemini_api_key: Gemini API key
        
    Returns:
        Status dictionary
    """
    try:
        client = get_gemini_client(api_key=gemini_api_key)
        available = client.is_available()
        return {
            "llm_available": available,
            "llm_api_url": "https://generativelanguage.googleapis.com/",
            "llm_model": getattr(client, "model_name", None),
            "available_models": client.list_models(),
            "rag_engine_ready": True,
        }
    except Exception as e:
        logger.error(f"get_llm_status error: {e}")
        return {
            "llm_available": False,
            "llm_api_url": "https://generativelanguage.googleapis.com/",
            "llm_model": None,
            "available_models": [],
            "rag_engine_ready": False,
        }


def _fallback_answer(context: str) -> str:
    """
    Provide fallback answer when Gemini is unavailable
    
    Args:
        context: Context to display
        
    Returns:
        Fallback answer text
    """
    if not context or not context.strip():
        return (
            "🙏 Krishna says:\n\n"
            "The LLM service is not available. However, your question has been noted. "
            "Please ensure that the GEMINI_API_KEY environment variable is set and "
            "you have network access to Google Generative Language API."
        )
    return f"🙏 Krishna says:\n\nThe Bhagavad Gita teachings:\n\n{context[:1500]}\n\n(Extended answer unavailable - please check your connection.)"

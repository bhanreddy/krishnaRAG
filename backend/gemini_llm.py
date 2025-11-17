"""
Gemini LLM Interface - Uses Google Gemini API for inference
Replaces local Ollama with cloud-based Gemini
"""
import os
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiLLMClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(
        self,
        model_name: str = "gemini-1.0-pro",  # <--- FIX
        api_key: str = None,
        timeout: int = 60
    ):
        """
        Initialize Gemini LLM Client
        
        Args:
            model_name: Name of the Gemini model (e.g., 'gemini-pro', 'gemini-1.5-pro')
            api_key: Google Gemini API key
            timeout: Request timeout in seconds (not used for Gemini but kept for compatibility)
        """
        self.model_name = model_name
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.timeout = timeout
        
        if not self.api_key:
            logger.error("GEMINI_API_KEY not provided!")
            raise ValueError("GEMINI_API_KEY environment variable or api_key parameter required")
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"Gemini client initialized with model: {model_name}")
    
    def is_available(self) -> bool:
        """Check if Gemini API is available"""
        try:
            # Test with a simple request
            test_response = self.model.generate_content("Hello", stream=False)
            if test_response:
                logger.info("✓ Gemini API connection successful")
                return True
            return False
        except Exception as e:
            logger.error(f"Gemini API test failed: {e}")
            # Try to list available models and update model if possible
            try:
                models = self.list_models()
                logger.info(f"Available Gemini models: {models}")
                # If current model is not in the listed models, pick the first available
                if models and self.model_name not in models:
                    self.model_name = models[0]
                    self.model = genai.GenerativeModel(self.model_name)
                    # Retry a simple request
                    test_response = self.model.generate_content("Hello", stream=False)
                    if test_response:
                        logger.info(f"✓ Gemini API connection successful with model {self.model_name}")
                        return True
            except Exception as e2:
                logger.error(f"Failed to list or switch models: {e2}")
            return False
    
    def list_models(self) -> list:
        """List available models (Gemini has limited public models)"""
        try:
            # Use the SDK to list models for the given API key
            try:
                sdk_models = genai.list_models()
                # SDK may return list of model dicts or strings
                model_names = []
                for m in sdk_models:
                    if isinstance(m, dict) and m.get('name'):
                        model_names.append(m['name'])
                    elif isinstance(m, str):
                        model_names.append(m)
                return model_names
            except Exception:
                # Fallback: return a list of common model names
                return ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash", "models/text-bison-001", "models/chat-bison-001"]
        except Exception as e:
            logger.error(f"Error listing Gemini models: {e}")
            return ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop_sequences: Optional[list] = None
    ) -> str:
        """
        Generate text using Gemini API
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            top_p: Nucleus sampling parameter
            stop_sequences: Sequences to stop generation
            
        Returns:
            Generated text
        """
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stop_sequences=stop_sequences or []
            )
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=False
            )
            
            if response and response.text:
                return response.text.strip()
            return "No response generated"
            
        except Exception as e:
            logger.error(f"Generation error: {e}")
            raise
    
    def chat(
        self,
        messages: list,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Chat endpoint using Gemini
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated response
        """
        try:
            # Convert messages to prompt format (Gemini API format)
            prompt = self._format_messages_to_prompt(messages)
            
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=False
            )
            
            if response and response.text:
                return response.text.strip()
            return "No response generated"
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise
    
    def _format_messages_to_prompt(self, messages: list) -> str:
        """Convert message list to prompt format"""
        prompt_parts = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            prompt_parts.append(f"{role}: {content}")
        return "\n".join(prompt_parts)


# Global Gemini client instance
_gemini_client: Optional[GeminiLLMClient] = None


def get_gemini_client(
    model_name: str = "gemini-1.0-pro",  # <--- FIX
    api_key: str = None
) -> GeminiLLMClient:
    """Get or create Gemini client"""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiLLMClient(model_name=model_name, api_key=api_key)
    return _gemini_client


def test_gemini_connection(api_key: str = None) -> Dict[str, Any]:
    """Test connection to Gemini API"""
    try:
        client = get_gemini_client(api_key=api_key)
        return {
            "available": client.is_available(),
            "model": client.model_name,
            "status": "Connected to Gemini API"
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e),
            "status": "Failed to connect to Gemini API"
        }

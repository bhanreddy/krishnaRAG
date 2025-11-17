"""
Local LLM Interface - Uses external LLM service for inference.
Supports both local Ollama and other local LLM services.
"""
import os
import requests
import json
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LocalLLMClient:
    """Client for interacting with local LLM services (Ollama, LM Studio, etc.)"""
    
    def __init__(
        self, 
        model_name: str = "neural-chat",
        api_url: str = None,
        timeout: int = 60
    ):
        """
        Initialize Local LLM Client
        
        Args:
            model_name: Name of the model (e.g., 'neural-chat', 'mistral', 'llama2')
            api_url: URL of the LLM service (default: http://127.0.0.1:11435 for Ollama)
            timeout: Request timeout in seconds
        """
        self.model_name = model_name
        self.api_url = api_url or os.environ.get('LLM_API_URL', 'http://127.0.0.1:11435')
        self.timeout = timeout
        self.is_ollama = 'ollama' in self.api_url.lower() or 'ollama' in model_name.lower()
        
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        try:
            if self.is_ollama:
                # Ollama uses /api/tags endpoint
                resp = requests.get(f"{self.api_url}/api/tags", timeout=5)
            else:
                # Generic health endpoint
                resp = requests.get(f"{self.api_url}/health", timeout=5)
            return resp.status_code == 200
        except Exception as e:
            logger.warning(f"LLM service unavailable: {e}")
            return False
    
    def list_models(self) -> list:
        """List available models from the LLM service"""
        try:
            if self.is_ollama:
                resp = requests.get(f"{self.api_url}/api/tags", timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    return [m['name'] for m in data.get('models', [])]
            return []
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop_sequences: Optional[list] = None
    ) -> str:
        """
        Generate text using the local LLM
        
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
            if self.is_ollama:
                return self._generate_ollama(
                    prompt, max_tokens, temperature, top_p, stop_sequences
                )
            else:
                return self._generate_generic(
                    prompt, max_tokens, temperature, top_p, stop_sequences
                )
        except Exception as e:
            logger.error(f"Generation error: {e}")
            raise
    
    def _generate_ollama(
        self, 
        prompt: str, 
        max_tokens: int,
        temperature: float,
        top_p: float,
        stop_sequences: Optional[list]
    ) -> str:
        """Generate using Ollama API"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "num_predict": max_tokens,
            }
        }
        
        if stop_sequences:
            payload["stop"] = stop_sequences
        
        response = requests.post(
            f"{self.api_url}/api/generate",
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    
    def _generate_generic(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_p: float,
        stop_sequences: Optional[list]
    ) -> str:
        """Generate using generic LLM API"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
        }
        
        if stop_sequences:
            payload["stop"] = stop_sequences
        
        response = requests.post(
            f"{self.api_url}/generate",
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("text", "").strip()
    
    def chat(
        self,
        messages: list,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Chat endpoint (if supported)
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated response
        """
        try:
            if self.is_ollama:
                payload = {
                    "model": self.model_name,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "top_p": top_p,
                        "num_predict": max_tokens,
                    }
                }
                response = requests.post(
                    f"{self.api_url}/api/chat",
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()
                result = response.json()
                return result.get("message", {}).get("content", "").strip()
            else:
                # Generic chat API
                payload = {
                    "model": self.model_name,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                }
                response = requests.post(
                    f"{self.api_url}/chat",
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise


# Global LLM client instance
_llm_client: Optional[LocalLLMClient] = None

def get_llm_client(
    model_name: str = "mistral",
    api_url: str = None
) -> LocalLLMClient:
    """Get or create LLM client"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LocalLLMClient(model_name=model_name, api_url=api_url)
    return _llm_client

def test_llm_connection() -> Dict[str, Any]:
    """Test connection to local LLM service"""
    client = get_llm_client()
    return {
        "available": client.is_available(),
        "api_url": client.api_url,
        "model": client.model_name,
        "models": client.list_models()
    }
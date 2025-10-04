"""
Ollama integration service for AI operations
"""

import httpx
import json
from typing import List, Optional, Dict, Any
from loguru import logger

from pkm_backend.core.config import settings


class OllamaService:
    """Service for interacting with Ollama LLM API"""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.default_model = settings.DEFAULT_LLM_MODEL
    
    async def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to Ollama API"""
        url = f"{self.base_url}/{endpoint}"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, json=data)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                logger.error(f"Request error to Ollama: {e}")
                raise Exception(f"Failed to connect to Ollama: {e}")
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error from Ollama: {e}")
                raise Exception(f"Ollama API error: {e}")
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """Generate text using Ollama"""
        
        model = model or self.default_model
        
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if system_prompt:
            data["system"] = system_prompt
        
        response = await self._make_request("api/generate", data)
        return response.get("response", "")
    
    async def cleanup_text(self, text: str, cleanup_type: str = "full") -> str:
        """Clean up and improve text quality"""
        
        system_prompts = {
            "grammar": "You are a grammar expert. Fix only grammar and spelling errors in the following text. Keep the original meaning and style intact.",
            "structure": "You are a writing expert. Improve the structure and flow of the following text while keeping the original meaning.",
            "clarity": "You are a clarity expert. Make the following text clearer and more concise while preserving all important information.",
            "full": "You are a writing expert. Improve the grammar, structure, and clarity of the following text while preserving the original meaning."
        }
        
        system_prompt = system_prompts.get(cleanup_type, system_prompts["full"])
        prompt = f"Please improve the following text:\n\n{text}"
        
        return await self.generate(prompt, system_prompt=system_prompt, temperature=0.3)
    
    async def rephrase_text(self, text: str, style: str = "academic") -> str:
        """Rephrase text in a specific style"""
        
        style_prompts = {
            "academic": "Rephrase the following text in a formal, academic style suitable for research papers.",
            "casual": "Rephrase the following text in a casual, conversational style.",
            "formal": "Rephrase the following text in a formal, professional style.",
            "creative": "Rephrase the following text in a creative, engaging style."
        }
        
        system_prompt = style_prompts.get(style, style_prompts["academic"])
        prompt = f"Please rephrase this text:\n\n{text}"
        
        return await self.generate(prompt, system_prompt=system_prompt, temperature=0.5)
    
    async def search_notes(self, query: str, note_contents: List[str]) -> List[Dict[str, Any]]:
        """Search through notes using semantic understanding"""
        
        system_prompt = """You are a search expert. Given a query and a list of note contents, 
        rank them by relevance to the query. Return a JSON array of objects with:
        - index: the index of the note in the input list
        - relevance_score: a float between 0 and 1
        - snippet: a brief excerpt that matches the query
        
        Only include notes with relevance_score > 0.1"""
        
        notes_text = "\n\n".join([f"Note {i}: {content}" for i, content in enumerate(note_contents)])
        prompt = f"Query: {query}\n\nNotes:\n{notes_text}"
        
        response = await self.generate(prompt, system_prompt=system_prompt, temperature=0.2)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning("Failed to parse search results as JSON")
            return []
    
    async def chat_with_notes(self, message: str, note_contents: List[str], conversation_history: Optional[List[str]] = None) -> str:
        """Chat about notes with context"""
        
        system_prompt = """You are a helpful assistant that can answer questions about the user's notes. 
        Use the provided note contents as context to answer questions accurately. 
        If the answer isn't in the notes, say so clearly."""
        
        context = "\n\n".join([f"Note {i+1}: {content}" for i, content in enumerate(note_contents)])
        
        prompt = f"Context from notes:\n{context}\n\nQuestion: {message}"
        
        if conversation_history:
            history = "\n".join(conversation_history[-5:])  # Last 5 messages
            prompt = f"Previous conversation:\n{history}\n\n{prompt}"
        
        return await self.generate(prompt, system_prompt=system_prompt, temperature=0.6)
    
    async def list_models(self) -> List[str]:
        """List available models in Ollama"""
        
        try:
            response = await self._make_request("api/tags", {})
            models = response.get("models", [])
            return [model["name"] for model in models]
        except Exception:
            logger.warning("Failed to list Ollama models")
            return [self.default_model]
    
    async def check_health(self) -> bool:
        """Check if Ollama is running and accessible"""
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False


# Global service instance
ollama_service = OllamaService()
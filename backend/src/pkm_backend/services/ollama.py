"""
Ollama integration service for AI operations using the official Ollama Python library
"""

import asyncio
from typing import List, Optional, Dict, Any
from loguru import logger
import ollama
from ollama import AsyncClient, ResponseError

from pkm_backend.core.config import settings


class OllamaService:
    """Service for interacting with Ollama using the official Python library"""
    
    def __init__(self):
        self.host = settings.OLLAMA_BASE_URL
        self.default_model = settings.DEFAULT_LLM_MODEL
        self.client = AsyncClient(host=self.host)
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """Generate text using Ollama chat API"""
        
        model = model or self.default_model
        
        # Prepare messages for chat format
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user", 
            "content": prompt
        })
        
        try:
            response = await self.client.chat(
                model=model,
                messages=messages,
                options={
                    "temperature": temperature
                }
            )
            
            return response['message']['content']
            
        except ResponseError as e:
            logger.error(f"Ollama API error: {e.error}")
            raise Exception(f"Ollama API error: {e.error}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"Failed to generate text: {e}")
    
    async def cleanup_text(self, text: str, cleanup_type: str = "full") -> str:
        """Clean up and improve text quality"""
        
        system_prompts = {
            "grammar": "You are a grammar expert. Fix only grammar and spelling errors in the following text. Keep the original meaning and style intact.",
            "structure": "You are a writing expert. Improve the structure and flow of the following text while keeping the original meaning.",
            "clarity": "You are a clarity expert. Make the following text clearer and more concise while preserving all important information.",
            "full": "You are a writing expert. Improve the grammar, structure, and clarity of the following text while preserving the original meaning."
        }
        
        system_prompt = system_prompts.get(cleanup_type, system_prompts["full"])
        
        return await self.generate(
            prompt=text,
            system_prompt=system_prompt,
            temperature=0.3  # Lower temperature for more consistent cleanup
        )
    
    async def rephrase_text(
        self, 
        text: str, 
        style: str = "professional",
        temperature: float = 0.7
    ) -> str:
        """Rephrase text in a specific style"""
        
        style_prompts = {
            "academic": "You are an academic writing expert. Rephrase the following text in a formal, scholarly tone suitable for academic papers. Use precise terminology and maintain objectivity.",
            "professional": "You are a business writing expert. Rephrase the following text in a professional, corporate tone suitable for workplace communication.",
            "casual": "You are a communication expert. Rephrase the following text in a casual, friendly tone suitable for informal conversations.",
            "creative": "You are a creative writing expert. Rephrase the following text in an engaging, creative style that captures attention while maintaining the core message.",
            "formal": "You are a formal writing expert. Rephrase the following text in a formal, respectful tone suitable for official communications."
        }
        
        system_prompt = style_prompts.get(style, style_prompts["professional"])
        
        return await self.generate(
            prompt=text,
            system_prompt=system_prompt,
            temperature=temperature
        )
    
    async def chat_with_context(
        self,
        message: str,
        context: str = "",
        temperature: float = 0.7
    ) -> str:
        """Chat with provided context"""
        
        if context:
            system_prompt = f"You are a helpful assistant. Use the following context to answer questions:\n\n{context}\n\nAnswer based on the provided context when relevant, but you can also use your general knowledge."
        else:
            system_prompt = "You are a helpful assistant. Provide clear, informative answers to questions."
        
        return await self.generate(
            prompt=message,
            system_prompt=system_prompt,
            temperature=temperature
        )
    
    async def semantic_search_query(self, query: str, temperature: float = 0.3) -> str:
        """Generate semantic search variations of a query"""
        
        system_prompt = """You are a search expert. Given a search query, generate 3-5 semantically similar variations that could help find related content. 
        Return only the variations, one per line, without explanations or numbering."""
        
        return await self.generate(
            prompt=f"Search query: {query}",
            system_prompt=system_prompt,
            temperature=temperature
        )
    
    async def check_model_availability(self, model: Optional[str] = None) -> bool:
        """Check if a model is available locally"""
        model = model or self.default_model
        
        try:
            models = await self.client.list()
            available_models = [m['name'] for m in models['models']]
            return model in available_models
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False
    
    async def pull_model(self, model: Optional[str] = None) -> bool:
        """Pull a model if not available"""
        model = model or self.default_model
        
        try:
            await self.client.pull(model)
            logger.info(f"Successfully pulled model: {model}")
            return True
        except Exception as e:
            logger.error(f"Error pulling model {model}: {e}")
            return False
    
    async def list_models(self) -> List[str]:
        """List available models"""
        try:
            models_response = await self.client.list()
            return [model['name'] for model in models_response['models']]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    async def check_health(self) -> bool:
        """Check if Ollama service is healthy"""
        try:
            # Try to list models as a health check
            await self.client.list()
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False


# Global service instance
ollama_service = OllamaService()
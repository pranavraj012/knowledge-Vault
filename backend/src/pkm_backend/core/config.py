"""
Core configuration settings for the PKM Backend
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    # Project info
    PROJECT_NAME: str = "PKM Backend"
    DESCRIPTION: str = "Privacy-focused Personal Knowledge Management System Backend"
    VERSION: str = "0.1.0"
    
    # Server settings
    HOST: str = Field(default="localhost", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    ENVIRONMENT: str = Field(default="development", description="Environment (development/production)")
    
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed CORS origins"
    )
    
    # Database settings
    DATABASE_URL: str = Field(
        default="sqlite:///./pkm.db",
        description="Database connection URL"
    )
    
    # Security settings
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production",
        description="Secret key for JWT tokens"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    
    # File storage settings
    NOTES_STORAGE_PATH: str = Field(
        default="./data/notes",
        description="Path to store markdown notes"
    )
    WORKSPACES_STORAGE_PATH: str = Field(
        default="./data/workspaces",
        description="Path to store workspace data"
    )
    
    # Ollama settings
    OLLAMA_BASE_URL: str = Field(
        default="http://localhost:11434",
        description="Ollama API base URL"
    )
    DEFAULT_LLM_MODEL: str = Field(
        default="llama3.2:1b",
        description="Default LLM model for AI operations"
    )
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: Optional[str] = Field(default=None, description="Log file path")
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )


# Create global settings instance
settings = Settings()
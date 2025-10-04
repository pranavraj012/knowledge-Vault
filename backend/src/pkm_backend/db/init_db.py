"""
Database initialization script
"""

import os
from sqlalchemy import text
from loguru import logger

from pkm_backend.db.database import engine, create_tables
from pkm_backend.core.config import settings


def init_database():
    """Initialize the database with tables and sample data"""
    
    logger.info("Initializing database...")
    
    # Create data directories
    os.makedirs(settings.NOTES_STORAGE_PATH, exist_ok=True)
    os.makedirs(settings.WORKSPACES_STORAGE_PATH, exist_ok=True)
    os.makedirs("./data", exist_ok=True)
    
    # Create all tables
    create_tables()
    
    logger.info("Database initialization completed")


def reset_database():
    """Reset the database (drop all tables and recreate)"""
    
    logger.warning("Resetting database - all data will be lost!")
    
    # Drop all tables
    from pkm_backend.models.database import Base
    Base.metadata.drop_all(bind=engine)
    
    # Recreate tables
    init_database()
    
    logger.info("Database reset completed")


if __name__ == "__main__":
    init_database()
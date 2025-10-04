"""
Database models for the PKM system
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from pkm_backend.db.database import Base


class Workspace(Base):
    """Workspace model for organizing notes by subject/topic"""
    __tablename__ = "workspaces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(7), default="#3B82F6")  # Hex color code
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    notes = relationship("Note", back_populates="workspace", cascade="all, delete-orphan")


class Note(Base):
    """Note model for storing markdown content"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=False)
    file_path = Column(String(1000), nullable=True)  # Relative path from notes storage
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Workspace relationship
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    workspace = relationship("Workspace", back_populates="notes")
    
    # Tags relationship
    tags = relationship("Tag", secondary="note_tags", back_populates="notes")


class Tag(Base):
    """Tag model for categorizing notes"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    color = Column(String(7), default="#6B7280")  # Hex color code
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    notes = relationship("Note", secondary="note_tags", back_populates="tags")


class NoteTag(Base):
    """Association table for Note-Tag many-to-many relationship"""
    __tablename__ = "note_tags"
    
    note_id = Column(Integer, ForeignKey("notes.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class AISession(Base):
    """Track AI interactions and queries"""
    __tablename__ = "ai_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_type = Column(String(50), nullable=False)  # 'cleanup', 'rephrase', 'search', 'chat'
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    model_used = Column(String(100), nullable=False)
    
    # Associated notes (for context)
    note_ids = Column(Text, nullable=True)  # JSON array of note IDs
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processing_time_ms = Column(Integer, nullable=True)
    success = Column(Boolean, default=True)
"""
Pydantic schemas for API requests and responses
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


# Base schemas
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# Workspace schemas
class WorkspaceBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    color: str = Field(default="#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$")


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")


class Workspace(WorkspaceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class WorkspaceWithNotes(Workspace):
    notes: List["Note"] = []


# Tag schemas
class TagBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(default="#6B7280", pattern=r"^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    pass


class TagUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")


class Tag(TagBase):
    id: int
    created_at: datetime


# Note schemas
class NoteBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    workspace_id: int


class NoteCreate(NoteBase):
    tag_ids: List[int] = []


class NoteUpdate(BaseSchema):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = Field(None, min_length=1)
    workspace_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class Note(NoteBase):
    id: int
    file_path: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[Tag] = []


class NoteWithWorkspace(Note):
    workspace: Workspace


# AI schemas
class AICleanupRequest(BaseSchema):
    note_id: int
    cleanup_type: str = Field(..., pattern=r"^(grammar|structure|clarity|full)$")


class AIRephraseRequest(BaseSchema):
    text: str = Field(..., min_length=1)
    style: str = Field(default="academic", pattern=r"^(academic|casual|formal|creative)$")


class AISearchRequest(BaseSchema):
    query: str = Field(..., min_length=1)
    workspace_ids: Optional[List[int]] = None
    max_results: int = Field(default=10, ge=1, le=50)


class AIChatRequest(BaseSchema):
    message: str = Field(..., min_length=1)
    note_ids: Optional[List[int]] = None  # Notes to include as context
    conversation_id: Optional[str] = None


class AIResponse(BaseSchema):
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    processing_time_ms: Optional[int] = None
    model_used: str


# Search schemas
class SearchResult(BaseSchema):
    note_id: int
    note_title: str
    relevance_score: float
    snippet: str
    workspace_name: str


class SearchResponse(BaseSchema):
    results: List[SearchResult]
    total_count: int
    query: str


# Export schemas
class ExportRequest(BaseSchema):
    workspace_ids: Optional[List[int]] = None
    note_ids: Optional[List[int]] = None
    format: str = Field(..., pattern=r"^(pdf|markdown|html)$")
    include_metadata: bool = True


class ExportResponse(BaseSchema):
    success: bool
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    error: Optional[str] = None
"""
Search API endpoints
"""

import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from pkm_backend.db.database import get_db
from pkm_backend.models.database import Note as NoteModel, Workspace as WorkspaceModel, AISession as AISessionModel
from pkm_backend.models.schemas import (
    AISearchRequest,
    SearchResponse,
    SearchResult
)
from pkm_backend.services.ollama import ollama_service

router = APIRouter()


@router.post("/", response_model=SearchResponse)
async def search_notes(
    request: AISearchRequest,
    db: Session = Depends(get_db)
):
    """Search notes using AI-powered semantic search"""
    
    start_time = time.time()
    
    try:
        # Build query to get notes
        query = db.query(NoteModel)
        
        # Filter by workspace if specified
        if request.workspace_ids:
            query = query.filter(NoteModel.workspace_id.in_(request.workspace_ids))
        
        # Get all notes for search
        notes = query.all()
        
        if not notes:
            return SearchResponse(
                results=[],
                total_count=0,
                query=request.query
            )
        
        # Prepare note contents for AI search
        note_contents = [f"{note.title}\n\n{note.content}" for note in notes]
        
        # Use AI to search and rank notes
        search_results = await ollama_service.search_notes(request.query, note_contents)
        
        # Convert AI results to our schema
        results = []
        for result in search_results[:request.max_results]:
            if result.get("relevance_score", 0) > 0.1:  # Filter low relevance
                note_index = result.get("index", 0)
                if 0 <= note_index < len(notes):
                    note = notes[note_index]
                    
                    results.append(SearchResult(
                        note_id=note.id,
                        note_title=note.title,
                        relevance_score=result.get("relevance_score", 0),
                        snippet=result.get("snippet", note.content[:200] + "..."),
                        workspace_name=note.workspace.name
                    ))
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log the search session
        ai_session = AISessionModel(
            session_type="search",
            query=request.query,
            response=f"Found {len(results)} results",
            model_used=ollama_service.default_model,
            processing_time_ms=processing_time,
            success=True
        )
        db.add(ai_session)
        db.commit()
        
        return SearchResponse(
            results=results,
            total_count=len(results),
            query=request.query
        )
        
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log failed search
        ai_session = AISessionModel(
            session_type="search",
            query=request.query,
            model_used=ollama_service.default_model,
            processing_time_ms=processing_time,
            success=False
        )
        db.add(ai_session)
        db.commit()
        
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/simple")
async def simple_search(
    q: str,
    workspace_id: int = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Simple text-based search without AI"""
    
    # Build query
    query = db.query(NoteModel)
    
    # Filter by workspace if specified
    if workspace_id:
        query = query.filter(NoteModel.workspace_id == workspace_id)
    
    # Simple text search in title and content
    search_filter = f"%{q}%"
    query = query.filter(
        (NoteModel.title.ilike(search_filter)) |
        (NoteModel.content.ilike(search_filter))
    )
    
    # Get results
    notes = query.limit(limit).all()
    
    # Convert to search results
    results = []
    for note in notes:
        # Simple snippet extraction
        content_lower = note.content.lower()
        query_lower = q.lower()
        
        snippet = note.content[:200] + "..."
        if query_lower in content_lower:
            start_pos = content_lower.find(query_lower)
            snippet_start = max(0, start_pos - 50)
            snippet_end = min(len(note.content), start_pos + 150)
            snippet = "..." + note.content[snippet_start:snippet_end] + "..."
        
        results.append(SearchResult(
            note_id=note.id,
            note_title=note.title,
            relevance_score=1.0,  # Simple search doesn't calculate relevance
            snippet=snippet,
            workspace_name=note.workspace.name
        ))
    
    return SearchResponse(
        results=results,
        total_count=len(results),
        query=q
    )
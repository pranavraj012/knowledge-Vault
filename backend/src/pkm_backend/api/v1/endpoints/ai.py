"""
AI API endpoints for Ollama integration
"""

import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from pkm_backend.db.database import get_db
from pkm_backend.models.database import Note as NoteModel, AISession as AISessionModel
from pkm_backend.models.schemas import (
    AICleanupRequest,
    AIRephraseRequest,
    AIChatRequest,
    AIResponse
)
from pkm_backend.services.ollama import ollama_service

router = APIRouter()


@router.post("/cleanup", response_model=AIResponse)
async def cleanup_note(
    request: AICleanupRequest,
    db: Session = Depends(get_db)
):
    """Clean up and improve a note's content using AI"""
    
    # Get the note
    note = db.query(NoteModel).filter(NoteModel.id == request.note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    start_time = time.time()
    
    try:
        # Use Ollama to clean up the content
        cleaned_content = await ollama_service.cleanup_text(note.content, request.cleanup_type)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log the AI session
        ai_session = AISessionModel(
            session_type="cleanup",
            query=f"Cleanup type: {request.cleanup_type}",
            response=cleaned_content,
            model_used=ollama_service.default_model,
            note_ids=str([request.note_id]),
            processing_time_ms=processing_time,
            success=True
        )
        db.add(ai_session)
        db.commit()
        
        return AIResponse(
            success=True,
            response=cleaned_content,
            processing_time_ms=processing_time,
            model_used=ollama_service.default_model
        )
        
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log failed session
        ai_session = AISessionModel(
            session_type="cleanup",
            query=f"Cleanup type: {request.cleanup_type}",
            model_used=ollama_service.default_model,
            note_ids=str([request.note_id]),
            processing_time_ms=processing_time,
            success=False
        )
        db.add(ai_session)
        db.commit()
        
        return AIResponse(
            success=False,
            error=str(e),
            processing_time_ms=processing_time,
            model_used=ollama_service.default_model
        )


@router.post("/rephrase", response_model=AIResponse)
async def rephrase_text(
    request: AIRephraseRequest,
    db: Session = Depends(get_db)
):
    """Rephrase text in a specific style using AI"""
    
    start_time = time.time()
    
    try:
        # Use Ollama to rephrase the text
        rephrased_text = await ollama_service.rephrase_text(request.text, request.style)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log the AI session
        ai_session = AISessionModel(
            session_type="rephrase",
            query=f"Style: {request.style}, Text: {request.text[:100]}...",
            response=rephrased_text,
            model_used=ollama_service.default_model,
            processing_time_ms=processing_time,
            success=True
        )
        db.add(ai_session)
        db.commit()
        
        return AIResponse(
            success=True,
            response=rephrased_text,
            processing_time_ms=processing_time,
            model_used=ollama_service.default_model
        )
        
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log failed session
        ai_session = AISessionModel(
            session_type="rephrase",
            query=f"Style: {request.style}, Text: {request.text[:100]}...",
            model_used=ollama_service.default_model,
            processing_time_ms=processing_time,
            success=False
        )
        db.add(ai_session)
        db.commit()
        
        return AIResponse(
            success=False,
            error=str(e),
            processing_time_ms=processing_time,
            model_used=ollama_service.default_model
        )


@router.post("/chat", response_model=AIResponse)
async def chat_with_notes(
    request: AIChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with AI about your notes"""
    
    start_time = time.time()
    
    try:
        # Get note contents for context
        note_contents = []
        if request.note_ids:
            notes = db.query(NoteModel).filter(NoteModel.id.in_(request.note_ids)).all()
            note_contents = [f"{note.title}\n\n{note.content}" for note in notes]
        
        # Use Ollama to generate response
        response_text = await ollama_service.chat_with_notes(request.message, note_contents)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log the AI session
        ai_session = AISessionModel(
            session_type="chat",
            query=request.message,
            response=response_text,
            model_used=ollama_service.default_model,
            note_ids=str(request.note_ids) if request.note_ids else None,
            processing_time_ms=processing_time,
            success=True
        )
        db.add(ai_session)
        db.commit()
        
        return AIResponse(
            success=True,
            response=response_text,
            processing_time_ms=processing_time,
            model_used=ollama_service.default_model
        )
        
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        
        # Log failed session
        ai_session = AISessionModel(
            session_type="chat",
            query=request.message,
            model_used=ollama_service.default_model,
            note_ids=str(request.note_ids) if request.note_ids else None,
            processing_time_ms=processing_time,
            success=False
        )
        db.add(ai_session)
        db.commit()
        
        return AIResponse(
            success=False,
            error=str(e),
            processing_time_ms=processing_time,
            model_used=ollama_service.default_model
        )


@router.get("/models", response_model=List[str])
async def list_available_models():
    """List available AI models from Ollama"""
    
    try:
        models = await ollama_service.list_models()
        return models
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to connect to Ollama: {e}"
        )


@router.get("/health")
async def check_ai_health():
    """Check if AI service (Ollama) is available"""
    
    is_healthy = await ollama_service.check_health()
    
    if not is_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ollama service is not available"
        )
    
    return {"status": "healthy", "service": "ollama"}
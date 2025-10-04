"""
Notes API endpoints
"""

import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from pkm_backend.db.database import get_db
from pkm_backend.models.database import Note as NoteModel, Workspace as WorkspaceModel, Tag as TagModel
from pkm_backend.models.schemas import (
    Note,
    NoteCreate,
    NoteUpdate,
    NoteWithWorkspace
)
from pkm_backend.core.config import settings

router = APIRouter()


def _save_note_to_file(note: NoteModel) -> str:
    """Save note content to markdown file"""
    
    # Create workspace directory if it doesn't exist
    workspace_dir = os.path.join(settings.NOTES_STORAGE_PATH, f"workspace_{note.workspace_id}")
    os.makedirs(workspace_dir, exist_ok=True)
    
    # Generate filename from note title
    safe_title = "".join(c for c in note.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')
    filename = f"{note.id}_{safe_title}.md"
    
    file_path = os.path.join(workspace_dir, filename)
    
    # Write content to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"# {note.title}\n\n")
        f.write(note.content)
    
    # Return relative path
    return os.path.relpath(file_path, settings.NOTES_STORAGE_PATH)


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    """Create a new note"""
    
    # Verify workspace exists
    workspace = db.query(WorkspaceModel).filter(WorkspaceModel.id == note.workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace not found"
        )
    
    # Create note
    db_note = NoteModel(
        title=note.title,
        content=note.content,
        workspace_id=note.workspace_id
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    # Save to file
    try:
        file_path = _save_note_to_file(db_note)
        db_note.file_path = file_path
        db.commit()
        db.refresh(db_note)
    except Exception as e:
        # If file save fails, we still keep the note in DB
        pass
    
    # Add tags if provided
    if note.tag_ids:
        tags = db.query(TagModel).filter(TagModel.id.in_(note.tag_ids)).all()
        db_note.tags = tags
        db.commit()
        db.refresh(db_note)
    
    return db_note


@router.get("/", response_model=List[Note])
async def list_notes(
    workspace_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of notes, optionally filtered by workspace"""
    
    query = db.query(NoteModel)
    
    if workspace_id:
        query = query.filter(NoteModel.workspace_id == workspace_id)
    
    notes = query.offset(skip).limit(limit).all()
    return notes


@router.get("/{note_id}", response_model=NoteWithWorkspace)
async def get_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific note with workspace information"""
    
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note


@router.put("/{note_id}", response_model=Note)
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    db: Session = Depends(get_db)
):
    """Update a note"""
    
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Verify workspace exists if updating workspace_id
    if note_update.workspace_id and note_update.workspace_id != note.workspace_id:
        workspace = db.query(WorkspaceModel).filter(WorkspaceModel.id == note_update.workspace_id).first()
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Workspace not found"
            )
    
    # Update fields
    update_data = note_update.model_dump(exclude_unset=True, exclude={'tag_ids'})
    for field, value in update_data.items():
        setattr(note, field, value)
    
    # Update tags if provided
    if note_update.tag_ids is not None:
        tags = db.query(TagModel).filter(TagModel.id.in_(note_update.tag_ids)).all()
        note.tags = tags
    
    db.commit()
    db.refresh(note)
    
    # Update file
    try:
        file_path = _save_note_to_file(note)
        note.file_path = file_path
        db.commit()
        db.refresh(note)
    except Exception:
        pass
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    """Delete a note"""
    
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Delete file if it exists
    if note.file_path:
        try:
            full_path = os.path.join(settings.NOTES_STORAGE_PATH, note.file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception:
            pass
    
    db.delete(note)
    db.commit()
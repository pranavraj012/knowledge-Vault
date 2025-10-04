"""
Tags API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from pkm_backend.db.database import get_db
from pkm_backend.models.database import Tag as TagModel
from pkm_backend.models.schemas import (
    Tag,
    TagCreate,
    TagUpdate
)

router = APIRouter()


@router.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db)
):
    """Create a new tag"""
    
    # Check if tag name already exists
    existing = db.query(TagModel).filter(TagModel.name == tag.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists"
        )
    
    db_tag = TagModel(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    
    return db_tag


@router.get("/", response_model=List[Tag])
async def list_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of all tags"""
    
    tags = db.query(TagModel).offset(skip).limit(limit).all()
    return tags


@router.get("/{tag_id}", response_model=Tag)
async def get_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific tag"""
    
    tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    return tag


@router.put("/{tag_id}", response_model=Tag)
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    db: Session = Depends(get_db)
):
    """Update a tag"""
    
    tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    # Check name uniqueness if updating name
    if tag_update.name and tag_update.name != tag.name:
        existing = db.query(TagModel).filter(TagModel.name == tag_update.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists"
            )
    
    # Update fields
    update_data = tag_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tag, field, value)
    
    db.commit()
    db.refresh(tag)
    
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db)
):
    """Delete a tag"""
    
    tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    db.delete(tag)
    db.commit()
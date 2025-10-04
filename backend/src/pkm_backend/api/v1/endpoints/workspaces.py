"""
Workspace API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from pkm_backend.db.database import get_db
from pkm_backend.models.database import Workspace as WorkspaceModel
from pkm_backend.models.schemas import (
    Workspace,
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceWithNotes
)

router = APIRouter()


@router.post("/", response_model=Workspace, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace: WorkspaceCreate,
    db: Session = Depends(get_db)
):
    """Create a new workspace"""
    
    # Check if workspace name already exists
    existing = db.query(WorkspaceModel).filter(WorkspaceModel.name == workspace.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace with this name already exists"
        )
    
    db_workspace = WorkspaceModel(**workspace.model_dump())
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    
    return db_workspace


@router.get("/", response_model=List[Workspace])
async def list_workspaces(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of all workspaces"""
    
    workspaces = db.query(WorkspaceModel).offset(skip).limit(limit).all()
    return workspaces


@router.get("/{workspace_id}", response_model=WorkspaceWithNotes)
async def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific workspace with its notes"""
    
    workspace = db.query(WorkspaceModel).filter(WorkspaceModel.id == workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    
    return workspace


@router.put("/{workspace_id}", response_model=Workspace)
async def update_workspace(
    workspace_id: int,
    workspace_update: WorkspaceUpdate,
    db: Session = Depends(get_db)
):
    """Update a workspace"""
    
    workspace = db.query(WorkspaceModel).filter(WorkspaceModel.id == workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    
    # Check name uniqueness if updating name
    if workspace_update.name and workspace_update.name != workspace.name:
        existing = db.query(WorkspaceModel).filter(WorkspaceModel.name == workspace_update.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Workspace with this name already exists"
            )
    
    # Update fields
    update_data = workspace_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workspace, field, value)
    
    db.commit()
    db.refresh(workspace)
    
    return workspace


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    """Delete a workspace and all its notes"""
    
    workspace = db.query(WorkspaceModel).filter(WorkspaceModel.id == workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    
    db.delete(workspace)
    db.commit()
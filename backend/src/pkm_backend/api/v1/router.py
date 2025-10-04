"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from pkm_backend.api.v1.endpoints import workspaces, notes, tags, ai, search


api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
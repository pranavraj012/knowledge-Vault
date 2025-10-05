"""
Test configuration and fixtures for PKM Backend
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from pkm_backend.main import app
from pkm_backend.db.database import get_db, Base
from pkm_backend.models.database import Workspace, Note, Tag


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client(db_session):
    """Create a test client with fresh database"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_workspace(db_session):
    """Create a sample workspace for testing"""
    workspace = Workspace(
        name="Test Workspace",
        description="A workspace for testing",
        color="#3B82F6"
    )
    db_session.add(workspace)
    db_session.commit()
    db_session.refresh(workspace)
    return workspace


@pytest.fixture
def sample_tag(db_session):
    """Create a sample tag for testing"""
    tag = Tag(
        name="test-tag",
        color="#10B981"
    )
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    return tag


@pytest.fixture
def sample_note(db_session, sample_workspace):
    """Create a sample note for testing"""
    note = Note(
        title="Test Note",
        content="# Test Note\n\nThis is a test note with some content.",
        workspace_id=sample_workspace.id
    )
    db_session.add(note)
    db_session.commit()
    db_session.refresh(note)
    return note


# Configure pytest for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
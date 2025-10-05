"""
Test notes API endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_create_note(client: TestClient, sample_workspace):
    """Test creating a new note"""
    note_data = {
        "title": "My First Note",
        "content": "# Hello World\n\nThis is my first note!",
        "workspace_id": sample_workspace.id,
        "tag_ids": []
    }
    
    response = client.post("/api/v1/notes/", json=note_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == note_data["title"]
    assert data["content"] == note_data["content"]
    assert data["workspace_id"] == sample_workspace.id
    assert "id" in data
    assert "created_at" in data


def test_list_notes(client: TestClient, sample_note):
    """Test listing notes"""
    response = client.get("/api/v1/notes/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == sample_note.title


def test_list_notes_by_workspace(client: TestClient, sample_note, sample_workspace):
    """Test listing notes filtered by workspace"""
    response = client.get(f"/api/v1/notes/?workspace_id={sample_workspace.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(note["workspace_id"] == sample_workspace.id for note in data)


def test_get_note(client: TestClient, sample_note):
    """Test getting a specific note"""
    response = client.get(f"/api/v1/notes/{sample_note.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == sample_note.id
    assert data["title"] == sample_note.title
    assert "workspace" in data


def test_update_note(client: TestClient, sample_note):
    """Test updating a note"""
    update_data = {
        "title": "Updated Note Title",
        "content": "# Updated Content\n\nThis note has been updated!"
    }
    
    response = client.put(f"/api/v1/notes/{sample_note.id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["content"] == update_data["content"]


def test_delete_note(client: TestClient, sample_note):
    """Test deleting a note"""
    response = client.delete(f"/api/v1/notes/{sample_note.id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    response = client.get(f"/api/v1/notes/{sample_note.id}")
    assert response.status_code == 404


def test_create_note_with_tags(client: TestClient, sample_workspace, sample_tag):
    """Test creating a note with tags"""
    note_data = {
        "title": "Tagged Note",
        "content": "This note has tags!",
        "workspace_id": sample_workspace.id,
        "tag_ids": [sample_tag.id]
    }
    
    response = client.post("/api/v1/notes/", json=note_data)
    assert response.status_code == 201
    
    data = response.json()
    assert len(data["tags"]) == 1
    assert data["tags"][0]["id"] == sample_tag.id


def test_create_note_invalid_workspace(client: TestClient):
    """Test creating note with invalid workspace fails"""
    note_data = {
        "title": "Invalid Note",
        "content": "This should fail",
        "workspace_id": 999,  # Non-existent workspace
        "tag_ids": []
    }
    
    response = client.post("/api/v1/notes/", json=note_data)
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]
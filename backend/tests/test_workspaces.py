"""
Test workspace API endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_create_workspace(client: TestClient, db_session):
    """Test creating a new workspace"""
    workspace_data = {
        "name": "Computer Science",
        "description": "CS coursework and notes",
        "color": "#3B82F6"
    }
    
    response = client.post("/api/v1/workspaces/", json=workspace_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == workspace_data["name"]
    assert data["description"] == workspace_data["description"]
    assert data["color"] == workspace_data["color"]
    assert "id" in data
    assert "created_at" in data


def test_list_workspaces(client: TestClient, sample_workspace):
    """Test listing workspaces"""
    response = client.get("/api/v1/workspaces/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == sample_workspace.name


def test_get_workspace(client: TestClient, sample_workspace):
    """Test getting a specific workspace"""
    response = client.get(f"/api/v1/workspaces/{sample_workspace.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == sample_workspace.id
    assert data["name"] == sample_workspace.name


def test_update_workspace(client: TestClient, sample_workspace):
    """Test updating a workspace"""
    update_data = {
        "name": "Updated Workspace",
        "description": "Updated description"
    }
    
    response = client.put(f"/api/v1/workspaces/{sample_workspace.id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]


def test_delete_workspace(client: TestClient, sample_workspace):
    """Test deleting a workspace"""
    response = client.delete(f"/api/v1/workspaces/{sample_workspace.id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    response = client.get(f"/api/v1/workspaces/{sample_workspace.id}")
    assert response.status_code == 404


def test_create_workspace_duplicate_name(client: TestClient, sample_workspace):
    """Test creating workspace with duplicate name fails"""
    workspace_data = {
        "name": sample_workspace.name,  # Same name as existing
        "description": "This should fail"
    }
    
    response = client.post("/api/v1/workspaces/", json=workspace_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]
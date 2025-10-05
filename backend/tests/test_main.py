"""
Test basic application functionality
"""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_api_docs_available(client: TestClient):
    """Test that API documentation is available"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema(client: TestClient):
    """Test that OpenAPI schema is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "PKM Backend"
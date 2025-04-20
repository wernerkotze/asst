import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(test_client):
    """Test the root endpoint returns the expected response."""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to the ASST API"
    assert "docs" in data
    assert "redoc" in data


def test_health_check(test_client):
    """Test the health check endpoint returns healthy status."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

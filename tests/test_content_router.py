import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime

from app.models.schemas import ContentGenerationRequest, ContentGenerationResponse


@pytest.fixture
def sample_content_request():
    """Sample content generation request for testing."""
    return {
        "brand_name": "Test Brand",
        "content_type": "blog_post",
        "topic": "Test Topic",
        "target_audience": ["professionals", "executives"],
        "tone": "professional",
        "keywords": ["test", "content", "generation"],
        "max_length": 1000
    }


@pytest.fixture
def sample_content_response():
    """Sample content generation response for testing."""
    return {
        "brand_name": "Test Brand",
        "content_type": "blog_post",
        "title": "Test Topic: A Test Brand Perspective",
        "content": "This is a sample blog post content for testing purposes.",
        "meta_description": "Learn about Test Topic in this insightful blog post from Test Brand.",
        "suggested_tags": ["test", "content", "generation", "Technology", "Test"],
        "generation_date": datetime.now().isoformat()
    }


@patch("app.routers.content_router.generate_content")
def test_generate_content_endpoint_success(mock_generate_content, test_client, override_get_db,
                                          sample_content_request, sample_content_response):
    """Test successful content generation endpoint."""
    # Setup the mock
    mock_generate_content.return_value = AsyncMock(return_value=sample_content_response)
    
    # Make the request
    response = test_client.post("/generate/content/", json=sample_content_request)
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["brand_name"] == sample_content_request["brand_name"]
    assert data["content_type"] == sample_content_request["content_type"]
    assert "title" in data
    assert "content" in data
    assert "meta_description" in data
    assert "suggested_tags" in data
    assert "generation_date" in data


@patch("app.routers.content_router.generate_content")
def test_generate_content_endpoint_error(mock_generate_content, test_client, override_get_db,
                                        sample_content_request):
    """Test content generation endpoint with error."""
    # Setup the mock to raise an exception
    mock_generate_content.side_effect = Exception("Test error")
    
    # Make the request
    response = test_client.post("/generate/content/", json=sample_content_request)
    
    # Check the response
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Content generation failed" in data["detail"]

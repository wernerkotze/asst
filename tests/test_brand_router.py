import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime

from app.models.persona import BrandAnalysisRequest, PersonaProfile


@pytest.fixture
def sample_brand_request():
    """Sample brand analysis request for testing."""
    return {
        "brand_name": "Test Brand",
        "industry": "Technology",
        "pinterest_board": "username/test-board",
        "keywords": ["test", "brand", "tech"]
    }


@pytest.fixture
def sample_brand_response():
    """Sample brand analysis response for testing."""
    return {
        "id": "persona_12345",
        "pipelineId": None,
        "brand_name": "Test Brand",
        "industry": "Technology",
        "name": "Vintage Cozy",
        "colors": ["#C16639", "#708D81", "#F5A9B8"],
        "tone_keywords": ["playful", "cozy", "vintage"],
        "style_keywords": ["home", "retro", "comfort"],
        "content_themes": ["home", "retro", "comfort"],
        "voice_description": "Warm, nostalgic, friendly tone",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }


@patch("app.routers.brand_router.analyze_brand")
def test_analyze_brand_endpoint_success(mock_analyze_brand, test_client, override_get_db, 
                                        sample_brand_request, sample_brand_response):
    """Test successful brand analysis endpoint."""
    # Setup the mock to return the sample response directly
    mock_analyze_brand.return_value = sample_brand_response
    
    # Make the request
    response = test_client.post("/analyze/brand/", json=sample_brand_request)
    
    # Check the response
    assert response.status_code == 201
    data = response.json()
    assert data["brand_name"] == sample_brand_request["brand_name"]
    assert data["industry"] == sample_brand_request["industry"]
    assert "tone_keywords" in data
    assert "style_keywords" in data
    assert "content_themes" in data
    assert "voice_description" in data
    assert "createdAt" in data


@patch("app.routers.brand_router.analyze_brand")
def test_analyze_brand_endpoint_error(mock_analyze_brand, test_client, override_get_db,
                                     sample_brand_request):
    """Test brand analysis endpoint with error."""
    # Setup the mock to raise an exception
    mock_analyze_brand.side_effect = Exception("Test error")
    
    # Make the request
    response = test_client.post("/analyze/brand/", json=sample_brand_request)
    
    # Check the response
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Failed to analyze Pinterest board" in data["detail"]

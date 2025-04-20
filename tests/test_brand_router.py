import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime

from app.models.schemas import BrandAnalysisRequest, BrandAnalysisResponse


@pytest.fixture
def sample_brand_request():
    """Sample brand analysis request for testing."""
    return {
        "brand_name": "Test Brand",
        "industry": "Technology",
        "keywords": ["test", "brand", "tech"],
        "time_period": "last_month"
    }


@pytest.fixture
def sample_brand_response():
    """Sample brand analysis response for testing."""
    return {
        "brand_name": "Test Brand",
        "sentiment_score": 0.75,
        "market_position": {
            "rank": 5,
            "market_share": "8%",
            "growth_trend": "stable"
        },
        "strengths": ["Quality products", "Brand recognition"],
        "weaknesses": ["Limited market reach", "High prices"],
        "recommendations": ["Expand to new markets", "Adjust pricing strategy"],
        "analysis_date": datetime.now().isoformat()
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
    assert response.status_code == 200
    data = response.json()
    assert data["brand_name"] == sample_brand_request["brand_name"]
    assert "sentiment_score" in data
    assert "market_position" in data
    assert "strengths" in data
    assert "weaknesses" in data
    assert "recommendations" in data
    assert "analysis_date" in data


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
    assert "Brand analysis failed" in data["detail"]

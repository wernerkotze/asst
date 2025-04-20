import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime

from app.models.schemas import CompetitorAnalysisRequest, CompetitorAnalysisResponse, CompetitorInfo


@pytest.fixture
def sample_competitor_request():
    """Sample competitor analysis request for testing."""
    return {
        "brand_name": "Test Brand",
        "industry": "Technology",
        "competitors": [
            {
                "name": "Competitor A",
                "website": "https://competitora.com",
                "market_share": "20%"
            },
            {
                "name": "Competitor B",
                "website": "https://competitorb.com",
                "market_share": "15%"
            }
        ],
        "analysis_depth": "standard"
    }


@pytest.fixture
def sample_competitor_response():
    """Sample competitor analysis response for testing."""
    return {
        "brand_name": "Test Brand",
        "industry": "Technology",
        "competitors": [
            {
                "name": "Competitor A",
                "strengths": ["Market leader", "Strong R&D"],
                "weaknesses": ["High prices", "Poor customer service"],
                "market_share": "20%",
                "sentiment_score": 0.65
            },
            {
                "name": "Competitor B",
                "strengths": ["Innovative products", "Good pricing"],
                "weaknesses": ["Limited reach", "New to market"],
                "market_share": "15%",
                "sentiment_score": 0.72
            }
        ],
        "competitive_landscape": {
            "market_concentration": "medium",
            "entry_barriers": "moderate",
            "disruption_potential": "high"
        },
        "opportunities": ["Underserved segments", "International expansion"],
        "threats": ["New entrants", "Regulatory changes"],
        "analysis_date": datetime.now().isoformat()
    }


@patch("app.routers.competitor_router.analyze_competitors")
def test_analyze_competitors_endpoint_success(mock_analyze_competitors, test_client, override_get_db,
                                             sample_competitor_request, sample_competitor_response):
    """Test successful competitor analysis endpoint."""
    # Setup the mock to return the sample response directly
    mock_analyze_competitors.return_value = sample_competitor_response
    
    # Make the request
    response = test_client.post("/analyze/competitors/", json=sample_competitor_request)
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["brand_name"] == sample_competitor_request["brand_name"]
    assert data["industry"] == sample_competitor_request["industry"]
    assert "competitors" in data
    assert len(data["competitors"]) == len(sample_competitor_response["competitors"])
    assert "competitive_landscape" in data
    assert "opportunities" in data
    assert "threats" in data
    assert "analysis_date" in data


@patch("app.routers.competitor_router.analyze_competitors")
def test_analyze_competitors_endpoint_error(mock_analyze_competitors, test_client, override_get_db,
                                          sample_competitor_request):
    """Test competitor analysis endpoint with error."""
    # Setup the mock to raise an exception
    mock_analyze_competitors.side_effect = Exception("Test error")
    
    # Make the request
    response = test_client.post("/analyze/competitors/", json=sample_competitor_request)
    
    # Check the response
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "Competitor analysis failed" in data["detail"]

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime

from app.models.competitor import CompetitorAnalysisRequest, ContentFramework


@pytest.fixture
def sample_competitor_request():
    """Sample competitor analysis request for testing."""
    return {
        "seedAccounts": ["ChelseaFC", "talkchelsea"],
        "pipelineId": "pipeline_67890",
        "tweetLimit": 200
    }


@pytest.fixture
def sample_competitor_response():
    """Sample competitor analysis response for testing."""
    return {
        "id": "framework_12345",
        "pipelineId": "pipeline_67890",
        "seedAccounts": ["ChelseaFC", "talkchelsea"],
        "contentCategories": {"news": 0.4, "meme": 0.3, "opinion": 0.3},
        "postingFrequency": {"perDay": 3, "perWeek": 21},
        "peakTimes": {"hours": [12, 18], "days": ["Sat", "Tue"]},
        "hashtagStrategy": ["#ChelseaFC", "#CFC", "#KTBFFH"],
        "stylePresets": ["witty", "concise"],
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
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
    assert response.status_code == 201
    data = response.json()
    assert "seedAccounts" in data
    assert data["seedAccounts"] == sample_competitor_response["seedAccounts"]
    assert "contentCategories" in data
    assert "postingFrequency" in data
    assert "peakTimes" in data
    assert "hashtagStrategy" in data
    assert "stylePresets" in data
    assert "createdAt" in data
    assert "updatedAt" in data


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
    assert "Twitter analysis failed" in data["detail"]

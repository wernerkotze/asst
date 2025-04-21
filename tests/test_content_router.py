import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime

from app.models.schemas import ContentGenerationRequest, ContentGenerationResponse
from app.models.content_generator import (
    ContentSource, ContentRetrievalRequest, ContentEnhanceRequest,
    ContentPersonalizeRequest, ContentImageRequest, ContentFormatRequest
)


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
    # Setup the mock to return the sample response directly
    mock_generate_content.return_value = sample_content_response
    
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


@pytest.fixture
def sample_retrieve_content_request():
    """Sample content retrieval request for testing."""
    return {
        "pipelineId": "pipeline_123",
        "sources": ["news", "sports"],
        "limit": 10
    }


@pytest.fixture
def sample_enhance_content_request():
    """Sample content enhancement request for testing."""
    return {
        "rawContentIds": ["raw_1", "raw_2"],
        "pipelineId": "pipeline_123"
    }


@pytest.fixture
def sample_personalize_content_request():
    """Sample content personalization request for testing."""
    return {
        "enhancedContentId": "enhanced_123",
        "personaId": "persona_123",
        "stylePreset": "enthusiastic"
    }


@pytest.fixture
def sample_image_request():
    """Sample image generation request for testing."""
    return {
        "text": "Chelsea FC wins the Premier League",
        "method": "dalle"
    }


@pytest.fixture
def sample_format_content_request():
    """Sample content formatting request for testing."""
    return {
        "personalizedContentId": "personalized_123",
        "channel": "twitter",
        "mediaUrls": ["https://example.com/image1.jpg"]
    }


@patch("app.routers.content_generator_router.retrieve_content")
def test_retrieve_content_endpoint_success(mock_retrieve_content, test_client, override_get_db,
                                           sample_retrieve_content_request):
    """Test successful content retrieval endpoint."""
    # Setup the mock to return sample data
    mock_retrieve_content.return_value = [
        {
            "id": "raw_1",
            "source": "news",
            "title": "Test News",
            "body": "Test news content",
            "url": "https://example.com/news",
            "publishedAt": datetime.now().isoformat(),
            "author": "Test Author",
            "imageUrl": "https://example.com/image.jpg",
            "tags": ["News", "Test"]
        }
    ]
    
    # Make the request
    response = test_client.post("/content/retrieve", json=sample_retrieve_content_request)
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "raw_1"
    assert data[0]["source"] == "news"


@patch("app.routers.content_generator_router.enhance_content")
def test_enhance_content_endpoint_success(mock_enhance_content, test_client, override_get_db,
                                         sample_enhance_content_request):
    """Test successful content enhancement endpoint."""
    # Setup the mock to return sample data
    mock_enhance_content.return_value = [
        {
            "rawContentId": "raw_1",
            "enhancedText": "Enhanced test content",
            "sentiment": "positive",
            "suggestedHashtags": ["#Test", "#Content"],
            "suggestedMedia": ["https://example.com/suggested.jpg"]
        }
    ]
    
    # Make the request
    response = test_client.post("/content/enhance", json=sample_enhance_content_request)
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["rawContentId"] == "raw_1"
    assert "enhancedText" in data[0]
    assert "sentiment" in data[0]
    assert "suggestedHashtags" in data[0]


@patch("app.routers.content_generator_router.personalize_content")
def test_personalize_content_endpoint_success(mock_personalize_content, test_client, override_get_db,
                                              sample_personalize_content_request):
    """Test successful content personalization endpoint."""
    # Setup the mock to return sample data
    mock_personalize_content.return_value = {
        "enhancedContentId": "enhanced_123",
        "personalizedText": "INCREDIBLE! Chelsea FC wins again! #CFC",
        "personaId": "persona_123",
        "stylePreset": "enthusiastic"
    }
    
    # Make the request
    response = test_client.post("/content/personalize", json=sample_personalize_content_request)
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["enhancedContentId"] == "enhanced_123"
    assert data["personaId"] == "persona_123"
    assert "personalizedText" in data
    assert "stylePreset" in data


@patch("app.routers.content_generator_router.generate_image")
def test_generate_image_endpoint_success(mock_generate_image, test_client, override_get_db,
                                        sample_image_request):
    """Test successful image generation endpoint."""
    # Setup the mock to return sample data
    mock_generate_image.return_value = "https://example.com/generated_image.jpg"
    
    # Make the request
    response = test_client.post("/content/image", json=sample_image_request)
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "https://example.com/generated_image.jpg" == data


@patch("app.routers.content_generator_router.format_content")
def test_format_content_endpoint_success(mock_format_content, test_client, override_get_db,
                                         sample_format_content_request):
    """Test successful content formatting endpoint."""
    # Setup the mock to return sample data
    mock_format_content.return_value = {
        "personalizedContentId": "personalized_123",
        "formattedText": "INCREDIBLE! Chelsea FC wins again! #CFC",
        "channel": "twitter",
        "mediaUrls": ["https://example.com/image1.jpg"],
        "id": "formatted_123"
    }
    
    # Make the request
    response = test_client.post("/content/format", json=sample_format_content_request)
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["personalizedContentId"] == "personalized_123"
    assert data["channel"] == "twitter"
    assert "formattedText" in data
    assert "mediaUrls" in data

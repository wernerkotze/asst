import pytest
from unittest.mock import patch, AsyncMock
import asyncio
from datetime import datetime

from app.models.content_generator import (
    ContentSource, RawContentItem, EnhancedContentItem, PersonalizedContentItem,
    FormattedContentItem, ContentRetrievalRequest, ContentEnhanceRequest,
    ContentPersonalizeRequest, ContentImageRequest, ContentFormatRequest
)
from app.services.content_generator_service import (
    retrieve_content, enhance_content, personalize_content,
    generate_image, format_content, _create_content_items
)


@pytest.fixture
def sample_raw_content_item():
    """Sample raw content item for testing."""
    return RawContentItem(
        id="raw_test_1",
        source=ContentSource.NEWS,
        title="Test Content",
        body="This is test content for Chelsea FC",
        url="https://example.com/test",
        publishedAt=datetime.now(),
        author="Test Author",
        imageUrl="https://example.com/image.jpg",
        tags=["Chelsea", "Test"]
    )


@pytest.fixture
def sample_enhanced_content_item(sample_raw_content_item):
    """Sample enhanced content item for testing."""
    return EnhancedContentItem(
        rawContentId=sample_raw_content_item.id,
        enhancedText="Enhanced content for Chelsea FC with hashtags #CFC #Chelsea",
        sentiment="positive",
        suggestedHashtags=["#CFC", "#Chelsea"],
        suggestedMedia=["https://example.com/images/suggested_1.jpg"]
    )


@pytest.fixture
def sample_personalized_content_item(sample_enhanced_content_item):
    """Sample personalized content item for testing."""
    return PersonalizedContentItem(
        enhancedContentId=sample_enhanced_content_item.rawContentId,
        personalizedText="INCREDIBLE! Chelsea FC wins again! #CFC #Chelsea",
        personaId="persona_123",
        stylePreset="enthusiastic"
    )


@pytest.fixture
def sample_formatted_content_item(sample_personalized_content_item):
    """Sample formatted content item for testing."""
    return FormattedContentItem(
        personalizedContentId=sample_personalized_content_item.enhancedContentId,
        formattedText="INCREDIBLE! Chelsea FC wins again! #CFC #Chelsea",
        channel="twitter",
        mediaUrls=["https://example.com/images/formatted_1.jpg"],
        id="formatted_123"
    )


@pytest.mark.asyncio
async def test_create_content_items():
    """Test _create_content_items helper function."""
    items = [
        {
            "title": "Test 1",
            "body": "Test body 1",
            "url": "https://example.com/1",
            "publishedAt": datetime.now(),
            "author": "Author 1",
            "imageUrl": "https://example.com/1.jpg",
            "tags": ["Tag1", "Tag2"]
        },
        {
            "title": "Test 2",
            "body": "Test body 2",
            "url": "https://example.com/2",
            "publishedAt": datetime.now(),
            "author": "Author 2",
            "imageUrl": "https://example.com/2.jpg",
            "tags": ["Tag3", "Tag4"]
        }
    ]
    
    result = await _create_content_items(items, ContentSource.NEWS, 2, "test_prefix")
    
    assert len(result) == 2
    assert result[0].id == "test_prefix_0"
    assert result[0].source == ContentSource.NEWS
    assert result[0].title == "Test 1"
    assert result[1].id == "test_prefix_1"
    assert result[1].source == ContentSource.NEWS
    assert result[1].title == "Test 2"


@pytest.mark.asyncio
async def test_retrieve_content():
    """Test retrieve_content function."""
    request = ContentRetrievalRequest(
        pipelineId="pipeline_123",
        sources=[ContentSource.NEWS, ContentSource.SPORTS],
        limit=4
    )
    
    # Mock the fetch functions to return known data
    with patch('app.services.content_generator_service._fetch_news_content') as mock_news, \
         patch('app.services.content_generator_service._fetch_sports_content') as mock_sports:
        
        # Setup mocks
        mock_news.return_value = [
            RawContentItem(
                id="raw_news_1",
                source=ContentSource.NEWS,
                title="News 1",
                body="News body 1",
                url="https://example.com/news1",
                publishedAt=datetime.now(),
                author="News Author 1",
                imageUrl="https://example.com/news1.jpg",
                tags=["News", "Tag1"]
            )
        ]
        
        mock_sports.return_value = [
            RawContentItem(
                id="raw_sports_1",
                source=ContentSource.SPORTS,
                title="Sports 1",
                body="Sports body 1",
                url="https://example.com/sports1",
                publishedAt=datetime.now(),
                author="Sports Author 1",
                imageUrl="https://example.com/sports1.jpg",
                tags=["Sports", "Tag1"]
            )
        ]
        
        # Call the function
        result = await retrieve_content(request, AsyncMock())
        
        # Check results
        assert len(result) == 2
        assert result[0].id == "raw_news_1"
        assert result[0].source == ContentSource.NEWS
        assert result[1].id == "raw_sports_1"
        assert result[1].source == ContentSource.SPORTS
        
        # Verify mocks were called correctly
        mock_news.assert_called_once_with(2)  # limit divided by 2 sources
        mock_sports.assert_called_once_with(2)  # limit divided by 2 sources


@pytest.mark.asyncio
async def test_retrieve_content_empty_sources():
    """Test retrieve_content function with empty sources."""
    request = ContentRetrievalRequest(
        pipelineId="pipeline_123",
        sources=[],
        limit=4
    )
    
    # Call the function
    result = await retrieve_content(request, AsyncMock())
    
    # Check results
    assert len(result) == 0


@pytest.mark.asyncio
async def test_enhance_content():
    """Test enhance_content function."""
    request = ContentEnhanceRequest(
        rawContentIds=["raw_1", "raw_2"],
        pipelineId="pipeline_123"
    )
    
    # Call the function
    result = await enhance_content(request, AsyncMock())
    
    # Check results
    assert len(result) == 2
    assert result[0].rawContentId == "raw_1"
    assert result[1].rawContentId == "raw_2"
    assert all(item.sentiment in ["positive", "neutral", "negative"] for item in result)
    assert all(len(item.suggestedHashtags) > 0 for item in result)
    assert all(len(item.suggestedMedia) > 0 for item in result)


@pytest.mark.asyncio
async def test_enhance_content_empty_ids():
    """Test enhance_content function with empty content IDs."""
    request = ContentEnhanceRequest(
        rawContentIds=[],
        pipelineId="pipeline_123"
    )
    
    # Call the function
    result = await enhance_content(request, AsyncMock())
    
    # Check results
    assert len(result) == 0


@pytest.mark.asyncio
async def test_personalize_content():
    """Test personalize_content function."""
    request = ContentPersonalizeRequest(
        enhancedContentId="enhanced_123",
        personaId="persona_123",
        stylePreset="witty"
    )
    
    # Call the function
    result = await personalize_content(request, AsyncMock())
    
    # Check results
    assert result.enhancedContentId == "enhanced_123"
    assert result.personaId == "persona_123"
    assert result.stylePreset == "witty"
    assert "witty" in result.personalizedText.lower() or "#cfc" in result.personalizedText.lower()


@pytest.mark.asyncio
async def test_personalize_content_validation_error():
    """Test personalize_content function with validation error."""
    request = ContentPersonalizeRequest(
        enhancedContentId="",  # Empty ID should cause validation error
        personaId="persona_123",
        stylePreset="witty"
    )
    
    # Call the function and expect a ValueError
    with pytest.raises(ValueError):
        await personalize_content(request, AsyncMock())


@pytest.mark.asyncio
async def test_generate_image():
    """Test generate_image function."""
    request = ContentImageRequest(
        text="Chelsea FC wins the Premier League",
        method="dalle"
    )
    
    # Call the function
    result = await generate_image(request, AsyncMock())
    
    # Check results
    assert result is not None
    assert "example.com" in result
    assert "dalle" in result


@pytest.mark.asyncio
async def test_generate_image_empty_text():
    """Test generate_image function with empty text."""
    request = ContentImageRequest(
        text="",
        method="dalle"
    )
    
    # Call the function
    result = await generate_image(request, AsyncMock())
    
    # Check results
    assert "default_placeholder" in result


@pytest.mark.asyncio
async def test_format_content():
    """Test format_content function."""
    request = ContentFormatRequest(
        personalizedContentId="personalized_123",
        channel="twitter",
        mediaUrls=["https://example.com/image1.jpg"]
    )
    
    # Call the function
    result = await format_content(request, AsyncMock())
    
    # Check results
    assert result.personalizedContentId == "personalized_123"
    assert result.channel == "twitter"
    assert len(result.mediaUrls) == 1
    assert result.mediaUrls[0] == "https://example.com/image1.jpg"
    assert len(result.formattedText) <= 280  # Twitter character limit


@pytest.mark.asyncio
async def test_format_content_validation_error():
    """Test format_content function with validation error."""
    request = ContentFormatRequest(
        personalizedContentId="",  # Empty ID should cause validation error
        channel="twitter",
        mediaUrls=["https://example.com/image1.jpg"]
    )
    
    # Call the function and expect a ValueError
    with pytest.raises(ValueError):
        await format_content(request, AsyncMock())


@pytest.mark.asyncio
async def test_format_content_unsupported_channel():
    """Test format_content function with unsupported channel."""
    request = ContentFormatRequest(
        personalizedContentId="personalized_123",
        channel="unsupported_channel",  # This should default to twitter
        mediaUrls=["https://example.com/image1.jpg"]
    )
    
    # Call the function
    result = await format_content(request, AsyncMock())
    
    # Check results
    assert result.channel == "twitter"  # Should default to twitter

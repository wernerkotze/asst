import pytest
from unittest.mock import patch, AsyncMock
import asyncio

from app.services.brand_service import extract_board_id, fetch_pinterest_pins, analyze_brand, analyze_colors, analyze_text
from app.models.persona import PersonaProfile, BrandAnalysisRequest, PinterestPin


@pytest.mark.asyncio
async def test_extract_board_id_with_url():
    """Test extract_board_id with a Pinterest URL."""
    # Test with a full URL
    board_url = "https://www.pinterest.com/username/boardname/"
    result = await extract_board_id(board_url)
    assert result == "username/boardname"
    
    # Test with a URL without trailing slash
    board_url = "https://pinterest.com/username/boardname"
    result = await extract_board_id(board_url)
    assert result == "username/boardname"


@pytest.mark.asyncio
async def test_extract_board_id_with_id():
    """Test extract_board_id with a board ID."""
    # Test with a board ID in the format username/boardname
    board_id = "username/boardname"
    result = await extract_board_id(board_id)
    assert result == "username/boardname"
    
    # Test with a non-standard input
    board_id = "some-random-string"
    result = await extract_board_id(board_id)
    assert result == "some-random-string"


@pytest.mark.asyncio
@patch('app.services.brand_service.get_settings')
async def test_fetch_pinterest_pins(mock_get_settings):
    """Test fetch_pinterest_pins function."""
    # Setup mock settings
    mock_settings = AsyncMock()
    mock_settings.pinterest_api_key = "test_api_key"
    mock_get_settings.return_value = mock_settings
    
    # Call the function
    result = await fetch_pinterest_pins("username/boardname", 10)
    
    # Check results
    assert len(result) == 10
    assert all(isinstance(pin, PinterestPin) for pin in result)
    assert all(pin.id.startswith("pin_") for pin in result)
    assert all(pin.description for pin in result)
    assert all(pin.imageUrl for pin in result)
    assert all(pin.link for pin in result)


@pytest.mark.asyncio
@patch('app.services.brand_service.fetch_pinterest_pins')
@patch('app.services.brand_service.analyze_colors')
@patch('app.services.brand_service.analyze_text')
async def test_analyze_brand(mock_analyze_text, mock_analyze_colors, mock_fetch_pins):
    """Test analyze_brand function."""
    # Setup mock response for fetch_pinterest_pins
    mock_fetch_pins.return_value = [
        PinterestPin(
            id="pin1",
            description="Chelsea wins the Premier League #CFC #Chelsea #Football",
            imageUrl="https://example.com/image1.jpg",
            link="https://example.com/link1"
        ),
        PinterestPin(
            id="pin2",
            description="Chelsea FC unveils new home kit for the season #ChelseaFC #Kit",
            imageUrl="https://example.com/image2.jpg",
            link="https://example.com/link2"
        )
    ]
    
    # Setup mock response for analyze_colors
    mock_analyze_colors.return_value = ["#C16639", "#708D81", "#F5A9B8"]
    
    # Setup mock response for analyze_text
    mock_analyze_text.return_value = {
        "traits": ["playful", "cozy", "vintage"],
        "keywords": ["home", "retro", "comfort"],
        "voiceDescription": "Warm, nostalgic, friendly tone"
    }
    
    # Create request
    request = BrandAnalysisRequest(
        brand_name="Chelsea FC",
        pinterest_board="username/chelsea-board",
        industry="Sports"
    )
    
    # Call the function
    result = await analyze_brand(request, AsyncMock())
    
    # Check results
    assert isinstance(result, PersonaProfile)
    assert result.brand_name == "Chelsea FC"
    assert result.industry == "Sports"
    assert len(result.tone_keywords) > 0
    assert len(result.style_keywords) > 0
    assert len(result.content_themes) > 0
    
    # Verify mock was called correctly
    mock_fetch_pins.assert_called_once_with("username/chelsea-board")


@pytest.mark.asyncio
@patch('app.services.brand_service.fetch_pinterest_pins')
@patch('app.services.brand_service.analyze_colors')
@patch('app.services.brand_service.analyze_text')
async def test_analyze_brand_empty_pins(mock_analyze_text, mock_analyze_colors, mock_fetch_pins):
    """Test analyze_brand with empty pins."""
    # Setup mock to return empty list
    mock_fetch_pins.return_value = []
    
    # Setup mock response for analyze_colors
    mock_analyze_colors.return_value = ["#C16639", "#708D81", "#F5A9B8"]
    
    # Setup mock response for analyze_text
    mock_analyze_text.return_value = {
        "traits": ["playful", "cozy", "vintage"],
        "keywords": ["home", "retro", "comfort"],
        "voiceDescription": "Warm, nostalgic, friendly tone"
    }
    
    # Create request
    request = BrandAnalysisRequest(
        brand_name="Chelsea FC",
        pinterest_board="username/chelsea-board",
        industry="Sports"
    )
    
    # Call the function
    result = await analyze_brand(request, AsyncMock())
    
    # Check results
    assert isinstance(result, PersonaProfile)
    assert result.brand_name == "Chelsea FC"
    assert result.industry == "Sports"
    # Should have values from the mocked analyze_text and analyze_colors
    assert len(result.tone_keywords) > 0
    assert len(result.style_keywords) > 0
    assert len(result.content_themes) > 0
    
    # Verify mock was called correctly
    mock_fetch_pins.assert_called_once_with("username/chelsea-board")


@pytest.mark.asyncio
@patch('app.services.brand_service.fetch_pinterest_pins')
async def test_analyze_brand_error_handling(mock_fetch_pins):
    """Test analyze_brand error handling."""
    # Setup mock to raise an exception
    mock_fetch_pins.side_effect = Exception("Test error")
    
    # Create request
    request = BrandAnalysisRequest(
        brand_name="Chelsea FC",
        pinterest_board="username/chelsea-board",
        industry="Sports"
    )
    
    # Call the function and expect it to handle the error
    result = await analyze_brand(request, AsyncMock())
    
    # Check results - should return a default profile
    assert isinstance(result, PersonaProfile)
    assert result.brand_name == "Chelsea FC"
    assert result.industry == "Sports"
    assert len(result.tone_keywords) > 0
    assert len(result.style_keywords) > 0
    assert len(result.content_themes) > 0

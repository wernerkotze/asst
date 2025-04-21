import logging
import re
from typing import Any, Dict, List
from urllib.parse import urlparse

from app.models.persona import PersonaProfile, BrandAnalysisRequest, PinterestPin

# Set up logging
logger = logging.getLogger(__name__)

async def extract_board_id(board_url_or_id: str) -> str:
    """
    Extract the board ID from a Pinterest board URL or ID string.
    
    Args:
        board_url_or_id: Pinterest board URL or ID
        
    Returns:
        str: Extracted board ID in the format 'username/boardname'
    """
    # If it's already in the format username/boardname, return as is
    if re.match(r'^[\w-]+/[\w-]+$', board_url_or_id):
        return board_url_or_id
    
    # If it's a URL, extract the path
    parsed_url = urlparse(board_url_or_id)
    if parsed_url.netloc in ['pinterest.com', 'www.pinterest.com']:
        # Extract username/boardname from path
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return f"{path_parts[0]}/{path_parts[1]}"
    
    # If we couldn't parse it, return as is and let the Pinterest API handle it
    return board_url_or_id

async def fetch_pinterest_pins(board_id: str, limit: int = 100) -> List[PinterestPin]:
    """
    Fetch pins from a Pinterest board using the Pinterest API.
    
    Args:
        board_id: Pinterest board ID in the format 'username/boardname'
        limit: Maximum number of pins to fetch
        
    Returns:
        List[PinterestPin]: List of pins from the board
    """
    logger.info(f"Fetching pins from Pinterest board: {board_id}")
    
    settings = get_settings()
    api_key = settings.pinterest_api_key
    
    # In a real implementation, this would use the Pinterest API
    # For now, we'll return mock data
    mock_pins = [
        PinterestPin(
            id=f"pin_{i}",
            description=f"Pin {i} description with {theme} theme",
            imageUrl=f"https://example.com/pin_{i}.jpg",
            link=f"https://example.com/pin_{i}"
        )
        for i, theme in enumerate([
            "vintage", "cozy", "warm", "nostalgic", "retro", 
            "comfortable", "homey", "classic", "traditional", "rustic"
        ])
    ]
    
    return mock_pins[:limit]

async def analyze_colors(pins: List[PinterestPin]) -> List[str]:
    """
    Analyze dominant colors from pin images.
    
    Args:
        pins: List of Pinterest pins
        
    Returns:
        List[str]: List of dominant color hex codes
    """
    logger.info(f"Analyzing colors from {len(pins)} pins")
    
    # In a real implementation, this would use ColorThief or a similar library
    # For now, we'll return mock data
    mock_colors = [
        "#C16639", "#708D81", "#F5A9B8", "#D1A280", "#8B5D33",
        "#BFCAD6", "#E8D2AE", "#7D4F50", "#B58B6D", "#6E8C91"
    ]
    
    # Return top 5 colors
    return mock_colors[:5]

async def analyze_text(pins: List[PinterestPin]) -> Dict[str, Any]:
    """
    Analyze pin descriptions to extract tone, keywords, and thematic traits.
    
    Args:
        pins: List of Pinterest pins
        
    Returns:
        Dict: Dictionary containing extracted traits, keywords, and voice description
    """
    logger.info(f"Analyzing text from {len(pins)} pins")
    
    # In a real implementation, this would use OpenAI or a similar service
    # For now, we'll return mock data
    mock_analysis = {
        "traits": ["playful", "cozy", "vintage", "warm", "nostalgic"],
        "keywords": ["home", "retro", "comfort", "classic", "traditional"],
        "voiceDescription": "Warm, nostalgic, friendly tone with a focus on comfort and tradition"
    }
    
    return mock_analysis

async def analyze_brand(request: BrandAnalysisRequest, db: Any) -> PersonaProfile:
    """
    Analyze a brand based on a Pinterest board and generate a persona profile.
    
    Args:
        request: The brand analysis request containing board ID and assets
        db: Database connection
        
    Returns:
        PersonaProfile: The generated persona profile
    """
    board_id = await extract_board_id(request.boardId)
    logger.info(f"Analyzing brand from Pinterest board: {board_id}")
    
    try:
        # 1. Fetch pins from Pinterest board
        pins = await fetch_pinterest_pins(board_id)
        logger.info(f"Fetched {len(pins)} pins from board")
        
        # 2. Analyze colors from pin images
        colors = await analyze_colors(pins)
        logger.info(f"Extracted dominant colors: {colors}")
        
        # 3. Analyze text from pin descriptions
        text_analysis = await analyze_text(pins)
        logger.info(f"Completed text analysis")
        
        # 4. Generate persona profile
        persona = PersonaProfile(
            pipelineId=request.pipelineId,
            name="Vintage Cozy",  # In a real implementation, this would be generated from the analysis
            colors=colors,
            traits=text_analysis["traits"],
            voiceDescription=text_analysis["voiceDescription"],
            keywords=text_analysis["keywords"]
        )
        
        # 5. Save to database
        if db:
            # In a real implementation, this would save to the database
            # persona.id = await db.personas.insert_one(persona.dict()).inserted_id
            persona.id = "persona_" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        return persona
    except Exception as e:
        logger.error(f"Error analyzing brand: {str(e)}")
        raise

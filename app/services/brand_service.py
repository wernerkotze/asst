import logging
import re
import io
import tempfile
from typing import Any, Dict, List
from datetime import datetime
from urllib.parse import urlparse

import requests
from PIL import Image
from colorthief import ColorThief

from app.config import get_settings
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
    Fetch pins from a Pinterest board using the Pinterest API v5.
    
    Args:
        board_id: Pinterest board ID in the format 'username/boardname'
        limit: Maximum number of pins to fetch
        
    Returns:
        List[PinterestPin]: List of pins from the board
    """
    logger.info(f"Fetching pins from Pinterest board: {board_id}")
    
    settings = get_settings()
    access_token = settings.pinterest_access_token
    
    if not access_token:
        logger.warning("Pinterest access token not found. Using mock data.")
        # Fallback to mock data if no access token is available
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
    
    try:
        # Pinterest API v5 endpoint for board pins
        url = f"https://api.pinterest.com/v5/boards/{board_id}/pins"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept-Language": "en-US",
            "Content-Type": "application/json"
        }
        
        params = {
            "page_size": min(limit, 100),  # API limit is 100 per page
            "bookmark": ""
        }
        
        pins = []
        total_pins = 0
        
        # Paginate through results if needed
        while total_pins < limit:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                logger.error(f"Pinterest API error: {response.status_code} - {response.text}")
                raise Exception(f"Failed to fetch pins: {response.text}")
            
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                break
            
            # Process each pin
            for item in items:
                pin_id = item.get("id")
                description = item.get("description", "")
                link = item.get("link")
                
                # Get the image URL from the media object
                media = item.get("media", {})
                images = media.get("images", {})
                
                # Get the largest image available
                image_url = None
                for size in ["original", "1200x", "600x"]:
                    if size in images:
                        image_url = images[size].get("url")
                        if image_url:
                            break
                
                if not image_url and "image_large_url" in media:
                    image_url = media["image_large_url"]
                
                if pin_id and image_url:
                    pins.append(PinterestPin(
                        id=pin_id,
                        description=description,
                        imageUrl=image_url,
                        link=link
                    ))
                    
                    total_pins += 1
                    if total_pins >= limit:
                        break
            
            # Check if there are more pages
            bookmark = data.get("bookmark")
            if not bookmark or bookmark == params["bookmark"]:
                break
            
            params["bookmark"] = bookmark
        
        logger.info(f"Successfully fetched {len(pins)} pins from board {board_id}")
        return pins
        
    except Exception as e:
        logger.error(f"Error fetching Pinterest pins: {str(e)}")
        # Fallback to mock data in case of error
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
    Analyze dominant colors from pin images using ColorThief.
    
    Args:
        pins: List of Pinterest pins
        
    Returns:
        List[str]: List of dominant color hex codes
    """
    logger.info(f"Analyzing colors from {len(pins)} pins")
    
    # Fallback colors in case of errors
    fallback_colors = [
        "#C16639", "#708D81", "#F5A9B8", "#D1A280", "#8B5D33",
        "#BFCAD6", "#E8D2AE", "#7D4F50", "#B58B6D", "#6E8C91"
    ]
    
    if not pins:
        logger.warning("No pins provided for color analysis")
        return fallback_colors[:5]
    
    colors = []
    
    try:
        for pin in pins:
            try:
                # Download the image
                response = requests.get(pin.imageUrl, stream=True)
                
                if response.status_code != 200:
                    logger.warning(f"Failed to download image: {pin.imageUrl}")
                    continue
                
                # Create a temporary file to store the image
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_file_path = temp_file.name
                
                # Use ColorThief to extract the dominant color
                color_thief = ColorThief(temp_file_path)
                dominant_color = color_thief.get_color(quality=1)
                
                # Convert RGB to hex
                hex_color = '#{:02x}{:02x}{:02x}'.format(dominant_color[0], dominant_color[1], dominant_color[2])
                colors.append(hex_color)
                
                # Also get the color palette (for future use)
                # palette = color_thief.get_palette(color_count=5)
                
                # Clean up the temporary file
                import os
                os.unlink(temp_file_path)
                
            except Exception as e:
                logger.warning(f"Error analyzing color for pin {pin.id}: {str(e)}")
        
        # If we couldn't extract any colors, use fallback
        if not colors:
            logger.warning("No colors could be extracted, using fallback colors")
            return fallback_colors[:5]
        
        # Return the top 5 most common colors (or fewer if we have less than 5)
        from collections import Counter
        color_counts = Counter(colors)
        top_colors = [color for color, _ in color_counts.most_common(5)]
        
        return top_colors
        
    except Exception as e:
        logger.error(f"Error in color analysis: {str(e)}")
        return fallback_colors[:5]

async def analyze_text(pins: List[PinterestPin]) -> Dict[str, Any]:
    """
    Analyze pin descriptions to extract tone, keywords, and thematic traits using OpenAI.
    
    Args:
        pins: List of Pinterest pins
        
    Returns:
        Dict: Dictionary containing extracted traits, keywords, and voice description
    """
    logger.info(f"Analyzing text from {len(pins)} pins")
    
    # Fallback analysis in case of errors
    fallback_analysis = {
        "traits": ["playful", "cozy", "vintage", "warm", "nostalgic"],
        "keywords": ["home", "retro", "comfort", "classic", "traditional"],
        "voiceDescription": "Warm, nostalgic, friendly tone with a focus on comfort and tradition"
    }
    
    if not pins:
        logger.warning("No pins provided for text analysis")
        return fallback_analysis
    
    try:
        # Collect all pin descriptions
        descriptions = [pin.description for pin in pins if pin.description]
        
        if not descriptions:
            logger.warning("No descriptions found in pins")
            return fallback_analysis
        
        # Combine descriptions for analysis
        combined_text = "\n".join(descriptions)
        
        # Use OpenAI for text analysis
        settings = get_settings()
        api_key = settings.api_key
        
        if not api_key:
            logger.warning("OpenAI API key not found. Using fallback analysis.")
            return fallback_analysis
        
        import openai
        openai.api_key = api_key
        
        # Create the prompt for OpenAI
        prompt = f"""Analyze the following Pinterest pin descriptions to extract:
        1. Tone keywords (e.g., playful, serious, professional)
        2. Style keywords (e.g., vintage, modern, minimalist)
        3. Content themes (e.g., home, travel, fashion)
        4. A voice description that captures the overall tone and style
        
        Pin Descriptions:
        {combined_text}
        
        Format your response as JSON with these keys: traits, keywords, content_themes, voiceDescription
        """
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or another appropriate model
            messages=[
                {"role": "system", "content": "You are an AI assistant that analyzes text to extract tone, style, and thematic elements."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        # Extract the response
        result_text = response.choices[0].message.content
        
        # Parse the JSON response
        import json
        try:
            result = json.loads(result_text)
            
            # Ensure all required keys are present
            analysis = {
                "traits": result.get("traits", fallback_analysis["traits"]),
                "keywords": result.get("keywords", fallback_analysis["keywords"]),
                "content_themes": result.get("content_themes", fallback_analysis["keywords"][:3]),
                "voiceDescription": result.get("voiceDescription", fallback_analysis["voiceDescription"])
            }
            
            return analysis
            
        except json.JSONDecodeError:
            logger.error(f"Failed to parse OpenAI response as JSON: {result_text}")
            return fallback_analysis
            
    except Exception as e:
        logger.error(f"Error in text analysis: {str(e)}")
        return fallback_analysis

async def analyze_brand(request: BrandAnalysisRequest, db: Any) -> PersonaProfile:
    """
    Analyze a brand based on a Pinterest board and generate a persona profile.
    
    Args:
        request: The brand analysis request containing board ID and assets
        db: Database connection
        
    Returns:
        PersonaProfile: The generated persona profile
    """
    # Use pinterest_board field if available, otherwise try boardId
    board_id_field = getattr(request, 'pinterest_board', None) or getattr(request, 'boardId', '')
    board_id = await extract_board_id(board_id_field)
    logger.info(f"Analyzing brand from Pinterest board: {board_id}")
    
    try:
        # 1. Fetch pins from Pinterest board
        pins = await fetch_pinterest_pins(board_id)
        logger.info(f"Fetched {len(pins)} pins from board")
        
        if not pins:
            raise Exception("No pins could be fetched from the board")
        
        # 2. Analyze colors from pin images
        colors = await analyze_colors(pins)
        logger.info(f"Extracted dominant colors: {colors}")
        
        # 3. Analyze text from pin descriptions
        text_analysis = await analyze_text(pins)
        logger.info(f"Completed text analysis")
        
        # 4. Generate a name for the persona based on the analysis
        persona_name = "Default Profile"
        try:
            # Try to generate a name based on the top traits and keywords
            traits = text_analysis.get("traits", [])
            keywords = text_analysis.get("keywords", [])
            
            if traits and keywords:
                # Take the first trait and keyword to form a name
                trait = traits[0].capitalize()
                keyword = keywords[0].capitalize()
                persona_name = f"{trait} {keyword}"
            elif traits:
                # Use the top two traits
                if len(traits) >= 2:
                    persona_name = f"{traits[0].capitalize()} {traits[1].capitalize()}"
                else:
                    persona_name = f"{traits[0].capitalize()} Style"
            elif keywords:
                # Use the top two keywords
                if len(keywords) >= 2:
                    persona_name = f"{keywords[0].capitalize()} {keywords[1].capitalize()}"
                else:
                    persona_name = f"{keywords[0].capitalize()} Style"
        except Exception as e:
            logger.warning(f"Error generating persona name: {str(e)}")
        
        # 5. Generate persona profile
        persona = PersonaProfile(
            pipelineId=getattr(request, 'pipelineId', None),
            brand_name=request.brand_name,
            industry=request.industry,
            name=persona_name,
            colors=colors,
            tone_keywords=text_analysis.get("traits", []),
            style_keywords=text_analysis.get("keywords", []),
            content_themes=text_analysis.get("content_themes", text_analysis.get("keywords", [])[:3]),
            voice_description=text_analysis.get("voiceDescription", "Warm, friendly tone")
        )
        
        # 6. Save to database
        if db:
            try:
                # In a real implementation with MongoDB
                persona_dict = persona.dict(exclude={"id"})
                result = await db.personas.insert_one(persona_dict)
                persona.id = str(result.inserted_id)
                logger.info(f"Saved persona to database with ID: {persona.id}")
            except Exception as e:
                logger.error(f"Error saving to database: {str(e)}")
                # Fallback to a generated ID if database save fails
                persona.id = "persona_" + datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            # Generate an ID if no database is provided
            persona.id = "persona_" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        return persona
    except Exception as e:
        logger.error(f"Error analyzing brand: {str(e)}")
        # Return a default profile instead of raising an exception
        return PersonaProfile(
            brand_name=request.brand_name,
            industry=request.industry,
            name="Default Profile",
            colors=["#C16639", "#708D81", "#F5A9B8"],
            tone_keywords=["professional", "friendly", "informative"],
            style_keywords=["clean", "modern", "simple"],
            content_themes=["industry news", "tips", "product updates"],
            voice_description="Professional and friendly tone with a focus on providing value"
        )

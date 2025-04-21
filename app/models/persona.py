from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class PersonaProfile(BaseModel):
    """Persona profile derived from brand analysis."""
    id: Optional[str] = Field(None, description="Persona profile ID")
    pipelineId: Optional[str] = Field(None, description="Reference to pipeline")
    brand_name: str = Field(..., description="Name of the brand")
    industry: str = Field(..., description="Industry of the brand")
    name: str = Field(..., description="Name of the persona")
    colors: List[str] = Field(default=[], description="Color hex codes for the brand palette")
    tone_keywords: List[str] = Field(default=[], description="Tone keywords for the persona")
    style_keywords: List[str] = Field(default=[], description="Style keywords for the persona")
    content_themes: List[str] = Field(default=[], description="Content themes for the persona")
    voice_description: str = Field(..., description="Description of the persona's voice")
    createdAt: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updatedAt: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "persona_12345",
                "pipelineId": "pipeline_67890",
                "brand_name": "Chelsea FC",
                "industry": "Sports",
                "name": "Vintage Cozy",
                "colors": ["#C16639", "#708D81", "#F5A9B8"],
                "tone_keywords": ["playful", "cozy", "vintage"],
                "style_keywords": ["home", "retro", "comfort"],
                "content_themes": ["home", "retro", "comfort"],
                "voice_description": "Warm, nostalgic, friendly tone"
            }
        }

class BrandAnalysisRequest(BaseModel):
    """Request for brand analysis from Pinterest board."""
    brand_name: str = Field(..., description="Name of the brand")
    industry: str = Field(..., description="Industry of the brand")
    pinterest_board: str = Field(..., description="Pinterest board ID or URL")
    keywords: List[str] = Field(default=[], description="Keywords associated with the brand")
    pipelineId: Optional[str] = Field(None, description="Pipeline ID to associate with the persona")
    assets: Optional[List[HttpUrl]] = Field(default=[], description="Optional URLs to brand assets")
    
    class Config:
        schema_extra = {
            "example": {
                "brand_name": "Chelsea FC",
                "industry": "Sports",
                "pinterest_board": "username/chelsea-board",
                "keywords": ["football", "premier league", "chelsea"],
                "pipelineId": "pipeline_67890",
                "assets": ["https://example.com/logo.png"]
            }
        }

class PinterestPin(BaseModel):
    """Data model for a Pinterest pin."""
    id: str = Field(..., description="Pinterest pin ID")
    description: str = Field(default="", description="Pin description")
    imageUrl: HttpUrl = Field(..., description="URL to the pin image")
    link: Optional[HttpUrl] = Field(None, description="Link associated with the pin")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "123456789012345678",
                "description": "Cozy vintage living room with warm colors",
                "imageUrl": "https://i.pinimg.com/originals/12/34/56/123456789012345678.jpg",
                "link": "https://example.com/vintage-decor"
            }
        }

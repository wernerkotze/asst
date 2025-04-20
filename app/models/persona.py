from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

class PersonaProfile(BaseModel):
    """Persona profile derived from brand analysis."""
    id: Optional[str] = Field(None, description="Persona profile ID")
    pipelineId: Optional[str] = Field(None, description="Reference to pipeline")
    name: str = Field(..., description="Name of the persona")
    colors: List[str] = Field(default=[], description="Color hex codes for the brand palette")
    traits: List[str] = Field(default=[], description="Personality traits of the persona")
    voiceDescription: str = Field(..., description="Description of the persona's voice")
    keywords: List[str] = Field(default=[], description="Key phrases and terms associated with the persona")
    createdAt: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updatedAt: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "persona_12345",
                "pipelineId": "pipeline_67890",
                "name": "Vintage Cozy",
                "colors": ["#C16639", "#708D81", "#F5A9B8"],
                "traits": ["playful", "cozy", "vintage"],
                "voiceDescription": "Warm, nostalgic, friendly tone",
                "keywords": ["home", "retro", "comfort"]
            }
        }

class BrandAnalysisRequest(BaseModel):
    """Request for brand analysis from Pinterest board."""
    boardId: str = Field(..., description="Pinterest board ID or URL")
    assets: Optional[List[HttpUrl]] = Field(default=[], description="Optional URLs to brand assets")
    pipelineId: Optional[str] = Field(None, description="Pipeline ID to associate with the persona")
    
    class Config:
        schema_extra = {
            "example": {
                "boardId": "username/boardname",
                "assets": ["https://example.com/logo.png"],
                "pipelineId": "pipeline_67890"
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

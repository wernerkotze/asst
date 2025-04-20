from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum

from app.models.content import ContentType, MediaType, ContentStatus

class ContentSource(str, Enum):
    """Source type for content retrieval."""
    NEWS = "news"
    SPORTS = "sports"
    TWITTER = "twitter"
    RSS = "rss"
    CUSTOM = "custom"

class RawContentItem(BaseModel):
    """Raw content item retrieved from external sources."""
    id: Optional[str] = Field(None, description="Content item ID")
    source: ContentSource = Field(..., description="Source of the content")
    title: str = Field(..., description="Title of the content")
    body: str = Field(..., description="Body text of the content")
    url: Optional[HttpUrl] = Field(None, description="URL to the original content")
    publishedAt: Optional[datetime] = Field(None, description="When the content was published")
    author: Optional[str] = Field(None, description="Author of the content")
    imageUrl: Optional[HttpUrl] = Field(None, description="URL to the content image")
    tags: List[str] = Field(default=[], description="Tags associated with the content")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "raw_12345",
                "source": "news",
                "title": "Chelsea wins Premier League",
                "body": "Chelsea FC has won the Premier League after a decisive victory...",
                "url": "https://example.com/news/chelsea-wins",
                "publishedAt": "2025-04-20T15:30:00Z",
                "author": "Sports Reporter",
                "imageUrl": "https://example.com/images/chelsea-win.jpg",
                "tags": ["Chelsea", "Premier League", "Football"]
            }
        }

class EnhancedContentItem(BaseModel):
    """Content item enhanced with hashtags, sentiment, and media suggestions."""
    rawContentId: str = Field(..., description="ID of the raw content item")
    enhancedText: str = Field(..., description="Enhanced text with hashtags")
    sentiment: str = Field(..., description="Sentiment of the content")
    suggestedHashtags: List[str] = Field(default=[], description="Suggested hashtags")
    suggestedMedia: List[str] = Field(default=[], description="Suggested media URLs")
    
    class Config:
        schema_extra = {
            "example": {
                "rawContentId": "raw_12345",
                "enhancedText": "Chelsea wins Premier League! What a performance by the Blues! #CFC #PremierLeague",
                "sentiment": "positive",
                "suggestedHashtags": ["#CFC", "#PremierLeague", "#Champions"],
                "suggestedMedia": ["https://example.com/images/chelsea-win.jpg"]
            }
        }

class PersonalizedContentItem(BaseModel):
    """Content item personalized with AI using persona and style preset."""
    enhancedContentId: str = Field(..., description="ID of the enhanced content item")
    personalizedText: str = Field(..., description="Personalized text using AI")
    personaId: str = Field(..., description="ID of the persona used")
    stylePreset: str = Field(..., description="Style preset used")
    
    class Config:
        schema_extra = {
            "example": {
                "enhancedContentId": "enhanced_12345",
                "personalizedText": "INCREDIBLE! Our boys in blue have done it again! Chelsea are Premier League champions! 🏆 #CFC #PremierLeague",
                "personaId": "persona_67890",
                "stylePreset": "witty"
            }
        }

class FormattedContentItem(BaseModel):
    """Content item formatted for a specific channel."""
    personalizedContentId: str = Field(..., description="ID of the personalized content item")
    formattedText: str = Field(..., description="Formatted text for the channel")
    channel: str = Field(..., description="Channel to publish to")
    mediaUrls: List[str] = Field(default=[], description="Media URLs to include")
    
    class Config:
        schema_extra = {
            "example": {
                "personalizedContentId": "personalized_12345",
                "formattedText": "INCREDIBLE! Our boys in blue have done it again! Chelsea are Premier League champions! 🏆 #CFC #PremierLeague",
                "channel": "twitter",
                "mediaUrls": ["https://storage.asst.ai/media/chelsea-win-generated.jpg"]
            }
        }

class ContentRetrievalRequest(BaseModel):
    """Request to retrieve content based on pipeline settings."""
    pipelineId: str = Field(..., description="ID of the pipeline")
    sources: List[ContentSource] = Field(default=[ContentSource.NEWS], description="Sources to retrieve content from")
    limit: int = Field(default=10, description="Maximum number of items to retrieve")
    
    class Config:
        schema_extra = {
            "example": {
                "pipelineId": "pipeline_12345",
                "sources": ["news", "twitter"],
                "limit": 10
            }
        }

class ContentEnhanceRequest(BaseModel):
    """Request to enhance raw content items."""
    rawContentIds: List[str] = Field(..., description="IDs of raw content items to enhance")
    pipelineId: str = Field(..., description="ID of the pipeline")
    
    class Config:
        schema_extra = {
            "example": {
                "rawContentIds": ["raw_12345", "raw_67890"],
                "pipelineId": "pipeline_12345"
            }
        }

class ContentPersonalizeRequest(BaseModel):
    """Request to personalize enhanced content."""
    enhancedContentId: str = Field(..., description="ID of the enhanced content")
    personaId: str = Field(..., description="ID of the persona to use")
    stylePreset: str = Field(..., description="Style preset to use")
    
    class Config:
        schema_extra = {
            "example": {
                "enhancedContentId": "enhanced_12345",
                "personaId": "persona_67890",
                "stylePreset": "witty"
            }
        }

class ContentImageRequest(BaseModel):
    """Request to generate or fetch images for content."""
    text: str = Field(..., description="Text to generate image for")
    method: str = Field(default="dalle", description="Method to use (dalle, google)")
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Chelsea FC winning the Premier League",
                "method": "dalle"
            }
        }

class ContentFormatRequest(BaseModel):
    """Request to format content for a specific channel."""
    personalizedContentId: str = Field(..., description="ID of the personalized content")
    channel: str = Field(..., description="Channel to format for")
    mediaUrls: List[str] = Field(default=[], description="Media URLs to include")
    
    class Config:
        schema_extra = {
            "example": {
                "personalizedContentId": "personalized_12345",
                "channel": "twitter",
                "mediaUrls": ["https://example.com/images/chelsea-win.jpg"]
            }
        }

class ContentGenerationState(BaseModel):
    """State of the content generation process."""
    pipelineId: str = Field(..., description="ID of the pipeline")
    rawContent: Optional[List[RawContentItem]] = Field(default=None, description="Raw content items")
    enhancedContent: Optional[List[EnhancedContentItem]] = Field(default=None, description="Enhanced content items")
    personalizedContent: Optional[List[PersonalizedContentItem]] = Field(default=None, description="Personalized content items")
    formattedContent: Optional[List[FormattedContentItem]] = Field(default=None, description="Formatted content items")
    currentStep: str = Field(default="retrieve", description="Current step in the process")
    createdAt: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updatedAt: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "pipelineId": "pipeline_12345",
                "currentStep": "enhance",
                "rawContent": [
                    {
                        "id": "raw_12345",
                        "source": "news",
                        "title": "Chelsea wins Premier League",
                        "body": "Chelsea FC has won the Premier League after a decisive victory..."
                    }
                ]
            }
        }

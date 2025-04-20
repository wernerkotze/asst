from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    """Type of content to generate."""
    TWEET = "tweet"
    INSTAGRAM_POST = "instagram_post"
    LINKEDIN_POST = "linkedin_post"
    BLOG_POST = "blog_post"
    FACEBOOK_POST = "facebook_post"

class MediaType(str, Enum):
    """Type of media to include with content."""
    IMAGE = "image"
    VIDEO = "video"
    GIF = "gif"
    CAROUSEL = "carousel"
    NONE = "none"

class ContentStatus(str, Enum):
    """Status of content in the workflow."""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    REJECTED = "rejected"

class SourceContent(BaseModel):
    """Source content used for generation."""
    id: Optional[str] = Field(None, description="Source content ID")
    type: str = Field(..., description="Type of source (e.g., 'news', 'tweet', 'stats')")
    content: str = Field(..., description="The source content text")
    url: Optional[HttpUrl] = Field(None, description="URL to the source content")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata about the source")
    sentiment: Optional[float] = Field(None, description="Sentiment score of the source content")
    extracted_at: datetime = Field(default_factory=datetime.now, description="When the content was extracted")

class MediaContent(BaseModel):
    """Media content to include with the post."""
    type: MediaType = Field(..., description="Type of media")
    url: Optional[HttpUrl] = Field(None, description="URL to the media")
    alt_text: Optional[str] = Field(None, description="Alt text for accessibility")
    caption: Optional[str] = Field(None, description="Caption for the media")
    generated: bool = Field(default=False, description="Whether this media was AI-generated")

class ContentGenerationRequest(BaseModel):
    """Request model for content generation."""
    pipeline_id: str = Field(..., description="ID of the pipeline to use")
    content_type: ContentType = Field(..., description="Type of content to generate")
    source_content: Optional[List[SourceContent]] = Field(default=None, description="Source content to use for generation")
    prompt: Optional[str] = Field(None, description="Custom prompt to guide generation")
    target_length: Optional[int] = Field(None, description="Target length in characters")
    include_hashtags: bool = Field(default=True, description="Whether to include hashtags")
    include_emojis: bool = Field(default=True, description="Whether to include emojis")
    include_media: bool = Field(default=True, description="Whether to include media")
    
    class Config:
        schema_extra = {
            "example": {
                "pipeline_id": "chelsea_fc_pipeline",
                "content_type": "tweet",
                "source_content": [
                    {
                        "type": "match_stats",
                        "content": "Chelsea 2-0 Arsenal, Goals: Mount (23'), Havertz (65')",
                        "metadata": {"competition": "Premier League", "match_day": 24}
                    }
                ],
                "include_hashtags": True,
                "include_emojis": True
            }
        }

class ContentGenerationResponse(BaseModel):
    """Response model for content generation."""
    id: Optional[str] = Field(None, description="Generated content ID")
    pipeline_id: str = Field(..., description="ID of the pipeline used")
    content_type: ContentType = Field(..., description="Type of content generated")
    content: str = Field(..., description="The generated content text")
    source_content_ids: List[str] = Field(default=[], description="IDs of source content used")
    media: List[MediaContent] = Field(default=[], description="Media to include with the post")
    hashtags: List[str] = Field(default=[], description="Hashtags included in the content")
    sentiment: float = Field(default=0.0, description="Sentiment score of the generated content")
    status: ContentStatus = Field(default=ContentStatus.DRAFT, description="Status of the content")
    platform_specific_formatting: Dict[str, Any] = Field(default={}, description="Platform-specific formatting")
    scheduled_for: Optional[datetime] = Field(None, description="When the content is scheduled for publishing")
    created_at: datetime = Field(default_factory=datetime.now, description="When the content was generated")
    updated_at: datetime = Field(default_factory=datetime.now, description="When the content was last updated")
    
    class Config:
        schema_extra = {
            "example": {
                "pipeline_id": "chelsea_fc_pipeline",
                "content_type": "tweet",
                "content": "FULL TIME: Chelsea 2-0 Arsenal! 🔥 Mount and Havertz with the goals as the Blues dominate at the Bridge! #CFC #CHEARS",
                "hashtags": ["#CFC", "#CHEARS"],
                "sentiment": 0.85,
                "status": "draft",
                "created_at": "2025-04-20T18:30:00"
            }
        }

class ContentPublishRequest(BaseModel):
    """Request model for publishing content."""
    content_id: str = Field(..., description="ID of the content to publish")
    platforms: List[str] = Field(..., description="Platforms to publish to")
    schedule_for: Optional[datetime] = Field(None, description="When to publish the content")
    
    class Config:
        schema_extra = {
            "example": {
                "content_id": "content_12345",
                "platforms": ["twitter"],
                "schedule_for": "2025-04-21T12:00:00Z"
            }
        }

class ContentPublishResponse(BaseModel):
    """Response model for content publishing."""
    content_id: str = Field(..., description="ID of the published content")
    status: ContentStatus = Field(..., description="New status of the content")
    platform_posts: Dict[str, Any] = Field(default={}, description="Details of posts on each platform")
    scheduled_for: Optional[datetime] = Field(None, description="When the content is scheduled for")
    published_at: Optional[datetime] = Field(None, description="When the content was published")
    
    class Config:
        schema_extra = {
            "example": {
                "content_id": "content_12345",
                "status": "scheduled",
                "platform_posts": {
                    "twitter": {"status": "scheduled", "platform_id": None}
                },
                "scheduled_for": "2025-04-21T12:00:00Z"
            }
        }

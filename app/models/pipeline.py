from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum

class PipelineType(str, Enum):
    """Type of pipeline for content automation."""
    BUSINESS = "business"
    AI_INFLUENCER = "ai_influencer"
    AUTOMATED_SOCIAL = "automated_social"

class DataSource(BaseModel):
    """Data source configuration for a pipeline."""
    name: str = Field(..., description="Name of the data source")
    type: str = Field(..., description="Type of data source (e.g., 'twitter', 'news', 'pinterest')")
    config: Dict[str, Any] = Field(default={}, description="Configuration parameters for the data source")
    active: bool = Field(default=True, description="Whether this data source is active")

class PublishingSchedule(BaseModel):
    """Publishing schedule configuration."""
    frequency: str = Field(..., description="Posting frequency (e.g., 'daily', 'weekly')")
    times: List[str] = Field(default=[], description="Preferred posting times in HH:MM format")
    days: List[str] = Field(default=[], description="Preferred posting days")
    timezone: str = Field(default="UTC", description="Timezone for the schedule")

class PersonaProfile(BaseModel):
    """Persona profile for content generation."""
    name: str = Field(..., description="Name of the persona")
    description: str = Field(..., description="Description of the persona")
    tone: List[str] = Field(default=[], description="Tone attributes (e.g., 'casual', 'professional')")
    voice: str = Field(default="neutral", description="Voice style")
    color_palette: List[str] = Field(default=[], description="Color hex codes for the brand palette")
    keywords: List[str] = Field(default=[], description="Key phrases and terms associated with the persona")
    emoji_usage: str = Field(default="moderate", description="Emoji usage level (none, light, moderate, heavy)")
    avatar_url: Optional[HttpUrl] = Field(None, description="URL to the persona's avatar image")

class ContentFramework(BaseModel):
    """Content framework derived from competitor analysis."""
    content_mix: Dict[str, float] = Field(default={}, description="Content type distribution (e.g., {'news': 0.3, 'memes': 0.2})")
    optimal_posting_times: List[Dict[str, Any]] = Field(default=[], description="Optimal times to post")
    hashtag_strategy: List[str] = Field(default=[], description="Recommended hashtags")
    engagement_tactics: List[str] = Field(default=[], description="Tactics to increase engagement")
    content_length: Dict[str, Any] = Field(default={}, description="Recommended content length per platform")

class Pipeline(BaseModel):
    """Pipeline configuration for content automation."""
    id: Optional[str] = Field(None, description="Pipeline ID")
    userId: Optional[str] = Field(None, description="User ID of the pipeline owner")
    name: str = Field(..., description="Name of the pipeline")
    type: PipelineType = Field(..., description="Type of pipeline")
    description: str = Field(..., description="Description of the pipeline")
    persona: PersonaProfile = Field(..., description="Persona profile for this pipeline")
    content_framework: ContentFramework = Field(..., description="Content framework for this pipeline")
    data_sources: List[DataSource] = Field(default=[], description="Data sources for this pipeline")
    publishing_schedule: PublishingSchedule = Field(..., description="Publishing schedule for this pipeline")
    target_platforms: List[str] = Field(default=["twitter"], description="Target platforms for publishing")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    active: bool = Field(default=True, description="Whether this pipeline is active")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "pipeline_12345",
                "userId": "user_67890",
                "name": "Chelsea FC Fan Account",
                "type": "ai_influencer",
                "description": "AI-powered Chelsea FC fan account posting match updates and fan banter",
                "persona": {
                    "name": "BluesFanAI",
                    "description": "Passionate Chelsea FC supporter with deep knowledge of the club's history",
                    "tone": ["enthusiastic", "witty", "knowledgeable"],
                    "voice": "casual",
                    "color_palette": ["#034694", "#FFFFFF", "#ED1C24"],
                    "keywords": ["Chelsea", "Blues", "Stamford Bridge", "Premier League"],
                    "emoji_usage": "moderate"
                },
                "content_framework": {
                    "content_mix": {"match_updates": 0.4, "stats": 0.3, "fan_banter": 0.2, "news": 0.1},
                    "optimal_posting_times": [
                        {"day": "match_day", "times": ["1h_before", "halftime", "fulltime"]}
                    ],
                    "hashtag_strategy": ["#CFC", "#Chelsea", "#KTBFFH"],
                    "engagement_tactics": ["polls during matches", "questions to fans"]
                },
                "data_sources": [
                    {
                        "name": "Football Data API",
                        "type": "sports_api",
                        "config": {"team_id": "chelsea_fc"}
                    },
                    {
                        "name": "Twitter Mentions",
                        "type": "twitter",
                        "config": {"keywords": ["#CFC", "Chelsea FC"]}
                    }
                ],
                "publishing_schedule": {
                    "frequency": "daily",
                    "times": ["08:00", "12:00", "18:00"],
                    "days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
                    "timezone": "Europe/London"
                },
                "target_platforms": ["twitter", "instagram"]
            }
        }

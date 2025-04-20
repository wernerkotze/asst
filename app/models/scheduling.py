from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum

class PostStatus(str, Enum):
    """Status of a scheduled post."""
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

class ScheduledPost(BaseModel):
    """Model for a post scheduled for publication."""
    id: Optional[str] = Field(None, description="Scheduled post ID")
    contentId: str = Field(..., description="Reference to content_pieces")
    pipelineId: str = Field(..., description="Reference to pipelines")
    channel: str = Field(..., description="Social media channel")
    scheduledTime: datetime = Field(..., description="When the post is scheduled to be published")
    status: PostStatus = Field(default=PostStatus.SCHEDULED, description="Current status of the post")
    postedAt: Optional[datetime] = Field(None, description="When the post was actually published")
    platformPostId: Optional[str] = Field(None, description="ID returned by platform API")
    failureReason: Optional[str] = Field(None, description="Error message if failed")
    retryCount: int = Field(default=0, description="Number of retry attempts")
    createdAt: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updatedAt: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "scheduled_12345",
                "contentId": "content_67890",
                "pipelineId": "pipeline_54321",
                "channel": "twitter",
                "scheduledTime": "2025-04-21T09:00:00Z",
                "status": "scheduled",
                "retryCount": 0
            }
        }

class ScheduleRequest(BaseModel):
    """Request to schedule a post."""
    contentId: str = Field(..., description="ID of the content to schedule")
    channel: str = Field(..., description="Channel to publish to")
    scheduledTime: datetime = Field(..., description="When to publish the post")
    
    class Config:
        schema_extra = {
            "example": {
                "contentId": "content_67890",
                "channel": "twitter",
                "scheduledTime": "2025-04-21T09:00:00Z"
            }
        }

class ScheduleResponse(BaseModel):
    """Response from scheduling a post."""
    scheduledPostId: str = Field(..., description="ID of the scheduled post")
    contentId: str = Field(..., description="ID of the content")
    channel: str = Field(..., description="Channel to publish to")
    scheduledTime: datetime = Field(..., description="When the post is scheduled to be published")
    status: PostStatus = Field(..., description="Current status of the post")
    
    class Config:
        schema_extra = {
            "example": {
                "scheduledPostId": "scheduled_12345",
                "contentId": "content_67890",
                "channel": "twitter",
                "scheduledTime": "2025-04-21T09:00:00Z",
                "status": "scheduled"
            }
        }

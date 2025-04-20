from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime, date
from enum import Enum

class MetricType(str, Enum):
    """Type of engagement metric."""
    IMPRESSIONS = "impressions"
    LIKES = "likes"
    SHARES = "shares"
    COMMENTS = "comments"
    CLICKS = "clicks"
    PROFILE_VISITS = "profile_visits"
    FOLLOWERS_GAINED = "followers_gained"
    ENGAGEMENT_RATE = "engagement_rate"

class TimeRange(str, Enum):
    """Time range for analytics."""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    CUSTOM = "custom"

class ContentPerformance(BaseModel):
    """Performance metrics for a specific content piece."""
    content_id: str = Field(..., description="ID of the content")
    platform: str = Field(..., description="Platform where content was published")
    platform_post_id: Optional[str] = Field(None, description="ID of the post on the platform")
    metrics: Dict[MetricType, int] = Field(default={}, description="Performance metrics")
    engagement_rate: float = Field(default=0.0, description="Engagement rate percentage")
    published_at: datetime = Field(..., description="When the content was published")
    measured_at: datetime = Field(default_factory=datetime.now, description="When these metrics were measured")
    
    class Config:
        schema_extra = {
            "example": {
                "content_id": "content_12345",
                "platform": "twitter",
                "platform_post_id": "1234567890",
                "metrics": {
                    "impressions": 5000,
                    "likes": 120,
                    "shares": 45,
                    "comments": 15
                },
                "engagement_rate": 3.6,
                "published_at": "2025-04-15T12:00:00Z",
                "measured_at": "2025-04-20T18:30:00Z"
            }
        }

class PerformanceAnalyticsRequest(BaseModel):
    """Request model for performance analytics."""
    pipeline_id: Optional[str] = Field(None, description="Filter by pipeline ID")
    platform: Optional[str] = Field(None, description="Filter by platform")
    content_type: Optional[str] = Field(None, description="Filter by content type")
    time_range: TimeRange = Field(default=TimeRange.WEEK, description="Time range for analytics")
    start_date: Optional[date] = Field(None, description="Start date for custom time range")
    end_date: Optional[date] = Field(None, description="End date for custom time range")
    
    class Config:
        schema_extra = {
            "example": {
                "pipeline_id": "chelsea_fc_pipeline",
                "platform": "twitter",
                "time_range": "month"
            }
        }

class ContentTypePerformance(BaseModel):
    """Performance metrics aggregated by content type."""
    content_type: str = Field(..., description="Type of content")
    total_posts: int = Field(..., description="Total number of posts")
    average_engagement_rate: float = Field(..., description="Average engagement rate")
    metrics_totals: Dict[MetricType, int] = Field(default={}, description="Total metrics by type")
    metrics_averages: Dict[MetricType, float] = Field(default={}, description="Average metrics by type")
    best_performing_content_id: Optional[str] = Field(None, description="ID of best performing content")

class TimePerformance(BaseModel):
    """Performance metrics aggregated by time."""
    time_slot: str = Field(..., description="Time slot (e.g., 'morning', '12:00')")
    day_of_week: Optional[str] = Field(None, description="Day of week")
    average_engagement_rate: float = Field(..., description="Average engagement rate")
    post_count: int = Field(..., description="Number of posts in this time slot")

class PerformanceAnalyticsResponse(BaseModel):
    """Response model for performance analytics."""
    pipeline_id: Optional[str] = Field(None, description="Pipeline ID if filtered")
    platform: Optional[str] = Field(None, description="Platform if filtered")
    time_range: TimeRange = Field(..., description="Time range of the analytics")
    start_date: date = Field(..., description="Start date of the analytics period")
    end_date: date = Field(..., description="End date of the analytics period")
    total_posts: int = Field(..., description="Total number of posts in the period")
    overall_engagement_rate: float = Field(..., description="Overall engagement rate")
    content_type_performance: List[ContentTypePerformance] = Field(default=[], description="Performance by content type")
    time_performance: List[TimePerformance] = Field(default=[], description="Performance by time")
    top_performing_content: List[ContentPerformance] = Field(default=[], description="Top performing content")
    recommendations: List[str] = Field(default=[], description="AI-generated recommendations based on the analytics")
    generated_at: datetime = Field(default_factory=datetime.now, description="When these analytics were generated")
    
    class Config:
        schema_extra = {
            "example": {
                "pipeline_id": "chelsea_fc_pipeline",
                "platform": "twitter",
                "time_range": "month",
                "start_date": "2025-03-20",
                "end_date": "2025-04-20",
                "total_posts": 90,
                "overall_engagement_rate": 2.8,
                "content_type_performance": [
                    {
                        "content_type": "match_updates",
                        "total_posts": 40,
                        "average_engagement_rate": 3.5,
                        "metrics_totals": {
                            "likes": 4800,
                            "shares": 1200
                        },
                        "metrics_averages": {
                            "likes": 120,
                            "shares": 30
                        }
                    }
                ],
                "time_performance": [
                    {
                        "time_slot": "18:00-20:00",
                        "day_of_week": "saturday",
                        "average_engagement_rate": 4.2,
                        "post_count": 15
                    }
                ],
                "recommendations": [
                    "Post more match updates on Saturdays between 18:00-20:00",
                    "Increase usage of polls in your tweets for higher engagement"
                ]
            }
        }

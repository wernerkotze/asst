from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum

class TweetCategory(str, Enum):
    """Categories for tweet classification."""
    NEWS = "news"
    COMMENTARY = "commentary"
    MEME = "meme"
    PROMO = "promo"
    QUESTION = "question"
    STATS = "stats"
    OTHER = "other"

class TweetSentiment(str, Enum):
    """Sentiment categories for tweets."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class Tweet(BaseModel):
    """Model for a Twitter tweet."""
    id: str = Field(..., description="Twitter tweet ID")
    text: str = Field(..., description="Tweet text content")
    author: str = Field(..., description="Twitter handle of the author")
    created_at: datetime = Field(..., description="When the tweet was created")
    retweets: int = Field(default=0, description="Number of retweets")
    likes: int = Field(default=0, description="Number of likes")
    replies: int = Field(default=0, description="Number of replies")
    hashtags: List[str] = Field(default=[], description="Hashtags used in the tweet")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "1234567890",
                "text": "Chelsea just scored! What a goal by Mount! #CFC #Chelsea",
                "author": "ChelseaFC",
                "created_at": "2025-04-20T15:30:00Z",
                "retweets": 1200,
                "likes": 5000,
                "replies": 300,
                "hashtags": ["CFC", "Chelsea"]
            }
        }

class AnalyzedTweet(Tweet):
    """Tweet with additional analysis data."""
    category: TweetCategory = Field(..., description="Category of the tweet")
    sentiment: TweetSentiment = Field(..., description="Sentiment of the tweet")
    engagement_score: float = Field(..., description="Engagement score (retweets*2 + likes)")
    hour_of_day: int = Field(..., description="Hour of the day when posted (0-23)")
    day_of_week: str = Field(..., description="Day of the week when posted")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "1234567890",
                "text": "Chelsea just scored! What a goal by Mount! #CFC #Chelsea",
                "author": "ChelseaFC",
                "created_at": "2025-04-20T15:30:00Z",
                "retweets": 1200,
                "likes": 5000,
                "replies": 300,
                "hashtags": ["CFC", "Chelsea"],
                "category": "news",
                "sentiment": "positive",
                "engagement_score": 7400,
                "hour_of_day": 15,
                "day_of_week": "Sat"
            }
        }

class ContentFramework(BaseModel):
    """Content framework derived from competitor analysis."""
    id: Optional[str] = Field(None, description="Content framework ID")
    pipelineId: Optional[str] = Field(None, description="Reference to pipeline")
    seedAccounts: List[str] = Field(..., description="Twitter handles used for analysis")
    contentCategories: Dict[str, float] = Field(..., description="Content type distribution (e.g., {'news': 0.4, 'meme': 0.3})")
    postingFrequency: Dict[str, int] = Field(..., description="Posting frequency (per day, per week)")
    peakTimes: Dict[str, List[Any]] = Field(..., description="Optimal posting times")
    hashtagStrategy: List[str] = Field(default=[], description="Recommended hashtags")
    stylePresets: List[str] = Field(default=[], description="Writing style presets")
    createdAt: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updatedAt: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "framework_12345",
                "pipelineId": "pipeline_67890",
                "seedAccounts": ["@ChelseaFC", "@talkchelsea"],
                "contentCategories": {"news": 0.4, "meme": 0.3, "opinion": 0.3},
                "postingFrequency": {"perDay": 3, "perWeek": 21},
                "peakTimes": {"hours": [12, 18], "days": ["Sat", "Tue"]},
                "hashtagStrategy": ["#ChelseaFC", "#CFC", "#KTBFFH"],
                "stylePresets": ["witty", "concise"]
            }
        }

class CompetitorAnalysisRequest(BaseModel):
    """Request for competitor analysis."""
    seedAccounts: List[str] = Field(..., description="Twitter handles to analyze")
    pipelineId: Optional[str] = Field(None, description="Pipeline ID to associate with the framework")
    tweetLimit: int = Field(default=200, description="Maximum number of tweets to analyze per account")
    
    class Config:
        schema_extra = {
            "example": {
                "seedAccounts": ["ChelseaFC", "talkchelsea"],
                "pipelineId": "pipeline_67890",
                "tweetLimit": 200
            }
        }

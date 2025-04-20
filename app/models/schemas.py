from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

# Brand Analysis Models
class BrandAnalysisRequest(BaseModel):
    """Request model for brand analysis."""
    brand_name: str = Field(..., description="Name of the brand to analyze")
    industry: str = Field(..., description="Industry sector of the brand")
    keywords: List[str] = Field(default=[], description="Keywords related to the brand")
    time_period: Optional[str] = Field(None, description="Time period for analysis (e.g., 'last_month', 'last_year')")
    
    class Config:
        schema_extra = {
            "example": {
                "brand_name": "Example Corp",
                "industry": "Technology",
                "keywords": ["innovation", "tech", "software"],
                "time_period": "last_month"
            }
        }

class BrandAnalysisResponse(BaseModel):
    """Response model for brand analysis."""
    brand_name: str = Field(..., description="Name of the analyzed brand")
    sentiment_score: float = Field(..., description="Overall sentiment score (0-1)")
    market_position: Dict[str, Any] = Field(..., description="Market positioning data")
    strengths: List[str] = Field(..., description="Identified brand strengths")
    weaknesses: List[str] = Field(..., description="Identified brand weaknesses")
    recommendations: List[str] = Field(..., description="Strategic recommendations")
    analysis_date: datetime = Field(default_factory=datetime.now, description="Date of analysis")
    
    class Config:
        schema_extra = {
            "example": {
                "brand_name": "Example Corp",
                "sentiment_score": 0.78,
                "market_position": {
                    "rank": 3,
                    "market_share": "12%",
                    "growth_trend": "positive"
                },
                "strengths": ["Strong online presence", "Innovative products"],
                "weaknesses": ["Customer service issues", "Limited market reach"],
                "recommendations": ["Improve customer support", "Expand to new markets"],
                "analysis_date": "2025-04-20T15:30:00"
            }
        }

# Competitor Analysis Models
class CompetitorInfo(BaseModel):
    """Model for competitor information."""
    name: str = Field(..., description="Competitor name")
    website: Optional[str] = Field(None, description="Competitor website URL")
    market_share: Optional[str] = Field(None, description="Estimated market share")

class CompetitorAnalysisRequest(BaseModel):
    """Request model for competitor analysis."""
    brand_name: str = Field(..., description="Name of the brand")
    industry: str = Field(..., description="Industry sector")
    competitors: List[CompetitorInfo] = Field(default=[], description="Known competitors")
    analysis_depth: str = Field("standard", description="Depth of analysis: 'basic', 'standard', or 'deep'")
    
    class Config:
        schema_extra = {
            "example": {
                "brand_name": "Example Corp",
                "industry": "Technology",
                "competitors": [
                    {"name": "TechGiant", "website": "https://techgiant.com", "market_share": "25%"},
                    {"name": "InnovateCo", "website": "https://innovateco.com", "market_share": "15%"}
                ],
                "analysis_depth": "standard"
            }
        }

class CompetitorAnalysisResponse(BaseModel):
    """Response model for competitor analysis."""
    brand_name: str = Field(..., description="Name of the brand")
    industry: str = Field(..., description="Industry sector")
    competitors: List[Dict[str, Any]] = Field(..., description="Analyzed competitors with details")
    competitive_landscape: Dict[str, Any] = Field(..., description="Overall competitive landscape")
    opportunities: List[str] = Field(..., description="Market opportunities")
    threats: List[str] = Field(..., description="Market threats")
    analysis_date: datetime = Field(default_factory=datetime.now, description="Date of analysis")
    
    class Config:
        schema_extra = {
            "example": {
                "brand_name": "Example Corp",
                "industry": "Technology",
                "competitors": [
                    {
                        "name": "TechGiant",
                        "strengths": ["Brand recognition", "R&D budget"],
                        "weaknesses": ["Slow innovation cycle", "High prices"],
                        "market_share": "25%",
                        "sentiment_score": 0.65
                    }
                ],
                "competitive_landscape": {
                    "market_concentration": "high",
                    "entry_barriers": "significant",
                    "disruption_potential": "medium"
                },
                "opportunities": ["Underserved SMB market", "Emerging markets expansion"],
                "threats": ["New entrants with lower prices", "Changing regulations"],
                "analysis_date": "2025-04-20T15:30:00"
            }
        }

# Content Generation Models
class ContentGenerationRequest(BaseModel):
    """Request model for content generation."""
    brand_name: str = Field(..., description="Name of the brand")
    content_type: str = Field(..., description="Type of content (e.g., 'blog_post', 'social_media', 'email')")
    topic: str = Field(..., description="Content topic or title")
    target_audience: List[str] = Field(..., description="Target audience segments")
    tone: str = Field("professional", description="Content tone (e.g., 'casual', 'professional', 'technical')")
    keywords: List[str] = Field(default=[], description="Keywords to include")
    max_length: Optional[int] = Field(None, description="Maximum content length")
    
    class Config:
        schema_extra = {
            "example": {
                "brand_name": "Example Corp",
                "content_type": "blog_post",
                "topic": "The Future of AI in Business",
                "target_audience": ["executives", "IT professionals"],
                "tone": "professional",
                "keywords": ["artificial intelligence", "business transformation", "automation"],
                "max_length": 1500
            }
        }

class ContentGenerationResponse(BaseModel):
    """Response model for content generation."""
    brand_name: str = Field(..., description="Name of the brand")
    content_type: str = Field(..., description="Type of content")
    title: str = Field(..., description="Content title")
    content: str = Field(..., description="Generated content")
    meta_description: Optional[str] = Field(None, description="SEO meta description")
    suggested_tags: List[str] = Field(default=[], description="Suggested tags/categories")
    generation_date: datetime = Field(default_factory=datetime.now, description="Date of generation")
    
    class Config:
        schema_extra = {
            "example": {
                "brand_name": "Example Corp",
                "content_type": "blog_post",
                "title": "The Future of AI in Business: Transforming Operations",
                "content": "Lorem ipsum dolor sit amet...",
                "meta_description": "Discover how AI is transforming business operations and creating new opportunities for growth.",
                "suggested_tags": ["AI", "Business Transformation", "Technology Trends"],
                "generation_date": "2025-04-20T15:30:00"
            }
        }

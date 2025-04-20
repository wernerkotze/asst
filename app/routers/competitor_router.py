from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List

from app.models.competitor import CompetitorAnalysisRequest, ContentFramework
from app.services.competitor_service import analyze_competitors
from app.db import get_db

router = APIRouter(
    prefix="/analyze/competitors",
    tags=["competitors"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)

@router.post("/", response_model=ContentFramework, status_code=status.HTTP_201_CREATED)
async def analyze_competitors_endpoint(
    request: CompetitorAnalysisRequest,
    db: Any = Depends(get_db)
) -> ContentFramework:
    """
    Analyze Twitter accounts to generate a content framework.
    
    - **seedAccounts**: List of Twitter handles to analyze
    - **pipelineId**: Optional pipeline ID to associate with the framework
    - **tweetLimit**: Maximum number of tweets to analyze per account
    """
    try:
        result = await analyze_competitors(request, db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Twitter analysis failed: {str(e)}"
        )

@router.get("/frameworks/{framework_id}", response_model=ContentFramework)
async def get_framework_endpoint(
    framework_id: str,
    db: Any = Depends(get_db)
) -> ContentFramework:
    """
    Get a specific content framework by ID.
    
    - **framework_id**: ID of the content framework
    """
    try:
        # In a real implementation, this would retrieve from the database
        # framework = await db.competitor_analyses.find_one({"_id": framework_id})
        # if not framework:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"Content framework with ID {framework_id} not found"
        #     )
        # return ContentFramework(**framework)
        
        # For now, return mock data
        return ContentFramework(
            id=framework_id,
            seedAccounts=["@ChelseaFC", "@talkchelsea"],
            contentCategories={"news": 0.4, "meme": 0.3, "opinion": 0.3},
            postingFrequency={"perDay": 3, "perWeek": 21},
            peakTimes={"hours": [12, 18], "days": ["Sat", "Tue"]},
            hashtagStrategy=["#ChelseaFC", "#CFC", "#KTBFFH"],
            stylePresets=["witty", "concise"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get content framework: {str(e)}"
        )

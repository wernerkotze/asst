from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any

from app.models.schemas import CompetitorAnalysisRequest, CompetitorAnalysisResponse
from app.services.competitor_service import analyze_competitors
from app.db import get_db

router = APIRouter(
    prefix="/analyze/competitors",
    tags=["competitors"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CompetitorAnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_competitors_endpoint(
    request: CompetitorAnalysisRequest,
    db: Any = Depends(get_db)
) -> CompetitorAnalysisResponse:
    """
    Analyze competitors based on the provided information.
    
    - **brand_name**: Name of the brand
    - **industry**: Industry sector
    - **competitors**: List of known competitors with details
    - **analysis_depth**: Depth of analysis ('basic', 'standard', or 'deep')
    """
    try:
        result = await analyze_competitors(request, db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Competitor analysis failed: {str(e)}"
        )

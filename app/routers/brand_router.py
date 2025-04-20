from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any

from app.models.schemas import BrandAnalysisRequest, BrandAnalysisResponse
from app.services.brand_service import analyze_brand
from app.db import get_db

router = APIRouter(
    prefix="/analyze/brand",
    tags=["brand"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=BrandAnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_brand_endpoint(
    request: BrandAnalysisRequest,
    db: Any = Depends(get_db)
) -> BrandAnalysisResponse:
    """
    Analyze a brand based on the provided information.
    
    - **brand_name**: Name of the brand to analyze
    - **industry**: Industry sector of the brand
    - **keywords**: Keywords related to the brand
    - **time_period**: Time period for analysis
    """
    try:
        result = await analyze_brand(request, db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Brand analysis failed: {str(e)}"
        )

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from typing import Any, List, Optional

from app.models.persona import BrandAnalysisRequest, PersonaProfile
from app.services.brand_service import analyze_brand
from app.db import get_db

router = APIRouter(
    prefix="/analyze/brand",
    tags=["brand"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)

@router.post("/", response_model=PersonaProfile, status_code=status.HTTP_201_CREATED)
async def analyze_brand_endpoint(
    request: BrandAnalysisRequest,
    db: Any = Depends(get_db)
) -> PersonaProfile:
    """
    Generate a persona profile from a Pinterest board.
    
    - **boardId**: Pinterest board ID or URL
    - **assets**: Optional URLs to brand assets
    - **pipelineId**: Optional pipeline ID to associate with the persona
    """
    try:
        result = await analyze_brand(request, db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze Pinterest board: {str(e)}"
        )

@router.post("/upload", response_model=List[str], status_code=status.HTTP_200_OK)
async def upload_brand_assets(
    files: List[UploadFile] = File(...),
    db: Any = Depends(get_db)
) -> List[str]:
    """
    Upload brand assets (logos, style guides, etc.) for brand analysis.
    
    Returns URLs to the uploaded files.
    """
    try:
        # In a real implementation, this would upload files to S3 or similar
        # For now, we'll just return mock URLs
        file_urls = [f"https://storage.asst.ai/brand-assets/{file.filename}" for file in files]
        return file_urls
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload brand assets: {str(e)}"
        )

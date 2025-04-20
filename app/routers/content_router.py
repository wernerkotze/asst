from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any

from app.models.schemas import ContentGenerationRequest, ContentGenerationResponse
from app.services.content_service import generate_content
from app.db import get_db

router = APIRouter(
    prefix="/generate/content",
    tags=["content"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ContentGenerationResponse, status_code=status.HTTP_200_OK)
async def generate_content_endpoint(
    request: ContentGenerationRequest,
    db: Any = Depends(get_db)
) -> ContentGenerationResponse:
    """
    Generate content based on the provided information.
    
    - **brand_name**: Name of the brand
    - **content_type**: Type of content (e.g., 'blog_post', 'social_media', 'email')
    - **topic**: Content topic or title
    - **target_audience**: Target audience segments
    - **tone**: Content tone (e.g., 'casual', 'professional', 'technical')
    - **keywords**: Keywords to include
    - **max_length**: Maximum content length
    """
    try:
        result = await generate_content(request, db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content generation failed: {str(e)}"
        )

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List

from app.models.content_generator import (
    RawContentItem, EnhancedContentItem, PersonalizedContentItem, FormattedContentItem,
    ContentRetrievalRequest, ContentEnhanceRequest, ContentPersonalizeRequest,
    ContentImageRequest, ContentFormatRequest
)
from app.services.content_generator_service import (
    retrieve_content, enhance_content, personalize_content,
    generate_image, format_content
)
from app.db import get_db

router = APIRouter(
    prefix="/content",
    tags=["content_generator"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)

@router.post("/retrieve", response_model=List[RawContentItem])
async def retrieve_content_endpoint(
    request: ContentRetrievalRequest,
    db: Any = Depends(get_db)
) -> List[RawContentItem]:
    """
    Step 1: Retrieve content from various sources based on pipeline settings.
    
    - **pipelineId**: ID of the pipeline
    - **sources**: Sources to retrieve content from (news, sports, twitter, rss)
    - **limit**: Maximum number of items to retrieve
    """
    try:
        return await retrieve_content(request, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve content: {str(e)}"
        )

@router.post("/enhance", response_model=List[EnhancedContentItem])
async def enhance_content_endpoint(
    request: ContentEnhanceRequest,
    db: Any = Depends(get_db)
) -> List[EnhancedContentItem]:
    """
    Step 2: Enhance raw content with hashtags, sentiment, and media suggestions.
    
    - **rawContentIds**: IDs of raw content items to enhance
    - **pipelineId**: ID of the pipeline
    """
    try:
        return await enhance_content(request, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enhance content: {str(e)}"
        )

@router.post("/personalize", response_model=PersonalizedContentItem)
async def personalize_content_endpoint(
    request: ContentPersonalizeRequest,
    db: Any = Depends(get_db)
) -> PersonalizedContentItem:
    """
    Step 3: Personalize content using OpenAI with persona and style preset.
    
    - **enhancedContentId**: ID of the enhanced content
    - **personaId**: ID of the persona to use
    - **stylePreset**: Style preset to use
    """
    try:
        return await personalize_content(request, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to personalize content: {str(e)}"
        )

@router.post("/image", response_model=str)
async def generate_image_endpoint(
    request: ContentImageRequest,
    db: Any = Depends(get_db)
) -> str:
    """
    Step 4: Generate or fetch an image for content.
    
    - **text**: Text to generate image for
    - **method**: Method to use (dalle, google)
    """
    try:
        return await generate_image(request, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate image: {str(e)}"
        )

@router.post("/format", response_model=FormattedContentItem)
async def format_content_endpoint(
    request: ContentFormatRequest,
    db: Any = Depends(get_db)
) -> FormattedContentItem:
    """
    Step 5: Format content for a specific channel.
    
    - **personalizedContentId**: ID of the personalized content
    - **channel**: Channel to format for
    - **mediaUrls**: Media URLs to include
    """
    try:
        return await format_content(request, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to format content: {str(e)}"
        )

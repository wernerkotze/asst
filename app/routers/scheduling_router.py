from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List, Optional

from app.models.scheduling import ScheduledPost, ScheduleRequest, ScheduleResponse, PostStatus
from app.services.scheduling_service import (
    schedule_post, get_scheduled_post, list_scheduled_posts, 
    publish_post_now, cancel_scheduled_post
)
from app.db import get_db

router = APIRouter(
    prefix="/schedule",
    tags=["scheduling"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)

@router.post("/post", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def schedule_post_endpoint(
    request: ScheduleRequest,
    db: Any = Depends(get_db)
) -> ScheduleResponse:
    """
    Schedule a post for publication.
    
    - **contentId**: ID of the content to schedule
    - **channel**: Channel to publish to (e.g., twitter, instagram)
    - **scheduledTime**: When to publish the post (ISO format)
    """
    try:
        scheduled_post = await schedule_post(request, db)
        return ScheduleResponse(
            scheduledPostId=scheduled_post.id,
            contentId=scheduled_post.contentId,
            channel=scheduled_post.channel,
            scheduledTime=scheduled_post.scheduledTime,
            status=scheduled_post.status
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to schedule post: {str(e)}"
        )

@router.get("/posts", response_model=List[ScheduledPost])
async def list_scheduled_posts_endpoint(
    pipeline_id: Optional[str] = None,
    status: Optional[PostStatus] = None,
    db: Any = Depends(get_db)
) -> List[ScheduledPost]:
    """
    List scheduled posts, optionally filtered by pipeline ID and status.
    
    - **pipeline_id**: Optional pipeline ID to filter by
    - **status**: Optional status to filter by (scheduled, published, failed)
    """
    try:
        return await list_scheduled_posts(pipeline_id, status, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list scheduled posts: {str(e)}"
        )

@router.get("/posts/{post_id}", response_model=ScheduledPost)
async def get_scheduled_post_endpoint(
    post_id: str,
    db: Any = Depends(get_db)
) -> ScheduledPost:
    """
    Get a specific scheduled post by ID.
    
    - **post_id**: ID of the scheduled post
    """
    try:
        scheduled_post = await get_scheduled_post(post_id, db)
        if not scheduled_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scheduled post with ID {post_id} not found"
            )
        return scheduled_post
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get scheduled post: {str(e)}"
        )

@router.post("/posts/{post_id}/publish-now", response_model=ScheduledPost)
async def publish_post_now_endpoint(
    post_id: str,
    db: Any = Depends(get_db)
) -> ScheduledPost:
    """
    Immediately publish a scheduled post.
    
    - **post_id**: ID of the scheduled post
    """
    try:
        return await publish_post_now(post_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to publish post: {str(e)}"
        )

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_scheduled_post_endpoint(
    post_id: str,
    db: Any = Depends(get_db)
) -> None:
    """
    Cancel a scheduled post.
    
    - **post_id**: ID of the scheduled post
    """
    try:
        success = await cancel_scheduled_post(post_id, db)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scheduled post with ID {post_id} not found"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel scheduled post: {str(e)}"
        )

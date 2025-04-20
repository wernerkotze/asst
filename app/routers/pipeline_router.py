from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List, Optional

from app.models.pipeline import Pipeline, PipelineType
from app.services.pipeline_service import create_pipeline, get_pipeline, list_pipelines, update_pipeline, delete_pipeline
from app.db import get_db

router = APIRouter(
    prefix="/pipelines",
    tags=["pipelines"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Pipeline, status_code=status.HTTP_201_CREATED)
async def create_pipeline_endpoint(
    pipeline: Pipeline,
    db: Any = Depends(get_db)
) -> Pipeline:
    """
    Create a new content automation pipeline.
    
    - **name**: Name of the pipeline
    - **type**: Type of pipeline (business, ai_influencer, automated_social)
    - **description**: Description of the pipeline
    - **persona**: Persona profile for this pipeline
    - **content_framework**: Content framework for this pipeline
    - **data_sources**: Data sources for this pipeline
    - **publishing_schedule**: Publishing schedule for this pipeline
    - **target_platforms**: Target platforms for publishing
    """
    try:
        result = await create_pipeline(pipeline, db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create pipeline: {str(e)}"
        )

@router.get("/{pipeline_id}", response_model=Pipeline)
async def get_pipeline_endpoint(
    pipeline_id: str,
    db: Any = Depends(get_db)
) -> Pipeline:
    """
    Get a specific pipeline by ID.
    """
    try:
        result = await get_pipeline(pipeline_id, db)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pipeline with ID {pipeline_id} not found"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get pipeline: {str(e)}"
        )

@router.get("/", response_model=List[Pipeline])
async def list_pipelines_endpoint(
    pipeline_type: Optional[PipelineType] = None,
    active_only: bool = True,
    db: Any = Depends(get_db)
) -> List[Pipeline]:
    """
    List all pipelines, optionally filtered by type and active status.
    """
    try:
        result = await list_pipelines(pipeline_type, active_only, db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list pipelines: {str(e)}"
        )

@router.put("/{pipeline_id}", response_model=Pipeline)
async def update_pipeline_endpoint(
    pipeline_id: str,
    pipeline: Pipeline,
    db: Any = Depends(get_db)
) -> Pipeline:
    """
    Update an existing pipeline.
    """
    try:
        result = await update_pipeline(pipeline_id, pipeline, db)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pipeline with ID {pipeline_id} not found"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update pipeline: {str(e)}"
        )

@router.delete("/{pipeline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pipeline_endpoint(
    pipeline_id: str,
    db: Any = Depends(get_db)
) -> None:
    """
    Delete a pipeline.
    """
    try:
        result = await delete_pipeline(pipeline_id, db)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pipeline with ID {pipeline_id} not found"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete pipeline: {str(e)}"
        )

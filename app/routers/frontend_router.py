from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Set up templates
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

router = APIRouter(
    tags=["frontend"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)

@router.get("/brand-tool")
async def brand_tool_page(request: Request):
    """
    Serve the brand generation tool frontend page.
    """
    return templates.TemplateResponse(
        "brand_tool.html", 
        {"request": request}
    )

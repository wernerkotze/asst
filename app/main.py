import logging
from pathlib import Path
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import brand_router, competitor_router, content_router, pipeline_router, scheduling_router, content_generator_router, frontend_router
from app.db import init_mongodb, close_db_connections

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ASST API",
    description="AI-Driven Social Media Automation Suite",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Set up templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# Include routers
app.include_router(frontend_router.router)
app.include_router(pipeline_router.router)
app.include_router(brand_router.router)
app.include_router(competitor_router.router)
app.include_router(content_router.router)
app.include_router(scheduling_router.router)
app.include_router(content_generator_router.router)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting up the application")
    try:
        # Initialize database connection
        await init_mongodb()
        logger.info("Database connection initialized")
    except Exception as e:
        logger.error(f"Error initializing services: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down the application")
    try:
        # Close database connections
        await close_db_connections()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the ASST API - AI-Driven Social Media Automation Suite",
        "description": "Enable brands, influencers, and creators to go from inspiration to published social content in minutes",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

import logging
import boto3
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# Set up logging
logger = logging.getLogger(__name__)

# Global database client instances
dynamodb_client = None
mongodb_client = None

async def init_dynamodb():
    """Initialize the DynamoDB client."""
    global dynamodb_client
    
    try:
        # Initialize the DynamoDB client
        dynamodb_client = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        logger.info("DynamoDB client initialized successfully")
        
        # TODO: Create tables if they don't exist
        
        return dynamodb_client
    except Exception as e:
        logger.error(f"Failed to initialize DynamoDB client: {e}")
        raise

async def init_mongodb():
    """Initialize the MongoDB client."""
    global mongodb_client
    
    try:
        # Initialize the MongoDB client
        mongodb_client = AsyncIOMotorClient(settings.mongodb_url)
        db = mongodb_client[settings.db_name]
        logger.info("MongoDB client initialized successfully")
        
        # TODO: Create collections if they don't exist
        
        return db
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB client: {e}")
        raise

async def get_db():
    """Get database client based on configuration."""
    # TODO: Implement logic to choose between DynamoDB and MongoDB
    # For now, we'll use MongoDB as the default
    if mongodb_client is None:
        return await init_mongodb()
    return mongodb_client[settings.db_name]

async def close_db_connections():
    """Close database connections."""
    if mongodb_client:
        mongodb_client.close()
        logger.info("MongoDB connection closed")

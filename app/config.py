import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    api_key: str = os.getenv("API_KEY", "")
    
    # Database Configuration
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "27017"))
    db_name: str = os.getenv("DB_NAME", "asst")
    
    # AWS Configuration (for DynamoDB)
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "us-west-2")
    
    # MongoDB Connection String (alternative to individual settings)
    mongodb_url: str = os.getenv(
        "MONGODB_URL", 
        f"mongodb://{db_host}:{db_port}/{db_name}"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Function to get settings (for dependency injection)
def get_settings():
    """Return the settings instance."""
    return settings

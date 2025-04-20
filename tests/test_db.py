import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import boto3
from motor.motor_asyncio import AsyncIOMotorClient

from app.db import init_dynamodb, init_mongodb, get_db, close_db_connections


@pytest.fixture
def mock_boto3_resource():
    """Mock boto3 resource for testing."""
    mock = MagicMock()
    return mock


@pytest.fixture
def mock_motor_client():
    """Mock MongoDB motor client for testing."""
    mock = MagicMock()
    mock.__getitem__.return_value = MagicMock()
    return mock


@patch("app.db.boto3.resource")
@patch("app.db.settings")
async def test_init_dynamodb(mock_settings, mock_resource, mock_boto3_resource):
    """Test DynamoDB initialization."""
    # Setup mocks
    mock_resource.return_value = mock_boto3_resource
    mock_settings.aws_access_key_id = "test_key"
    mock_settings.aws_secret_access_key = "test_secret"
    mock_settings.aws_region = "test-region-1"
    
    # Call the function
    result = await init_dynamodb()
    
    # Verify results
    assert result == mock_boto3_resource
    mock_resource.assert_called_once_with(
        'dynamodb',
        aws_access_key_id="test_key",
        aws_secret_access_key="test_secret",
        region_name="test-region-1"
    )


@patch("app.db.AsyncIOMotorClient")
@patch("app.db.settings")
async def test_init_mongodb(mock_settings, mock_motor, mock_motor_client):
    """Test MongoDB initialization."""
    # Setup mocks
    mock_motor.return_value = mock_motor_client
    mock_settings.mongodb_url = "mongodb://test_host:9999/test_db"
    mock_settings.db_name = "test_db"
    
    # Call the function
    result = await init_mongodb()
    
    # Verify results
    assert result == mock_motor_client.__getitem__.return_value
    mock_motor.assert_called_once_with("mongodb://test_host:9999/test_db")
    mock_motor_client.__getitem__.assert_called_once_with("test_db")


@patch("app.db.init_mongodb")
@patch("app.db.mongodb_client", None)
async def test_get_db_init(mock_init_mongodb, mock_motor_client):
    """Test get_db when client is not initialized."""
    # Setup mocks
    mock_init_mongodb.return_value = mock_motor_client
    
    # Call the function
    result = await get_db()
    
    # Verify results
    assert result == mock_motor_client
    mock_init_mongodb.assert_called_once()


@patch("app.db.mongodb_client")
async def test_get_db_existing(mock_mongodb_client, mock_motor_client):
    """Test get_db when client is already initialized."""
    # Setup mocks
    mock_mongodb_client.__getitem__.return_value = mock_motor_client
    
    # Call the function
    result = await get_db()
    
    # Verify results
    assert result == mock_motor_client


@patch("app.db.mongodb_client")
async def test_close_db_connections(mock_mongodb_client):
    """Test closing database connections."""
    # Call the function
    await close_db_connections()
    
    # Verify results
    mock_mongodb_client.close.assert_called_once()

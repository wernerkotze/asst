import pytest
from unittest.mock import patch, MagicMock
import os

from app.config import Settings


@patch.dict(os.environ, {
    "API_KEY": "test_api_key",
    "DB_HOST": "test_host",
    "DB_PORT": "9999",
    "DB_NAME": "test_db",
    "AWS_ACCESS_KEY_ID": "test_aws_key",
    "AWS_SECRET_ACCESS_KEY": "test_aws_secret",
    "AWS_REGION": "test-region-1",
    "MONGODB_URL": "mongodb://test_host:9999/test_db"
})
def test_settings_from_env():
    """Test that settings are loaded correctly from environment variables."""
    settings = Settings()
    
    assert settings.api_key == "test_api_key"
    assert settings.db_host == "test_host"
    assert settings.db_port == 9999
    assert settings.db_name == "test_db"
    assert settings.aws_access_key_id == "test_aws_key"
    assert settings.aws_secret_access_key == "test_aws_secret"
    assert settings.aws_region == "test-region-1"
    assert settings.mongodb_url == "mongodb://test_host:9999/test_db"


def test_settings_defaults():
    """Test that settings have appropriate defaults when env vars are not set."""
    # Create a clean environment without our test variables
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        
        assert settings.api_key == ""
        assert settings.db_host == "localhost"
        assert settings.db_port == 27017
        assert settings.db_name == "asst"
        assert settings.aws_access_key_id == ""
        assert settings.aws_secret_access_key == ""
        assert settings.aws_region == "us-west-2"
        assert "mongodb://localhost:27017/asst" in settings.mongodb_url

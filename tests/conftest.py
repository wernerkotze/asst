import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.db import get_db


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Create a mock database for testing."""
    mock = AsyncMock()
    return mock


@pytest.fixture
def override_get_db(mock_db):
    """Override the get_db dependency for testing."""
    async def _override_get_db():
        return mock_db
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides = {}

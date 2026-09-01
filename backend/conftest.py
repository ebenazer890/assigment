"""
Pytest configuration and fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.db.database import get_db
from app.main import app


# Test Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    return engine


@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    """Create test session factory"""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    return TestingSessionLocal


@pytest.fixture
def db(test_engine, test_session_factory):
    """Create test database session"""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    db = test_session_factory()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db):
    """Create test FastAPI client"""
    def override_get_db():
        return db
    
    app.dependency_overrides[get_db] = override_get_db
    
    from fastapi.testclient import TestClient
    return TestClient(app)


# Pytest configuration options
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow"
    )


# Performance markers
@pytest.mark.slow
def test_large_dataset():
    """Mark slow tests"""
    pass

"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv
from app.db.models import Base

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./role_ai.db")

# Create engine with SQLite-specific settings if needed
if "sqlite" in DATABASE_URL.lower():
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("APP_DEBUG", "False").lower() == "true",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("APP_DEBUG", "False").lower() == "true",
        pool_pre_ping=True,
        pool_recycle=3600,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database by creating all tables"""
    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    """Drop all tables (for testing/reset)"""
    Base.metadata.drop_all(bind=engine)

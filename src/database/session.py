"""
Database Session Management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from config import settings
from models.base import Base
from models.user_mfa import UserMFA

# Import all models to register them with SQLAlchemy
import models  # noqa: F401

# Auth services use sync SQLAlchemy queries (db.query), so expose a sync session here.
sync_database_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

engine = create_engine(
    sync_database_url,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
)

SessionLocal = sessionmaker(
    engine,
    class_=Session,
    expire_on_commit=False,
)


def get_db():
    """Get database session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def ensure_auth_tables() -> None:
    """Create auth-related support tables if they do not already exist."""
    Base.metadata.create_all(bind=engine, tables=[UserMFA.__table__])

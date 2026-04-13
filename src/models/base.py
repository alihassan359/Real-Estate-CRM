"""
Base Model for all database entities
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """Base model for all entities"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

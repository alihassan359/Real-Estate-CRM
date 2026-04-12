"""
Tenant Model
"""

from sqlalchemy import Column, String, Boolean

from models.base import BaseModel


class Tenant(BaseModel):
    """Tenant model for multi-tenant system"""
    __tablename__ = "tenants"
    
    name = Column(String(255), unique=True, index=True)
    slug = Column(String(100), unique=True)
    description = Column(String(500), nullable=True)
    logo_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    max_users = Column(int, default=10)

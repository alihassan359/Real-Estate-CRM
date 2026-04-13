"""
Tenant Model - Multi-tenant SaaS
"""

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

from models.base import BaseModel


class SubscriptionPlan(str, Enum):
    """Subscription plan types"""
    FREE = "FREE"
    BASIC = "BASIC"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"


class TenantStatus(str, Enum):
    """Tenant status types"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class Tenant(BaseModel):
    """Tenant model for multi-tenant system"""
    __tablename__ = "tenants"
    
    tenant_code = Column(String(20), unique=True, index=True, nullable=False)
    company_name = Column(String(255), unique=True, index=True, nullable=False)
    company_email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    logo_url = Column(String(500), nullable=True)
    
    subscription_plan = Column(SQLEnum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    paid_until = Column(DateTime(timezone=True), nullable=True)
    status = Column(SQLEnum(TenantStatus), default=TenantStatus.ACTIVE, index=True)
    
    settings = Column(String, default='{}')  # JSON
    metadata_info = Column(String, default='{}')  # JSON - renamed from 'metadata' (reserved in SQLAlchemy)
    
    # Relationships
    users = relationship("User", back_populates="tenant")
    
    def __repr__(self):
        return f"<Tenant {self.tenant_code}: {self.company_name}>"

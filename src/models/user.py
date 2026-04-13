"""
User Model - Authentication & Multi-tenant
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from uuid import UUID as PYUUID

from models.base import BaseModel


class UserRole(str, Enum):
    """User role types"""
    SUPER_ADMIN = "SUPER_ADMIN"
    PLATFORM_ADMIN = "PLATFORM_ADMIN"
    TENANT_OWNER = "TENANT_OWNER"
    MANAGER = "MANAGER"
    OPERATOR = "OPERATOR"
    ACCOUNTANT = "ACCOUNTANT"
    SALESMAN = "SALESMAN"


class UserStatus(str, Enum):
    """User status types"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class User(BaseModel):
    """User model - authentication and authorization"""
    __tablename__ = "users"
    
    # Tenant relationship
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Personal info
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Role & Permissions
    role = Column(SQLEnum(UserRole), default=UserRole.OPERATOR, index=True)
    permissions = Column(String, default='[]')  # JSON array of permissions
    
    # Status
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE, index=True)
    email_verified = Column(Boolean, default=False)
    
    # Tracking
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}: {self.role}>"
    
    def is_owner(self):
        """Check if user is tenant owner"""
        return self.role == UserRole.TENANT_OWNER
    
    def is_admin(self):
        """Check if user has admin role"""
        return self.role in [UserRole.TENANT_OWNER, UserRole.MANAGER, UserRole.PLATFORM_ADMIN, UserRole.SUPER_ADMIN]

"""
Tenant API Schemas - Request and Response models
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field

from models.tenant import SubscriptionPlan, TenantStatus


# ============================================================================
# REQUEST SCHEMAS
# ============================================================================

class TenantCreateRequest(BaseModel):
    """Create tenant request"""
    company_name: str = Field(..., min_length=3, max_length=255)
    company_email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    subscription_plan: SubscriptionPlan = Field(default=SubscriptionPlan.FREE)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    
    class Config:
        from_attributes = True


class TenantUpdateRequest(BaseModel):
    """Update tenant request"""
    company_name: Optional[str] = Field(None, min_length=3, max_length=255)
    company_email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    logo_url: Optional[str] = Field(None, max_length=500)
    
    class Config:
        from_attributes = True


class TenantSettingsUpdateRequest(BaseModel):
    """Update tenant settings request"""
    settings: Dict[str, Any] = Field(...)
    
    class Config:
        from_attributes = True


class UpgradeSubscriptionRequest(BaseModel):
    """Upgrade subscription request"""
    new_plan: SubscriptionPlan = Field(...)
    months: int = Field(default=1, ge=1, le=36)
    
    class Config:
        from_attributes = True


class SuspendTenantRequest(BaseModel):
    """Suspend tenant request"""
    reason: Optional[str] = Field(None, max_length=500)
    
    class Config:
        from_attributes = True


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class TenantResponse(BaseModel):
    """Tenant response"""
    id: int
    tenant_code: str
    company_name: str
    company_email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    logo_url: Optional[str]
    subscription_plan: str
    paid_until: Optional[datetime]
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TenantDetailResponse(TenantResponse):
    """Detailed tenant response with settings"""
    settings: dict = Field(default_factory=dict)
    
    class Config:
        from_attributes = True


class TenantUsageResponse(BaseModel):
    """Tenant usage response"""
    current_users: int
    max_users: int
    current_deals: int
    max_deals: int
    storage_used_mb: int
    storage_limit_mb: int
    subscription_plan: str
    status: str
    paid_until: Optional[str]
    
    class Config:
        from_attributes = True


class TenantListResponse(BaseModel):
    """Tenant list response"""
    success: bool
    data: List[TenantResponse]
    pagination: dict = Field(
        default_factory=dict,
        description="Pagination info (skip, limit, total)"
    )
    
    class Config:
        from_attributes = True


class SingleTenantResponse(BaseModel):
    """Single tenant response"""
    success: bool
    data: TenantDetailResponse
    
    class Config:
        from_attributes = True


class TenantCreatedResponse(BaseModel):
    """Tenant created response"""
    success: bool
    message: str
    data: TenantResponse
    
    class Config:
        from_attributes = True


class TenantUpdatedResponse(BaseModel):
    """Tenant updated response"""
    success: bool
    message: str
    data: TenantResponse
    
    class Config:
        from_attributes = True


class TenantDeletedResponse(BaseModel):
    """Tenant deleted response"""
    success: bool
    message: str
    
    class Config:
        from_attributes = True


class TenantActionResponse(BaseModel):
    """Tenant action response"""
    success: bool
    message: str
    data: Optional[TenantResponse] = None
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    detail: str
    code: Optional[str] = None
    
    class Config:
        from_attributes = True

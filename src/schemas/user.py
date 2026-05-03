"""
User API Schemas - Request and Response models
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

from models.user import UserRole, UserStatus
from config.permissions import Permission


# ============================================================================
# REQUEST SCHEMAS
# ============================================================================

class UserCreateRequest(BaseModel):
    """Create user request"""
    email: EmailStr = Field(..., description="User email")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=8, max_length=255)
    role: UserRole = Field(default=UserRole.OPERATOR)
    
    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    """Update user profile request"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)
    
    class Config:
        from_attributes = True


class UserRoleUpdateRequest(BaseModel):
    """Update user role request"""
    role: UserRole = Field(..., description="New role")
    
    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    """Change password request"""
    current_password: str = Field(..., min_length=8, max_length=255)
    new_password: str = Field(..., min_length=8, max_length=255)
    
    class Config:
        from_attributes = True


class ResetPasswordRequest(BaseModel):
    """Reset password request (admin action)"""
    new_password: str = Field(..., min_length=8, max_length=255)
    
    class Config:
        from_attributes = True


class SuspendUserRequest(BaseModel):
    """Suspend user request"""
    reason: Optional[str] = Field(None, max_length=500)
    
    class Config:
        from_attributes = True


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class UserResponse(BaseModel):
    """User response"""
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    avatar_url: Optional[str]
    role: str
    status: str
    email_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Detailed user response with permissions"""
    permissions: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """User list response"""
    success: bool
    data: List[UserResponse]
    pagination: dict = Field(
        default_factory=dict,
        description="Pagination info (page, limit, total)"
    )
    
    class Config:
        from_attributes = True


class SingleUserResponse(BaseModel):
    """Single user response"""
    success: bool
    data: UserDetailResponse
    
    class Config:
        from_attributes = True


class UserCreatedResponse(BaseModel):
    """User created response"""
    success: bool
    message: str
    data: UserResponse
    
    class Config:
        from_attributes = True


class UserUpdatedResponse(BaseModel):
    """User updated response"""
    success: bool
    message: str
    data: UserResponse
    
    class Config:
        from_attributes = True


class UserDeletedResponse(BaseModel):
    """User deleted response"""
    success: bool
    message: str
    
    class Config:
        from_attributes = True


class PasswordChangedResponse(BaseModel):
    """Password changed response"""
    success: bool
    message: str
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    detail: str
    code: Optional[str] = None
    
    class Config:
        from_attributes = True

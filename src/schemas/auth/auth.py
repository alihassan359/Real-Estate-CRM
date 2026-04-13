"""
Pydantic schemas for authentication
"""

from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from models.user import UserRole, UserStatus


class TokenResponse(BaseModel):
    """JWT Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)


class UserResponse(UserBase):
    """User response schema"""
    id: UUID
    tenant_id: UUID
    role: UserRole
    status: UserStatus
    email_verified: bool
    avatar_url: Optional[str]
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TenantResponse(BaseModel):
    """Tenant response schema"""
    id: UUID
    tenant_code: str
    company_name: str
    company_email: Optional[str]
    phone: Optional[str]
    subscription_plan: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SignupRequest(UserBase):
    """User signup request schema"""
    password: str = Field(..., min_length=8, max_length=50)
    confirm_password: str = Field(..., min_length=8, max_length=50)
    company_name: str = Field(..., min_length=3, max_length=100)
    company_phone: Optional[str] = Field(None, max_length=20)
    company_city: Optional[str] = Field(None, max_length=100)
    accept_terms: bool = Field(...)

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate passwords match"""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

    @validator('accept_terms')
    def terms_required(cls, v):
        """Validate terms acceptance"""
        if not v:
            raise ValueError('You must accept terms and conditions')
        return v


class SignupResponse(BaseModel):
    """Signup response schema"""
    success: bool
    message: str
    data: dict = None  # Contains user, tenant, tokens


class LoginRequest(BaseModel):
    """User login request schema"""
    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    """Login response schema"""
    success: bool
    message: str
    data: dict = None  # Contains user, tokens


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Refresh token response schema"""
    success: bool
    data: dict  # Contains access_token, expires_in


class LogoutResponse(BaseModel):
    """Logout response schema"""
    success: bool
    message: str


class CurrentUserResponse(BaseModel):
    """Current user with tenant info"""
    user: UserResponse
    tenant: TenantResponse


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str
    error: dict = None  # Contains field, code, details
    status_code: int


class GoogleAuthRequest(BaseModel):
    """Google OAuth token request schema"""
    id_token: str = Field(..., description="Google ID token")


class GoogleAuthResponse(BaseModel):
    """Google OAuth response schema"""
    success: bool
    message: str
    is_new_user: bool = False
    data: dict = None  # Contains user, tenant (if new), tokens


class AdminSignupRequest(UserBase):
    """Admin signup request schema"""
    password: str = Field(..., min_length=8, max_length=50)
    confirm_password: str = Field(..., min_length=8, max_length=50)

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate passwords match"""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


class AdminSignupResponse(BaseModel):
    """Admin signup response schema"""
    success: bool
    message: str
    data: dict = None  # Contains user, tokens, admin flag


class TenantLoginRequest(BaseModel):
    """Tenant login request schema"""
    email: EmailStr
    password: str = Field(..., min_length=1)
    tenant_code: Optional[str] = Field(None, description="Optional tenant code for additional validation")


class TenantLoginResponse(BaseModel):
    """Tenant login response schema"""
    success: bool
    message: str
    data: dict = None  # Contains user, tokens


class ForgotPasswordRequest(BaseModel):
    """Forgot password request schema."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request schema."""
    token: str = Field(..., min_length=10)
    new_password: str = Field(..., min_length=8, max_length=50)
    confirm_password: str = Field(..., min_length=8, max_length=50)

    @validator('confirm_password')
    def reset_passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class MfaVerifyRequest(BaseModel):
    """Verify TOTP code request schema."""
    code: str = Field(..., min_length=6, max_length=8)


class MfaDisableRequest(BaseModel):
    """Disable MFA request schema."""
    code: str = Field(..., min_length=6, max_length=8)


class MfaLoginVerifyRequest(BaseModel):
    """MFA challenge verification request schema."""
    mfa_token: str = Field(..., min_length=20)
    code: Optional[str] = Field(None, min_length=6, max_length=8)
    backup_code: Optional[str] = Field(None, min_length=6, max_length=32)

    @validator('backup_code')
    def at_least_one_factor(cls, v, values):
        if not v and not values.get('code'):
            raise ValueError('Either code or backup_code is required')
        return v

"""
Authentication Schemas
"""

from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    """Signup request schema"""
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

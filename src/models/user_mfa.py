"""
User MFA model for storing TOTP configuration and backup codes.
"""

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from models.base import BaseModel


class UserMFA(BaseModel):
    """Per-user MFA configuration."""
    __tablename__ = "user_mfa"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    secret = Column(String(64), nullable=False)
    is_enabled = Column(Boolean, default=False, index=True)
    backup_codes = Column(Text, default="[]")
    last_verified_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")

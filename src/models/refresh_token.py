"""
Refresh Token Model - Token storage and management
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

from models.base import BaseModel


class RefreshToken(BaseModel):
    """Refresh token model for token storage"""
    __tablename__ = "refresh_tokens"
    
    # Relationship
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Token details
    token_hash = Column(String(500), unique=True, nullable=False, index=True)
    is_revoked = Column(Boolean, default=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Tracking
    used_at = Column(DateTime(timezone=True), nullable=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    revoked_reason = Column(String(255), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")
    
    def is_expired(self) -> bool:
        """Check if token is expired"""
        if self.expires_at.tzinfo is not None:
            return datetime.now(self.expires_at.tzinfo) > self.expires_at
        return datetime.utcnow() > self.expires_at
    
    def can_use(self) -> bool:
        """Check if token can be used"""
        return not self.is_revoked and not self.is_expired()
    
    def __repr__(self):
        return f"<RefreshToken user_id={self.user_id} expires_at={self.expires_at}>"

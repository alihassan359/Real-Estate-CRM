"""
Notification Model
"""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Text
from datetime import datetime

from models.base import BaseModel


class Notification(BaseModel):
    """Notification model"""
    __tablename__ = "notifications"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    message = Column(Text)
    type = Column(String(50))  # payment_reminder, alert, info, success
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

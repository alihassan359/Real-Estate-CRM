"""
Audit Log Model
"""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from datetime import datetime

from models.base import BaseModel


class AuditLog(BaseModel):
    """Audit log model for tracking changes"""
    __tablename__ = "audit_logs"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    entity_type = Column(String(100))
    entity_id = Column(Integer)
    action = Column(String(50))  # create, update, delete
    old_values = Column(Text, nullable=True)  # JSON
    new_values = Column(Text, nullable=True)  # JSON
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

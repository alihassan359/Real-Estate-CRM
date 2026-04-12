"""
Job Log Model
"""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from datetime import datetime

from models.base import BaseModel


class JobLog(BaseModel):
    """Job execution log model"""
    __tablename__ = "job_logs"
    
    job_name = Column(String(255), index=True)
    status = Column(String(50))  # success, failed, running
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    result = Column(Text, nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)

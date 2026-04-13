"""
Project Model
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Numeric
from datetime import datetime

from models.base import BaseModel


class Project(BaseModel):
    """Project model"""
    __tablename__ = "projects"
    
    name = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    location = Column(String(255))
    city = Column(String(100))
    total_plots = Column(Integer)
    available_plots = Column(Integer)
    total_area = Column(Numeric(10, 2))  # in sq ft/meters
    price_per_sq_ft = Column(Numeric(10, 2))
    status = Column(String(50), default="active")  # active, completed, on_hold
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

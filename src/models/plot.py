"""
Plot Model
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Decimal

from models.base import BaseModel


class Plot(BaseModel):
    """Plot/Property model"""
    __tablename__ = "plots"
    
    plot_number = Column(String(50), unique=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    size = Column(Decimal(10, 2))  # in sq ft/meters
    location = Column(String(255))
    price = Column(Decimal(12, 2))
    status = Column(String(50), default="available")  # available, reserved, sold
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

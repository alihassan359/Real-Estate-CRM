"""
Deal Model
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, DateTime, Text
from datetime import datetime

from models.base import BaseModel


class Deal(BaseModel):
    """Deal/Contract model"""
    __tablename__ = "deals"
    
    deal_number = Column(String(50), unique=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    plot_id = Column(Integer, ForeignKey("plots.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    contract_date = Column(DateTime, default=datetime.utcnow)
    agreement_price = Column(Numeric(12, 2))
    down_payment = Column(Numeric(12, 2))
    remaining_balance = Column(Numeric(12, 2))
    payment_plan = Column(String(50))  # monthly, quarterly, semi-annual, annual
    status = Column(String(50), default="active")  # active, completed, cancelled
    notes = Column(Text, nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

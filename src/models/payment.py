"""
Payment Model
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, DateTime, Text
from datetime import datetime

from models.base import BaseModel


class Payment(BaseModel):
    """Payment transaction model"""
    __tablename__ = "payments"
    
    payment_number = Column(String(50), unique=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Numeric(12, 2))
    payment_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    payment_method = Column(String(50))  # bank_transfer, cash, check, online
    reference_number = Column(String(100), nullable=True)
    status = Column(String(50), default="pending")  # pending, paid, overdue, cancelled
    notes = Column(Text, nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

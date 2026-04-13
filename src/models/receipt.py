"""
Receipt Model
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, DateTime
from datetime import datetime

from models.base import BaseModel


class Receipt(BaseModel):
    """Receipt model"""
    __tablename__ = "receipts"
    
    receipt_number = Column(String(50), unique=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"))
    deal_id = Column(Integer, ForeignKey("deals.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Numeric(12, 2))
    issued_date = Column(DateTime, default=datetime.utcnow)
    description = Column(String(500))
    pdf_url = Column(String(500), nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

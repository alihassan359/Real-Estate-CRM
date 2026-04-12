"""
Client Model
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text

from models.base import BaseModel


class Client(BaseModel):
    """Client model"""
    __tablename__ = "clients"
    
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    cnic = Column(String(20), unique=True, nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100))
    province = Column(String(100), nullable=True)
    postal_code = Column(String(10), nullable=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

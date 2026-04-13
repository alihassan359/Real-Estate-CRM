"""Models package"""

# Import all models so they register with SQLAlchemy
from models.base import BaseModel
from models.user import User
from models.tenant import Tenant
from models.refresh_token import RefreshToken
from models.client import Client
from models.deal import Deal
from models.payment import Payment
from models.project import Project
from models.plot import Plot
from models.audit_log import AuditLog
from models.user_mfa import UserMFA
from models.job_log import JobLog
from models.notification import Notification
from models.receipt import Receipt

__all__ = [
    "BaseModel",
    "User",
    "Tenant",
    "RefreshToken",
    "Client",
    "Deal",
    "Payment",
    "Project",
    "Plot",
    "AuditLog",
    "UserMFA",
    "JobLog",
    "Notification",
    "Receipt",
]

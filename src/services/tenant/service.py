"""
Tenant Service - Business logic for tenant management
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.tenant import Tenant, SubscriptionPlan, TenantStatus
from schemas.tenant import TenantCreateRequest, TenantUpdateRequest
import json


class TenantService:
    """Service for tenant management operations"""
    
    # Subscription plan limits
    PLAN_LIMITS = {
        SubscriptionPlan.FREE: {
            "max_users": 2,
            "max_deals": 10,
            "max_storage_mb": 100,
        },
        SubscriptionPlan.BASIC: {
            "max_users": 5,
            "max_deals": 100,
            "max_storage_mb": 1024,
        },
        SubscriptionPlan.PRO: {
            "max_users": 20,
            "max_deals": 1000,
            "max_storage_mb": 5120,
        },
        SubscriptionPlan.ENTERPRISE: {
            "max_users": 100,
            "max_deals": 10000,
            "max_storage_mb": 51200,
        },
    }
    
    # Default tenant settings
    DEFAULT_SETTINGS = {
        "enable_whatsapp": True,
        "enable_email": True,
        "enable_sms": False,
        "commission_percentage": 0,
        "currency": "PKR",
        "timezone": "Asia/Karachi",
        "date_format": "DD-MM-YYYY",
        "language": "urdu",
        "auto_receipt": True,
        "payment_reminder_days": 7,
        "late_fee_percentage": 0,
        "features": {
            "advanced_analytics": False,
            "custom_branding": False,
            "api_access": False,
        }
    }
    
    @staticmethod
    def generate_tenant_code(company_name: str, db: Session) -> str:
        """Generate unique tenant code from company name"""
        # Take first 2-5 characters and uppercase
        base_code = ''.join(word[0].upper() for word in company_name.split()[:3])
        base_code = base_code[:5]
        
        # Check if code exists
        counter = 1
        code = base_code
        while db.query(Tenant).filter(Tenant.tenant_code == code).first():
            code = f"{base_code}{counter}"
            counter += 1
        
        return code
    
    @staticmethod
    def create_tenant(
        db: Session,
        company_name: str,
        company_email: Optional[str] = None,
        phone: Optional[str] = None,
        subscription_plan: SubscriptionPlan = SubscriptionPlan.FREE,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
    ) -> Tenant:
        """Create a new tenant"""
        
        # Check if company already exists
        existing = db.query(Tenant).filter(Tenant.company_name == company_name).first()
        if existing:
            raise ValueError(f"Tenant with company name '{company_name}' already exists")
        
        # Generate tenant code
        tenant_code = TenantService.generate_tenant_code(company_name, db)
        
        # Create tenant
        tenant = Tenant(
            tenant_code=tenant_code,
            company_name=company_name,
            company_email=company_email,
            phone=phone,
            subscription_plan=subscription_plan,
            address=address,
            city=city,
            country=country,
            status=TenantStatus.ACTIVE,
            settings=json.dumps(TenantService.DEFAULT_SETTINGS),
            metadata_info=json.dumps({}),
        )
        
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        
        return tenant
    
    @staticmethod
    def get_tenant_by_id(db: Session, tenant_id: int) -> Optional[Tenant]:
        """Get tenant by ID"""
        return db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    @staticmethod
    def get_tenant_by_code(db: Session, tenant_code: str) -> Optional[Tenant]:
        """Get tenant by code"""
        return db.query(Tenant).filter(Tenant.tenant_code == tenant_code).first()
    
    @staticmethod
    def get_all_tenants(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        status: Optional[TenantStatus] = None,
    ) -> tuple[List[Tenant], int]:
        """Get all tenants with pagination"""
        
        query = db.query(Tenant)
        
        # Apply status filter
        if status:
            query = query.filter(Tenant.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        tenants = query.offset(skip).limit(limit).all()
        
        return tenants, total
    
    @staticmethod
    def update_tenant(
        db: Session,
        tenant_id: int,
        company_name: Optional[str] = None,
        company_email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        logo_url: Optional[str] = None,
    ) -> Tenant:
        """Update tenant information"""
        
        tenant = TenantService.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        if company_name is not None:
            tenant.company_name = company_name
        if company_email is not None:
            tenant.company_email = company_email
        if phone is not None:
            tenant.phone = phone
        if address is not None:
            tenant.address = address
        if city is not None:
            tenant.city = city
        if country is not None:
            tenant.country = country
        if logo_url is not None:
            tenant.logo_url = logo_url
        
        tenant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(tenant)
        
        return tenant
    
    @staticmethod
    def update_settings(
        db: Session,
        tenant_id: int,
        settings: dict,
    ) -> Tenant:
        """Update tenant settings"""
        
        tenant = TenantService.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        # Merge with existing settings
        current_settings = json.loads(tenant.settings or '{}')
        current_settings.update(settings)
        
        tenant.settings = json.dumps(current_settings)
        tenant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(tenant)
        
        return tenant
    
    @staticmethod
    def upgrade_subscription(
        db: Session,
        tenant_id: int,
        new_plan: SubscriptionPlan,
        months: int = 1,
    ) -> Tenant:
        """Upgrade subscription plan"""
        
        tenant = TenantService.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        # Calculate paid_until date
        paid_until = datetime.utcnow() + timedelta(days=30 * months)
        
        tenant.subscription_plan = new_plan
        tenant.paid_until = paid_until
        tenant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(tenant)
        
        return tenant
    
    @staticmethod
    def suspend_tenant(
        db: Session,
        tenant_id: int,
        reason: Optional[str] = None,
    ) -> Tenant:
        """Suspend tenant account"""
        
        tenant = TenantService.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        tenant.status = TenantStatus.SUSPENDED
        
        # Add reason to metadata
        metadata = json.loads(tenant.metadata_info or '{}')
        metadata['suspension_reason'] = reason
        metadata['suspended_at'] = datetime.utcnow().isoformat()
        tenant.metadata_info = json.dumps(metadata)
        
        tenant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(tenant)
        
        return tenant
    
    @staticmethod
    def reactivate_tenant(db: Session, tenant_id: int) -> Tenant:
        """Reactivate suspended tenant"""
        
        tenant = TenantService.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        tenant.status = TenantStatus.ACTIVE
        
        # Update metadata
        metadata = json.loads(tenant.metadata_info or '{}')
        metadata['reactivated_at'] = datetime.utcnow().isoformat()
        tenant.metadata_info = json.dumps(metadata)
        
        tenant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(tenant)
        
        return tenant
    
    @staticmethod
    def deactivate_tenant(db: Session, tenant_id: int) -> Tenant:
        """Deactivate tenant"""
        
        tenant = TenantService.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        tenant.status = TenantStatus.INACTIVE
        tenant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(tenant)
        
        return tenant
    
    @staticmethod
    def get_tenant_usage(db: Session, tenant_id: int) -> dict:
        """Get tenant usage statistics"""
        from models.user import User
        from models.deal import Deal
        
        tenant = TenantService.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        # Get counts
        user_count = db.query(User).filter(User.tenant_id == tenant_id).count()
        deal_count = db.query(Deal).filter(Deal.tenant_id == tenant_id).count() if hasattr(Deal, 'tenant_id') else 0
        
        # Get plan limits
        limits = TenantService.PLAN_LIMITS.get(
            tenant.subscription_plan,
            TenantService.PLAN_LIMITS[SubscriptionPlan.FREE]
        )
        
        return {
            "current_users": user_count,
            "max_users": limits["max_users"],
            "current_deals": deal_count,
            "max_deals": limits["max_deals"],
            "storage_used_mb": 0,  # TODO: Implement storage tracking
            "storage_limit_mb": limits["max_storage_mb"],
            "subscription_plan": tenant.subscription_plan.value,
            "status": tenant.status.value,
            "paid_until": tenant.paid_until.isoformat() if tenant.paid_until else None,
        }
    
    @staticmethod
    def get_settings(db: Session, tenant_id: int) -> dict:
        """Get tenant settings"""
        
        tenant = TenantService.get_tenant_by_id(db, tenant_id)
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        return json.loads(tenant.settings or '{}')

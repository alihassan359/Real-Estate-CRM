"""
Tenant Management Tests
Validate tenant CRUD operations and business logic
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.tenant import Tenant, SubscriptionPlan, TenantStatus
from models.user import User
from services.tenant.service import TenantService
from database.session import SessionLocal


class TestTenantService:
    """Test tenant service operations"""
    
    @pytest.fixture(scope="function")
    def db(self):
        """Get database session"""
        session = SessionLocal()
        yield session
        session.close()
    
    def test_generate_tenant_code(self, db: Session):
        """Test tenant code generation"""
        # Test with single word
        code1 = TenantService.generate_tenant_code("Acme", db)
        assert code1 == "A"
        
        # Test with multiple words
        code2 = TenantService.generate_tenant_code("Real Estate Corp", db)
        assert code2 == "REC"
        
        # Verify uniqueness
        code3 = TenantService.generate_tenant_code("Real Estate Corp", db)
        assert code3 != code2  # Should generate different code
    
    def test_create_tenant(self, db: Session):
        """Test tenant creation"""
        tenant = TenantService.create_tenant(
            db=db,
            company_name="Test Company",
            company_email="test@example.com",
            phone="+1234567890",
            subscription_plan=SubscriptionPlan.BASIC,
            city="New York",
            country="USA",
        )
        
        assert tenant.id is not None
        assert tenant.company_name == "Test Company"
        assert tenant.subscription_plan == SubscriptionPlan.BASIC
        assert tenant.status == TenantStatus.ACTIVE
        assert tenant.settings is not None
        
        # Verify in database
        fetched = db.query(Tenant).filter(Tenant.id == tenant.id).first()
        assert fetched is not None
        assert fetched.company_name == "Test Company"
    
    def test_create_tenant_duplicate_company_name(self, db: Session):
        """Test duplicate company name rejection"""
        TenantService.create_tenant(
            db=db,
            company_name="Duplicate Test",
        )
        
        # Try to create another with same name
        with pytest.raises(ValueError, match="already exists"):
            TenantService.create_tenant(
                db=db,
                company_name="Duplicate Test",
            )
    
    def test_get_tenant_by_id(self, db: Session):
        """Test get tenant by ID"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Get Test Tenant",
        )
        
        fetched = TenantService.get_tenant_by_id(db, created.id)
        assert fetched is not None
        assert fetched.id == created.id
        
        # Test non-existent
        fetched = TenantService.get_tenant_by_id(db, 99999)
        assert fetched is None
    
    def test_get_tenant_by_code(self, db: Session):
        """Test get tenant by code"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Code Test Tenant",
        )
        
        fetched = TenantService.get_tenant_by_code(db, created.tenant_code)
        assert fetched is not None
        assert fetched.tenant_code == created.tenant_code
    
    def test_update_tenant(self, db: Session):
        """Test tenant update"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Update Test",
        )
        
        updated = TenantService.update_tenant(
            db=db,
            tenant_id=created.id,
            phone="+1234567890",
            city="New York",
            logo_url="https://example.com/logo.png",
        )
        
        assert updated.phone == "+1234567890"
        assert updated.city == "New York"
        assert updated.logo_url == "https://example.com/logo.png"
    
    def test_update_settings(self, db: Session):
        """Test settings update"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Settings Test",
        )
        
        new_settings = {
            "currency": "USD",
            "timezone": "America/New_York",
            "language": "en",
        }
        
        updated = TenantService.update_settings(
            db=db,
            tenant_id=created.id,
            settings=new_settings,
        )
        
        # Verify settings were updated
        settings = TenantService.get_settings(db, created.id)
        assert settings["currency"] == "USD"
        assert settings["timezone"] == "America/New_York"
    
    def test_upgrade_subscription(self, db: Session):
        """Test subscription upgrade"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Upgrade Test",
            subscription_plan=SubscriptionPlan.FREE,
        )
        
        upgraded = TenantService.upgrade_subscription(
            db=db,
            tenant_id=created.id,
            new_plan=SubscriptionPlan.PRO,
            months=12,
        )
        
        assert upgraded.subscription_plan == SubscriptionPlan.PRO
        assert upgraded.paid_until is not None
    
    def test_suspend_tenant(self, db: Session):
        """Test tenant suspension"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Suspend Test",
        )
        
        suspended = TenantService.suspend_tenant(
            db=db,
            tenant_id=created.id,
            reason="Non-payment",
        )
        
        assert suspended.status == TenantStatus.SUSPENDED
    
    def test_reactivate_tenant(self, db: Session):
        """Test tenant reactivation"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Reactivate Test",
        )
        
        # Suspend first
        TenantService.suspend_tenant(db=db, tenant_id=created.id)
        
        # Reactivate
        reactivated = TenantService.reactivate_tenant(db=db, tenant_id=created.id)
        
        assert reactivated.status == TenantStatus.ACTIVE
    
    def test_deactivate_tenant(self, db: Session):
        """Test tenant deactivation"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Deactivate Test",
        )
        
        deactivated = TenantService.deactivate_tenant(db=db, tenant_id=created.id)
        
        assert deactivated.status == TenantStatus.INACTIVE
    
    def test_get_all_tenants_pagination(self, db: Session):
        """Test tenant listing with pagination"""
        # Create multiple tenants
        for i in range(5):
            TenantService.create_tenant(
                db=db,
                company_name=f"Tenant {i}",
            )
        
        # Get first page
        tenants, total = TenantService.get_all_tenants(db=db, skip=0, limit=2)
        assert len(tenants) == 2
        assert total >= 5
        
        # Get second page
        tenants2, _ = TenantService.get_all_tenants(db=db, skip=2, limit=2)
        assert len(tenants2) == 2
    
    def test_get_all_tenants_status_filter(self, db: Session):
        """Test tenant listing with status filter"""
        # Create active tenant
        active = TenantService.create_tenant(
            db=db,
            company_name="Active Tenant",
        )
        
        # Create suspended tenant
        suspended = TenantService.create_tenant(
            db=db,
            company_name="Suspended Tenant",
        )
        TenantService.suspend_tenant(db=db, tenant_id=suspended.id)
        
        # Get only active
        tenants, _ = TenantService.get_all_tenants(
            db=db,
            status=TenantStatus.ACTIVE,
        )
        
        active_ids = [t.id for t in tenants]
        assert active.id in active_ids
        assert suspended.id not in active_ids
    
    def test_get_tenant_usage(self, db: Session):
        """Test tenant usage retrieval"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Usage Test",
            subscription_plan=SubscriptionPlan.PRO,
        )
        
        usage = TenantService.get_tenant_usage(db, created.id)
        
        assert usage["current_users"] >= 0
        assert usage["max_users"] > 0
        assert usage["subscription_plan"] == "PRO"
        assert usage["status"] == "ACTIVE"
    
    def test_subscription_plan_limits(self):
        """Test subscription plan limits"""
        limits = TenantService.PLAN_LIMITS
        
        assert limits[SubscriptionPlan.FREE]["max_users"] == 2
        assert limits[SubscriptionPlan.BASIC]["max_users"] == 5
        assert limits[SubscriptionPlan.PRO]["max_users"] == 20
        assert limits[SubscriptionPlan.ENTERPRISE]["max_users"] == 100
        
        # Verify all plans have required keys
        required_keys = {"max_users", "max_deals", "max_storage_mb"}
        for plan, limits_dict in limits.items():
            assert set(limits_dict.keys()) == required_keys


class TestTenantDataIntegrity:
    """Test data integrity and constraints"""
    
    @pytest.fixture(scope="function")
    def db(self):
        """Get database session"""
        session = SessionLocal()
        yield session
        session.close()
    
    def test_tenant_code_uniqueness(self, db: Session):
        """Test tenant code uniqueness constraint"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Unique Code Test",
        )
        
        # Try to manually create duplicate (will fail at DB constraint level)
        duplicate = Tenant(
            tenant_code=created.tenant_code,
            company_name="Different Name",
            subscription_plan=SubscriptionPlan.FREE,
        )
        db.add(duplicate)
        
        with pytest.raises(Exception):  # SQLAlchemy integrity error
            db.commit()
    
    def test_tenant_company_name_uniqueness(self, db: Session):
        """Test company name uniqueness"""
        TenantService.create_tenant(
            db=db,
            company_name="Unique Name",
        )
        
        with pytest.raises(ValueError):
            TenantService.create_tenant(
                db=db,
                company_name="Unique Name",
            )
    
    def test_default_settings_on_creation(self, db: Session):
        """Test default settings are set on tenant creation"""
        created = TenantService.create_tenant(
            db=db,
            company_name="Default Settings Test",
        )
        
        settings = TenantService.get_settings(db, created.id)
        
        # Verify default settings
        assert "currency" in settings
        assert "timezone" in settings
        assert "language" in settings
        assert settings["enable_email"] is True
        assert settings["commission_percentage"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

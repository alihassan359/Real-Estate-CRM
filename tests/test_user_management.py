"""
User Management Tests
"""

import pytest
from sqlalchemy.orm import Session
from models.user import User, UserRole, UserStatus
from services.user.service import UserService
from config.permissions import Permission, has_permission, has_any_permission, has_all_permissions


class TestUserService:
    """Test UserService methods"""
    
    @pytest.fixture
    def mock_db(self, mocker):
        """Mock database session"""
        return mocker.MagicMock(spec=Session)
    
    def test_get_user_permissions_tenant_owner(self):
        """Test getting permissions for TENANT_OWNER role"""
        permissions = [p for p in [Permission.CREATE_USER, Permission.VIEW_USERS, Permission.MANAGE_ROLES]]
        
        assert has_permission(UserRole.TENANT_OWNER, Permission.CREATE_USER)
        assert has_permission(UserRole.TENANT_OWNER, Permission.VIEW_USERS)
        assert has_permission(UserRole.TENANT_OWNER, Permission.MANAGE_ROLES)
    
    def test_get_user_permissions_operator(self):
        """Test getting permissions for OPERATOR role"""
        assert has_permission(UserRole.OPERATOR, Permission.CREATE_DEAL)
        assert has_permission(UserRole.OPERATOR, Permission.VIEW_OWN_DEALS)
        assert not has_permission(UserRole.OPERATOR, Permission.DELETE_USER)
        assert not has_permission(UserRole.OPERATOR, Permission.MANAGE_ROLES)
    
    def test_has_any_permission(self):
        """Test has_any_permission function"""
        permissions = [Permission.CREATE_DEAL, Permission.DELETE_DEAL]
        
        # MANAGER has CREATE_DEAL
        assert has_any_permission(UserRole.MANAGER, permissions)
        
        # OPERATOR doesn't have DELETE_DEAL but has CREATE_DEAL
        assert has_any_permission(UserRole.OPERATOR, permissions)
        
        # ACCOUNTANT doesn't have either
        assert not has_any_permission(
            UserRole.ACCOUNTANT,
            [Permission.DELETE_DEAL, Permission.MANAGE_ROLES]
        )
    
    def test_has_all_permissions(self):
        """Test has_all_permissions function"""
        permissions = [Permission.CREATE_USER, Permission.VIEW_USERS]
        
        # TENANT_OWNER has both
        assert has_all_permissions(UserRole.TENANT_OWNER, permissions)
        
        # MANAGER doesn't have both
        assert not has_all_permissions(UserRole.MANAGER, permissions)
    
    def test_permission_hierarchy(self):
        """Test permission hierarchy"""
        # SUPER_ADMIN should have all permissions
        super_admin_perms = [p for p in Permission]
        
        assert all(
            has_permission(UserRole.SUPER_ADMIN, perm)
            for perm in super_admin_perms[:5]  # Check at least first 5
        )
        
        # OPERATOR has limited permissions
        operator_perms = [
            Permission.CREATE_DEAL,
            Permission.VIEW_OWN_DEALS,
            Permission.UPDATE_DEAL,
        ]
        
        assert all(
            has_permission(UserRole.OPERATOR, perm)
            for perm in operator_perms
        )


class TestRoleHierarchy:
    """Test role hierarchy"""
    
    def test_role_values(self):
        """Test role enum values"""
        assert UserRole.SUPER_ADMIN.value == "SUPER_ADMIN"
        assert UserRole.PLATFORM_ADMIN.value == "PLATFORM_ADMIN"
        assert UserRole.TENANT_OWNER.value == "TENANT_OWNER"
        assert UserRole.MANAGER.value == "MANAGER"
        assert UserRole.OPERATOR.value == "OPERATOR"
        assert UserRole.ACCOUNTANT.value == "ACCOUNTANT"
        assert UserRole.SALESMAN.value == "SALESMAN"
    
    def test_user_status_values(self):
        """Test user status enum values"""
        assert UserStatus.ACTIVE.value == "ACTIVE"
        assert UserStatus.INACTIVE.value == "INACTIVE"
        assert UserStatus.SUSPENDED.value == "SUSPENDED"


class TestPermissionMatrix:
    """Test complete permission matrix"""
    
    def test_super_admin_full_access(self):
        """SUPER_ADMIN should have all critical permissions"""
        critical_perms = [
            Permission.MANAGE_TENANTS,
            Permission.MANAGE_PLATFORM_ADMINS,
            Permission.CREATE_USER,
            Permission.DELETE_USER,
            Permission.VIEW_AUDIT_LOGS,
        ]
        
        for perm in critical_perms:
            assert has_permission(UserRole.SUPER_ADMIN, perm), \
                f"SUPER_ADMIN missing {perm}"
    
    def test_tenant_owner_tenant_control(self):
        """TENANT_OWNER should control their tenant"""
        owner_perms = [
            Permission.CREATE_USER,
            Permission.VIEW_USERS,
            Permission.DELETE_USER,
            Permission.MANAGE_ROLES,
            Permission.CREATE_DEAL,
            Permission.RECORD_PAYMENT,
            Permission.MANAGE_SETTINGS,
        ]
        
        for perm in owner_perms:
            assert has_permission(UserRole.TENANT_OWNER, perm), \
                f"TENANT_OWNER missing {perm}"
    
    def test_operator_limited_access(self):
        """OPERATOR should have limited access"""
        # Should NOT have
        restricted_perms = [
            Permission.CREATE_USER,
            Permission.DELETE_USER,
            Permission.MANAGE_ROLES,
            Permission.RECORD_PAYMENT,
            Permission.DELETE_DEAL,
        ]
        
        for perm in restricted_perms:
            assert not has_permission(UserRole.OPERATOR, perm), \
                f"OPERATOR shouldn't have {perm}"
        
        # Should have
        allowed_perms = [
            Permission.CREATE_DEAL,
            Permission.VIEW_OWN_DEALS,
        ]
        
        for perm in allowed_perms:
            assert has_permission(UserRole.OPERATOR, perm), \
                f"OPERATOR missing {perm}"
    
    def test_accountant_payment_focused(self):
        """ACCOUNTANT should focus on payments"""
        required_perms = [
            Permission.RECORD_PAYMENT,
            Permission.VIEW_PAYMENTS,
            Permission.GENERATE_RECEIPT,
            Permission.RECONCILE_PAYMENTS,
            Permission.EXPORT_PAYMENTS,
        ]
        
        for perm in required_perms:
            assert has_permission(UserRole.ACCOUNTANT, perm), \
                f"ACCOUNTANT missing {perm}"
        
        # Should NOT have user management
        assert not has_permission(UserRole.ACCOUNTANT, Permission.CREATE_USER)
        assert not has_permission(UserRole.ACCOUNTANT, Permission.DELETE_USER)
    
    def test_salesman_limited_deal_view(self):
        """SALESMAN should have limited deal viewing"""
        perms = [
            Permission.VIEW_OWN_DEALS,
            Permission.UPDATE_DEAL,
            Permission.VIEW_OWN_CLIENTS,
        ]
        
        for perm in perms:
            assert has_permission(UserRole.SALESMAN, perm), \
                f"SALESMAN missing {perm}"
        
        # Should NOT have comprehensive access
        assert not has_permission(UserRole.SALESMAN, Permission.VIEW_ALL_DEALS)
        assert not has_permission(UserRole.SALESMAN, Permission.CREATE_DEAL)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

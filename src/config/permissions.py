"""
Permission definitions and mappings
"""

from enum import Enum
from models.user import UserRole

# ============================================================================
# PERMISSIONS
# ============================================================================

class Permission(str, Enum):
    """All available permissions in the system"""
    
    # DEAL PERMISSIONS
    CREATE_DEAL = "create_deal"
    VIEW_ALL_DEALS = "view_all_deals"
    VIEW_OWN_DEALS = "view_own_deals"
    UPDATE_DEAL = "update_deal"
    DELETE_DEAL = "delete_deal"
    APPROVE_DEAL = "approve_deal"
    REJECT_DEAL = "reject_deal"
    
    # PAYMENT PERMISSIONS
    RECORD_PAYMENT = "record_payment"
    VIEW_PAYMENTS = "view_payments"
    GENERATE_RECEIPT = "generate_receipt"
    RECONCILE_PAYMENTS = "reconcile_payments"
    EXPORT_PAYMENTS = "export_payments"
    
    # CLIENT PERMISSIONS
    CREATE_CLIENT = "create_client"
    VIEW_ALL_CLIENTS = "view_all_clients"
    VIEW_OWN_CLIENTS = "view_own_clients"
    EDIT_CLIENT = "edit_client"
    DELETE_CLIENT = "delete_client"
    
    # PROJECT PERMISSIONS
    CREATE_PROJECT = "create_project"
    VIEW_ALL_PROJECTS = "view_all_projects"
    EDIT_PROJECT = "edit_project"
    DELETE_PROJECT = "delete_project"
    
    # USER PERMISSIONS
    CREATE_USER = "create_user"
    VIEW_USERS = "view_users"
    EDIT_USER = "edit_user"
    DELETE_USER = "delete_user"
    MANAGE_ROLES = "manage_roles"
    SUSPEND_USER = "suspend_user"
    
    # REPORT PERMISSIONS
    VIEW_REPORTS = "view_reports"
    EXPORT_REPORTS = "export_reports"
    VIEW_ANALYTICS = "view_analytics"
    VIEW_AUDIT_LOGS = "view_audit_logs"
    
    # TENANT PERMISSIONS
    MANAGE_TENANTS = "manage_tenants"
    VIEW_ASSIGNED_TENANTS = "view_assigned_tenants"
    VIEW_ALL_TENANTS = "view_all_tenants"
    MANAGE_TENANT_SETTINGS = "manage_tenant_settings"
    SUSPEND_TENANT = "suspend_tenant"
    
    # ADMIN PERMISSIONS
    MANAGE_PLATFORM_ADMINS = "manage_platform_admins"
    MANAGE_SUBSCRIPTION_PLANS = "manage_subscription_plans"
    SYSTEM_CONFIGURATION = "system_configuration"
    
    # INTEGRATION PERMISSIONS
    MANAGE_INTEGRATIONS = "manage_integrations"
    MANAGE_SETTINGS = "manage_settings"


# ============================================================================
# ROLE TO PERMISSIONS MAPPING
# ============================================================================

ROLE_PERMISSIONS = {
    UserRole.SUPER_ADMIN: [
        # Tenant management
        Permission.MANAGE_TENANTS,
        Permission.VIEW_ALL_TENANTS,
        Permission.SUSPEND_TENANT,
        
        # User management
        Permission.CREATE_USER,
        Permission.VIEW_USERS,
        Permission.EDIT_USER,
        Permission.DELETE_USER,
        Permission.MANAGE_ROLES,
        Permission.SUSPEND_USER,
        
        # Admin
        Permission.MANAGE_PLATFORM_ADMINS,
        Permission.MANAGE_SUBSCRIPTION_PLANS,
        Permission.SYSTEM_CONFIGURATION,
        
        # Audit & Reports
        Permission.VIEW_AUDIT_LOGS,
        Permission.VIEW_REPORTS,
        Permission.EXPORT_REPORTS,
    ],
    
    UserRole.PLATFORM_ADMIN: [
        # Limited tenant management
        Permission.VIEW_ASSIGNED_TENANTS,
        Permission.MANAGE_TENANT_SETTINGS,
        Permission.SUSPEND_TENANT,
        
        # Reports
        Permission.VIEW_AUDIT_LOGS,
        Permission.VIEW_REPORTS,
    ],
    
    UserRole.TENANT_OWNER: [
        # User management
        Permission.CREATE_USER,
        Permission.VIEW_USERS,
        Permission.EDIT_USER,
        Permission.DELETE_USER,
        Permission.MANAGE_ROLES,
        Permission.SUSPEND_USER,
        
        # Deal management
        Permission.CREATE_DEAL,
        Permission.VIEW_ALL_DEALS,
        Permission.APPROVE_DEAL,
        Permission.REJECT_DEAL,
        Permission.DELETE_DEAL,
        
        # Payment management
        Permission.RECORD_PAYMENT,
        Permission.VIEW_PAYMENTS,
        Permission.GENERATE_RECEIPT,
        Permission.RECONCILE_PAYMENTS,
        Permission.EXPORT_PAYMENTS,
        
        # Client management
        Permission.CREATE_CLIENT,
        Permission.VIEW_ALL_CLIENTS,
        Permission.EDIT_CLIENT,
        Permission.DELETE_CLIENT,
        
        # Project management
        Permission.CREATE_PROJECT,
        Permission.VIEW_ALL_PROJECTS,
        Permission.EDIT_PROJECT,
        Permission.DELETE_PROJECT,
        
        # Reports & Analytics
        Permission.VIEW_REPORTS,
        Permission.EXPORT_REPORTS,
        Permission.VIEW_ANALYTICS,
        Permission.VIEW_AUDIT_LOGS,
        
        # Settings
        Permission.MANAGE_SETTINGS,
        Permission.MANAGE_INTEGRATIONS,
    ],
    
    UserRole.MANAGER: [
        # User management (limited - only can manage subordinates)
        Permission.VIEW_USERS,
        Permission.CREATE_USER,
        Permission.EDIT_USER,
        
        # Deal management
        Permission.CREATE_DEAL,
        Permission.VIEW_ALL_DEALS,
        Permission.UPDATE_DEAL,
        
        # Client management
        Permission.CREATE_CLIENT,
        Permission.VIEW_ALL_CLIENTS,
        Permission.EDIT_CLIENT,
        
        # Project management
        Permission.CREATE_PROJECT,
        Permission.VIEW_ALL_PROJECTS,
        
        # Reports
        Permission.VIEW_REPORTS,
        Permission.VIEW_ANALYTICS,
    ],
    
    UserRole.OPERATOR: [
        # Deal management
        Permission.CREATE_DEAL,
        Permission.VIEW_OWN_DEALS,
        Permission.UPDATE_DEAL,
        
        # Client management
        Permission.CREATE_CLIENT,
        Permission.VIEW_OWN_CLIENTS,
        
        # Comments
        Permission.VIEW_REPORTS,
    ],
    
    UserRole.ACCOUNTANT: [
        # Deal viewing
        Permission.VIEW_ALL_DEALS,
        
        # Payment management
        Permission.RECORD_PAYMENT,
        Permission.VIEW_PAYMENTS,
        Permission.GENERATE_RECEIPT,
        Permission.RECONCILE_PAYMENTS,
        Permission.EXPORT_PAYMENTS,
        
        # Reports
        Permission.VIEW_REPORTS,
        Permission.EXPORT_REPORTS,
    ],
    
    UserRole.SALESMAN: [
        # Deal management (limited)
        Permission.VIEW_OWN_DEALS,
        Permission.UPDATE_DEAL,
        
        # Client viewing
        Permission.VIEW_OWN_CLIENTS,
    ],
}


def get_user_permissions(role: UserRole) -> list[Permission]:
    """Get all permissions for a given role"""
    return ROLE_PERMISSIONS.get(role, [])


def has_permission(role: UserRole, permission: Permission) -> bool:
    """Check if a role has a specific permission"""
    permissions = get_user_permissions(role)
    return permission in permissions


def has_any_permission(role: UserRole, permissions: list[Permission]) -> bool:
    """Check if role has any of the given permissions"""
    user_perms = get_user_permissions(role)
    return any(perm in user_perms for perm in permissions)


def has_all_permissions(role: UserRole, permissions: list[Permission]) -> bool:
    """Check if role has all of the given permissions"""
    user_perms = get_user_permissions(role)
    return all(perm in user_perms for perm in permissions)

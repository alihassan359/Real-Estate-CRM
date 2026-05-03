"""
Role-Based Access Control (RBAC) Middleware
Checks user permissions for protected endpoints
"""

from fastapi import HTTPException, Depends
from typing import List

from config.permissions import Permission, has_permission, has_any_permission, has_all_permissions
from middlewares.auth_middleware import get_current_user
from models.user import User


def check_permission(required_permission: Permission):
    """
    Dependency to check if current user has a specific permission
    
    Usage:
        @router.post("/deals")
        async def create_deal(user: User = Depends(check_permission(Permission.CREATE_DEAL))):
            pass
    """
    async def verify_permission(user: User = Depends(get_current_user)) -> User:
        if not has_permission(user.role, required_permission):
            raise HTTPException(
                status_code=403,
                detail=f"Missing permission: {required_permission.value}"
            )
        return user
    return verify_permission


def check_any_permission(permissions: List[Permission]):
    """
    Check if user has ANY of the given permissions
    """
    async def verify_permission(user: User = Depends(get_current_user)) -> User:
        if not has_any_permission(user.role, permissions):
            perms_str = ", ".join([p.value for p in permissions])
            raise HTTPException(
                status_code=403,
                detail=f"Missing at least one permission: {perms_str}"
            )
        return user
    return verify_permission


def check_all_permissions(permissions: List[Permission]):
    """
    Check if user has ALL of the given permissions
    """
    async def verify_permission(user: User = Depends(get_current_user)) -> User:
        if not has_all_permissions(user.role, permissions):
            perms_str = ", ".join([p.value for p in permissions])
            raise HTTPException(
                status_code=403,
                detail=f"Missing required permissions: {perms_str}"
            )
        return user
    return verify_permission


async def check_tenant_owner(user: User = Depends(get_current_user)) -> User:
    """Check if user is a tenant owner"""
    if user.role.value != "TENANT_OWNER":
        raise HTTPException(
            status_code=403,
            detail="Only tenant owners can perform this action"
        )
    return user


async def check_admin(user: User = Depends(get_current_user)) -> User:
    """Check if user is an admin (TENANT_OWNER, MANAGER, PLATFORM_ADMIN, SUPER_ADMIN)"""
    if user.role.value not in ["TENANT_OWNER", "MANAGER", "PLATFORM_ADMIN", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return user


async def check_super_admin(user: User = Depends(get_current_user)) -> User:
    """Check if user is a super admin"""
    if user.role.value != "SUPER_ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Super admin access required"
        )
    return user


async def check_platform_admin(user: User = Depends(get_current_user)) -> User:
    """Check if user is a platform admin or super admin"""
    if user.role.value not in ["PLATFORM_ADMIN", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=403,
            detail="Platform admin access required"
        )
    return user

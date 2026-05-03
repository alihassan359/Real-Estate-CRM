"""
Users Management Routes - Complete CRUD and permission management
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from database.session import get_db
from middlewares.auth_middleware import get_current_user
from middlewares.rbac_middleware import (
    check_permission,
    check_tenant_owner,
)
from models.user import User, UserRole, UserStatus
from services.user.service import UserService
from schemas.user import (
    UserCreateRequest,
    UserUpdateRequest,
    UserRoleUpdateRequest,
    ChangePasswordRequest,
    ResetPasswordRequest,
    SuspendUserRequest,
    UserResponse,
    UserDetailResponse,
    UserListResponse,
    SingleUserResponse,
    UserCreatedResponse,
    UserUpdatedResponse,
    UserDeletedResponse,
    PasswordChangedResponse,
    ErrorResponse,
)
from config.permissions import Permission

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserCreatedResponse,
    status_code=201,
    summary="Create a new user",
    responses={
        403: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
    }
)
async def create_user(
    request: UserCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.CREATE_USER)),
):
    """Create a new user in the tenant"""
    try:
        # Verify user can create in this tenant
        if current_user.role not in [UserRole.TENANT_OWNER, UserRole.MANAGER]:
            raise HTTPException(
                status_code=403,
                detail="Only TENANT_OWNER or MANAGER can create users"
            )
        
        # Create the user
        new_user = UserService.create_user(
            db=db,
            tenant_id=current_user.tenant_id,
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
            role=request.role,
            phone=request.phone,
            created_by=current_user.id,
        )
        
        return UserCreatedResponse(
            success=True,
            message="User created successfully",
            data=UserResponse.from_orm(new_user),
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")


@router.get(
    "/",
    response_model=UserListResponse,
    summary="List users in tenant",
    responses={
        403: {"model": ErrorResponse},
    }
)
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.VIEW_USERS)),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    role: str = Query(None),
    status: str = Query(None),
):
    """List all users in the tenant with pagination"""
    
    # Parse role filter
    role_filter = None
    if role:
        try:
            role_filter = UserRole[role.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid role: {role}")
    
    # Parse status filter
    status_filter = None
    if status:
        try:
            status_filter = UserStatus[status.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    # Get users
    users, total = UserService.get_tenant_users(
        db=db,
        tenant_id=current_user.tenant_id,
        skip=skip,
        limit=limit,
        role=role_filter,
        status=status_filter,
    )
    
    return UserListResponse(
        success=True,
        data=[UserResponse.from_orm(u) for u in users],
        pagination={
            "skip": skip,
            "limit": limit,
            "total": total,
        }
    )


@router.get(
    "/{user_id}",
    response_model=SingleUserResponse,
    summary="Get user details",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def get_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed user information"""
    
    # Get the requested user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot view user from different tenant")
    
    if user.id != current_user.id and current_user.role not in [
        UserRole.TENANT_OWNER,
        UserRole.MANAGER,
    ]:
        raise HTTPException(status_code=403, detail="Cannot view other user's profile")
    
    # Get permissions
    permissions = UserService.get_user_permissions(user)
    
    user_detail = UserDetailResponse.from_orm(user)
    user_detail.permissions = permissions
    
    return SingleUserResponse(
        success=True,
        data=user_detail,
    )


@router.patch(
    "/{user_id}/profile",
    response_model=UserUpdatedResponse,
    summary="Update user profile",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def update_profile(
    user_id: int = Path(..., gt=0),
    request: UserUpdateRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update user profile information"""
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot update user from different tenant")
    
    if user.id != current_user.id and current_user.role not in [
        UserRole.TENANT_OWNER,
        UserRole.MANAGER,
    ]:
        raise HTTPException(status_code=403, detail="Cannot update other user's profile")
    
    # Update profile
    updated_user = UserService.update_user_profile(
        db=db,
        user_id=user_id,
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        avatar_url=request.avatar_url,
    )
    
    return UserUpdatedResponse(
        success=True,
        message="Profile updated successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.patch(
    "/{user_id}/role",
    response_model=UserUpdatedResponse,
    summary="Update user role",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def update_role(
    user_id: int = Path(..., gt=0),
    request: UserRoleUpdateRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.MANAGE_ROLES)),
) -> UserUpdatedResponse:
    """Update user role"""
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot update user from different tenant")
    
    if current_user.role != UserRole.TENANT_OWNER:
        raise HTTPException(status_code=403, detail="Only TENANT_OWNER can change roles")
    
    # Update role
    updated_user = UserService.update_user_role(
        db=db,
        user_id=user_id,
        new_role=request.role,
    )
    
    return UserUpdatedResponse(
        success=True,
        message="User role updated successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.post(
    "/{user_id}/change-password",
    response_model=PasswordChangedResponse,
    summary="Change user password",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def change_password(
    user_id: int = Path(..., gt=0),
    request: ChangePasswordRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Change user password - users can only change their own"""
    
    # Check authorization
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only change your own password")
    
    try:
        UserService.change_password(
            db=db,
            user_id=user_id,
            current_password=request.current_password,
            new_password=request.new_password,
        )
        
        return PasswordChangedResponse(
            success=True,
            message="Password changed successfully",
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{user_id}/reset-password",
    response_model=PasswordChangedResponse,
    summary="Reset user password (admin)",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def reset_password(
    user_id: int = Path(..., gt=0),
    request: ResetPasswordRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_tenant_owner),
):
    """Reset user password - admin action"""
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot reset password for user from different tenant")
    
    UserService.reset_password(
        db=db,
        user_id=user_id,
        new_password=request.new_password,
    )
    
    return PasswordChangedResponse(
        success=True,
        message="Password reset successfully",
    )


@router.patch(
    "/{user_id}/disable",
    response_model=UserUpdatedResponse,
    summary="Disable user account",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def disable_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.SUSPEND_USER)),
):
    """Disable user account"""
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot disable user from different tenant")
    
    updated_user = UserService.disable_user(db=db, user_id=user_id)
    
    return UserUpdatedResponse(
        success=True,
        message="User disabled successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.patch(
    "/{user_id}/enable",
    response_model=UserUpdatedResponse,
    summary="Enable user account",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def enable_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.SUSPEND_USER)),
):
    """Enable user account"""
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot enable user from different tenant")
    
    updated_user = UserService.enable_user(db=db, user_id=user_id)
    
    return UserUpdatedResponse(
        success=True,
        message="User enabled successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.patch(
    "/{user_id}/suspend",
    response_model=UserUpdatedResponse,
    summary="Suspend user account",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def suspend_user(
    user_id: int = Path(..., gt=0),
    request: SuspendUserRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.SUSPEND_USER)),
):
    """Suspend user account"""
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot suspend user from different tenant")
    
    updated_user = UserService.suspend_user(db=db, user_id=user_id, reason=request.reason)
    
    return UserUpdatedResponse(
        success=True,
        message="User suspended successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.delete(
    "/{user_id}",
    response_model=UserDeletedResponse,
    summary="Delete user (soft delete)",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def delete_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.DELETE_USER)),
):
    """Delete user - marks as INACTIVE"""
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot delete user from different tenant")
    
    # Prevent deleting yourself
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    UserService.disable_user(db=db, user_id=user_id)
    
    return UserDeletedResponse(
        success=True,
        message="User deleted successfully",
    )

from models.user import User, UserRole, UserStatus
from services.user.service import UserService
from schemas.user import (
    UserCreateRequest,
    UserUpdateRequest,
    UserRoleUpdateRequest,
    ChangePasswordRequest,
    ResetPasswordRequest,
    SuspendUserRequest,
    UserResponse,
    UserDetailResponse,
    UserListResponse,
    SingleUserResponse,
    UserCreatedResponse,
    UserUpdatedResponse,
    UserDeletedResponse,
    PasswordChangedResponse,
    ErrorResponse,
)
from config.permissions import Permission

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserCreatedResponse,
    status_code=201,
    summary="Create a new user",
    responses={
        403: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
    }
)
async def create_user(
    request: UserCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.CREATE_USER)),
):
    """
    Create a new user in the tenant
    
    **Permissions Required:**
    - `create_user`
    
    **Allowed Roles:**
    - TENANT_OWNER
    - MANAGER
    """
    try:
        # Verify user can create in this tenant
        if current_user.role not in [UserRole.TENANT_OWNER, UserRole.MANAGER]:
            raise HTTPException(
                status_code=403,
                detail="Only TENANT_OWNER or MANAGER can create users"
            )
        
        # Create the user
        new_user = UserService.create_user(
            db=db,
            tenant_id=current_user.tenant_id,
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
            role=request.role,
            phone=request.phone,
            created_by=current_user.id,
        )
        
        return UserCreatedResponse(
            success=True,
            message="User created successfully",
            data=UserResponse.from_orm(new_user),
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")


@router.get(
    "/",
    response_model=UserListResponse,
    summary="List users in tenant",
    responses={
        403: {"model": ErrorResponse},
    }
)
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.VIEW_USERS)),
    skip: int = Query(0, ge=0, description="Skip count"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    role: str = Query(None, description="Filter by role"),
    status: str = Query(None, description="Filter by status"),
):
    """
    List all users in the tenant with pagination
    
    **Permissions Required:**
    - `view_users`
    
    **Allowed Roles:**
    - TENANT_OWNER
    - MANAGER
    - All users (see own info)
    """
    
    # Parse role filter
    role_filter = None
    if role:
        try:
            role_filter = UserRole[role.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid role: {role}")
    
    # Parse status filter
    status_filter = None
    if status:
        try:
            status_filter = UserStatus[status.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    # Get users
    users, total = UserService.get_tenant_users(
        db=db,
        tenant_id=current_user.tenant_id,
        skip=skip,
        limit=limit,
        role=role_filter,
        status=status_filter,
    )
    
    return UserListResponse(
        success=True,
        data=[UserResponse.from_orm(u) for u in users],
        pagination={
            "skip": skip,
            "limit": limit,
            "total": total,
        }
    )


@router.get(
    "/{user_id}",
    response_model=SingleUserResponse,
    summary="Get user details",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def get_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get detailed user information
    
    Users can see their own profile. Admins can see any user in their tenant.
    """
    
    # Get the requested user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot view user from different tenant")
    
    if user.id != current_user.id and current_user.role not in [
        UserRole.TENANT_OWNER,
        UserRole.MANAGER,
    ]:
        raise HTTPException(status_code=403, detail="Cannot view other user's profile")
    
    # Get permissions
    permissions = UserService.get_user_permissions(user)
    
    user_detail = UserDetailResponse.from_orm(user)
    user_detail.permissions = permissions
    
    return SingleUserResponse(
        success=True,
        data=user_detail,
    )


@router.patch(
    "/{user_id}/profile",
    response_model=UserUpdatedResponse,
    summary="Update user profile",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def update_profile(
    user_id: int = Path(..., gt=0),
    request: UserUpdateRequest = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update user profile information
    
    Users can update their own profile. Admins can update any user.
    """
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot update user from different tenant")
    
    if user.id != current_user.id and current_user.role not in [
        UserRole.TENANT_OWNER,
        UserRole.MANAGER,
    ]:
        raise HTTPException(status_code=403, detail="Cannot update other user's profile")
    
    # Update profile
    updated_user = UserService.update_user_profile(
        db=db,
        user_id=user_id,
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        avatar_url=request.avatar_url,
    )
    
    return UserUpdatedResponse(
        success=True,
        message="Profile updated successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.patch(
    "/{user_id}/role",
    response_model=UserUpdatedResponse,
    summary="Update user role",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def update_role(
    user_id: int = Path(..., gt=0),
    request: UserRoleUpdateRequest = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.MANAGE_ROLES)),
) -> UserUpdatedResponse:
    """
    Update user role
    
    **Permissions Required:**
    - `manage_roles`
    
    **Allowed Roles:**
    - TENANT_OWNER
    """
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot update user from different tenant")
    
    if current_user.role != UserRole.TENANT_OWNER:
        raise HTTPException(status_code=403, detail="Only TENANT_OWNER can change roles")
    
    # Update role
    updated_user = UserService.update_user_role(
        db=db,
        user_id=user_id,
        new_role=request.role,
    )
    
    return UserUpdatedResponse(
        success=True,
        message="User role updated successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.post(
    "/{user_id}/change-password",
    response_model=PasswordChangedResponse,
    summary="Change user password",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def change_password(
    user_id: int = Path(..., gt=0),
    request: ChangePasswordRequest = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Change user password
    
    Users can only change their own password.
    """
    
    # Check authorization
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only change your own password")
    
    try:
        UserService.change_password(
            db=db,
            user_id=user_id,
            current_password=request.current_password,
            new_password=request.new_password,
        )
        
        return PasswordChangedResponse(
            success=True,
            message="Password changed successfully",
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/{user_id}/reset-password",
    response_model=PasswordChangedResponse,
    summary="Reset user password (admin)",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def reset_password(
    user_id: int = Path(..., gt=0),
    request: ResetPasswordRequest = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_tenant_owner),
):
    """
    Reset user password (admin action)
    
    **Permissions Required:**
    - Must be TENANT_OWNER
    """
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot reset password for user from different tenant")
    
    UserService.reset_password(
        db=db,
        user_id=user_id,
        new_password=request.new_password,
    )
    
    return PasswordChangedResponse(
        success=True,
        message="Password reset successfully",
    )


@router.patch(
    "/{user_id}/disable",
    response_model=UserUpdatedResponse,
    summary="Disable user account",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def disable_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.SUSPEND_USER)),
):
    """
    Disable user account
    
    **Permissions Required:**
    - `suspend_user`
    """
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot disable user from different tenant")
    
    updated_user = UserService.disable_user(db=db, user_id=user_id)
    
    return UserUpdatedResponse(
        success=True,
        message="User disabled successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.patch(
    "/{user_id}/enable",
    response_model=UserUpdatedResponse,
    summary="Enable user account",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def enable_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.SUSPEND_USER)),
):
    """
    Enable user account
    
    **Permissions Required:**
    - `suspend_user`
    """
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot enable user from different tenant")
    
    updated_user = UserService.enable_user(db=db, user_id=user_id)
    
    return UserUpdatedResponse(
        success=True,
        message="User enabled successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.patch(
    "/{user_id}/suspend",
    response_model=UserUpdatedResponse,
    summary="Suspend user account",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def suspend_user(
    user_id: int = Path(..., gt=0),
    request: SuspendUserRequest = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.SUSPEND_USER)),
):
    """
    Suspend user account
    
    **Permissions Required:**
    - `suspend_user`
    """
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot suspend user from different tenant")
    
    updated_user = UserService.suspend_user(db=db, user_id=user_id, reason=request.reason)
    
    return UserUpdatedResponse(
        success=True,
        message="User suspended successfully",
        data=UserResponse.from_orm(updated_user),
    )


@router.delete(
    "/{user_id}",
    response_model=UserDeletedResponse,
    summary="Delete user (soft delete)",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def delete_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission(Permission.DELETE_USER)),
):
    """
    Delete user (soft delete - marks as INACTIVE)
    
    **Permissions Required:**
    - `delete_user`
    """
    
    # Get the user
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check authorization
    if user.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=403, detail="Cannot delete user from different tenant")
    
    # Prevent deleting yourself
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    UserService.disable_user(db=db, user_id=user_id)
    
    return UserDeletedResponse(
        success=True,
        message="User deleted successfully",
    )


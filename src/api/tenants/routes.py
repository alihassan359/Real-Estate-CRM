"""
Tenant Management Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from database.session import get_db
from middlewares.auth_middleware import get_current_user
from middlewares.rbac_middleware import check_super_admin, check_platform_admin, check_permission
from models.user import User
from models.tenant import Tenant, TenantStatus
from services.tenant.service import TenantService
from schemas.tenant import (
    TenantCreateRequest,
    TenantUpdateRequest,
    TenantSettingsUpdateRequest,
    UpgradeSubscriptionRequest,
    SuspendTenantRequest,
    TenantResponse,
    TenantDetailResponse,
    TenantUsageResponse,
    TenantListResponse,
    SingleTenantResponse,
    TenantCreatedResponse,
    TenantUpdatedResponse,
    TenantActionResponse,
    ErrorResponse,
)
from config.permissions import Permission

router = APIRouter(prefix="/tenants", tags=["Tenants"])


@router.post(
    "/",
    response_model=TenantCreatedResponse,
    status_code=201,
    summary="Create a new tenant",
    responses={
        403: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
    }
)
async def create_tenant(
    request: TenantCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_platform_admin),
):
    """Create a new tenant (Platform Admin or Super Admin only)"""
    try:
        # Create tenant
        tenant = TenantService.create_tenant(
            db=db,
            company_name=request.company_name,
            company_email=request.company_email,
            phone=request.phone,
            subscription_plan=request.subscription_plan,
            address=request.address,
            city=request.city,
            country=request.country,
        )
        
        return TenantCreatedResponse(
            success=True,
            message="Tenant created successfully",
            data=TenantResponse.from_orm(tenant),
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating tenant: {str(e)}")


@router.get(
    "/",
    response_model=TenantListResponse,
    summary="List all tenants",
    responses={
        403: {"model": ErrorResponse},
    }
)
async def list_tenants(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query(None),
):
    """List all tenants (Super Admin only)"""
    
    # Parse status filter
    status_filter = None
    if status:
        try:
            status_filter = TenantStatus[status.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    
    # Get tenants
    tenants, total = TenantService.get_all_tenants(
        db=db,
        skip=skip,
        limit=limit,
        status=status_filter,
    )
    
    return TenantListResponse(
        success=True,
        data=[TenantResponse.from_orm(t) for t in tenants],
        pagination={
            "skip": skip,
            "limit": limit,
            "total": total,
        }
    )


@router.get(
    "/{tenant_id}",
    response_model=SingleTenantResponse,
    summary="Get tenant details",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def get_tenant(
    tenant_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get tenant details"""
    
    # Get tenant
    tenant = TenantService.get_tenant_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check authorization - only super admin or tenant owner can view
    if current_user.tenant_id != tenant_id and current_user.role.value != "SUPER_ADMIN":
        raise HTTPException(status_code=403, detail="Cannot view this tenant")
    
    # Get settings
    settings = TenantService.get_settings(db, tenant_id)
    
    tenant_detail = TenantDetailResponse.from_orm(tenant)
    tenant_detail.settings = settings
    
    return SingleTenantResponse(
        success=True,
        data=tenant_detail,
    )


@router.patch(
    "/{tenant_id}",
    response_model=TenantUpdatedResponse,
    summary="Update tenant information",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def update_tenant(
    tenant_id: int = Path(..., gt=0),
    request: TenantUpdateRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update tenant information"""
    
    # Get tenant
    tenant = TenantService.get_tenant_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check authorization
    if current_user.tenant_id != tenant_id and current_user.role.value != "SUPER_ADMIN":
        raise HTTPException(status_code=403, detail="Cannot update this tenant")
    
    # Update tenant
    updated_tenant = TenantService.update_tenant(
        db=db,
        tenant_id=tenant_id,
        company_name=request.company_name,
        company_email=request.company_email,
        phone=request.phone,
        address=request.address,
        city=request.city,
        country=request.country,
        logo_url=request.logo_url,
    )
    
    return TenantUpdatedResponse(
        success=True,
        message="Tenant updated successfully",
        data=TenantResponse.from_orm(updated_tenant),
    )


@router.patch(
    "/{tenant_id}/settings",
    response_model=SingleTenantResponse,
    summary="Update tenant settings",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def update_settings(
    tenant_id: int = Path(..., gt=0),
    request: TenantSettingsUpdateRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update tenant settings"""
    
    # Get tenant
    tenant = TenantService.get_tenant_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check authorization
    if current_user.tenant_id != tenant_id and current_user.role.value != "SUPER_ADMIN":
        raise HTTPException(status_code=403, detail="Cannot update this tenant's settings")
    
    # Update settings
    updated_tenant = TenantService.update_settings(
        db=db,
        tenant_id=tenant_id,
        settings=request.settings,
    )
    
    # Get updated settings
    settings = TenantService.get_settings(db, tenant_id)
    tenant_detail = TenantDetailResponse.from_orm(updated_tenant)
    tenant_detail.settings = settings
    
    return SingleTenantResponse(
        success=True,
        data=tenant_detail,
    )


@router.patch(
    "/{tenant_id}/subscription",
    response_model=TenantUpdatedResponse,
    summary="Upgrade subscription",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def upgrade_subscription(
    tenant_id: int = Path(..., gt=0),
    request: UpgradeSubscriptionRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
):
    """Upgrade tenant subscription (Super Admin only)"""
    
    # Get tenant
    tenant = TenantService.get_tenant_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Upgrade subscription
    updated_tenant = TenantService.upgrade_subscription(
        db=db,
        tenant_id=tenant_id,
        new_plan=request.new_plan,
        months=request.months,
    )
    
    return TenantUpdatedResponse(
        success=True,
        message="Subscription upgraded successfully",
        data=TenantResponse.from_orm(updated_tenant),
    )


@router.get(
    "/{tenant_id}/usage",
    response_model=TenantUsageResponse,
    summary="Get tenant usage",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def get_usage(
    tenant_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get tenant usage statistics"""
    
    # Check authorization
    if current_user.tenant_id != tenant_id and current_user.role.value not in ["SUPER_ADMIN", "PLATFORM_ADMIN"]:
        raise HTTPException(status_code=403, detail="Cannot view this tenant's usage")
    
    # Get usage
    usage = TenantService.get_tenant_usage(db, tenant_id)
    
    return TenantUsageResponse(**usage)


@router.patch(
    "/{tenant_id}/suspend",
    response_model=TenantActionResponse,
    summary="Suspend tenant",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def suspend_tenant(
    tenant_id: int = Path(..., gt=0),
    request: SuspendTenantRequest = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
):
    """Suspend tenant (Super Admin only)"""
    
    # Get tenant
    tenant = TenantService.get_tenant_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Suspend tenant
    updated_tenant = TenantService.suspend_tenant(
        db=db,
        tenant_id=tenant_id,
        reason=request.reason,
    )
    
    return TenantActionResponse(
        success=True,
        message="Tenant suspended successfully",
        data=TenantResponse.from_orm(updated_tenant),
    )


@router.patch(
    "/{tenant_id}/reactivate",
    response_model=TenantActionResponse,
    summary="Reactivate tenant",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def reactivate_tenant(
    tenant_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
):
    """Reactivate tenant (Super Admin only)"""
    
    # Get tenant
    tenant = TenantService.get_tenant_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Reactivate tenant
    updated_tenant = TenantService.reactivate_tenant(db=db, tenant_id=tenant_id)
    
    return TenantActionResponse(
        success=True,
        message="Tenant reactivated successfully",
        data=TenantResponse.from_orm(updated_tenant),
    )


@router.patch(
    "/{tenant_id}/deactivate",
    response_model=TenantActionResponse,
    summary="Deactivate tenant",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def deactivate_tenant(
    tenant_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
):
    """Deactivate tenant (Super Admin only)"""
    
    # Get tenant
    tenant = TenantService.get_tenant_by_id(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Deactivate tenant
    updated_tenant = TenantService.deactivate_tenant(db=db, tenant_id=tenant_id)
    
    return TenantActionResponse(
        success=True,
        message="Tenant deactivated successfully",
        data=TenantResponse.from_orm(updated_tenant),
    )

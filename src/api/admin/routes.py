"""
Admin Routes - System administration and monitoring
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.session import get_db
from middlewares.auth_middleware import get_current_user
from middlewares.rbac_middleware import check_super_admin
from models.user import User
from models.tenant import TenantStatus
from services.tenant.service import TenantService
from schemas.tenant import (
    TenantResponse,
    TenantListResponse,
    ErrorResponse,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


# ============================================================================
# TENANT MANAGEMENT ENDPOINTS
# ============================================================================

@router.get(
    "/tenants",
    response_model=TenantListResponse,
    summary="List all tenants (Super Admin)",
    responses={
        403: {"model": ErrorResponse},
    }
)
async def list_all_tenants(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query(None),
):
    """List all tenants in system (Super Admin only)"""
    
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


# ============================================================================
# SYSTEM STATISTICS & MONITORING
# ============================================================================

@router.get("/users")
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
):
    """Get all users (admin only)"""
    # TODO: Implement advanced user statistics
    return {"message": "All users"}


@router.get("/stats")
async def get_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
):
    """Get system statistics"""
    # TODO: Implement comprehensive system statistics
    return {"message": "System stats"}


@router.post("/backup")
async def create_backup(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
):
    """Create database backup"""
    # TODO: Implement database backup functionality
    return {"message": "Backup created"}


@router.get("/logs")
async def get_system_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_super_admin),
    limit: int = 100,
):
    """Get system logs"""
    # TODO: Implement system logging and retrieval
    return {"message": "System logs"}

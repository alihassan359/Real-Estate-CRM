"""
Dashboard Routes
"""

from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview")
async def get_dashboard_overview():
    """Get dashboard overview with KPIs"""
    # TODO: Implement
    return {"message": "Dashboard overview"}


@router.get("/recent-deals")
async def get_recent_deals(limit: int = 10):
    """Get recent deals"""
    # TODO: Implement
    return {"message": "Recent deals"}


@router.get("/pending-payments")
async def get_pending_payments(limit: int = 10):
    """Get pending payments"""
    # TODO: Implement
    return {"message": "Pending payments"}


@router.get("/reports")
async def get_reports():
    """Get various reports"""
    # TODO: Implement
    return {"message": "Reports"}

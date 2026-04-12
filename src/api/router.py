"""Main API Router"""

from fastapi import APIRouter

router = APIRouter()

# Health endpoint
@router.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}

# Status endpoint  
@router.get("/status")
async def status():
    """API status"""
    return {
        "service": "Real Estate CRM API",
        "status": "running",
        "version": "1.0.0"
    }

# Routes placeholder
@router.get("/")
async def root():
    """API root"""
    return {
        "message": "Welcome to Real Estate CRM API",
        "version": "1.0.0"
    }

# Include auth router
from api.auth.routes import router as auth_router
router.include_router(auth_router)

# Include tenants router
from api.tenants.routes import router as tenants_router
router.include_router(tenants_router)

# Include users router
from api.users.routes import router as users_router
router.include_router(users_router)

# Include clients router
from api.clients.routes import router as clients_router
router.include_router(clients_router)

# Include projects router
from api.projects.routes import router as projects_router
router.include_router(projects_router)

# Include deals router
from api.deals.routes import router as deals_router
router.include_router(deals_router)

# Include payments router
from api.payments.routes import router as payments_router
router.include_router(payments_router)

# Include receipts router
from api.receipts.routes import router as receipts_router
router.include_router(receipts_router)

# Include notifications router
from api.notifications.routes import router as notifications_router
router.include_router(notifications_router)

# Include dashboard router
from api.dashboard.routes import router as dashboard_router
router.include_router(dashboard_router)

# Include admin router
from api.admin.routes import router as admin_router
router.include_router(admin_router)

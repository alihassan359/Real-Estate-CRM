"""API Router - Main entry point for all API routes"""

from fastapi import APIRouter

# Create router
router = APIRouter()

# Health endpoint
@router.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}

# V1 routes
@router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Real Estate CRM API v1.0",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "tenants": "/tenants",
            "clients": "/clients",
            "deals": "/deals",
            "payments": "/payments"
        }
    }

# Welcome message
@router.get("/status")
async def status():
    """API status endpoint"""
    return {
        "status": "running",
        "service": "Real Estate CRM API",
        "version": "1.0.0"
    }

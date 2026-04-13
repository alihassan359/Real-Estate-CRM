"""
Server Configuration and Startup
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from api.router import router as api_router
from database.session import ensure_auth_tables

# Configure logging
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events"""
    # Startup
    ensure_auth_tables()
    logger.info("🚀 Starting Real Estate CRM API")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    yield
    # Shutdown
    logger.info("🛑 Shutting down Real Estate CRM API")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Real Estate CRM API - Complete property management system",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(api_router, prefix="/api")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
            "version": settings.VERSION,
        }
    
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(
        "server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )

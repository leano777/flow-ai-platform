"""
Flow AI Platform - API v1 Router

Main API router that includes all endpoint modules.
Provides centralized routing for the Flow AI Platform API.
"""

from fastapi import APIRouter
import structlog

logger = structlog.get_logger(__name__)

# Create main API router
api_router = APIRouter()

# Health check endpoint
@api_router.get("/health", tags=["Health"])
async def api_health():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "api_version": "v1",
        "service": "flow-ai-api"
    }

# Welcome endpoint
@api_router.get("/", tags=["Root"])
async def api_root():
    """API root endpoint with information."""
    return {
        "message": "Welcome to Flow AI Platform API v1",
        "description": "Revolutionary business operating system with AI agents as team members",
        "version": "v1",
        "endpoints": {
            "health": "/api/v1/health",
            "docs": "/api/v1/docs",
            "auth": "/api/v1/auth",
            "agents": "/api/v1/agents",
            "workflows": "/api/v1/workflows",
            "users": "/api/v1/users"
        }
    }

# Import and include routers
from src.api.v1.endpoints import auth

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Additional routers will be added as we create them:
# from src.api.v1.endpoints import users, agents, workflows
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])
# api_router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])

logger.info("✅ API v1 router configured")
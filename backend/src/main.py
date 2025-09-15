"""
Flow AI Platform - Main FastAPI Application

Revolutionary business operating system with AI agents as team members.
This is the core FastAPI application that coordinates the entire platform.
"""

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from src.core.config import settings
from src.core.logging import setup_logging
from src.core.database import engine, Base
from src.core.exceptions import setup_exception_handlers
from src.api.v1.router import api_router
from src.middleware.security import SecurityHeadersMiddleware
from src.middleware.logging import LoggingMiddleware

# Setup structured logging
setup_logging()
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info("🚀 Flow AI Platform starting up...")

    # Create database tables if they don't exist
    if settings.ENVIRONMENT == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("📊 Database tables created")

    logger.info("✅ Flow AI Platform startup complete")

    yield

    # Shutdown
    logger.info("🔄 Flow AI Platform shutting down...")
    await engine.dispose()
    logger.info("✅ Flow AI Platform shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Flow AI Platform API",
    description="""
    Revolutionary business operating system with AI agents as team members.

    This platform transforms how businesses operate by using AI agents to handle:
    - Customer interactions and support
    - Process automation and optimization
    - Data analysis and insights
    - Team coordination and project management

    Built with FastAPI, Next.js, Swift, and n8n workflow automation.
    """,
    version="0.1.0",
    openapi_url="/api/v1/openapi.json" if settings.ENVIRONMENT != "production" else None,
    docs_url="/api/v1/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/api/v1/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
)

# Security middleware
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.CORS_ORIGINS,
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)

# Exception handlers
setup_exception_handlers(app)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "service": "flow-ai-backend",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT
    }


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with platform information."""
    return {
        "message": "Welcome to Flow AI Platform",
        "description": "Revolutionary business operating system with AI agents as team members",
        "version": "0.1.0",
        "docs": "/api/v1/docs" if settings.ENVIRONMENT != "production" else None,
        "health": "/health",
        "api": "/api/v1"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_config=None,  # Use our custom logging
    )
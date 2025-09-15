"""
Flow AI Platform - Exception Handling

Custom exceptions and error handling for the Flow AI Platform.
Provides structured error responses and proper HTTP status codes.
"""

from typing import Any, Dict, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
import structlog

logger = structlog.get_logger(__name__)


# =============================================================================
# Custom Exception Classes
# =============================================================================

class FlowAIException(Exception):
    """Base exception for Flow AI Platform."""

    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(FlowAIException):
    """Authentication related errors."""

    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR",
            details=details,
        )


class AuthorizationError(FlowAIException):
    """Authorization related errors."""

    def __init__(self, message: str = "Insufficient permissions", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHORIZATION_ERROR",
            details=details,
        )


class ValidationError(FlowAIException):
    """Data validation errors."""

    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class NotFoundError(FlowAIException):
    """Resource not found errors."""

    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            details=details,
        )


class ConflictError(FlowAIException):
    """Resource conflict errors."""

    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT_ERROR",
            details=details,
        )


class RateLimitError(FlowAIException):
    """Rate limiting errors."""

    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_ERROR",
            details=details,
        )


class ExternalServiceError(FlowAIException):
    """External service integration errors."""

    def __init__(self, message: str = "External service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details,
        )


class DatabaseError(FlowAIException):
    """Database operation errors."""

    def __init__(self, message: str = "Database error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR",
            details=details,
        )


class AgentError(FlowAIException):
    """AI agent related errors."""

    def __init__(self, message: str = "Agent error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="AGENT_ERROR",
            details=details,
        )


class WorkflowError(FlowAIException):
    """Workflow execution errors."""

    def __init__(self, message: str = "Workflow error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="WORKFLOW_ERROR",
            details=details,
        )


# =============================================================================
# Exception Handlers
# =============================================================================

async def flow_ai_exception_handler(request: Request, exc: FlowAIException) -> JSONResponse:
    """Handle Flow AI custom exceptions."""
    logger.error(
        "Flow AI exception occurred",
        error_code=exc.error_code,
        message=exc.message,
        status_code=exc.status_code,
        details=exc.details,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
            "timestamp": None,  # Will be added by middleware
            "path": request.url.path,
            "method": request.method,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions."""
    logger.warning(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        method=request.method,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "details": {},
            },
            "timestamp": None,  # Will be added by middleware
            "path": request.url.path,
            "method": request.method,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    logger.warning(
        "Validation error occurred",
        errors=exc.errors(),
        path=request.url.path,
        method=request.method,
    )

    # Format validation errors for better readability
    formatted_errors = []
    for error in exc.errors():
        formatted_errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": {
                    "errors": formatted_errors,
                },
            },
            "timestamp": None,  # Will be added by middleware
            "path": request.url.path,
            "method": request.method,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(
        "Unexpected exception occurred",
        exception=str(exc),
        exception_type=type(exc).__name__,
        path=request.url.path,
        method=request.method,
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {},
            },
            "timestamp": None,  # Will be added by middleware
            "path": request.url.path,
            "method": request.method,
        },
    )


# =============================================================================
# Exception Handler Setup
# =============================================================================

def setup_exception_handlers(app: FastAPI) -> None:
    """Set up exception handlers for the FastAPI application."""

    # Custom Flow AI exceptions
    app.add_exception_handler(FlowAIException, flow_ai_exception_handler)

    # FastAPI HTTP exceptions
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)

    # Validation errors
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    # Catch-all for unexpected exceptions
    app.add_exception_handler(Exception, generic_exception_handler)

    logger.info("✅ Exception handlers configured")


# =============================================================================
# Utility Functions
# =============================================================================

def raise_not_found(resource: str, identifier: Any = None) -> None:
    """Raise a standardized not found error."""
    message = f"{resource} not found"
    if identifier:
        message += f" (ID: {identifier})"

    raise NotFoundError(
        message=message,
        details={"resource": resource, "identifier": str(identifier) if identifier else None}
    )


def raise_validation_error(field: str, message: str, value: Any = None) -> None:
    """Raise a standardized validation error."""
    raise ValidationError(
        message=f"Validation failed for field '{field}': {message}",
        details={"field": field, "message": message, "value": str(value) if value else None}
    )


def raise_conflict_error(resource: str, field: str, value: Any) -> None:
    """Raise a standardized conflict error."""
    raise ConflictError(
        message=f"{resource} with {field} '{value}' already exists",
        details={"resource": resource, "field": field, "value": str(value)}
    )
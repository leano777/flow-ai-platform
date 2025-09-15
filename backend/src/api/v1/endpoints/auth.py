"""
Flow AI Platform - Authentication Endpoints

REST API endpoints for user authentication, registration, and account management.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from src.core.database import get_db
from src.core.exceptions import AuthenticationError
from src.services.auth import AuthService
from src.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    RefreshTokenRequest,
    EmailVerificationRequest,
    AuthResponse,
    TokenResponse,
    UserResponse,
    MessageResponse,
)

logger = structlog.get_logger(__name__)
router = APIRouter()
security = HTTPBearer()


# Dependency to get client IP and user agent
def get_client_info(request: Request) -> tuple[Optional[str], Optional[str]]:
    """Extract client IP address and user agent from request."""
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    return ip_address, user_agent


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with optional organization",
)
async def register_user(
    user_data: UserRegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user account."""
    logger.info("User registration attempt", email=user_data.email)

    # Register user
    user = await AuthService.register_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        organization_name=user_data.organization_name,
    )

    # Get client info for session tracking
    ip_address, user_agent = get_client_info(request)

    # Authenticate user immediately after registration
    user, access_token, refresh_token = await AuthService.authenticate_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    # Prepare response
    tokens = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

    user_response = UserResponse.from_orm(user)

    return AuthResponse(user=user_response, tokens=tokens)


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="User login",
    description="Authenticate user with email and password",
)
async def login_user(
    login_data: UserLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Authenticate user and return access tokens."""
    logger.info("User login attempt", email=login_data.email)

    # Get client info for session tracking
    ip_address, user_agent = get_client_info(request)

    # Authenticate user
    user, access_token, refresh_token = await AuthService.authenticate_user(
        db=db,
        email=login_data.email,
        password=login_data.password,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    # Prepare response
    tokens = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

    user_response = UserResponse.from_orm(user)

    return AuthResponse(user=user_response, tokens=tokens)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Get new access token using refresh token",
)
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token using refresh token."""
    logger.info("Token refresh attempt")

    # Refresh tokens
    access_token, refresh_token = await AuthService.refresh_access_token(
        db=db,
        refresh_token=token_data.refresh_token,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="User logout",
    description="Logout user and revoke session",
)
async def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """Logout user and revoke session."""
    try:
        # Verify token to get user ID
        payload = AuthService.verify_token(credentials.credentials)
        user_id = int(payload.get("sub"))

        # Logout user (revoke all sessions)
        await AuthService.logout_user(db=db, user_id=user_id)

        logger.info("User logged out successfully", user_id=user_id)
        return MessageResponse(message="Successfully logged out")

    except Exception as e:
        logger.error("Logout failed", error=str(e))
        raise AuthenticationError("Failed to logout")


@router.post(
    "/verify-email",
    response_model=MessageResponse,
    summary="Verify email address",
    description="Verify user email address using verification token",
)
async def verify_email(
    verification_data: EmailVerificationRequest,
    db: AsyncSession = Depends(get_db),
):
    """Verify user email address."""
    logger.info("Email verification attempt", token=verification_data.token[:8] + "...")

    # Verify email
    user = await AuthService.verify_email(
        db=db,
        token=verification_data.token,
    )

    logger.info("Email verified successfully", user_id=user.id)
    return MessageResponse(message="Email verified successfully")


@router.post(
    "/password-reset-request",
    response_model=MessageResponse,
    summary="Request password reset",
    description="Send password reset email to user",
)
async def request_password_reset(
    reset_data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
):
    """Request password reset for user."""
    logger.info("Password reset request", email=reset_data.email)

    # Request password reset
    await AuthService.request_password_reset(
        db=db,
        email=reset_data.email,
    )

    # Always return success message for security
    return MessageResponse(
        message="If this email is registered, you will receive reset instructions"
    )


@router.post(
    "/password-reset-confirm",
    response_model=MessageResponse,
    summary="Confirm password reset",
    description="Reset password using reset token",
)
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db),
):
    """Reset password using reset token."""
    logger.info("Password reset confirmation", token=reset_data.token[:8] + "...")

    # Reset password
    user = await AuthService.reset_password(
        db=db,
        token=reset_data.token,
        new_password=reset_data.new_password,
    )

    logger.info("Password reset successfully", user_id=user.id)
    return MessageResponse(message="Password reset successfully")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get current authenticated user information",
)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """Get current authenticated user."""
    try:
        # Verify token
        payload = AuthService.verify_token(credentials.credentials)
        user_id = int(payload.get("sub"))

        # Get user from database
        from sqlalchemy import select
        from src.models.user import User

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user or not user.is_active_user:
            raise AuthenticationError("User not found or inactive")

        return UserResponse.from_orm(user)

    except Exception as e:
        logger.error("Failed to get current user", error=str(e))
        raise AuthenticationError("Invalid authentication credentials")


# Health check for auth service
@router.get(
    "/health",
    response_model=MessageResponse,
    summary="Authentication service health",
    description="Check authentication service health",
)
async def auth_health():
    """Check authentication service health."""
    return MessageResponse(message="Authentication service is healthy")
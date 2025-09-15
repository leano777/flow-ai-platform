"""
Flow AI Platform - Authentication Service

JWT-based authentication with secure password hashing and session management.
Supports user registration, login, password reset, and multi-factor authentication.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets
import structlog

from src.core.config import settings
from src.core.exceptions import AuthenticationError, ValidationError, NotFoundError
from src.models.user import User, UserSession, UserStatus
from src.models.organization import Organization

logger = structlog.get_logger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service for user management and JWT tokens."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        """Create a refresh token for long-term authentication."""
        data = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        }
        return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError as e:
            logger.warning("Token verification failed", error=str(e))
            raise AuthenticationError("Invalid token")

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> tuple[User, str, str]:
        """
        Authenticate user and return user object with tokens.

        Returns:
            tuple: (user, access_token, refresh_token)
        """
        # Get user by email
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            logger.warning("Authentication failed: user not found", email=email)
            raise AuthenticationError("Invalid email or password")

        # Check if user is locked
        if user.is_locked:
            logger.warning("Authentication failed: account locked", user_id=user.id)
            raise AuthenticationError("Account is temporarily locked due to failed login attempts")

        # Verify password
        if not AuthService.verify_password(password, user.password_hash):
            # Increment failed login attempts
            user.increment_failed_login()
            await db.commit()
            logger.warning("Authentication failed: invalid password", user_id=user.id)
            raise AuthenticationError("Invalid email or password")

        # Check user status
        if user.status != UserStatus.ACTIVE:
            logger.warning("Authentication failed: inactive user", user_id=user.id, status=user.status)
            raise AuthenticationError("Account is not active")

        if not user.is_verified:
            logger.warning("Authentication failed: unverified email", user_id=user.id)
            raise AuthenticationError("Email address not verified")

        # Update login tracking
        user.update_login_tracking()

        # Create tokens
        access_token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "org_id": user.organization_id,
        }
        access_token = AuthService.create_access_token(access_token_data)
        refresh_token = AuthService.create_refresh_token(user.id)

        # Create session record
        session = UserSession(
            user_id=user.id,
            session_token=secrets.token_urlsafe(32),
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(session)

        await db.commit()
        await db.refresh(user)

        logger.info("User authenticated successfully", user_id=user.id, email=user.email)
        return user, access_token, refresh_token

    @staticmethod
    async def register_user(
        db: AsyncSession,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        organization_name: Optional[str] = None
    ) -> User:
        """Register a new user account."""

        # Check if user already exists
        result = await db.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.warning("Registration failed: email already exists", email=email)
            raise ValidationError("Email address already registered")

        # Validate password strength
        AuthService.validate_password_strength(password)

        # Hash password
        password_hash = AuthService.hash_password(password)

        # Create organization if provided
        organization = None
        if organization_name:
            # Check if organization already exists
            org_result = await db.execute(
                select(Organization).where(Organization.name == organization_name)
            )
            organization = org_result.scalar_one_or_none()

            if not organization:
                # Create new organization
                organization = Organization(
                    name=organization_name,
                    slug=AuthService.generate_org_slug(organization_name)
                )
                db.add(organization)
                await db.flush()  # Get the ID

        # Create user
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            full_name=f"{first_name} {last_name}".strip(),
            organization_id=organization.id if organization else None,
            verification_token=secrets.token_urlsafe(32),
        )

        # Set role based on organization
        if organization and not organization.user_count:
            # First user in organization becomes admin
            user.role = "admin"
            organization.increment_usage("user")
        else:
            user.role = "user"
            if organization:
                organization.increment_usage("user")

        db.add(user)
        await db.commit()
        await db.refresh(user)

        logger.info("User registered successfully", user_id=user.id, email=user.email)
        return user

    @staticmethod
    async def verify_email(db: AsyncSession, token: str) -> User:
        """Verify user email address using verification token."""
        result = await db.execute(
            select(User).where(User.verification_token == token)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundError("Invalid verification token")

        user.email_verified = True
        user.email_verified_at = datetime.utcnow()
        user.verification_token = None
        user.status = UserStatus.ACTIVE

        await db.commit()
        logger.info("Email verified successfully", user_id=user.id)
        return user

    @staticmethod
    async def request_password_reset(db: AsyncSession, email: str) -> User:
        """Request password reset for user."""
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            # Don't reveal if email exists
            logger.warning("Password reset requested for non-existent email", email=email)
            raise NotFoundError("If this email is registered, you will receive reset instructions")

        # Generate reset token
        user.password_reset_token = secrets.token_urlsafe(32)
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)

        await db.commit()
        logger.info("Password reset requested", user_id=user.id)
        return user

    @staticmethod
    async def reset_password(db: AsyncSession, token: str, new_password: str) -> User:
        """Reset user password using reset token."""
        result = await db.execute(
            select(User).where(User.password_reset_token == token)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundError("Invalid reset token")

        if user.password_reset_expires < datetime.utcnow():
            raise ValidationError("Reset token has expired")

        # Validate new password
        AuthService.validate_password_strength(new_password)

        # Update password
        user.password_hash = AuthService.hash_password(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        user.password_changed_at = datetime.utcnow()

        # Revoke all existing sessions
        await db.execute(
            select(UserSession)
            .where(UserSession.user_id == user.id)
            .update({"is_active": False, "revoked_reason": "password_reset"})
        )

        await db.commit()
        logger.info("Password reset successfully", user_id=user.id)
        return user

    @staticmethod
    async def refresh_access_token(db: AsyncSession, refresh_token: str) -> tuple[str, str]:
        """Refresh access token using refresh token."""
        try:
            payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user_id = int(payload.get("sub"))
            token_type = payload.get("type")

            if token_type != "refresh":
                raise AuthenticationError("Invalid token type")

        except JWTError:
            raise AuthenticationError("Invalid refresh token")

        # Get user
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user or not user.is_active_user:
            raise AuthenticationError("User not found or inactive")

        # Create new tokens
        access_token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "org_id": user.organization_id,
        }
        new_access_token = AuthService.create_access_token(access_token_data)
        new_refresh_token = AuthService.create_refresh_token(user.id)

        logger.info("Token refreshed successfully", user_id=user.id)
        return new_access_token, new_refresh_token

    @staticmethod
    async def logout_user(db: AsyncSession, user_id: int, session_token: Optional[str] = None) -> None:
        """Logout user and revoke session(s)."""
        if session_token:
            # Revoke specific session
            await db.execute(
                select(UserSession)
                .where(UserSession.user_id == user_id, UserSession.session_token == session_token)
                .update({"is_active": False, "revoked_reason": "user_logout"})
            )
        else:
            # Revoke all user sessions
            await db.execute(
                select(UserSession)
                .where(UserSession.user_id == user_id)
                .update({"is_active": False, "revoked_reason": "user_logout"})
            )

        await db.commit()
        logger.info("User logged out", user_id=user_id)

    @staticmethod
    def validate_password_strength(password: str) -> None:
        """Validate password meets security requirements."""
        if len(password) < settings.PASSWORD_MIN_LENGTH:
            raise ValidationError(f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long")

        if settings.PASSWORD_REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            raise ValidationError("Password must contain at least one uppercase letter")

        if settings.PASSWORD_REQUIRE_LOWERCASE and not any(c.islower() for c in password):
            raise ValidationError("Password must contain at least one lowercase letter")

        if settings.PASSWORD_REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain at least one number")

        if settings.PASSWORD_REQUIRE_SPECIAL and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            raise ValidationError("Password must contain at least one special character")

    @staticmethod
    def generate_org_slug(name: str) -> str:
        """Generate organization slug from name."""
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
        slug = re.sub(r'\s+', '-', slug)
        slug = slug.strip('-')

        # Add random suffix to ensure uniqueness
        suffix = secrets.token_hex(4)
        return f"{slug}-{suffix}"
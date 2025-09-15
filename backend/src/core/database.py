"""
Flow AI Platform - Database Configuration

Async SQLAlchemy setup with PostgreSQL and connection pooling.
Provides base models, session management, and migration support.
"""

from typing import AsyncGenerator, Any, Optional
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    String,
    Text,
    JSON,
    Index,
    event,
)
from sqlalchemy.sql import func
from sqlalchemy.pool import NullPool
import structlog

from src.core.config import settings

logger = structlog.get_logger(__name__)

# Database engine configuration
engine_kwargs = {
    "url": settings.database_url_async,
    "echo": settings.DB_ECHO,
    "pool_size": settings.DB_POOL_SIZE,
    "max_overflow": settings.DB_MAX_OVERFLOW,
    "pool_pre_ping": True,
    "pool_recycle": 3600,  # Recycle connections after 1 hour
}

# Use NullPool for testing environments
if settings.ENVIRONMENT == "test":
    engine_kwargs["poolclass"] = NullPool

# Create async engine
engine: AsyncEngine = create_async_engine(**engine_kwargs)

# Create sessionmaker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """Base class for all database models."""

    # Common columns for all models
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at: DateTime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    updated_at: DateTime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )
    is_active: bool = Column(Boolean, default=True, nullable=False, index=True)

    # Metadata for tracking changes
    created_by_id: Optional[int] = Column(Integer, nullable=True, index=True)
    updated_by_id: Optional[int] = Column(Integer, nullable=True, index=True)

    # Soft delete support
    deleted_at: Optional[DateTime] = Column(DateTime(timezone=True), nullable=True, index=True)
    deleted_by_id: Optional[int] = Column(Integer, nullable=True)

    # Metadata storage
    metadata_: dict[str, Any] = Column("metadata", JSON, default=dict, nullable=False)

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"

    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted."""
        return self.deleted_at is not None

    def soft_delete(self, deleted_by_id: Optional[int] = None) -> None:
        """Soft delete the record."""
        self.deleted_at = func.now()
        self.deleted_by_id = deleted_by_id
        self.is_active = False

    def restore(self) -> None:
        """Restore a soft deleted record."""
        self.deleted_at = None
        self.deleted_by_id = None
        self.is_active = True


# Mixin classes for common functionality
class TimestampMixin:
    """Mixin for timestamp columns."""

    created_at: DateTime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    updated_at: DateTime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    )


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""

    deleted_at: Optional[DateTime] = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )
    deleted_by_id: Optional[int] = Column(Integer, nullable=True)

    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted."""
        return self.deleted_at is not None

    def soft_delete(self, deleted_by_id: Optional[int] = None) -> None:
        """Soft delete the record."""
        self.deleted_at = func.now()
        self.deleted_by_id = deleted_by_id

    def restore(self) -> None:
        """Restore a soft deleted record."""
        self.deleted_at = None
        self.deleted_by_id = None


class MetadataMixin:
    """Mixin for metadata storage."""

    metadata_: dict[str, Any] = Column(
        "metadata",
        JSON,
        default=dict,
        nullable=False,
    )

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value."""
        if self.metadata_ is None:
            self.metadata_ = {}
        self.metadata_[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value."""
        if self.metadata_ is None:
            return default
        return self.metadata_.get(key, default)

    def remove_metadata(self, key: str) -> None:
        """Remove metadata key."""
        if self.metadata_ and key in self.metadata_:
            del self.metadata_[key]


# Event listeners for automatic timestamp updates
@event.listens_for(Base, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):
    """Update timestamp before update."""
    target.updated_at = func.now()


# Database session dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.

    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Database utilities
async def create_database_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("📊 Database tables created successfully")


async def drop_database_tables() -> None:
    """Drop all database tables (use with caution!)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.warning("🗑️  Database tables dropped")


async def check_database_connection() -> bool:
    """
    Check if database connection is working.

    Returns:
        bool: True if connection is successful
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error("❌ Database connection failed", error=str(e))
        return False


# Transaction context manager
class DatabaseTransaction:
    """Context manager for database transactions."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> AsyncSession:
        """Enter transaction context."""
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit transaction context."""
        if exc_type is not None:
            await self.session.rollback()
            logger.error("🔄 Transaction rolled back", error=str(exc_val))
        else:
            await self.session.commit()
            logger.debug("✅ Transaction committed")


# Query utilities
class QueryFilters:
    """Common query filters for models."""

    @staticmethod
    def active_only(query):
        """Filter for active records only."""
        return query.filter(Base.is_active == True)

    @staticmethod
    def not_deleted(query):
        """Filter for non-deleted records."""
        return query.filter(Base.deleted_at.is_(None))

    @staticmethod
    def created_after(query, date):
        """Filter for records created after date."""
        return query.filter(Base.created_at >= date)

    @staticmethod
    def created_before(query, date):
        """Filter for records created before date."""
        return query.filter(Base.created_at <= date)

    @staticmethod
    def updated_after(query, date):
        """Filter for records updated after date."""
        return query.filter(Base.updated_at >= date)

    @staticmethod
    def by_user(query, user_id):
        """Filter for records created by user."""
        return query.filter(Base.created_by_id == user_id)
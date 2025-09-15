"""
Flow AI Platform - Configuration Management

Centralized configuration using Pydantic Settings for type safety and validation.
Supports environment variables, .env files, and secure secret management.
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseSettings, validator, Field
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # ==========================================================================
    # Basic Application Settings
    # ==========================================================================
    APP_NAME: str = "Flow AI Platform"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # ==========================================================================
    # Security Settings
    # ==========================================================================
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    BCRYPT_ROUNDS: int = Field(default=12, env="BCRYPT_ROUNDS")

    # Password validation
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True

    # ==========================================================================
    # Database Configuration
    # ==========================================================================
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_POOL_SIZE: int = Field(default=20, env="DB_POOL_SIZE")
    DB_MAX_OVERFLOW: int = Field(default=30, env="DB_MAX_OVERFLOW")
    DB_ECHO: bool = Field(default=False, env="DB_ECHO")

    # Redis Configuration
    REDIS_URL: str = Field(..., env="REDIS_URL")
    REDIS_MAX_CONNECTIONS: int = Field(default=100, env="REDIS_MAX_CONNECTIONS")

    # Qdrant Vector Database
    QDRANT_URL: str = Field(..., env="QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = Field(default=None, env="QDRANT_API_KEY")

    # ==========================================================================
    # API Keys for AI Services
    # ==========================================================================
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = Field(..., env="ANTHROPIC_API_KEY")
    GOOGLE_AI_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_AI_API_KEY")

    # ==========================================================================
    # n8n Workflow Engine
    # ==========================================================================
    N8N_WEBHOOK_URL: str = Field(..., env="N8N_WEBHOOK_URL")
    N8N_API_KEY: Optional[str] = Field(default=None, env="N8N_API_KEY")
    N8N_BASIC_AUTH_USER: str = Field(default="admin", env="N8N_BASIC_AUTH_USER")
    N8N_BASIC_AUTH_PASSWORD: str = Field(..., env="N8N_BASIC_AUTH_PASSWORD")

    # ==========================================================================
    # CORS and Security
    # ==========================================================================
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        env="CORS_ORIGINS"
    )
    SECURE_HEADERS: bool = Field(default=True, env="SECURE_HEADERS")
    DISABLE_CORS: bool = Field(default=False, env="DISABLE_CORS")

    # ==========================================================================
    # File Storage
    # ==========================================================================
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=25 * 1024 * 1024, env="MAX_FILE_SIZE")  # 25MB
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=["image/jpeg", "image/png", "image/gif", "application/pdf", "text/plain"],
        env="ALLOWED_FILE_TYPES"
    )

    # AWS S3 Configuration (optional)
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")

    # ==========================================================================
    # Email Configuration
    # ==========================================================================
    SMTP_HOST: Optional[str] = Field(default=None, env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_FROM_EMAIL: str = Field(default="noreply@flowai.com", env="SMTP_FROM_EMAIL")

    # ==========================================================================
    # Monitoring and Logging
    # ==========================================================================
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")

    # ==========================================================================
    # Rate Limiting
    # ==========================================================================
    RATE_LIMIT_PER_MINUTE: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_BURST: int = Field(default=200, env="RATE_LIMIT_BURST")

    # ==========================================================================
    # Feature Flags
    # ==========================================================================
    ENABLE_AGENT_BUILDER: bool = Field(default=True, env="ENABLE_AGENT_BUILDER")
    ENABLE_WORKFLOW_BUILDER: bool = Field(default=True, env="ENABLE_WORKFLOW_BUILDER")
    ENABLE_SOCIAL_LOGIN: bool = Field(default=True, env="ENABLE_SOCIAL_LOGIN")
    ENABLE_MOBILE_APP: bool = Field(default=True, env="ENABLE_MOBILE_APP")
    ENABLE_ANALYTICS: bool = Field(default=True, env="ENABLE_ANALYTICS")

    # ==========================================================================
    # Backup and Recovery
    # ==========================================================================
    BACKUP_ENABLED: bool = Field(default=True, env="BACKUP_ENABLED")
    BACKUP_INTERVAL_HOURS: int = Field(default=6, env="BACKUP_INTERVAL_HOURS")
    BACKUP_RETENTION_DAYS: int = Field(default=30, env="BACKUP_RETENTION_DAYS")
    BACKUP_S3_BUCKET: Optional[str] = Field(default=None, env="BACKUP_S3_BUCKET")

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("ALLOWED_FILE_TYPES", pre=True)
    def assemble_file_types(cls, v: Any) -> List[str]:
        """Parse allowed file types from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("LOG_LEVEL")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()

    @validator("ENVIRONMENT")
    def validate_environment(cls, v: str) -> str:
        """Validate environment."""
        valid_envs = ["development", "staging", "production"]
        if v.lower() not in valid_envs:
            raise ValueError(f"ENVIRONMENT must be one of {valid_envs}")
        return v.lower()

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production"

    @property
    def database_url_async(self) -> str:
        """Get async database URL for SQLAlchemy."""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

    @property
    def redis_settings(self) -> Dict[str, Any]:
        """Get Redis connection settings."""
        from urllib.parse import urlparse
        parsed = urlparse(self.REDIS_URL)
        return {
            "host": parsed.hostname,
            "port": parsed.port or 6379,
            "password": parsed.password,
            "db": int(parsed.path.lstrip("/")) if parsed.path else 0,
            "max_connections": self.REDIS_MAX_CONNECTIONS,
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Global settings instance
settings = get_settings()
#!/usr/bin/env python3
"""
Flow AI Platform - Development Server

Run the FastAPI development server without Docker for testing.
Use this for quick development when Docker is not available.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment variables for development
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./flow_ai_dev.db")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
os.environ.setdefault("JWT_SECRET", "dev-secret-key-change-in-production")

print("🚀 Starting Flow AI Platform Development Server")
print("📋 Environment: Development")
print("💾 Database: SQLite (for development without Docker)")
print("🔐 JWT Secret: Development key")
print()

if __name__ == "__main__":
    try:
        import uvicorn
        from src.main import app

        print("✅ FastAPI application loaded successfully")
        print("📖 API Documentation: http://localhost:8000/api/v1/docs")
        print("🏥 Health Check: http://localhost:8000/health")
        print()

        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Run: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)
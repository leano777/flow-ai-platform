"""
Flow AI Platform - Logging Configuration

Structured logging setup with JSON output for production environments.
Integrates with monitoring systems and provides context-aware logging.
"""

import logging
import sys
from typing import Any, Dict
import structlog
from structlog.types import Processor

from src.core.config import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""

    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL),
    )

    # Shared processors for all environments
    shared_processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.is_development:
        # Development: Pretty console output
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    else:
        # Production: JSON output for log aggregation
        processors = shared_processors + [
            structlog.processors.JSONRenderer()
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    """Get a configured logger instance."""
    return structlog.get_logger(name)


# Custom log processors
class RequestContextProcessor:
    """Add request context to log entries."""

    def __call__(self, logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Add request context if available."""
        # This would be populated by middleware
        request_id = getattr(structlog.contextvars, 'request_id', None)
        user_id = getattr(structlog.contextvars, 'user_id', None)

        if request_id:
            event_dict['request_id'] = request_id
        if user_id:
            event_dict['user_id'] = user_id

        return event_dict


class AgentContextProcessor:
    """Add AI agent context to log entries."""

    def __call__(self, logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Add agent context if available."""
        agent_id = getattr(structlog.contextvars, 'agent_id', None)
        agent_type = getattr(structlog.contextvars, 'agent_type', None)
        workflow_id = getattr(structlog.contextvars, 'workflow_id', None)

        if agent_id:
            event_dict['agent_id'] = agent_id
        if agent_type:
            event_dict['agent_type'] = agent_type
        if workflow_id:
            event_dict['workflow_id'] = workflow_id

        return event_dict


# Context managers for structured logging
class LogContext:
    """Context manager for adding structured log context."""

    def __init__(self, **context):
        self.context = context
        self.tokens = []

    def __enter__(self):
        for key, value in self.context.items():
            token = structlog.contextvars.bind_contextvars(**{key: value})
            self.tokens.append(token)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for token in reversed(self.tokens):
            token.__exit__(exc_type, exc_val, exc_tb)


# Convenience functions
def log_with_request_context(request_id: str, user_id: str = None):
    """Add request context to logs."""
    context = {'request_id': request_id}
    if user_id:
        context['user_id'] = user_id
    return LogContext(**context)


def log_with_agent_context(agent_id: str, agent_type: str = None, workflow_id: str = None):
    """Add agent context to logs."""
    context = {'agent_id': agent_id}
    if agent_type:
        context['agent_type'] = agent_type
    if workflow_id:
        context['workflow_id'] = workflow_id
    return LogContext(**context)
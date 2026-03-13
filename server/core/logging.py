"""Structured JSON logging utilities and request context propagation."""

import json
import logging
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

request_id_ctx_var: ContextVar[str | None] = ContextVar("request_id", default=None)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """Serialize log records into a JSON object with contextual fields.

        Args:
            record: Python log record emitted by the logging framework.

        Returns:
            JSON string representation of the structured log payload.
        """
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if request_id_ctx_var.get():
            payload["request_id"] = request_id_ctx_var.get()

        for key in (
            "method",
            "path",
            "status_code",
            "duration_ms",
            "job_id",
            "page_number",
            "document_name",
            "size_bytes",
            "total_pages",
            "error",
        ):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload)


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logging handlers to emit structured JSON logs.

    Args:
        level: Minimum logging severity level for the root logger.

    Returns:
        None.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a logger instance scoped to the provided module or component name.

    Args:
        name: Logger name, typically the module `__name__`.

    Returns:
        Configured logger instance for emitting application logs.
    """
    return logging.getLogger(name)

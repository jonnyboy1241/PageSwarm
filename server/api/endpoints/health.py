"""Health-check endpoint for service liveness and timestamp reporting."""

from datetime import UTC, datetime

from fastapi import APIRouter

from schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Return basic API health metadata used by probes and monitoring.

    Args:
        None.

    Returns:
        HealthResponse containing status, service identity, and current UTC timestamp.
    """
    return HealthResponse(
        status="ok",
        service="pageswarm-api",
        timestamp=datetime.now(UTC),
    )

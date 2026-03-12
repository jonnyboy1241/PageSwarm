"""Application entrypoint and FastAPI app wiring for PageSwarm."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.endpoints.health import router as health_router
from app.api.v1.api import api_router
from app.core.logging import get_logger, setup_logging
from app.core.middleware import RequestContextMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Run startup and shutdown hooks for the FastAPI application.

    Args:
        _: FastAPI app instance provided by FastAPI lifespan management.

    Returns:
        An async context manager lifecycle flow that yields control to app runtime.
    """
    setup_logging()
    logger.info("application_starting")
    yield
    logger.info("application_stopping")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance.

    Args:
        None.

    Returns:
        A configured FastAPI app with middleware, routers, and exception handling.
    """
    app = FastAPI(
        title="PageSwarm API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(RequestContextMiddleware)
    app.include_router(health_router, prefix="/api", tags=["health"])
    app.include_router(api_router, prefix="/api/v1")

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_, exc: Exception) -> JSONResponse:
        """Log unexpected errors and return a generic 500 response.

        Args:
            _: Request object supplied by FastAPI's exception handler interface.
            exc: Unhandled exception raised while processing a request.

        Returns:
            JSONResponse with a generic internal server error payload.
        """
        logger.exception("unhandled_exception", extra={"error": str(exc)})
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    return app


app = create_app()

"""
Trademark Search Pro - FastAPI Application
Entry point for the application. Configures logging, middleware, and routes.
"""

import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routes import health, version, data

# --- Logging Setup ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# --- App Initialization ---
app = FastAPI(
    title="Trademark Search Pro",
    description="CI/CD Demo API",
    version=os.getenv("APP_VERSION", "0.1.0"),
)

# --- Register Routers ---
app.include_router(health.router)
app.include_router(version.router)
app.include_router(data.router)


# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all handler so unhandled errors return JSON, not HTML tracebacks."""
    logger.error("Unhandled error on %s %s: %s", request.method, request.url, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.on_event("startup")
async def startup_event():
    env = os.getenv("ENVIRONMENT", "development")
    logger.info("Application starting in [%s] mode", env)

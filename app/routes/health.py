"""
Health check endpoint.
Returns a simple status to confirm the service is running.
Used by Docker HEALTHCHECK, load balancers, and monitoring tools.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy"}

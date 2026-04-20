"""
Version endpoint.
Returns the current app version and environment.
Useful for verifying which build is deployed.
"""

import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/version")
async def get_version():
    return {
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
    }

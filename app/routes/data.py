"""
Sample business-logic endpoint.
Demonstrates a typical CRUD-style API route backed by a service layer.
"""

import logging

from fastapi import APIRouter, HTTPException, Query

from app.services.data_service import search_trademarks

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.get("/data")
async def get_data(q: str = Query(default=None, max_length=100)):
    """
    Search sample trademark data.
    - Without query param: returns all records.
    - With ?q=<term>: filters results by name.
    """
    try:
        results = search_trademarks(q)
        return {
            "count": len(results),
            "query": q,
            "results": results,
        }
    except Exception as e:
        logger.error("Error fetching data: %s", e)
        raise HTTPException(status_code=500, detail="Failed to fetch data")

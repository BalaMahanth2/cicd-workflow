"""
Data service layer.
Contains business logic separated from the HTTP layer.
Uses an in-memory dataset (no database needed for this demo).
"""

from typing import Optional

# --- Sample in-memory dataset ---
TRADEMARKS = [
    {"id": 1, "name": "AcmeTech", "class": 9, "status": "registered"},
    {"id": 2, "name": "BrightWave", "class": 35, "status": "pending"},
    {"id": 3, "name": "CloudNine Solutions", "class": 42, "status": "registered"},
    {"id": 4, "name": "DataPulse", "class": 9, "status": "opposed"},
    {"id": 5, "name": "EcoVerde", "class": 30, "status": "registered"},
]


def search_trademarks(query: Optional[str] = None) -> list[dict]:
    """Return all trademarks, or filter by name (case-insensitive)."""
    if not query:
        return TRADEMARKS
    term = query.lower()
    return [t for t in TRADEMARKS if term in t["name"].lower()]

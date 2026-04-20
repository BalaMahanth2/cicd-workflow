"""Tests for the /api/data endpoint."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_data_returns_200():
    response = client.get("/api/data")
    assert response.status_code == 200


def test_data_returns_all_records_without_query():
    response = client.get("/api/data")
    data = response.json()
    assert data["count"] == 5
    assert data["query"] is None


def test_data_filters_by_query():
    response = client.get("/api/data?q=acme")
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["name"] == "AcmeTech"


def test_data_returns_empty_for_no_match():
    response = client.get("/api/data?q=nonexistent")
    data = response.json()
    assert data["count"] == 0
    assert data["results"] == []

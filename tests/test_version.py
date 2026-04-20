"""Tests for the /version endpoint."""

import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_version_returns_200():
    response = client.get("/version")
    assert response.status_code == 200


def test_version_contains_required_fields():
    response = client.get("/version")
    data = response.json()
    assert "version" in data
    assert "environment" in data


def test_version_respects_env_vars(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "2.0.0")
    monkeypatch.setenv("ENVIRONMENT", "testing")
    response = client.get("/version")
    data = response.json()
    assert data["version"] == "2.0.0"
    assert data["environment"] == "testing"

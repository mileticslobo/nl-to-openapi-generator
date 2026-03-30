"""Tests for app.main FastAPI routes."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ui_serves_html(client):
    """Test that the root endpoint serves HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


@patch("app.main.generate_openapi_spec")
def test_generate_endpoint_success(mock_generate, client):
    """Test successful spec generation via API."""
    mock_generate.return_value = {
        "yaml": "openapi: '3.0.3'\ninfo:\n  title: Test\n  version: '1.0.0'\npaths: {}",
        "parsed": {
            "openapi": "3.0.3",
            "info": {"title": "Test", "version": "1.0.0"},
            "paths": {}
        }
    }

    response = client.post(
        "/generate",
        json={"description": "A simple test API", "model": "gpt-4o"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "yaml" in data
    assert data["valid"] is True
    assert data["errors"] == []


def test_generate_endpoint_empty_description(client):
    """Test that empty description is rejected."""
    response = client.post(
        "/generate",
        json={"description": "   ", "model": "gpt-4o"}
    )

    assert response.status_code == 422


@patch("app.main.generate_openapi_spec")
def test_generate_endpoint_failure(mock_generate, client):
    """Test that generation errors are handled gracefully."""
    mock_generate.side_effect = Exception("API error")

    response = client.post(
        "/generate",
        json={"description": "Test", "model": "gpt-4o"}
    )

    assert response.status_code == 500
    assert "detail" in response.json()

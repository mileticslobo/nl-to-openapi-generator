"""Tests for app.validator module."""
import pytest
from app.validator import validate_spec


def test_validate_spec_valid():
    """Test that a valid minimal OpenAPI spec passes validation."""
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "Test API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "get": {
                    "summary": "List users",
                    "operationId": "listUsers",
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    is_valid, errors = validate_spec(spec)
    assert is_valid is True
    assert errors == []


def test_validate_spec_invalid():
    """Test that an invalid spec returns validation errors."""
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "Test API",
            # Missing required version field
        },
        "paths": {}
    }

    is_valid, errors = validate_spec(spec)
    assert is_valid is False
    assert len(errors) > 0


def test_validate_spec_malformed():
    """Test that a completely malformed spec doesn't crash."""
    spec = "not a dict"  # type: ignore

    is_valid, errors = validate_spec(spec)
    assert is_valid is False
    assert len(errors) > 0

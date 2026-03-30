"""Tests for app.generator module."""
import pytest
from unittest.mock import patch, MagicMock
from app.generator import generate_openapi_spec, _strip_markdown_fences


def test_strip_markdown_fences():
    """Test markdown fence removal."""
    yaml_with_fences = """```yaml
openapi: "3.0.3"
info:
  title: Test API
```"""

    result = _strip_markdown_fences(yaml_with_fences)
    assert result.startswith("openapi:")
    assert "```" not in result


def test_strip_markdown_fences_no_fences():
    """Test that YAML without fences is unchanged."""
    yaml_plain = """openapi: "3.0.3"
info:
  title: Test API"""

    result = _strip_markdown_fences(yaml_plain)
    assert result == yaml_plain


@patch("app.generator.client")
def test_generate_openapi_spec_success(mock_client):
    """Test successful spec generation with mocked OpenAI."""
    # Mock the OpenAI response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = """openapi: "3.0.3"
info:
  title: Test API
  version: "1.0.0"
paths:
  /test:
    get:
      summary: Test endpoint
      operationId: getTest
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
"""

    mock_client.chat.completions.create.return_value = mock_response

    result = generate_openapi_spec("A simple test API", model="gpt-4o")

    assert "yaml" in result
    assert "parsed" in result
    assert isinstance(result["parsed"], dict)
    assert result["parsed"]["openapi"] == "3.0.3"
    assert result["parsed"]["info"]["title"] == "Test API"


@patch("app.generator.client")
def test_generate_openapi_spec_invalid_yaml(mock_client):
    """Test that invalid YAML raises ValueError."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "not: valid: yaml: content:"

    mock_client.chat.completions.create.return_value = mock_response

    with pytest.raises(ValueError, match="invalid YAML"):
        generate_openapi_spec("Test", model="gpt-4o")


@patch("app.generator.client")
def test_generate_openapi_spec_non_dict_yaml(mock_client):
    """Test that non-dict YAML raises ValueError."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "- item1\n- item2"

    mock_client.chat.completions.create.return_value = mock_response

    with pytest.raises(ValueError, match="not a mapping"):
        generate_openapi_spec("Test", model="gpt-4o")

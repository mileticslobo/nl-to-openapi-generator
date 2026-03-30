from openapi_spec_validator import validate
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError


def validate_spec(spec_dict: dict) -> tuple[bool, list[str]]:
    """
    Validate an OpenAPI spec dict against the OpenAPI 3.x schema.

    Returns:
        (is_valid: bool, errors: list[str])
    """
    try:
        validate(spec_dict)
        return True, []
    except OpenAPIValidationError as exc:
        return False, [str(exc)]
    except Exception as exc:
        # Catch unexpected errors (e.g. malformed spec that breaks the validator)
        return False, [f"Unexpected validation error: {exc}"]

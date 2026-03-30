from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator

from app.generator import generate_openapi_spec
from app.validator import validate_spec

app: FastAPI = FastAPI(
    title="NL to OpenAPI Generator",
    description="Convert natural language API descriptions into valid OpenAPI 3.0 YAML specifications.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# --------------------------------------------------------------------------- #
# Request / Response models                                                    #
# --------------------------------------------------------------------------- #

class GenerateRequest(BaseModel):
    description: str
    model: str = "gpt-4o"

    @field_validator("description")
    @classmethod
    def description_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("description cannot be empty")
        return v.strip()


class GenerateResponse(BaseModel):
    yaml: str
    valid: bool
    errors: list[str]


# --------------------------------------------------------------------------- #
# Routes                                                                       #
# --------------------------------------------------------------------------- #

@app.get("/", include_in_schema=False)
async def serve_ui() -> FileResponse:
    return FileResponse("static/index.html")


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse, tags=["generator"])
async def generate(request: GenerateRequest) -> GenerateResponse:
    """
    Generate an OpenAPI 3.0.3 YAML specification from a natural language description.

    - **description**: plain-English description of the API endpoints you need
    - **model**: OpenAI model to use (default: gpt-4o)
    """
    try:
        result = generate_openapi_spec(request.description, model=request.model)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}")

    is_valid, errors = validate_spec(result["parsed"])

    return GenerateResponse(
        yaml=result["yaml"],
        valid=is_valid,
        errors=errors,
    )

import os
import logging
import yaml
from openai import OpenAI
from dotenv import load_dotenv
from app.prompts import SYSTEM_PROMPT

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _strip_markdown_fences(text: str) -> str:
    """Remove markdown code fences that the model may include despite instructions."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]  # drop the opening fence line (```yaml or ```)
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def generate_openapi_spec(description: str, model: str = "gpt-4o") -> dict:
    """
    Call the OpenAI API with an engineered prompt and return the parsed spec.

    Returns:
        {
            "yaml": str,        # raw YAML string
            "parsed": dict,     # parsed Python dict
        }

    Raises:
        ValueError: if the model output cannot be parsed as valid YAML.
        openai.OpenAIError: on API errors.
    """
    logger.info(f"Generating OpenAPI spec with {model} for description: {description[:100]}...")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Generate an OpenAPI 3.0.3 specification for the following API:\n\n"
                        f"{description}"
                    ),
                },
            ],
            temperature=0.2,  # low temperature for consistent, structured output
        )
        logger.debug(f"Received response from {model}")
    except Exception as exc:
        logger.error(f"OpenAI API error: {exc}")
        raise

    raw_output = response.choices[0].message.content
    clean_yaml = _strip_markdown_fences(raw_output)

    try:
        parsed = yaml.safe_load(clean_yaml)
        logger.debug("Successfully parsed YAML")
    except yaml.YAMLError as exc:
        logger.error(f"YAML parsing failed: {exc}")
        raise ValueError(f"Model returned invalid YAML: {exc}") from exc

    if not isinstance(parsed, dict):
        logger.error("Parsed output is not a dictionary")
        raise ValueError("Parsed YAML is not a mapping — unexpected model output.")

    logger.info("OpenAPI spec generation successful")
    return {
        "yaml": clean_yaml,
        "parsed": parsed,
    }

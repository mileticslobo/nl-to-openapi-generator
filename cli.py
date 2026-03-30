#!/usr/bin/env python3
"""
CLI entry point for NL to OpenAPI Generator.

Usage examples:
    python cli.py "An endpoint to list products and create a new product"
    python cli.py --file examples/users_api.txt --output out.yaml
    echo "Delete a user by ID" | python cli.py
"""

import argparse
import sys

from app.generator import generate_openapi_spec
from app.validator import validate_spec


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="nl-to-openapi",
        description="Generate an OpenAPI 3.0 YAML spec from a natural language description.",
    )
    parser.add_argument(
        "description",
        nargs="?",
        help="Natural language description of the API (passed directly as a string)",
    )
    parser.add_argument(
        "--file", "-f",
        metavar="PATH",
        help="Read the description from a .txt file instead",
    )
    parser.add_argument(
        "--output", "-o",
        metavar="PATH",
        help="Write the generated YAML to a file (default: stdout)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o)",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip OpenAPI spec validation",
    )
    args = parser.parse_args()

    # Resolve description source
    if args.file:
        try:
            with open(args.file) as fh:
                description = fh.read().strip()
        except FileNotFoundError:
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    elif args.description:
        description = args.description.strip()
    elif not sys.stdin.isatty():
        description = sys.stdin.read().strip()
    else:
        parser.print_help()
        sys.exit(1)

    if not description:
        print("Error: description is empty.", file=sys.stderr)
        sys.exit(1)

    print(f"[nl-to-openapi] Generating spec with {args.model}...", file=sys.stderr)

    try:
        result = generate_openapi_spec(description, model=args.model)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not args.no_validate:
        is_valid, errors = validate_spec(result["parsed"])
        if is_valid:
            print("[nl-to-openapi] Validation: PASSED ✓", file=sys.stderr)
        else:
            print("[nl-to-openapi] Validation: FAILED ✗", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)

    if args.output:
        with open(args.output, "w") as fh:
            fh.write(result["yaml"])
        print(f"[nl-to-openapi] Saved to {args.output}", file=sys.stderr)
    else:
        print(result["yaml"])


if __name__ == "__main__":
    main()

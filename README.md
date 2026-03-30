# NL to OpenAPI Generator

Convert a plain-English description of an API into a valid **OpenAPI 3.0.3 YAML** specification using the OpenAI API.

> **Portfolio project** demonstrating prompt engineering, structured LLM output, and OpenAPI fundamentals.

---

## Demo

**Input**
```
I need an endpoint to list users filtered by status, and another endpoint
to create a new user with name and email.
```

**Output** — a complete, validated OpenAPI 3.0.3 spec:
```yaml
openapi: "3.0.3"
info:
  title: Users API
  version: "1.0.0"
paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive, pending]
      ...
    post:
      summary: Create a user
      operationId: createUser
      requestBody:
        ...
components:
  schemas:
    User: ...
    CreateUserRequest: ...
    Error: ...
```

See [`examples/users_api.yaml`](examples/users_api.yaml) for the full output.

---

## Features

- **Natural language → OpenAPI 3.0.3 YAML** via GPT-4o
- **Prompt engineering** — carefully crafted system prompt enforces correct HTTP methods, path conventions, `$ref` reuse, required fields, and response codes
- **Validation** — every generated spec is validated with `openapi-spec-validator` before being returned
- **Web UI** — minimal single-page app with example prompts, model selector, and copy button
- **CLI** — pipe-friendly command-line tool for scripting and batch use
- **FastAPI backend** — auto-generated `/docs` (Swagger UI) for the generator's own API

---

## Tech Stack

| Layer      | Technology |
|------------|------------|
| Backend    | Python 3.11, FastAPI, Uvicorn |
| LLM        | OpenAI `gpt-4o` (via `openai` SDK) |
| Validation | `openapi-spec-validator` |
| YAML       | `pyyaml` |
| Frontend   | Vanilla HTML/CSS/JS (no build step) |

---

## Project Structure

```
nl-to-openapi-generator/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app — routes and request/response models
│   ├── generator.py     # OpenAI API call + YAML parsing
│   ├── validator.py     # openapi-spec-validator wrapper
│   └── prompts.py       # System prompt (core prompt engineering)
├── examples/
│   ├── users_api.txt    # Example natural language input
│   └── users_api.yaml   # Example generated output
├── static/
│   └── index.html       # Web UI (single file, no framework)
├── cli.py               # CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quickstart

### 1. Clone and install

```bash
git clone https://github.com/your-username/nl-to-openapi-generator.git
cd nl-to-openapi-generator

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set your API key

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-...
```

### 3a. Run the web app

```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) — the UI loads instantly.

The FastAPI auto-docs are available at [http://localhost:8000/docs](http://localhost:8000/docs).

### 3b. Use the CLI

```bash
# Pass description directly
python cli.py "An endpoint to list products and create a new product"

# Read from file, save to YAML
python cli.py --file examples/users_api.txt --output out.yaml

# Pipe input
echo "Delete a user by ID" | python cli.py

# Use a cheaper model
python cli.py --model gpt-4o-mini "List blog posts filtered by tag"
```

---

## How It Works

```
User input (natural language)
        │
        ▼
┌───────────────────┐
│   System Prompt   │  ← Prompt engineering:
│   (prompts.py)    │    enforces OpenAPI structure,
│                   │    HTTP conventions, $ref reuse
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   OpenAI API      │  gpt-4o, temperature=0.2
│   (generator.py)  │  (low temp = consistent output)
└────────┬──────────┘
         │ raw YAML string
         ▼
┌───────────────────┐
│   YAML Parser     │  yaml.safe_load()
│   (generator.py)  │  strips markdown fences if present
└────────┬──────────┘
         │ Python dict
         ▼
┌───────────────────┐
│   Validator       │  openapi-spec-validator
│   (validator.py)  │  returns (is_valid, errors)
└────────┬──────────┘
         │
         ▼
    JSON response
    { yaml, valid, errors }
```

### Prompt Engineering Highlights

The system prompt in `app/prompts.py` is the core of the project. Key decisions:

- **Temperature 0.2** — reduces hallucinations and produces more consistent YAML structure
- **"Output ONLY raw YAML"** — no markdown fences, no prose; model is told the first line must be `openapi: "3.0.3"`
- **Explicit rules for HTTP methods**, path design, pagination parameters, response codes, and `$ref` usage — without these, models tend to produce flat, non-reusable specs
- **Defensive stripping** — `generator.py` still strips markdown fences in case the model includes them despite instructions

---

## Example Prompts

| Prompt | What it exercises |
|--------|-------------------|
| `List users filtered by status, create a user with name and email` | query params, POST with requestBody, $ref schemas |
| `Product catalog: list with category/price filters, get by ID, create` | path params, multiple endpoints, reusable schemas |
| `Blog API: list posts, get by slug, create with tags array, delete by ID` | array fields, DELETE with 204, slug path param |

---

## Future Improvements

- [ ] **Streaming output** — stream tokens to the UI as they arrive
- [ ] **Multi-turn refinement** — "add an update endpoint" as a follow-up
- [ ] **YAML → JSON toggle** — output as JSON Schema or OpenAPI JSON
- [ ] **Swagger UI preview** — render the generated spec live using Swagger UI CDN
- [ ] **Export as file** — download button for the generated `.yaml`
- [ ] **GitHub Actions CI** — lint and validate example specs on push
- [ ] **Docker** — `Dockerfile` and `docker-compose.yml` for one-command startup
- [ ] **Tests** — pytest suite with mocked OpenAI responses

---

## License

MIT

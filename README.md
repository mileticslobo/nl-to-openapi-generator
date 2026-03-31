# NL to OpenAPI Generator

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Transform natural language into production-ready OpenAPI 3.0.3 specifications using AI**

> **Portfolio Project** showcasing full-stack development, AI integration, prompt engineering, and API design best practices.

---

## 🎯 Problem Solved

Writing OpenAPI specifications manually is tedious and error-prone. Developers spend hours crafting verbose YAML files, remembering HTTP conventions, and ensuring schema reusability. This tool eliminates that friction by converting plain English descriptions into validated, production-ready API specifications.

---

## 🚀 Live Demo

**Input Description:**
```
Create a REST API for managing users with the following features:
- List all users with optional filtering by status (active/inactive/pending)
- Create new users with name, email, and optional phone number
- Include proper error responses and pagination
```

**Generated OpenAPI 3.0.3 Specification:**
```yaml
openapi: "3.0.3"
info:
  title: User Management API
  version: "1.0.0"
  description: API for managing users with CRUD operations

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
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
      responses:
        '200':
          description: A list of users
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserList"
    post:
      summary: Create a user
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUserRequest"
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        '400':
          description: Invalid input
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        email:
          type: string
          format: email
        phone:
          type: string
        status:
          type: string
          enum: [active, inactive, pending]
        createdAt:
          type: string
          format: date-time
      required: [id, name, email, status]
    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: "#/components/schemas/User"
        pagination:
          type: object
          properties:
            page:
              type: integer
            totalItems:
              type: integer
            totalPages:
              type: integer
    CreateUserRequest:
      type: object
      properties:
        name:
          type: string
        email:
          type: string
          format: email
        phone:
          type: string
      required: [name, email]
    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
      required: [code, message]
```

See [`examples/users_api.yaml`](examples/users_api.yaml) for the complete generated specification.

---

## ✨ Key Features

- **🤖 AI-Powered Generation** — GPT-4o transforms natural language into valid OpenAPI specs
- **✅ Automatic Validation** — Every spec is validated against OpenAPI 3.0.3 standards
- **🎨 Web Interface** — Clean, responsive UI for interactive API design
- **🖥️ CLI Tool** — Command-line interface for automation and CI/CD integration
- **🏗️ Production Ready** — Docker support, comprehensive testing, and error handling
- **📚 Self-Documenting** — Auto-generated FastAPI docs at `/docs`

---

## 🏗️ Architecture & Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.9+, FastAPI, Uvicorn | REST API server with auto-generated docs |
| **AI Engine** | OpenAI GPT-4o API | Natural language processing and YAML generation |
| **Validation** | `openapi-spec-validator` | Ensures generated specs are valid |
| **Serialization** | `pyyaml` | YAML parsing and generation |
| **Frontend** | Vanilla HTML/CSS/JS | No-build web interface |
| **Testing** | pytest, pytest-asyncio | Comprehensive test coverage |
| **Deployment** | Docker, docker-compose | Containerized deployment |

---

## 📁 Project Structure

```
nl-to-openapi-generator/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application with routes
│   ├── generator.py     # OpenAI integration and YAML processing
│   ├── validator.py     # OpenAPI specification validation
│   └── prompts.py       # System prompts for AI (prompt engineering)
├── static/
│   └── index.html       # Web UI (single-page application)
├── tests/
│   ├── test_generator.py # Unit tests for AI generation
│   ├── test_main.py     # API endpoint tests
│   └── test_validator.py # Validation tests
├── examples/
│   ├── users_api.txt    # Sample input descriptions
│   └── users_api.yaml   # Sample generated outputs
├── cli.py               # Command-line interface
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
├── Dockerfile           # Container definition
├── docker-compose.yml   # Multi-container setup
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key

### 1. Clone and Setup

```bash
git clone https://github.com/mileticslobo/nl-to-openapi-generator.git
cd nl-to-openapi-generator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Run the Application

**Option A: Web Interface**
```bash
uvicorn app.main:app --reload
```
Open [http://localhost:8000](http://localhost:8000) for the web UI.

**Option B: Command Line**
```bash
# Direct input
python cli.py "Create endpoints to manage blog posts with CRUD operations"

# From file
python cli.py --file examples/users_api.txt --output api.yaml

# Piped input
echo "API for managing products with categories" | python cli.py

# Different model
python cli.py --model gpt-4o-mini "Simple user registration endpoint"
```

---

## 🔧 How It Works

```
Natural Language Input
        │
        ▼
┌─────────────────────┐
│   System Prompt     │  ← Carefully engineered prompts
│   (app/prompts.py)  │    enforce OpenAPI conventions
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   OpenAI GPT-4o     │  Temperature: 0.2 for consistency
│   (app/generator.py)│  Structured output generation
└─────────┬───────────┘
          │ Raw YAML Response
          ▼
┌─────────────────────┐
│   YAML Processing   │  Parse and clean response
│   (app/generator.py)│  Strip markdown fences if present
└─────────┬───────────┘
          │ Python Dictionary
          ▼
┌─────────────────────┐
│   OpenAPI Validator │  Validate against 3.0.3 spec
│   (app/validator.py)│  Return validation errors if any
└─────────┬───────────┘
          │
          ▼
   Validated API Spec
   { yaml, valid, errors }
```

### 🤖 Prompt Engineering

The core innovation lies in `app/prompts.py`. Key techniques:

- **Temperature Control**: 0.2 reduces hallucinations while maintaining creativity
- **Structured Instructions**: Explicit rules for HTTP methods, path design, and schema reuse
- **Defensive Parsing**: Robust handling of AI responses with fallback mechanisms
- **Convention Enforcement**: Ensures RESTful patterns and OpenAPI best practices

---

## 📋 Use Cases

### For Developers
- **Rapid Prototyping**: Sketch API designs without YAML syntax knowledge
- **Documentation Automation**: Generate specs from existing code comments
- **API Design Reviews**: Validate designs before implementation

### For Teams
- **Standardization**: Ensure consistent API documentation across projects
- **Onboarding**: Help new developers understand API structures quickly
- **Legacy Migration**: Document undocumented APIs from descriptions

### For Organizations
- **API Governance**: Maintain standards across multiple development teams
- **Developer Experience**: Reduce time spent on boilerplate documentation
- **Tool Integration**: CLI support for CI/CD pipelines

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_generator.py -v
```

---

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up --build

# Or with Docker directly
docker build -t nl-to-openapi .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key nl-to-openapi
```

---

## 🔮 Future Enhancements

- [ ] **Real-time Streaming**: Show generation progress in the UI
- [ ] **Multi-turn Conversations**: Refine specs with follow-up requests
- [ ] **Format Options**: JSON Schema, Postman collections
- [ ] **Live Preview**: Embedded Swagger UI for generated specs
- [ ] **GitHub Integration**: Pull request comments with generated specs
- [ ] **Custom Models**: Support for fine-tuned or local LLMs
- [ ] **Batch Processing**: Generate multiple specs from a directory
- [ ] **API Import**: Generate specs from existing API calls

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenAI for the GPT-4o model
- FastAPI community for excellent documentation
- OpenAPI Initiative for the specification standard

---

**Built with ❤️ by [Slobodan Miletic](https://github.com/mileticslobo)**

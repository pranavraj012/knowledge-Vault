# PKM Backend - Fast Setup Guide

## Quick Start

1. **Ensure UV is installed** and you're in the backend directory:
   ```bash
   cd e:\pkm\backend
   ```

2. **Install dependencies:**
   ```bash
   uv sync --extra dev
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

4. **Initialize database:**
   ```bash
   uv run python -m pkm_backend.cli init-db
   ```

5. **Start the server:**
   ```bash
   uv run uvicorn pkm_backend.main:app --reload --host localhost --port 8000
   ```

## API Endpoints

The server will run on http://localhost:8000

- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health
- **API Base**: http://localhost:8000/api/v1/

## Setting up Ollama (Optional for AI features)

1. Install Ollama from https://ollama.ai/
2. Pull a model: `ollama pull llama3.1`
3. Test: `uv run python -m pkm_backend.cli check-ollama`

## CLI Commands

```bash
# Database management
uv run python -m pkm_backend.cli init-db
uv run python -m pkm_backend.cli reset-db

# Ollama testing
uv run python -m pkm_backend.cli check-ollama
uv run python -m pkm_backend.cli test-ai "Hello world"

# Run server
uv run python -m pkm_backend.cli run-server
```

## Testing the API

```bash
# Create a workspace
curl -X POST "http://localhost:8000/api/v1/workspaces" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Workspace", "description": "My first workspace"}'

# Create a note
curl -X POST "http://localhost:8000/api/v1/notes" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Note", "content": "# Hello\n\nThis is my first note!", "workspace_id": 1}'

# List notes
curl "http://localhost:8000/api/v1/notes"
```

## Ready for Frontend Integration

The backend is now ready to be connected to a React/Next.js frontend! All CRUD operations for notes, workspaces, and tags are implemented, plus AI features when Ollama is available.
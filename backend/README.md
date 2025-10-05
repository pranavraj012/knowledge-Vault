# PKM Backend - Personal Knowledge Management System

A privacy-focused, student-friendly personal knowledge management system backend built with FastAPI. This backend provides APIs for managing notes, workspaces, and AI-powered features using locally hosted LLMs via Ollama.

## 🚀 Features

- **Notes Management**: Full CRUD operations for markdown notes
- **Workspaces**: Organize notes by subject/topic
- **Tags**: Categorize and filter notes with tags
- **AI Integration**: Local LLM integration via Ollama for:
  - Text cleanup and improvement
  - Style-based rephrasing
  - Semantic search through notes
  - Chat with your notes
- **File Storage**: Local markdown file storage with automatic sync
- **Privacy-First**: All data stored locally, no cloud dependencies
- **Modern API**: RESTful API with automatic OpenAPI documentation

## 📋 Prerequisites

- Python 3.11+
- [UV](https://github.com/astral-sh/uv) for package management
- [Ollama](https://ollama.ai/) for local LLM support

### Installing Ollama

1. Download and install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull a model (recommended: llama3.2:1b):
   ```bash
   ollama pull llama3.2:1b
   ```
3. Verify Ollama is running:
   ```bash
   ollama list
   ```

## 🛠️ Installation

1. **Clone and setup the project:**
   ```bash
   cd e:\pkm\backend
   ```

2. **Install dependencies with UV:**
   ```bash
   uv sync --extra dev
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to match your configuration.

4. **Initialize the database:**
   ```bash
   uv run python -m pkm_backend.cli init-db
   ```

## 🏃‍♂️ Running the Application

### Development Server

```bash
# Using UV
uv run python -m pkm_backend.cli run-server

# Or directly with uvicorn
uv run uvicorn pkm_backend.main:app --reload --host localhost --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production

```bash
uv run uvicorn pkm_backend.main:app --host 0.0.0.0 --port 8000
```

## 🔧 CLI Commands

The project includes a CLI for development and management tasks:

```bash
# Initialize database
uv run python -m pkm_backend.cli init-db

# Reset database (WARNING: deletes all data)
uv run python -m pkm_backend.cli reset-db

# Check Ollama connection and list models
uv run python -m pkm_backend.cli check-ollama

# Test AI functionality
uv run python -m pkm_backend.cli test-ai "Your test text here"

# Run development server
uv run python -m pkm_backend.cli run-server
```

## 📚 API Endpoints

### Core Endpoints

- `GET /health` - Health check
- `GET /api/v1/workspaces` - List workspaces
- `POST /api/v1/workspaces` - Create workspace
- `GET /api/v1/notes` - List notes
- `POST /api/v1/notes` - Create note
- `GET /api/v1/tags` - List tags

### AI Endpoints

- `POST /api/v1/ai/cleanup` - Cleanup note content
- `POST /api/v1/ai/rephrase` - Rephrase text in different styles
- `POST /api/v1/ai/chat` - Chat with your notes
- `GET /api/v1/ai/models` - List available AI models
- `GET /api/v1/ai/health` - Check AI service status

### Search Endpoints

- `POST /api/v1/search` - AI-powered semantic search
- `GET /api/v1/search/simple` - Simple text search

## 🏗️ Project Structure

```
src/pkm_backend/
├── api/
│   └── v1/
│       ├── endpoints/          # API endpoint definitions
│       └── router.py           # Main API router
├── core/
│   └── config.py              # Application configuration
├── db/
│   ├── database.py            # Database connection & session
│   └── init_db.py             # Database initialization
├── models/
│   ├── database.py            # SQLAlchemy models
│   └── schemas.py             # Pydantic schemas
├── services/
│   └── ollama.py              # Ollama LLM integration
├── cli.py                     # Development CLI
└── main.py                    # FastAPI application
```

## 🗄️ Database Schema

### Tables

- **workspaces**: Organize notes by subject
- **notes**: Store markdown content with metadata
- **tags**: Categorize notes
- **note_tags**: Many-to-many relationship between notes and tags
- **ai_sessions**: Track AI interactions and performance

## 🔌 Environment Variables

Key configuration options in `.env`:

```env
# Server
HOST=localhost
PORT=8000
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./pkm.db

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_LLM_MODEL=llama3.2:1b

# Storage
NOTES_STORAGE_PATH=./data/notes
WORKSPACES_STORAGE_PATH=./data/workspaces
```

## 🧪 Testing

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=pkm_backend
```

## 🚀 Development

### Code Formatting

```bash
# Format code with Black
uv run black src/

# Sort imports with isort
uv run isort src/

# Type checking with mypy
uv run mypy src/
```

### Pre-commit Hooks

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## 📖 Usage Examples

### Creating a Workspace

```bash
curl -X POST "http://localhost:8000/api/v1/workspaces" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Computer Science",
    "description": "CS coursework and notes",
    "color": "#3B82F6"
  }'
```

### Creating a Note

```bash
curl -X POST "http://localhost:8000/api/v1/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Data Structures Overview",
    "content": "# Data Structures\n\nArrays, linked lists, stacks, queues...",
    "workspace_id": 1,
    "tag_ids": []
  }'
```

### AI Text Cleanup

```bash
curl -X POST "http://localhost:8000/api/v1/ai/cleanup" \
  -H "Content-Type: application/json" \
  -d '{
    "note_id": 1,
    "cleanup_type": "full"
  }'
```

## 🎯 Roadmap

- [ ] Authentication and user management
- [ ] Export to PDF/HTML
- [ ] Full-text search with indexing
- [ ] Real-time collaborative editing
- [ ] Plugin system for extensions
- [ ] Advanced AI features (summarization, Q&A)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔧 Troubleshooting

### Ollama Connection Issues

1. Ensure Ollama is running: `ollama list`
2. Check the base URL in `.env`
3. Test connection: `uv run python -m pkm_backend.cli check-ollama`

### Database Issues

1. Reset database: `uv run python -m pkm_backend.cli reset-db`
2. Check file permissions in `./data/` directory
3. Verify SQLite installation

### Port Already in Use

Change the port in `.env` or kill the process:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

# Knowledge Vault 🧠

A privacy-focused, student-friendly Personal Knowledge Management (PKM) system designed for desktop use. Write and organize notes in Markdown, store data locally, and leverage on-device AI to enhance your learning and productivity.

## 🌟 Features

### Core Functionality
- **📝 Markdown Notes**: Rich text editing with full Markdown support
- **🗂️ Workspaces**: Organize notes by subject, course, or project
- **🏷️ Smart Tagging**: Flexible categorization system
- **🔍 Powerful Search**: Both traditional and AI-powered semantic search
- **📱 Modern UI**: Clean, responsive interface built with React/Next.js

### AI-Powered Features (Local LLM via Ollama)
- **✨ Text Enhancement**: Grammar correction, clarity improvement
- **🎨 Style Transformation**: Academic, casual, formal, creative writing styles
- **🤖 Chat with Notes**: Ask questions about your knowledge base
- **🧠 Smart Search**: Semantic understanding of your content
- **📊 Learning Insights**: AI-driven content analysis

### Privacy & Security
- **🔒 100% Local**: All data stored on your device
- **🚫 No Cloud Dependency**: Works completely offline
- **🔐 Your Data, Your Control**: No external services or data sharing
- **⚡ Fast Performance**: Direct file system access

## 🏗️ Architecture

```
knowledge-vault/
├── backend/                 # FastAPI backend
│   ├── src/pkm_backend/    # Main application code
│   ├── data/               # Local data storage
│   └── README.md           # Backend documentation
├── frontend/               # Next.js frontend (coming soon)
├── docs/                   # Project documentation
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+** with [UV](https://github.com/astral-sh/uv) package manager
2. **Node.js 18+** (for frontend, when available)
3. **Ollama** (optional, for AI features) - [Download here](https://ollama.ai/)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/pranavraj012/knowledge-Vault.git
cd knowledge-Vault

# Set up the backend
cd backend
uv sync --extra dev
cp .env.example .env

# Initialize database
uv run python -m pkm_backend.cli init-db

# Start the backend server
uv run uvicorn pkm_backend.main:app --reload --host localhost --port 8000
```

### AI Setup (Optional)

```bash
# Install Ollama from https://ollama.ai/
# Pull a language model
ollama pull llama3.1

# Test AI integration
cd backend
uv run python -m pkm_backend.cli check-ollama
uv run python -m pkm_backend.cli test-ai "Hello, test my AI setup!"
```

## 📖 Documentation

- **Backend API**: [Backend README](./backend/README.md)
- **API Documentation**: http://localhost:8000/docs (when server is running)
- **Quick Start Guide**: [Backend Quick Start](./backend/QUICKSTART.md)

## 🎯 Use Cases

### For Students
- **📚 Course Notes**: Organize by semester, subject, and topic
- **📋 Research Management**: Collect and connect research materials
- **✍️ Assignment Writing**: AI-assisted writing and editing
- **🔗 Knowledge Linking**: Cross-reference related concepts

### For Professionals
- **📊 Project Documentation**: Technical notes and specifications
- **💡 Idea Management**: Capture and develop concepts
- **📈 Meeting Notes**: Searchable records with AI insights
- **🎓 Continuous Learning**: Personal knowledge base

### For Researchers
- **📑 Literature Notes**: Organize academic papers and references
- **🔬 Experiment Logs**: Detailed research documentation
- **💭 Hypothesis Tracking**: Connect ideas across studies
- **📝 Paper Writing**: AI-assisted academic writing

## 🛠️ Development

### Backend Development

```bash
cd backend

# Install dev dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Code formatting
uv run black src/
uv run isort src/

# Type checking
uv run mypy src/

# Database management
uv run python -m pkm_backend.cli reset-db
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure code quality: `uv run black src/ && uv run pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📊 Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Ollama**: Local LLM integration
- **UV**: Fast Python package installer and resolver

### Frontend (Planned)
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **React Query**: Data fetching and caching

### Database
- **SQLite**: Lightweight, file-based database
- **Full-text search**: Built-in search capabilities
- **File storage**: Markdown files with database metadata

## 🗺️ Roadmap

### Phase 1: Core Backend ✅
- [x] Notes CRUD operations
- [x] Workspaces and tags
- [x] AI integration (Ollama)
- [x] Search functionality
- [x] API documentation

### Phase 2: Frontend Development 🚧
- [ ] React/Next.js setup
- [ ] Note editor with live preview
- [ ] Workspace management UI
- [ ] Search interface
- [ ] AI features integration

### Phase 3: Advanced Features 📋
- [ ] Real-time collaboration
- [ ] Export to PDF/HTML
- [ ] Plugin system
- [ ] Advanced AI features
- [ ] Mobile app

### Phase 4: Enterprise Features 🎯
- [ ] Team workspaces
- [ ] Advanced analytics
- [ ] Integration APIs
- [ ] Cloud sync options (optional)

## 🤝 Community

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Ideas and questions
- **Pull Requests**: Code contributions welcome

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama Team**: For making local LLM integration accessible
- **FastAPI Team**: For the excellent web framework
- **Open Source Community**: For the amazing tools that make this possible

---

**Built with ❤️ for students, researchers, and knowledge workers who value privacy and control over their data.**

**Star ⭐ this repository if you find it useful!**
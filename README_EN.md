# L10nLight - Modern Async Microservice for Offer Walls Management

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Litestar](https://img.shields.io/badge/Litestar-2.8+-green.svg)](https://litestar.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A high-performance asynchronous microservice built with **Litestar** framework for managing offer walls and associated offers. This project replicates and enhances the functionality of a Django REST Framework application with modern async architecture.

## ✨ Features

- 🚀 **High Performance**: Async Litestar + SQLAlchemy 2.0
- 🏗️ **Clean Architecture**: Domain-Driven Design
- 🐳 **Docker Ready**: Complete containerization
- 🧪 **Comprehensive Testing**: Unit + integration tests
- 📚 **Bilingual Docs**: English & Russian documentation
- ⚡ **Modern Tooling**: Pre-commit, CI/CD, type safety
- 🔒 **Secure**: CORS, validation, security scanning

## 🚀 Quick Start

### Docker (Recommended)
```bash
git clone https://github.com/soewal19/L10nLight.git
cd L10nLight
docker-compose up --build
curl http://localhost:8000/api/offerwalls/get_offer_names
```

### Local Development
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.server
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/offerwalls/{token}` | Get offer wall by UUID token |
| `GET` | `/api/offerwalls/by_url/{url}` | Get offer wall by URL |
| `GET` | `/api/offerwalls/get_offer_names` | Get all available offer names |
| `GET` | `/api/offerwalls` | List offer walls with filtering |

### Example Response
```json
{
  "token": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Sample OfferWall",
  "url": "https://example.com",
  "description": "A sample offer wall",
  "offer_assignments": [
    {
      "offer": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "id": 1,
        "url": "https://loanplus.com",
        "is_active": true,
        "name": "Loanplus",
        "sum_to": "10000",
        "term_to": 30,
        "percent_rate": 5
      }
    }
  ],
  "popup_assignments": []
}
```

## 🏛️ Architecture

```
┌─────────────────┐
│   Controllers   │  ← API Routes (Litestar)
└─────────────────┘
         │
┌─────────────────┐
│    Services     │  ← Business Logic
└─────────────────┘
         │
┌─────────────────┐
│    Entities     │  ← Domain Models
└─────────────────┘
         │
┌─────────────────┐
│   Repositories  │  ← Data Access (SQLAlchemy)
└─────────────────┘
```

## 🗄️ Data Models

- **OfferWall**: Container with unique token
- **Offer**: Individual offer with financial terms
- **OfferAssignment**: Many-to-many with ordering
- **PopupAssignment**: Popup offers with ordering
- **OfferChoices**: 34 predefined offer types

## 🧪 Testing

```bash
pytest                    # Run all tests
pytest --cov=app         # With coverage
pytest -v               # Verbose output
```

## 🛠️ Development Tools

```bash
make dev          # Start development server
make test         # Run tests
make lint         # Code quality checks
make format       # Format code
make docker-up    # Start Docker services
```

## 🐳 Docker Services

- **api**: Litestar application
- **db**: PostgreSQL 16
- **nginx**: Reverse proxy

## 📚 Documentation

- **[WORKFLOW.md](WORKFLOW.md)** - Development workflow
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[docs/tests/README.md](docs/tests/README.md)** - Testing guide

## 🔧 Configuration

```bash
APP_ENV=development
APP_DB_URL=postgresql+asyncpg://user:pass@localhost:5432/app
APP_ALLOWED_ORIGINS='["http://localhost:3000"]'
LOG_LEVEL=INFO
```

## 🔄 CI/CD

- ✅ Automated testing
- ✅ Code quality checks
- ✅ Security scanning
- ✅ Docker builds
- ✅ Deployment pipelines

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ Star this repository if it helped you!**

Made with ❤️ by [soewal19](https://github.com/soewal19)

</div>

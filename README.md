# Trademark Search Pro – CI/CD Demo

> A production-style, multi-stage automation pipeline designed to streamline the software delivery lifecycle from development to production. Runs entirely via **Docker** – no local Python installation required.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Phase 1 – CI & Dev Merge                                                │
│                                                                          │
│  Local PC ──► GitHub Repo ──► GitHub Actions (CI Pipeline)               │
│       feature/bugfix branch      ├─ Automated Tests (pytest)             │
│                                  ├─ Linting (flake8)                     │
│                                  └─ Security Scan (bandit)               │
│                                       │                                  │
│                             Checks pass? ──► Manual Code Review (PR)     │
│                                                   │                      │
│                                         Approved? ──► Merge to dev       │
│                                                        │                 │
│                                              Deploy to Dev Server        │
│                                              http://<IP>:5000            │
├──────────────────────────────────────────────────────────────────────────┤
│  Phase 2 – Staging & Live                                                │
│                                                                          │
│  Dev Server ──► Integration Tests + Security Scan (GitHub Actions)       │
│                          │                                               │
│                 Checks pass? ──► Manual QA (UI/UX, UAT)                  │
│                                       │                                  │
│                             Approved? ──► Merge to main                  │
│                                            │                             │
│                                   Deploy to Production                   │
│                                   http://<IP>:8000                       │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
development_workflow/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI entry point
│   ├── routes/
│   │   ├── health.py          # GET /health
│   │   ├── version.py         # GET /version
│   │   └── data.py            # GET /api/data
│   └── services/
│       └── data_service.py    # Business logic layer
├── tests/
│   ├── test_health.py
│   ├── test_version.py
│   └── test_data.py
├── .github/workflows/
│   ├── ci.yml                 # CI – lint, test, security scan
│   ├── cd-dev.yml             # CD – build & deploy to dev
│   └── cd-prod.yml            # CD – build & deploy to prod
├── Dockerfile                 # Multi-stage, non-root, slim
├── docker-compose.yml         # Dev (5000) + Prod (8000)
├── requirements.txt
├── .env.example
├── .dockerignore
├── .flake8
├── .gitignore
└── README.md
```

---

## Prerequisites

- **Docker Desktop** installed and running ([download](https://www.docker.com/products/docker-desktop/))
- No Python, pip, or any other runtime needed on your machine

---

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd development_workflow
```

### 2. Start both environments

```bash
docker compose up --build
```

| Environment | URL                        | Log Level |
|-------------|----------------------------|-----------|
| **Dev**     | `http://localhost:5000`     | DEBUG     |
| **Prod**    | `http://localhost:8000`     | WARNING   |

### 3. Start a single environment

```bash
# Dev only
docker compose up --build app_dev

# Prod only
docker compose up --build app_prod
```

### 4. Stop everything

```bash
docker compose down
```

---

## API Endpoints

| Method | Path          | Description                                   |
|--------|---------------|-----------------------------------------------|
| GET    | `/health`     | Health check – returns `{"status": "healthy"}` |
| GET    | `/version`    | App version & environment name                |
| GET    | `/api/data`   | All sample trademark records                  |
| GET    | `/api/data?q=acme` | Filter trademarks by name (case-insensitive) |

### Example requests

```bash
# Health check
curl http://localhost:5000/health

# Version info
curl http://localhost:8000/version

# Search data
curl "http://localhost:5000/api/data?q=cloud"
```

---

## CI/CD Pipelines (GitHub Actions)

### CI Pipeline (`ci.yml`)

**Trigger:** Pull request to `dev` or `main`

| Step | Tool   | Purpose                          |
|------|--------|----------------------------------|
| 1    | flake8 | Code style & linting             |
| 2    | pytest | Unit tests                       |
| 3    | bandit | Security vulnerability scanning  |

All steps must pass for the PR to be merge-ready.

### CD – Dev (`cd-dev.yml`)

**Trigger:** Push/merge to `dev` branch

1. Builds the Docker image
2. Runs a container on port 5000
3. Smoke-tests the `/health` endpoint
4. (Optional) Pushes image to container registry

### CD – Prod (`cd-prod.yml`)

**Trigger:** Push/merge to `main` branch

1. Builds the Docker image
2. Runs a container on port 8000
3. Smoke-tests the `/health` endpoint
4. (Optional) Pushes image to container registry

---

## Environment Variables

| Variable      | Default        | Description                       |
|---------------|----------------|-----------------------------------|
| `ENVIRONMENT` | `development`  | `development` or `production`     |
| `APP_VERSION` | `0.1.0`        | Semantic version shown in `/version` |
| `LOG_LEVEL`   | `INFO`         | Python log level                  |

Copy `.env.example` to `.env` to customize locally (`.env` is git-ignored).

---

## Security Practices

- **No secrets in code** – all config via environment variables
- **Non-root container** – app runs as `appuser` inside Docker
- **Multi-stage build** – build tools excluded from the final image
- **Bandit scan** – automated security analysis in CI
- **Minimal base image** – `python:3.12-slim`
- **`.env` is git-ignored** – only `.env.example` is committed

---

## Running Tests Locally (via Docker)

No local Python needed – run tests inside a container:

```bash
docker compose run --rm --no-deps app_dev sh -c "pip install pytest && pytest tests/ -v"
```

---

## License

MIT

## Quick Context

- Project: FastAPI + Beanie (MongoDB) TODO app. Main entry: `app/app.py`.
- Key patterns: Beanie Documents in `app/models/`, Pydantic v2 schemas in `app/schemas/`, route handlers under `app/api/api_v1/handlers/`, and business logic in `app/services/`.

## Architecture (Big Picture)

- app/app.py: creates FastAPI `app`, initializes Motor + Beanie in the `lifespan` asynccontextmanager. This file controls DB startup/shutdown.
- API routing: `app/api/api_v1/router.py` aggregates sub-routers. Add new feature routers here using `router.include_router(..., prefix='/your_prefix')`.
- Auth: `app/api/auth/jwt.py` contains login/refresh endpoints and token generation using helpers in `app/core/security.py`.
- Models: `app/models/*` are Beanie `Document` classes. IDs are UUIDs and mapped to Mongo `_id` via `alias="_id"`.
- Schemas: `app/schemas/*` use Pydantic v2. Note use of `validation_alias`/`serialization_alias` and `ConfigDict`/`model_config` to map `_id`↔`id`.
- Services vs Handlers: business logic lives in `app/services/*` (e.g., `UserService`) and handlers (in `app/api/.../handlers/`) translate service errors to `HTTPException` responses.

## Project-specific Conventions & Gotchas

- Absolute imports: use `from app.xxx import ...` (project package style), not relative imports. Many files rely on these absolute paths.
- Error handling: services raise Python errors (e.g., `ValueError`) — handlers are responsible for converting those into `fastapi.HTTPException` with proper `status_code`.
- ID handling: models use `id: UUID = Field(default_factory=uuid4, alias="_id")`. When querying with Beanie, pass stringified UUIDs where appropriate (e.g., `await User.get(str(uuid))`).
- Pydantic v2: schemas intentionally use `model_config = ConfigDict(from_attributes=True, populate_by_name=True)` to allow returning Beanie documents and expose `id` in JSON.
- JWT usage: access and refresh tokens use separate secret keys (`JWT_SECRET_KEY` and `JWT_REFRESH_SECRET_KEY`) and expirations are in `app/core/config.py`.

## Key Files to Reference

- `app/app.py` — FastAPI app lifecycle & Beanie init
- `app/core/config.py` — Settings (reads `.env` at repository root)
- `app/core/security.py` — password hashing and token creation helpers
- `app/api/api_v1/router.py` — where to register routers
- `app/api/auth/jwt.py` — login, refresh, test-token endpoints
- `app/services/user_service.py` — example service layer (no HTTP concerns)
- `app/api/api_v1/handlers/*.py` — HTTP layer; expect `HTTPException` responses here

## How to Run / Debug

- Local (dev):

```bash
pip install -r requirements.txt
uvicorn app.app:app --reload --host 127.0.0.1 --port 8000
```

- Docker (recommended for matching env):

```bash
docker-compose up --build
```

- Environment variables: `.env` at repo root is loaded by `app/core/config.py`. When using Docker, `docker-compose.yml` supplies `MONGO_CONNECTION_STRING`, `JWT_SECRET_KEY`, `JWT_REFRESH_SECRET_KEY`, `PROJECT_NAME`.

## Common Development Tasks & Examples

- Add a new route group: create `app/api/api_v1/handlers/your_feat.py` with an `APIRouter()` and then register it in `app/api/api_v1/router.py` using `router.include_router(your_router, prefix='/your_prefix', tags=['your_tag'])`.

- Create model + schema + handler pattern:
  - Model: `app/models/YourModel` extends `beanie.Document` and uses `id: UUID = Field(..., alias='_id')`.
  - Schema: `app/schemas/your_schema.py` uses Pydantic v2, map `_id`→`id` with `validation_alias`/`serialization_alias` or `populate_by_name=True`.
  - Service: business logic in `app/services/your_service.py` (raise Python errors, do not import FastAPI types).
  - Handler: HTTP layer in `app/api/api_v1/handlers/` — convert service errors to `HTTPException`.

## Authentication & Tokens

- Login endpoint: POST `/api/v1/auth/login` accepts `application/x-www-form-urlencoded` (OAuth2PasswordRequestForm) and returns `access_token` and `refresh_token`.
- Refresh endpoint: POST `/api/v1/auth/refresh` expects JSON `{ "refresh_token": "..." }` and returns a new access token.
- To protect endpoints, handlers depend on `get_current_user` at `app/api/api_v1/dependencies/user_deps.py`. This decodes JWT using `JWT_SECRET_KEY` and returns `User` (Beanie document).

## Tests & Linting

- There are no test files present. When adding tests, use async test clients (e.g., `httpx.AsyncClient` + `pytest-asyncio`) and provide a test Mongo instance (or use `mongomock` / docker test compose).

## When You Are Unsure — Quick Navigation Tips

- Where to add routes: `app/api/api_v1/router.py`
- Where to add business logic: `app/services/`
- Where to add DB models: `app/models/`
- How DB is initialized: read `app/app.py` lifespan function

---
If any part of the app lifecycle, environment setup, or local run commands are outdated or you want me to include explicit `.env` keys and example values, tell me which details to add and I'll update this file.

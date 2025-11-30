# C4 Documentation

This folder contains a Structurizr DSL `workspace.dsl` describing the system:

- Context: User, Nginx, Litestar API, PostgreSQL, and the existing DRF (reference).
- Containers: Nginx, Litestar API, PostgreSQL.
- Components: OfferWallController, Schemas, Models, DB Setup, Config, Error Handlers.
- Dynamics: Request flows for `GET /api/offerwalls/{token}` and `GET /api/offerwalls/get_offer_names`.

How to render:
- Option 1 (Structurizr Lite, Docker):
  - Run: `docker run -p 8080:8080 -v /absolute/path/to/docs/c4:/usr/local/structurizr structurizr/lite`
  - Open `http://localhost:8080` and load `workspace.dsl`.

- Option 2 (Structurizr CLI or Desktop):
  - Use Structurizr tooling to open `workspace.dsl` and export diagrams.

Notes:
- The microservice matches DRF behavior for the required endpoints and returns DRF-compatible shapes.
- Nginx proxies `/api/*` to Litestar and strips the `/api/` prefix.
- Config loads `.env` via pydantic-settings; set `APP_ALLOWED_ORIGINS` to a JSON array (e.g., `["*"]`) for CORS.
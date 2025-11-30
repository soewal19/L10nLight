workspace "Offer Admin Microservice" "C4 model of the Litestar-based microservice replicating DRF behavior" {

  model {
    user = person "User" "End user consuming the API"
    drf = softwareSystem "Existing DRF System" "Reference API for parity" { tags "External" }

    ms = softwareSystem "Offer Admin Microservice (Litestar)" "Isolated service with async SQLAlchemy and pydantic-settings" {

      nginx = container "Nginx" "Reverse proxy forwarding /api/* to Litestar" "Nginx" { tags "Container" }
      api = container "Litestar API" "Python 3.12, Granian/UVicorn runtime, Litestar ASGI app" "Python/Litestar" {
        tags "Container"

        controller = component "OfferWallController" "HTTP endpoints: GET /offerwalls/{token}, GET /offerwalls/get_offer_names" "Litestar Controller"
        schemas = component "Pydantic Schemas" "Response models mirroring DRF serializers" "Pydantic"
        models = component "SQLAlchemy Models" "Offer, OfferWall, OfferAssignment, PopupAssignment" "SQLAlchemy"
        db_setup = component "DB Setup" "Async engine, session maker, init_db, DI for AsyncSession" "SQLAlchemy Async"
        config = component "Config (pydantic-settings)" "Loads .env with APP_*: server, DB URL, CORS" "Pydantic Settings"
        errors = component "Error Handlers" "DRF-compatible 404 and validation handling" "Litestar"

        controller -> db_setup "Uses AsyncSession (dependency injection)"
        controller -> models "Queries and eager-loads nested offers"
        controller -> schemas "Serializes to DRF-compatible shapes"
        controller -> errors "Raises NotFound for missing token"
        db_setup -> models "Creates tables on startup (init_db)"
        api -> config "Reads app and DB settings from .env"
      }

      db = container "PostgreSQL" "Persistent storage for offers and offer walls" "Postgres"
    }

    user -> nginx "HTTP requests to domain.com/api/"
    nginx -> api "Proxy /api/* -> Litestar"
    api -> db "Async SQLAlchemy (asyncpg driver)"
    user -> drf "Consumes DRF (reference)" { tags "External" }
  }

  views {
    systemLandscape "Context" {
      include *
      autoLayout
    }

    container ms "Containers" {
      include nginx
      include api
      include db
      autoLayout
    }

    component api "Components" {
      include controller
      include schemas
      include models
      include db_setup
      include config
      include errors
      autoLayout
    }

    dynamic "Get OfferWall by Token" {
      user -> nginx "GET /api/offerwalls/{token}"
      nginx -> api "Proxy to ASGI"
      api -> controller "Route: /offerwalls/{token}"
      controller -> db_setup "Obtain AsyncSession"
      db_setup -> db "SELECT OfferWall + assignments + offers"
      controller -> schemas "Validate & serialize"
      controller -> user "200 JSON (DRF-compatible)"
    }

    dynamic "Get Offer Names" {
      user -> nginx "GET /api/offerwalls/get_offer_names"
      nginx -> api "Proxy to ASGI"
      api -> controller "Route: /offerwalls/get_offer_names"
      controller -> models "Read OfferChoices.choices"
      controller -> user "200 { 'offer_names': [...] }"
    }

    styles {
      element "External" { background "#bbbbbb" border "#888888" }
      element "Container" { background "#1168bd" color "#ffffff" }
      element "Person" { shape "Person" }
      element "Software System" { background "#438dd5" color "#ffffff" }
      element "Component" { background "#85bb65" color "#000000" }
    }
  }
}
import logging
import sys
from typing import Any, Dict

from litestar import Litestar, Router, Response
from litestar.config.cors import CORSConfig
from litestar.exceptions import NotFoundException
from litestar.openapi import OpenAPIConfig
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from litestar.di import Provide
from app.config import settings
from app.db import get_db_session, init_db
from app.errors import (
    not_found_handler,
    pydantic_validation_error_handler,
    sqlalchemy_error_handler,
)
from app.application.offerwall_service import OfferWallService
from app.routes.offerwalls import OfferWallController
from app.di.providers import provide_offerwall_repository, provide_offerwall_service

# Configure logging
def configure_logging() -> None:
    """Configure the logging for the application."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set log levels for specific loggers
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if settings.echo_sql else logging.WARNING
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configured with level: %s", logging.getLevelName(log_level))

# Call the logging configuration when the module is imported
configure_logging()

cors_config = CORSConfig(allow_origins=settings.allowed_origins)

openapi_config = OpenAPIConfig(
    title="L10nLight API",
    version="1.0.0",
    description="API документация для L10nLight микросервиса",
    contact={
        "name": "API Support",
        "email": "support@example.com",
        "url": "https://example.com/support"
    },
    license={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    tags=[
        {
            "name": "offerwalls",
            "description": "Операции с офферволлами"
        },
        {
            "name": "offers",
            "description": "Операции с предложениями"
        }
    ],
    security=[{"BearerAuth": []}],
    servers=[
        {
            "url": "http://localhost:5000",
            "description": "Development server"
        },
        {
            "url": "https://api.example.com",
            "description": "Production server"
        }
    ]
)

app = Litestar(
    openapi_config=openapi_config,
    route_handlers=[
        Router(
            path="/api",
            route_handlers=[OfferWallController],
            dependencies={"service": Provide(provide_offerwall_service, sync_to_thread=False)},
        )
    ],
    dependencies={
        "db_session": Provide(get_db_session),
        "repo": Provide(provide_offerwall_repository, sync_to_thread=False),
    },
    cors_config=cors_config,
    on_startup=[init_db],
    exception_handlers={
        NotFoundException: not_found_handler,
        ValidationError: pydantic_validation_error_handler,
        SQLAlchemyError: sqlalchemy_error_handler,
    },
)
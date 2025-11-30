from typing import Any
from litestar import Response
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from litestar.exceptions import NotFoundException
from litestar.response import Response
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

def not_found_handler(_request: Any, exc: NotFoundException) -> Response[dict[str, Any]]:
    return Response(content={"detail": "Not found."}, status_code=404)

def pydantic_validation_error_handler(_request: Any, exc: ValidationError) -> Response[dict[str, Any]]:
    return Response(content={"detail": str(exc)}, status_code=400)

def sqlalchemy_error_handler(_request: Any, exc: SQLAlchemyError) -> Response[dict[str, Any]]:
    return Response(content={"detail": "Database error", "error": str(exc)}, status_code=500)

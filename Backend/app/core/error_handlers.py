import logging
import sqlite3

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("cliniccare.api")


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning("HTTP %s for %s: %s", exc.status_code, request.url.path, exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(sqlite3.IntegrityError)
    async def integrity_error_handler(request: Request, exc: sqlite3.IntegrityError):
        logger.warning("Integrity error for %s: %s", request.url.path, exc)
        return JSONResponse(status_code=409, content={"detail": "Data conflicts with existing records"})

    @app.exception_handler(sqlite3.DatabaseError)
    async def database_error_handler(request: Request, exc: sqlite3.DatabaseError):
        logger.exception("Database error for %s", request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Database error"})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled server error for %s", request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

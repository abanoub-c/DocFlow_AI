"""Builds the FastAPI app and registers module routers. No business logic here."""
import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.modules.auth.router import router as auth_router
from src.modules.documents.router import router as documents_router
from src.modules.exports.router import router as exports_router
from src.modules.metrics.router import router as metrics_router
from src.modules.review.router import router as review_router
from src.platform.config import get_settings
from src.platform.errors import AppError

settings = get_settings()
logger = logging.getLogger("docflow")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logger.info("starting %s v%s (%s)", settings.app_name, settings.version, settings.environment)
    # TODO: create DB engine / check connection
    # TODO: optional in-process worker (for hosts with no background workers)
    yield
    logger.info("shutting down")
    # TODO: dispose DB engine, stop in-process worker


def _error_body(request: Request, code: str, message: str, details=None) -> dict:
    body = {
        "error": {
            "code": code,
            "message": message,
            "request_id": getattr(request.state, "request_id", None),
        }
    }
    if details is not None:
        body["error"]["details"] = details
    return body


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="Invoice and receipt extraction with validation and human review.",
        lifespan=lifespan,
        # Hide interactive docs in production if you prefer:
        # docs_url=None if settings.environment == "production" else "/docs",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        request.state.request_id = request_id
        start = time.perf_counter()
        response = await call_next(request)
        ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        # Log method + path + status only: never bodies or query strings (PII).
        logger.info(
            "%s %s -> %s (%.0f ms) request_id=%s",
            request.method, request.url.path, response.status_code, ms, request_id,
        )
        return response

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(request, exc.code, exc.message),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        details = [
            {"field": ".".join(str(p) for p in e["loc"]), "message": e["msg"]}
            for e in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content=_error_body(request, "validation_error", "Invalid request", details),
        )

    @app.get("/health", tags=["system"])
    async def health():
        # TODO: add dependency checks (database, storage) and return 503 if any fail
        return {
            "status": "ok",
            "version": settings.version,
            "environment": settings.environment,
        }

    app.include_router(auth_router)
    app.include_router(documents_router)
    app.include_router(review_router)
    app.include_router(exports_router)
    app.include_router(metrics_router)
    return app


app = create_app()
"""AllFix application entry point.

Run locally:  python -m allfix            (or: uvicorn allfix.main:app)
Load knowledge: python -m allfix load-knowledge
"""

from __future__ import annotations

import base64
import logging
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from . import db
from .api.routes import router
from .config import get_settings
from .knowledge import loader
from .strategist import ApiStrategist, make_strategist

log = logging.getLogger("allfix")


def create_app(model_client_factory=None, load_knowledge: bool = True, strategist=None) -> FastAPI:
    """model_client_factory: use the API backend with this client (tests). strategist: any backend."""
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await db.open_pool()
        applied = await db.migrate()
        if applied:
            log.info("applied migrations: %s", applied)
        if load_knowledge and settings.knowledge_dir.exists():
            counts = await loader.load(settings.knowledge_dir)
            log.info("knowledge loaded: %s", counts)
        yield
        await db.close_pool()

    app = FastAPI(title="AllFix", lifespan=lifespan)
    if strategist is None:
        strategist = ApiStrategist(model_client_factory) if model_client_factory else make_strategist()
    app.state.strategist = strategist

    if settings.allfix_password:
        expected = settings.allfix_password

        @app.middleware("http")
        async def basic_auth(request: Request, call_next):
            header = request.headers.get("authorization", "")
            ok = False
            if header.startswith("Basic "):
                try:
                    _, _, pw = base64.b64decode(header[6:]).decode().partition(":")
                    ok = secrets.compare_digest(pw, expected)
                except Exception:
                    ok = False
            if not ok:
                return Response(status_code=401, headers={"WWW-Authenticate": 'Basic realm="AllFix"'})
            return await call_next(request)

    app.include_router(router)

    dist = settings.frontend_dist
    if dist.exists():
        app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        async def spa(path: str):
            if path.startswith("api/"):
                return JSONResponse({"detail": "not found"}, status_code=404)
            candidate = dist / path
            if path and candidate.is_file() and dist in candidate.resolve().parents:
                return FileResponse(candidate)
            return FileResponse(dist / "index.html")

    return app


app = create_app()

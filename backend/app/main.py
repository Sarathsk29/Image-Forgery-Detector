from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routers import analyses, cases, health
from app.core.config import get_settings
from app.db.session import init_db


settings = get_settings()
Path(settings.local_storage_dir).mkdir(parents=True, exist_ok=True)
Path(settings.local_artifact_dir).mkdir(parents=True, exist_ok=True)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allow_origin.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(health.router, prefix=settings.api_v1_prefix, tags=["health"])
app.include_router(cases.router, prefix=settings.api_v1_prefix, tags=["cases"])
app.include_router(analyses.router, prefix=settings.api_v1_prefix, tags=["analyses"])

app.mount("/storage/uploads", StaticFiles(directory=settings.local_storage_dir), name="uploads")
app.mount("/storage/artifacts", StaticFiles(directory=settings.local_artifact_dir), name="artifacts")


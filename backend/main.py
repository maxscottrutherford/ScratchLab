from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from middleware.auth import AuthMiddleware
from routers import ai, analytics, courses, health, holes, rounds

settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)

# CORS must wrap auth so preflight OPTIONS requests get headers before JWT checks.
app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(rounds.router)
app.include_router(holes.router)
app.include_router(ai.router)
app.include_router(analytics.router)
app.include_router(courses.router)

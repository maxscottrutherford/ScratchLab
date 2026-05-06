from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

# Load monorepo root `.env` when present (same keys as root `.env.example`)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Server-side Supabase: use `SUPABASE_SECRET_KEY` only here or other backend code — never in mobile/web clients.

app = FastAPI(title="ScratchLab API")


@app.get("/health")
def health():
    return {"status": "ok"}

"""
Auth middleware and user dependency.

Session validation uses Supabase Auth GET /auth/v1/user with:
  - Authorization: Bearer <user JWT>
  - apikey: SUPABASE_SECRET_KEY (service role)

The service role key must be sent as `apikey` for Supabase REST/Auth; it is not the
HMAC secret used to decode JWTs locally. Never use SUPABASE_PUBLISHABLE_KEY on this
backend — only the secret key for server-side calls.
"""

from __future__ import annotations

from typing import Awaitable, Callable

import httpx
from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from config import get_settings
from database import get_supabase_admin
from models.user import User

PUBLIC_PATHS = frozenset(
    {
        "/",
        "/health",
        "/openapi.json",
        "/docs",
        "/redoc",
    }
)


class AuthError(Exception):
    pass


async def fetch_supabase_user(access_token: str) -> dict:
    settings = get_settings()
    base = str(settings.supabase_url).rstrip("/")
    url = f"{base}/auth/v1/user"
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(
            url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "apikey": settings.supabase_secret_key,
            },
        )
    if response.status_code != 200:
        raise AuthError("Invalid or expired token")
    return response.json()


class AuthMiddleware(BaseHTTPMiddleware):
    """Validates Supabase access tokens for non-public routes and sets `request.state`."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path
        if path in PUBLIC_PATHS or path.startswith("/docs/") or path.startswith("/redoc/"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"detail": "Missing or invalid Authorization header"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        token = auth_header.removeprefix("Bearer ").strip()
        if not token:
            return JSONResponse(
                {"detail": "Missing bearer token"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            payload = await fetch_supabase_user(token)
        except AuthError:
            return JSONResponse(
                {"detail": "Could not validate credentials"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        except httpx.HTTPError:
            return JSONResponse(
                {"detail": "Auth service unavailable"},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        user_id = payload.get("id")
        if not user_id:
            return JSONResponse(
                {"detail": "Invalid auth payload"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        request.state.user_id = user_id
        request.state.auth_payload = payload
        return await call_next(request)


async def get_current_user(request: Request) -> User:
    """Load `public.users` for the JWT subject (requires `AuthMiddleware` to have run)."""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    admin = get_supabase_admin()
    result = admin.table("users").select("*").eq("id", str(user_id)).limit(1).execute()
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found",
        )
    return User.model_validate(result.data[0])

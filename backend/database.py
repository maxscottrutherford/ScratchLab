from supabase import Client, create_client

from config import get_settings

_supabase_admin: Client | None = None


def _build_client() -> Client:
    settings = get_settings()
    url = str(settings.supabase_url).rstrip("/")
    return create_client(url, settings.supabase_secret_key)


def get_supabase_admin() -> Client:
    """Return a singleton Supabase client using the service role key (bypasses RLS)."""
    global _supabase_admin
    if _supabase_admin is None:
        _supabase_admin = _build_client()
    return _supabase_admin


# Lazy proxy so importers can use `database.supabase_admin.table(...)` after first use
class _SupabaseAdminProxy:
    def __getattr__(self, name: str):
        return getattr(get_supabase_admin(), name)


supabase_admin = _SupabaseAdminProxy()

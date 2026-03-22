from __future__ import annotations

import os

from dotenv import load_dotenv
from supabase import Client, create_client


_SUPABASE: Client | None = None


def get_supabase() -> Client:
    global _SUPABASE

    if _SUPABASE is not None:
        return _SUPABASE

    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be set in environment variables."
        )

    _SUPABASE = create_client(url, key)
    return _SUPABASE

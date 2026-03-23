from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from supabase import Client, create_client


_SUPABASE: Client | None = None
logger = logging.getLogger(__name__)


def get_supabase() -> Client:
    global _SUPABASE

    if _SUPABASE is not None:
        return _SUPABASE

    load_dotenv()
    try:
        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    except KeyError as exc:
        missing_key = exc.args[0]
        logger.exception("Missing required environment variable: %s", missing_key)
        raise RuntimeError(
            f"Missing required environment variable: {missing_key}. "
            "Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in deployment settings."
        ) from exc

    try:
        _SUPABASE = create_client(url, key)
    except Exception as exc:
        logger.exception("Failed to initialize Supabase client")
        raise RuntimeError("Failed to initialize Supabase client.") from exc

    return _SUPABASE

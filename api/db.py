from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from supabase import Client, create_client


_SUPABASE: Client | None = None
logger = logging.getLogger(__name__)


def _clean_env_value(name: str, value: str | None) -> str:
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    cleaned = value.strip().strip('"').strip("'")
    if not cleaned:
        raise RuntimeError(f"Environment variable {name} is empty")
    return cleaned


def get_supabase() -> Client:
    global _SUPABASE

    if _SUPABASE is not None:
        return _SUPABASE

    load_dotenv()
    try:
        url = _clean_env_value("SUPABASE_URL", os.environ.get("SUPABASE_URL"))

        raw_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if raw_key is None:
            # Backward compatibility for existing deployments still using SUPABASE_KEY.
            logger.warning(
                "SUPABASE_SERVICE_ROLE_KEY not set, falling back to SUPABASE_KEY"
            )
            raw_key = os.environ.get("SUPABASE_KEY")

        key = _clean_env_value("SUPABASE_SERVICE_ROLE_KEY", raw_key)

        if not url.startswith("http://") and not url.startswith("https://"):
            raise RuntimeError("SUPABASE_URL must start with http:// or https://")
    except KeyError as exc:
        missing_key = exc.args[0]
        logger.exception("Missing required environment variable: %s", missing_key)
        raise RuntimeError(
            f"Missing required environment variable: {missing_key}. "
            "Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in deployment settings."
        ) from exc
    except RuntimeError:
        logger.exception("Invalid Supabase environment configuration")
        raise

    try:
        _SUPABASE = create_client(url, key)
    except Exception as exc:
        logger.exception("Failed to initialize Supabase client")
        raise RuntimeError(
            "Failed to initialize Supabase client. "
            "Verify SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are correct and active."
        ) from exc

    return _SUPABASE

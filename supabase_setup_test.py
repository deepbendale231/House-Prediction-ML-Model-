from __future__ import annotations

import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import create_client
import os


def main() -> None:
    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in .env")
        sys.exit(1)

    try:
        client = create_client(supabase_url, supabase_key)
    except Exception as exc:
        print(f"ERROR: Failed to create Supabase client: {exc}")
        sys.exit(1)

    prediction_id: str | None = None

    dummy_features = {
        "longitude": -122.23,
        "latitude": 37.88,
        "housing_median_age": 41.0,
        "total_rooms": 880.0,
        "total_bedrooms": 129.0,
        "population": 322.0,
        "households": 126.0,
        "median_income": 8.3252,
        "ocean_proximity": "NEAR BAY",
    }

    payload = {
        "features": dummy_features,
        "predicted_price": 452600.00,
        "model_version": "v1.0-test",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        insert_resp = client.table("predictions").insert(payload).execute()
        inserted_rows = insert_resp.data or []
        if not inserted_rows:
            raise RuntimeError("Insert returned no rows")

        prediction_id = str(inserted_rows[0].get("id", ""))
        if not prediction_id:
            raise RuntimeError("Insert returned row without id")
    except Exception as exc:
        print(f"ERROR: Insert failed: {exc}")
        sys.exit(1)

    try:
        read_resp = (
            client.table("predictions")
            .select("*")
            .eq("id", prediction_id)
            .limit(1)
            .execute()
        )
        read_rows = read_resp.data or []
        if not read_rows:
            raise RuntimeError(f"Read returned no row for id={prediction_id}")
    except Exception as exc:
        print(f"ERROR: Read failed: {exc}")
        sys.exit(1)

    try:
        delete_resp = client.table("predictions").delete().eq("id", prediction_id).execute()
        deleted_rows = delete_resp.data or []
        if not deleted_rows:
            raise RuntimeError(f"Delete returned no row for id={prediction_id}")
    except Exception as exc:
        print(f"ERROR: Delete failed: {exc}")
        sys.exit(1)

    print("✅ Supabase connection OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Upload the generated sample files into Supabase bucket PDC."""

from __future__ import annotations

import mimetypes
import os
from pathlib import Path

from cloud_config import ACTIVE_CONFIG


def main() -> int:
    if ACTIVE_CONFIG.get("provider") != "supabase":
        print("This script is only for the Supabase configuration.")
        return 1

    try:
        from supabase import create_client
    except Exception as exc:
        print(f"Supabase package not available: {exc}")
        return 1

    sample_dir = Path("sample_files")
    if not sample_dir.exists():
        print("sample_files/ not found. Run: python generate_sample_files.py")
        return 1

    files = sorted(sample_dir.glob("*.txt"))
    if not files:
        print("No sample files found. Run: python generate_sample_files.py")
        return 1

    client = create_client(ACTIVE_CONFIG["url"], ACTIVE_CONFIG["key"])
    bucket = ACTIVE_CONFIG["bucket_name"]

    print(f"Uploading {len(files)} files to Supabase bucket '{bucket}'...\n")

    success_count = 0
    for index, path in enumerate(files, start=1):
        content_type = mimetypes.guess_type(path.name)[0] or "text/plain"
        try:
            with path.open("rb") as file_handle:
                client.storage.from_(bucket).upload(
                    path.name,
                    file_handle,
                    file_options={"content-type": content_type},
                )
            print(f"  [{index}/{len(files)}] ✓ {path.name}")
            success_count += 1
        except Exception as exc:
            print(f"  [{index}/{len(files)}] ✗ {path.name}: {exc}")

    print(f"\nDone. Uploaded {success_count}/{len(files)} files.")
    if success_count == len(files):
        print("Now refresh the Vercel /files page.")
        return 0

    print("If uploads failed with RLS errors, run supabase_bucket_setup.sql in the SQL editor first.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
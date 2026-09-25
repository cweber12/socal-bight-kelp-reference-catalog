"""Fetch NDBC standard meteorological year files into data/raw/ndbc_bight_buoys/.

Run:  python src/fetch/ndbc_bight_buoys.py

One file per station, the 2025 calendar-year standard meteorological file each of the five
stations offers. Each file in FILES is downloaded unmodified - the server sends gzip and the
gzip is what lands, never decompressed on the way in - and written beside a manifest carrying
the url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records: content_type, last_modified and etag, null when the server
sends none. data/ is git-ignored and reproducible from this script, which is the record of the
fetch (CONTEXT.md, "Record format"). Standard library only.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "ndbc_bight_buoys"
STDMET = "https://www.ndbc.noaa.gov/data/historical/stdmet"
FILES = (
    f"{STDMET}/46054h2025.txt.gz",
    f"{STDMET}/46053h2025.txt.gz",
    f"{STDMET}/46025h2025.txt.gz",
    f"{STDMET}/46069h2025.txt.gz",
    f"{STDMET}/46086h2025.txt.gz",
)

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = url.rsplit("/", 1)[-1]
    request = urllib.request.Request(url, headers={"User-Agent": f"kelpcatalog/{SOURCE_ID}"})
    with urllib.request.urlopen(request, timeout=180) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    manifest = {
        "url": url,
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "http_status": http_status,
        # What a repeat fetch records, not what it reproduces: Last-Modified moves when
        # the steward updates the file. No content_length - it duplicates bytes.
        "content_type": headers.get("Content-Type"),
        "last_modified": headers.get("Last-Modified"),
        "etag": headers.get("ETag"),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_bytes(body)
    (out_dir / f"manifest_{name}.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    for url in FILES:
        print(json.dumps(fetch(url, OUT_DIR), indent=2))


if __name__ == "__main__":
    main()

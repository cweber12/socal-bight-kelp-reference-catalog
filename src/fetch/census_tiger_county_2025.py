"""Fetch the Census TIGER/Line 2025 county shapefile into data/raw/census_tiger_county_2025/.

Run:  python src/fetch/census_tiger_county_2025.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. The archive is stored as served, still zipped; nothing is extracted.
data/ is git-ignored and reproducible from this script, which is the record of the fetch
(CONTEXT.md, "Record format"). Standard library only.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "census_tiger_county_2025"

# The one file listed at https://www2.census.gov/geo/tiger/TIGER2025/COUNTY/: every county
# and equivalent in the United States, one zipped shapefile. Fetched whole; the Bight
# counties are read out of it at fetch time, never extracted into the repo.
FILES = ("https://www2.census.gov/geo/tiger/TIGER2025/COUNTY/tl_2025_us_county.zip",)

REPO = "https://github.com/cweber12/socal-bight-kelp-reference-catalog"

# Name the catalog and give the steward a way to reach us.
USER_AGENT = f"kelpcatalog/{SOURCE_ID} (+{REPO})"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = url.rsplit("/", 1)[-1]
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=600) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    # A 200 is not enough: an error page served with a 200 must never be stored or
    # manifested as a verified archive. The file is a zip or it is not this file.
    if not body.startswith(b"PK\x03\x04"):
        raise RuntimeError(
            f"{url}: body is not a zip (first bytes {body[:4]!r}, "
            f"Content-Type {headers.get('Content-Type')!r})"
        )
    manifest = {
        "url": url,
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "http_status": http_status,
        # What a repeat fetch records, not what it reproduces: Last-Modified moves when
        # the Bureau re-releases the file. No content_length - it duplicates bytes.
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

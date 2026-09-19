"""Fetch the CDFW Administrative Kelp Beds file geodatabase into data/raw/cdfw_ds3135/.

Run:  python src/fetch/cdfw_ds3135.py

The file is the "Source download (File Geodatabase)" resource of the dataset page at
data.cnra.ca.gov, taken as the server sends it - a zip, never unpacked here. It is written
beside a manifest carrying the url, the time of the fetch, the sha256, the byte count, the
HTTP status and the response headers a repeat fetch records - content_type, last_modified
and etag, null when the server sends none. data/ is git-ignored and reproducible from this
script, which is the record of the fetch (CONTEXT.md, "Record format"). Standard library
only.

A 200 is not enough. A host that answers an error or a challenge page with status 200 would
be hashed and manifested as a VERIFIED fetch with nothing to reveal it, and CONTEXT.md
counts a route exercised, for a record whose tier is FETCHED, only when "its bytes were
taken". ZIP_MAGIC is the four-byte local file header a non-empty zip starts with (PK, then
0x03 0x04), which is what the served Content-Type claims. The 300-second timeout is what
sio_shore_stations.py and sccwrp_b08_rocky_reef.py use for files this size; noaa_oni.py's
120 is the outlier.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "cdfw_ds3135"
FILES = (
    "https://filelib.wildlife.ca.gov/Public/BDB/GIS/BIOS/Public_Datasets/3100_3199/ds3135.zip",
)

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID
ZIP_MAGIC = b"PK\x03\x04"


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = url.rsplit("/", 1)[-1]
    request = urllib.request.Request(url, headers={"User-Agent": f"kelpcatalog/{SOURCE_ID}"})
    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    if not body.startswith(ZIP_MAGIC):
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

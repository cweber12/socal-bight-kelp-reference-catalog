"""Fetch the CDFW Giant Kelp and Bull Kelp Enhanced Status Report into data/raw/cdfw_kelp_esr/.

Run:  python src/fetch/cdfw_kelp_esr.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. This API sends neither Last-Modified nor ETag. data/ is git-ignored
and reproducible from this script, which is the record of the fetch (CONTEXT.md, "Record
format"). Standard library only.

The report is a React single-page application whose HTML is a 2,960-byte shell holding
none of the report text; the text arrives from the API below, one response per report
page, 0 to 6 (catalog/sources/cdfw_kelp_esr.md, `access`). Each URL ends in the page
number and the server sends no Content-Disposition, so the served file name is that
number and each file is stored under it, with its manifest as manifest_<number>.json.

The body check is the JSON counterpart of the %PDF- check in src/fetch/sccwrp_tr1289.py:
a truncated or error-bodied 200 would otherwise be stored, hashed and manifested as a
VERIFIED fetch with nothing to reveal it.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "cdfw_kelp_esr"
API = "https://marinespecies-api.wildlife.ca.gov/api/reports/kelp"
PAGES = (0, 1, 2, 3, 4, 5, 6)
FILES = tuple(f"{API}/{page}" for page in PAGES)
PAYLOAD_KEY = "speciesESRPage"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = url.rsplit("/", 1)[-1]
    request = urllib.request.Request(url, headers={"User-Agent": f"kelpcatalog/{SOURCE_ID}"})
    with urllib.request.urlopen(request, timeout=120) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    payload = json.loads(body.decode("utf-8"))
    if PAYLOAD_KEY not in payload:
        raise SystemExit(f"{url}: {len(body)} bytes of JSON without a {PAYLOAD_KEY} key")
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

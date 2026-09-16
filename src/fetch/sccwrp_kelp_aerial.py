"""Fetch the SCB Regional Aerial Kelp Surveys pages into data/raw/sccwrp_kelp_aerial/.

Run:  python src/fetch/sccwrp_kelp_aerial.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. data/ is git-ignored and reproducible from this script, which is the
record of the fetch (CONTEXT.md, "Record format"). Standard library only.

The URLs are http://, not https://: the host's HTTPS certificate expired on 2026-03-25 and
urllib's default SSL context refuses it, while HTTP serves the same pages with a 200.

Each page must arrive from the URL asked for and carry a marker, a fragment of text the record
quotes from that page, which tells it apart from the other page and from an error or placeholder
page: urllib follows redirects silently, and a parked domain or a CDN default page answers 200, so
without the check a manifest would certify bytes that are not the page. The marker confirms which
page arrived, not that the whole page did.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "sccwrp_kelp_aerial"
FILES = (
    ("http://kelp.sccwrp.org/home.html", b"Region Nine Kelp Survey Consortium (RNKSC)"),
    ("http://kelp.sccwrp.org/reports.html", b"Status of the Kelp Beds, 2016."),
)

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(url: str, marker: bytes, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = url.rsplit("/", 1)[-1]
    request = urllib.request.Request(url, headers={"User-Agent": f"kelpcatalog/{SOURCE_ID}"})
    with urllib.request.urlopen(request, timeout=120) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
        served_url = response.url
    if served_url != url:
        raise SystemExit(f"{url} was served from {served_url}")
    if marker not in body:
        raise SystemExit(f"{url} did not return the page: {len(body)} bytes without {marker!r}")
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
    for url, marker in FILES:
        print(json.dumps(fetch(url, marker, OUT_DIR), indent=2))


if __name__ == "__main__":
    main()

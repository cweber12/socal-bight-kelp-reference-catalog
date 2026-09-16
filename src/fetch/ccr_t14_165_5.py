"""Fetch the full-text page of CCR Title 14 section 165.5 into data/raw/ccr_t14_165_5/.

Run:  python src/fetch/ccr_t14_165_5.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. This host sends neither Last-Modified nor ETag. data/ is git-ignored
and reproducible from this script, which is the record of the fetch (CONTEXT.md, "Record
format"). Standard library only.

The host answers HTTP 403 to urllib's default User-Agent and serves the page to this
script's own (catalog/sources/ccr_t14_165_5.md, `access`). The page carries the line "This
database is current through ...", which moves with the weekly Notice Register, so the
sha256 is expected to change whether or not the section does.

The URL's last path segment is the document id and the server sends no
Content-Disposition, so the page is stored under that id with the query string dropped,
which also keeps "?" out of a Windows file name. Its manifest is manifest_<id>.json.

The URL answers HTTP 301 to itself with query parameters appended, which urllib follows
silently. The page must arrive from that URL or one that extends its query string, and
carry two markers the record quotes: the opening of subsection (k), which tells it apart
from the other section 165.5 link on CDFW's page and from an error page answering 200, and
the last History note, which the page prints after the whole of subsection (k), so a body
cut off inside (k) is refused. The markers confirm which page arrived and that it reaches
past (k), not that every byte did.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE_ID = "ccr_t14_165_5"
FILES = (
    (
        "https://govt.westlaw.com/calregs/Document/IE6B507C0DA8311F08F04978BD7C3021A?viewType=FullText",
        (
            b"(k) Administrative kelp beds are defined as follows",
            b"19. Amendment of subsections (c) and (k)(2)(I) filed 12-9-2025; operative 1-1-2026"
            b" (Register 2025, No. 50).",
        ),
    ),
)

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(url: str, markers: tuple[bytes, ...], out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = urllib.parse.urlsplit(url).path.rsplit("/", 1)[-1]
    request = urllib.request.Request(url, headers={"User-Agent": f"kelpcatalog/{SOURCE_ID}"})
    with urllib.request.urlopen(request, timeout=120) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
        served_url = response.url
    if served_url != url and not served_url.startswith(url + "&"):
        raise SystemExit(f"{url} was served from {served_url}")
    for marker in markers:
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
    for url, markers in FILES:
        print(json.dumps(fetch(url, markers, OUT_DIR), indent=2))


if __name__ == "__main__":
    main()

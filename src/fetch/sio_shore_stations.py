"""Fetch the Shore Stations Program station archives into data/raw/sio_shore_stations/.

Run:  python src/fetch/sio_shore_stations.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. Archives are stored as served, still zipped. data/ is git-ignored and
reproducible from this script, which is the record of the fetch (CONTEXT.md, "Record
format"). Standard library only.

Every URL ends in /download, so the served file name comes from the Content-Disposition
header rather than the URL path; the manifest is named for it whole, extension included.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

SOURCE_ID = "sio_shore_stations"

# The first-listed component of the five station objects in collection
# https://library.ucsd.edu/dc/collection/bb4719748r whose stated coordinates put them
# inside the Bight as CONTEXT.md defines it - Point Conception south to the US-Mexico
# border. The collection's other five stations (Granite Canyon 36.44 N, Pacific Grove
# 36.62 N, Farallon Islands 37.70 N, Trinidad Beach 41.06 N, Trinidad Bay 41.06 N) lie
# north of Point Conception and are not fetched here; each station's latitude is printed
# in the header block of its own CSVs.
FILES = (
    "https://library.ucsd.edu/dc/object/bb07606686/_1_1.zip/download",  # Santa Barbara 34.40 N
    "https://library.ucsd.edu/dc/object/bb5914297b/_1_1.zip/download",  # Point Dume 34.02 N
    "https://library.ucsd.edu/dc/object/bb1067837x/_1_1.zip/download",  # Newport Beach 33.61 N
    "https://library.ucsd.edu/dc/object/bb8849478k/_1_1.zip/download",  # San Clemente 33.42 N
    "https://library.ucsd.edu/dc/object/bb4003017c/_1_1.zip/download",  # La Jolla 32.87 N
)

REPO = "https://github.com/cweber12/socal-bight-kelp-reference-catalog"

# Name the catalog and give the steward a way to reach us.
USER_AGENT = f"kelpcatalog/{SOURCE_ID} (+{REPO})"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    # A 200 is not enough: this host answers browser-like clients with an HTML
    # challenge page. Never store or manifest one as a verified archive.
    if not body.startswith(b"PK\x03\x04"):
        raise RuntimeError(
            f"{url}: body is not a zip (first bytes {body[:4]!r}, "
            f"Content-Type {headers.get('Content-Type')!r})"
        )
    # Every URL ends in /download, so the served name is in Content-Disposition and
    # there is no usable fallback: the URL path would name every file "download" and
    # each archive would overwrite the last. Refuse rather than guess.
    served = headers.get_filename()
    if not served:
        raise RuntimeError(f"{url}: no Content-Disposition filename; refusing to guess one")
    # get_filename() sanitises nothing, and the value is server-supplied.
    name = Path(served).name
    if name in ("", ".", ".."):
        raise RuntimeError(f"{url}: unusable served file name {served!r}")
    manifest = {
        "url": url,
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "http_status": http_status,
        # What a repeat fetch records, not what it reproduces: this host stamps
        # Last-Modified with the time it built the response. No content_length - it
        # duplicates bytes.
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
    # A failure part-way through leaves some archives on disk and others missing,
    # with nothing to mark the directory incomplete. Fetch what can be fetched,
    # then name every failure and exit non-zero.
    failures: list[tuple[str, Exception]] = []
    for url in FILES:
        try:
            print(json.dumps(fetch(url, OUT_DIR), indent=2))
        except Exception as exc:  # noqa: BLE001 - every failure is reported below
            failures.append((url, exc))
            print(f"FAILED {url}: {exc}", file=sys.stderr)
    if failures:
        print(
            f"\n{len(failures)} of {len(FILES)} files did not fetch; {OUT_DIR} is incomplete:",
            file=sys.stderr,
        )
        for url, exc in failures:
            print(f"  {url}: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

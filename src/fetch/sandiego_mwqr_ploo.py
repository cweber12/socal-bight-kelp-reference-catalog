"""Fetch the City of San Diego's 2026 PLOO monthly reports into data/raw/<SOURCE_ID>/.

Run:  python src/fetch/sandiego_mwqr_ploo.py

FILES holds the eight URLs the City's monthly water quality reports page
https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports/monthly-report-archives
links under its heading "2026 Monthly Receiving Waters Monitoring Reports for the PLOO" (the
page prints U+00A0 between "2026" and "Monthly"), in the
order it lists them, January to August; the page prints them as relative hrefs under
/sites/default/files/ and the files are on the same host, www.sandiego.gov. The record does not
hold the files the page lists under "PLOO Monthly Receiving Waters Monitoring Report Archives".
What the record states about that route is in catalog/sources/sandiego_mwqr_ploo.md: each
report's PDF page 3 is a letter headed "Public Utilities Department", and the page links "Public
Utilities Home", https://www.sandiego.gov/public-utilities, which the record's access walks to
and quotes.

Each file is downloaded unmodified and written beside a manifest carrying the url, the time of the
fetch, the sha256, the byte count, the HTTP status and the response headers a repeat fetch records
- content_type, last_modified and etag, null when the server sends none. data/ is git-ignored and
reproducible from this script, which is the record of the fetch (CONTEXT.md, "Record format").
Standard library only.

The body check follows sccwrp_kelp_status_2016.py: a truncated or error-bodied 200 would otherwise
be stored, hashed and manifested as a VERIFIED fetch with nothing to reveal it. %PDF- is the
signature the served Content-Type, application/pdf, claims.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "sandiego_mwqr_ploo"
BASE = "https://www.sandiego.gov/sites/default/files/"
FILES = tuple(
    f"{BASE}{folder}/ploo_mwqr_{month}_2026.pdf"
    for folder, month in (
        ("2026-02", "jan"),
        ("2026-03", "feb"),
        ("2026-04", "mar"),
        ("2026-05", "apr"),
        ("2026-07", "may"),
        ("2026-07", "jun"),
        ("2026-08", "jul"),
        ("2026-09", "aug"),
    )
)
PDF_MAGIC = b"%PDF-"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = url.rsplit("/", 1)[-1]
    request = urllib.request.Request(url, headers={"User-Agent": f"kelpcatalog/{SOURCE_ID}"})
    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    if not body.startswith(PDF_MAGIC):
        raise SystemExit(f"{url} did not return a PDF: body starts {body[:16]!r}")
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

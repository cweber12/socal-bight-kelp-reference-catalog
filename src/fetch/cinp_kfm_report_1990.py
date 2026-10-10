"""Fetch the Channel Islands kelp forest monitoring 1990 annual report into data/raw/<SOURCE_ID>/.

Run:  python src/fetch/cinp_kfm_report_1990.py

FILES holds the one URL the NPS DataStore lists for reference 68419,
https://irma.nps.gov/DataStore/Reference/Profile/68419, the entry of saved search 1508 titled
"Kelp Forest Monitoring, Channel Islands National Park: 1990 Annual Report". The holding is
485218, and POST /DataStore/Reference/GetHoldings with referenceId=68419&id=68419 gives its Url,
its FileDescription "chis_kelp90.pdf" and its FileSize 306257. What the record states about that
route is in catalog/sources/cinp_kfm_report_1990.md.

The URL's last segment is the holding id, so the file is stored under the name the response's
Content-Disposition gives it, and its manifest is manifest_<that name>.json. Each file is
downloaded unmodified and written beside a manifest carrying the url, the time of the fetch, the
sha256, the byte count, the HTTP status and the response headers a repeat fetch records -
content_type, last_modified and etag, null when the server sends none; this host sends neither
Last-Modified nor ETag. data/ is git-ignored and reproducible from this script, which is the record
of the fetch (CONTEXT.md, "Record format"). Standard library only.

The DataStore answers a holding it will not serve anonymously with HTTP 200 and its own home page
(catalog/sources/cinp_kfm.md, access), so a 200 proves nothing here. The body is kept only when it
begins with %PDF-, arrives under the file name the holding states, and is the size the holding
states.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "cinp_kfm_report_1990"
# (url, the holding's FileDescription, the holding's FileSize)
FILES = (("https://irma.nps.gov/DataStore/DownloadFile/485218", "chis_kelp90.pdf", 306257),)
PDF_MAGIC = b"%PDF-"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(url: str, expected_name: str, expected_size: int, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    request = urllib.request.Request(url, headers={"User-Agent": f"kelpcatalog/{SOURCE_ID}"})
    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    if not body.startswith(PDF_MAGIC):
        raise SystemExit(f"{url} did not return a PDF: body starts {body[:16]!r}")
    # get_filename() sanitises nothing, and the value is server-supplied.
    name = headers.get_filename()
    if name != expected_name:
        raise SystemExit(f"{url} named {name!r}, not the holding's {expected_name!r}")
    if len(body) != expected_size:
        raise SystemExit(f"{url} served {len(body)} bytes, not the holding's {expected_size}")
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
    for url, name, size in FILES:
        print(json.dumps(fetch(url, name, size, OUT_DIR), indent=2))


if __name__ == "__main__":
    main()

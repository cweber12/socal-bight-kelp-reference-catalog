"""Fetch the 2016 Status of the Kelp Beds report into data/raw/sccwrp_kelp_status_2016/.

Run:  python src/fetch/sccwrp_kelp_status_2016.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. data/ is git-ignored and reproducible from this script, which is the
record of the fetch (CONTEXT.md, "Record format"). Standard library only.

The body check follows sccwrp_b08_rocky_reef.py: a truncated or error-bodied 200 would
otherwise be stored, hashed and manifested as a VERIFIED fetch with nothing to reveal it.
%PDF- is the signature the served Content-Type claims.

The URL is http://, not https://: sccwrp_kelp_aerial's access records the host's HTTPS
certificate refused as expired. The file name holds a literal space, sent as %20; the file
is written under the name with the space restored, which is the name the host serves.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE_ID = "sccwrp_kelp_status_2016"
FILES = (
    "http://kelp.sccwrp.org/2016/"
    "Status_of_the_Kelp_Beds_2016_Ventura_Los%20Angeles_Orange_and_San_Diego_Counties.pdf",
)
PDF_MAGIC = b"%PDF-"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = urllib.parse.unquote(url.rsplit("/", 1)[-1])
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

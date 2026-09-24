"""Fetch the La Jolla cross-shore biogeochemistry CSV into data/raw/bcodmo_839175/.

Run:  python src/fetch/bcodmo_839175.py

The route is CONTEXT.md's second FETCHED limb, "a route the steward names as where the
source is to be had": the dataset's own authors state, under "Data availability" in
Kekuewa et al. 2022 (https://doi.org/10.1038/s41598-022-21831-y), which the BCO-DMO page
lists under "Related Publications" as a "Results" publication, "Data analyzed for this
study are available at BCO-DMO https://www.bco-dmo.org/dataset/839175." FILES holds the
URL that page prints for its one data file; the request is answered with HTTP 307 to a
presigned s3.amazonaws.com URL whose X-Amz-Date and X-Amz-Signature follow the second in
which the request is made, so the manifest records the URL requested, not the one that
served the bytes.

The file is written unmodified beside a manifest carrying the url, the time of the fetch,
the sha256, the byte count, the HTTP status and the response headers a repeat fetch
records - content_type, last_modified and etag, null when the server sends none. data/ is
git-ignored and reproducible from this script, which is the record of the fetch
(CONTEXT.md, "Record format"). Standard library only.

A 200 is not enough. A host that answers an error or a challenge page with status 200
would be hashed and manifested as a VERIFIED fetch with nothing to reveal it, and
CONTEXT.md counts a route exercised, for a record whose tier is FETCHED, only when "its
bytes were taken". STATED_MD5 is the checksum the dataset's Metadata HTML page states for
this file under "Data Files", and COLUMNS the twenty parameters its "Parameters" table
names, in order; the body is kept only when its MD5 is that one and its first line is
those columns.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "bcodmo_839175"
FILES = ("https://datadocs.bco-dmo.org/dataset/839175/file/933joGWHMjQER5/la_jolla_biogeochem.csv",)

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID

# https://www.bco-dmo.org/dataset/839175/description, "Data Files": "MD5:efa50...".
STATED_MD5 = "efa50ab1f2df08d0d434f3c8a193abbf"
# The same page's "Parameters" table, its Parameter column top to bottom.
COLUMNS = (
    "Sample,Station,Date,Time,ISO_DateTime_UTC,Lat,Long,Depth,Temp,Salinity,"
    "DO,DIC,TA,pH,Ar,NO3,PO4,SIL,NO2,NH3"
)


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = url.rsplit("/", 1)[-1]
    request = urllib.request.Request(url, headers={"User-Agent": f"kelpcatalog/{SOURCE_ID}"})
    with urllib.request.urlopen(request, timeout=120) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    digest = hashlib.md5(body).hexdigest()
    if digest != STATED_MD5:
        raise RuntimeError(f"{url}: MD5 {digest}, the page states {STATED_MD5}")
    first_line = body.split(b"\n", 1)[0].decode("ascii").strip()
    if first_line != COLUMNS:
        raise RuntimeError(f"{url}: first line is {first_line!r}, not the parameters table's")
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

"""Fetch the SeapHOx La Jolla kelp forest mooring CSV into data/raw/bcodmo_3638/.

Run:  python src/fetch/bcodmo_3638.py

The route is read as CONTEXT.md's second FETCHED limb, "a route the steward names as where
the source is to be had", and the access steps of catalog/sources/bcodmo_3638.md state what
that reading rests on: the dataset's Metadata HTML page states under "BCO-DMO Processing
Notes" that the data file was "Generated from original files "SeapOHx_Mooring [A-D].txt"
contributed by Christina Frieder", the Contact the landing page names at University of
California-San Diego Scripps, and BCO-DMO's Terms of Use state what submitting data to it
means. The related publication the page names states no data repository, so no statement
of the steward's own names this host - bcodmo_839175's route rests on one, and this one
does not. FILES holds the URL the page prints for its one data file; the request is
answered with HTTP 307 to a presigned s3.amazonaws.com URL whose X-Amz-Date and
X-Amz-Signature follow the second in which the request is made, so the manifest records
the URL requested, not the one that served the bytes.

The file is written unmodified beside a manifest carrying the url, the time of the fetch,
the sha256, the byte count, the HTTP status and the response headers a repeat fetch
records - content_type, last_modified and etag, null when the server sends none. data/ is
git-ignored and reproducible from this script, which is the record of the fetch
(CONTEXT.md, "Record format"). Standard library only.

A 200 is not enough. A host that answers an error or a challenge page with status 200
would be hashed and manifested as a VERIFIED fetch with nothing to reveal it, and
CONTEXT.md counts a route exercised, for a record whose tier is FETCHED, only when "its
bytes were taken". STATED_MD5 is the checksum the dataset's Metadata HTML page states for
this file under "Data Files", and COLUMNS the fifteen parameters its "Parameters" table
names; the body is kept only when its MD5 is that one and its first line names exactly
those fifteen, each once. The order is not checked: the file's header runs
Mooring_Id, Site_Description, Latitude, Longitude, ... where the table runs Mooring_Id,
Longitude, Latitude, Start_Date, ..., and the record's format field states both.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "bcodmo_3638"
FILES = ("https://datadocs.bco-dmo.org/dataset/3638/file/yppz4EZUyA21Z3/MOORING_DATA.csv",)

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID

# https://www.bco-dmo.org/dataset/3638/description, "Data Files": "MD5:105d7...".
STATED_MD5 = "105d7464cbc86f32a3e5bb6ff72075cf"
# The same page's "Parameters" table, its Parameter column top to bottom.
COLUMNS = frozenset(
    (
        "Mooring_Id,Longitude,Latitude,Start_Date,End_Date,Site_Description,Water_Depth,"
        "Sensor_ID,Deployment_No,Date,Time,Temperature,Salinity,Oxygen,pH"
    ).split(",")
)


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    name = url.rsplit("/", 1)[-1]
    request = urllib.request.Request(url, headers={"User-Agent": f"kelpcatalog/{SOURCE_ID}"})
    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    digest = hashlib.md5(body).hexdigest()
    if digest != STATED_MD5:
        raise RuntimeError(f"{url}: MD5 {digest}, the page states {STATED_MD5}")
    first_line = body.split(b"\n", 1)[0].decode("ascii").strip()
    header = first_line.split(",")
    if len(header) != len(COLUMNS) or set(header) != COLUMNS:
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

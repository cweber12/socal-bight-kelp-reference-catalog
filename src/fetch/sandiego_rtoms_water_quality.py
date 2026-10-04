"""Fetch the City of San Diego RTOMS water quality CSVs into data/raw/<SOURCE_ID>/.

Run:  python src/fetch/sandiego_rtoms_water_quality.py

FILES holds the eight download URLs the landing page
https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-water-quality/ prints under "Get
the data", in the order it lists them, which is also the order of the eight distribution entries
for identifier monitoring_ocean_rtoms_water_quality in the portal's DCAT catalog
https://raw.githubusercontent.com/COSD-PANDA/data-inventory/refs/heads/master/data.json. The files
are on seshat.datasd.org. What the source states about that route is quoted in the record's fourth
access step (catalog/sources/sandiego_rtoms_water_quality.md): the portal's Terms of Use,
https://data.sandiego.gov/help/guides/terms/, say the City makes datasets available for download
through the portal and define Data as data available for download through DataSD.org or
data.sandiego.gov, and the landing page itself prints the eight links.

Each file is downloaded unmodified and written beside a manifest carrying the url, the time of the
fetch, the sha256, the byte count, the HTTP status and the response headers a repeat fetch records
- content_type, last_modified and etag, null when the server sends none. data/ is git-ignored and
reproducible from this script, which is the record of the fetch (CONTEXT.md, "Record format").
Standard library only.

A 200 is not enough. A host that answers an error page with status 200 would be hashed and
manifested as a VERIFIED fetch with nothing to reveal it. HEADER is the nine fields of the data
dictionary the DCAT entry's describedBy names and the page links as "Download dictionary",
https://seshat.datasd.org/monitoring_ocean_rtoms/rtoms_dictionary_datasd.csv, in the order that
file lists them; a body is kept only when its Content-Type begins text/csv and its first line is
exactly that header.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
from pathlib import Path

SOURCE_ID = "sandiego_rtoms_water_quality"
BASE = "https://seshat.datasd.org/monitoring_ocean_rtoms_water_quality/"
FILES = tuple(
    f"{BASE}{outfall}_water_quality_{year}_datasd.csv"
    for year in ("2023", "2022", "2021", "2020")
    for outfall in ("PLOO", "SBOO")
)

# The "field" column of rtoms_dictionary_datasd.csv, top to bottom.
HEADER = (
    "project,Deployment#,unixtime_1000_gmt,datetime_pst,depth_m,parameter,units,value,"
    "qualifier_flag"
)

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
    content_type = headers.get("Content-Type") or ""
    if not content_type.startswith("text/csv"):
        raise RuntimeError(f"{url}: Content-Type {content_type!r}, not text/csv")
    first_line = body.split(b"\n", 1)[0].decode("ascii").rstrip("\r")
    if first_line != HEADER:
        raise RuntimeError(f"{url}: first line is {first_line!r}, not the dictionary's fields")
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

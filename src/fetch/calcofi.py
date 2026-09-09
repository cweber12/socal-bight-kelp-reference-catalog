"""Fetch CalCOFI station 93.3 28.0 hydrographic data into data/raw/calcofi/.

Run:  python src/fetch/calcofi.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. data/ is git-ignored and reproducible from this script, which is the
record of the fetch (CONTEXT.md, "Record format"). Standard library only.

FILES is built from a query template, not a fixed list of file URLs: the CalCOFI Bottle
Database is served whole by calcofi.org and one station at a time by ERDDAP, and this
record holds one station. Each URL is a tabledap request for every variable of one table,
constrained to a single sta_id. ERDDAP requires every constraint to be preceded by '&',
so the query begins '?&'; with no variable list before it, all variables are returned.

Naming. A query URL's path is the same for every query on a dataset, so the URL path
cannot name the file: two stations would both be written as siocalcofiHydroCast.csv and
the second would overwrite the first. ERDDAP answers with a Content-Disposition whose
file name carries a suffix derived from the query - the same query gives the same name
on a repeat fetch, and a different query a different name - so the served name is taken
from that header, as it is for sio_shore_stations.

That trades one hazard for its opposite, and BOTH are handled here. Silent overwrite:
the suffix hashes the query alone, so two tables constrained alike differ only by the
dataset prefix, and `taken` refuses a second file that would land on the first. Silent
accumulation: because the names are query-derived rather than fixed, editing STATION -
or a server upgrade changing how ERDDAP derives the suffix - makes a re-run write new
files BESIDE the old ones instead of over them, leaving a directory whose contents no
longer say which files this script fetched. So a run that fetched everything prunes what
it did not write. A run with any failure prunes nothing: the fetched files are still
wanted, and there is no complete set to prune against.
"""

from __future__ import annotations

import csv
import datetime as dt
import email.message
import hashlib
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE_ID = "calcofi"

ERDDAP = "https://oceanview.pfeg.noaa.gov/erddap/tabledap"

# CalCOFI line 93.3 station 28.0, spelled as the data spell it: sta_id is zero-padded to
# "[Line] [Station]" (Bottle Database Code Definitions, Sta_ID). CalCOFI's Station
# Positions page gives the station as Lat (dec) 32.91304, Lon (dec) -117.39438, which is
# between Point Conception and the US-Mexico border - the Bight, as CONTEXT.md defines it.
STATION = "093.3 028.0"

# The two tables of the Bottle Database, as the Bottle Database page names them: "The Cast
# table contains metadata." and "The Bottle table contains oceanographic data." No other
# CalCOFI dataset is fetched.
DATASETS = ("siocalcofiHydroCast", "siocalcofiHydroBottle")

# sta_id="093.3 028.0" percent-encoded: the quotes ERDDAP requires around a string value
# and the space inside the id both have to survive the URL.
STATION_CONSTRAINT = "&sta_id=" + urllib.parse.quote('"' + STATION + '"')

FILES = tuple(f"{ERDDAP}/{dataset}.csv?{STATION_CONSTRAINT}" for dataset in DATASETS)

REPO = "https://github.com/cweber12/socal-bight-kelp-reference-catalog"

# Name the catalog and give the steward a way to reach us.
USER_AGENT = f"kelpcatalog/{SOURCE_ID} (+{REPO})"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def served_name(headers: email.message.Message, url: str) -> str:
    """The file name the server gave, refusing anything unusable rather than guessing."""
    served = headers.get_filename()
    if not served:
        raise RuntimeError(f"{url}: no Content-Disposition filename; refusing to guess one")
    # get_filename() sanitises nothing, and the value is server-supplied. Report the
    # value as served, not the sanitised one: Path(".").name and Path("/").name are both
    # "", which would tell the operator nothing about what ERDDAP actually sent.
    name = Path(served).name
    if name in ("", ".", ".."):
        raise RuntimeError(f"{url}: unusable served file name {served!r}")
    return name


def check_csv(body: bytes, url: str) -> None:
    """Refuse a 200 that is not the whole CSV that was asked for.

    ERDDAP reports a bad query with an HTTP error status - a constraint missing its '&'
    or an unknown variable gives 400, a constraint matching no rows or an unknown
    datasetID gives 404 - and urlopen raises HTTPError on all of them, so those never
    reach this function. What does reach it is a 200 whose body is not what was ordered.
    tabledap streams its rows after the 200 and the Content-Type are already on the wire
    and sends no Content-Length, so a run that dies mid-stream can still complete the
    HTTP message, with the rows it managed and an error appended. A dropped connection
    raises IncompleteRead in urlopen, but that completed-but-short case does not: it
    would be stored, hashed and manifested as a verified fetch, and the record's row
    counts would quietly stop describing the file on disk.

    Every row of a tabledap CSV carries the same field count as its column-name row, so a
    truncated final row or an appended error line is a row of the wrong width.
    """
    rows = [r for r in csv.reader(io.StringIO(body.decode("ISO-8859-1"))) if r]
    if len(rows) < 3:
        raise RuntimeError(
            f"{url}: expected a name row, a units row and data, got {len(rows)} rows"
        )
    header = rows[0]
    if "sta_id" not in header:
        raise RuntimeError(f"{url}: no sta_id column in the name row {header[:6]}")
    ragged = [i for i, row in enumerate(rows) if len(row) != len(header)]
    if ragged:
        raise RuntimeError(
            f"{url}: {len(ragged)} row(s) do not have the name row's {len(header)} fields "
            f"(first at row {ragged[0]}: {rows[ragged[0]][:3]}); response is truncated or "
            f"carries an appended error"
        )


def fetch(url: str, out_dir: Path, taken: dict[str, str]) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    # A 200 is not enough. Content-Type first, which catches a host answering a
    # browser-like client with an HTML challenge page, then the body itself.
    content_type = headers.get("Content-Type")
    if not (content_type or "").startswith("text/csv"):
        raise RuntimeError(
            f"{url}: Content-Type is {content_type!r}, not text/csv (first bytes {body[:60]!r})"
        )
    check_csv(body, url)
    name = served_name(headers, url)
    if name in taken:
        raise RuntimeError(f"{url}: served name {name!r} already written by {taken[name]}")
    taken[name] = url
    manifest = {
        "url": url,
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "http_status": http_status,
        # What a repeat fetch records, not what it reproduces: this host stamps
        # Last-Modified with the time it built the response. No content_length - it
        # duplicates bytes.
        "content_type": content_type,
        "last_modified": headers.get("Last-Modified"),
        "etag": headers.get("ETag"),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_bytes(body)
    (out_dir / f"manifest_{name}.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def prune(out_dir: Path, keep: set[str]) -> list[str]:
    """Delete files this run did not write, so the directory holds exactly FILES."""
    removed = []
    for path in sorted(out_dir.iterdir()):
        if path.is_file() and path.name not in keep:
            path.unlink()
            removed.append(path.name)
    return removed


def main() -> None:
    # A failure part-way through leaves one table on disk and the other missing, with
    # nothing to mark the directory incomplete. Fetch what can be fetched, then name
    # every failure and exit non-zero.
    taken: dict[str, str] = {}
    failures: list[tuple[str, Exception]] = []
    for url in FILES:
        try:
            print(json.dumps(fetch(url, OUT_DIR, taken), indent=2))
        except Exception as exc:  # noqa: BLE001 - every failure is reported below
            failures.append((url, exc))
            print(f"FAILED {url}: {exc}", file=sys.stderr)
    if failures:
        print(
            f"\n{len(failures)} of {len(FILES)} files did not fetch; {OUT_DIR} is incomplete "
            f"and nothing was pruned:",
            file=sys.stderr,
        )
        for url, exc in failures:
            print(f"  {url}: {exc}", file=sys.stderr)
        raise SystemExit(1)
    keep = set(taken) | {f"manifest_{name}.json" for name in taken}
    for name in prune(OUT_DIR, keep):
        print(f"pruned {name}: not written by this run")


if __name__ == "__main__":
    main()

"""Fetch the CUGN Spray glider deployment sp030-20260701T1719 into data/raw/cugn_sp030_20260701/.

Run:  python src/fetch/cugn_sp030_20260701.py

The one file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. data/ is git-ignored and reproducible from this script, which is the
record of the fetch (CONTEXT.md, "Record format"). Standard library only.

The route. The dataset is served by the NOAA IOOS National Glider Data Assembly Center's
ERDDAP at gliders.ioos.us, which is not the steward's host: the steward's data-access page
(https://spraydata.ucsd.edu/data-access) names it - "The best place to access this data is
the National Glider Data Assembly Center (GDAC)." - so the route is the second limb of
CONTEXT.md's FETCHED, a route the steward names. The request is the unconstrained tabledap
CSV: no variable list and no constraint, so every variable and every row the service holds
on the day of the fetch is returned, which is the dataset as served that day. The dataset
is near-real-time and grows while the glider reports (its .das states
ioos_dac_completed "False" and a time_coverage_end that advances), so a repeat fetch on a
later day is a different file, and the record dates what it holds.

Naming. ERDDAP answers with a Content-Disposition whose file name carries a suffix derived
from the query - the same query gives the same name on a repeat fetch - so the served
name is taken from that header, as src/fetch/calcofi.py takes it. With one file there is
nothing to collide with, and `taken` is kept for the shape; a run that fetched everything
prunes what it did not write, so an edit to the query cannot leave the old name beside the
new one, and a failed run prunes nothing.
"""

from __future__ import annotations

import csv
import datetime as dt
import email.message
import hashlib
import io
import json
import sys
import urllib.request
from pathlib import Path

SOURCE_ID = "cugn_sp030_20260701"

ERDDAP = "https://gliders.ioos.us/erddap/tabledap"

# The ERDDAP dataset id, as the .das states it in id, title and trajectory_name.
DATASET = "sp030-20260701T1719"

# The unconstrained request: every variable, every row.
FILES = (f"{ERDDAP}/{DATASET}.csv",)

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
    name = Path(served).name
    if name in ("", ".", ".."):
        raise RuntimeError(f"{url}: unusable served file name {served!r}")
    return name


def check_csv(body: bytes, url: str) -> None:
    """Refuse a 200 that is not the whole CSV that was asked for.

    tabledap streams its rows after the 200 and the Content-Type are on the wire and
    sends no Content-Length, so a run that dies mid-stream can complete the HTTP message
    with the rows it managed and an error appended (src/fetch/calcofi.py, check_csv, says
    why that case reaches here and a bad query does not). Every row of a tabledap CSV
    carries the same field count as its column-name row, so a truncated final row or an
    appended error line is a row of the wrong width.
    """
    rows = [r for r in csv.reader(io.StringIO(body.decode("ISO-8859-1"))) if r]
    if len(rows) < 3:
        raise RuntimeError(
            f"{url}: expected a name row, a units row and data, got {len(rows)} rows"
        )
    header = rows[0]
    if "trajectory" not in header:
        raise RuntimeError(f"{url}: no trajectory column in the name row {header[:6]}")
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
    with urllib.request.urlopen(request, timeout=600) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
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
        # Last-Modified with the time it built the response and sends no ETag.
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

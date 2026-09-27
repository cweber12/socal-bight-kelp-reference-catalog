"""Fetch the Dirk Burcham Scientific Mooring and Jim Updike Seabed Station files.

Run:  python src/fetch/cms_burcham_updike_mooring.py

Each file in FILES is downloaded unmodified into data/raw/cms_burcham_updike_mooring/ and
written beside a manifest carrying the url, the time of the fetch, the sha256, the byte
count, the HTTP status and the response headers a repeat fetch records - content_type,
last_modified and etag, null when the server sends none. data/ is git-ignored and
reproducible from this script, which is the record of the fetch (CONTEXT.md, "Record
format"). Standard library only.

The collection page is
https://www.catalinamarinesociety.org/dirk-burchan-scientific-mooring-and-jim-updike-seabed-station.html.
It prints 26 data-file URLs as text, not as links, each written without a scheme as
www.catalinamarinesociety.org/files/<name>; each is requested here over https://. On
2026-09-27, 17 of the 26 answered HTTP 200 and are in FILES, in the order the page prints
them. The other 9 answered HTTP 404 and are not in FILES:

  * EXO2_02022025-03092025.txt
  * WIES_5ft_01052025-01302025-21292585..csv
  * WIES_30ft_01052025-01302025_22129128..csv
  * Thermograph_20ft_04272024-5262024_21894646.dat
  * Thermograph_80ft_04272024-05262024_21894635.dat
  * pH_95ft_04272024-05252025_21506840.dat
  * Current_95ft_04272024-05262024_2108000.dat
  * water-level_95ft_10132024-01052025_21511796.txt
  * pH_95ft_10132024-01052025_21506840.txt

The page's four deployment headings are each a link, and all four link the same file,
http://www.catalinamarinesociety.org/files/Merged_Sci_Mooring_12042014-10202014.txt. It
is the last entry of FILES, requested over https://, where it answered HTTP 200.

A missing file on this host answers HTTP 404, and urlopen raises on that before any check
here runs. fetch() also rejects a body that arrives with HTTP 200 but is HTML, so that a
web page served in a file's place is never stored as mooring data.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE_ID = "cms_burcham_updike_mooring"

BASE = "https://www.catalinamarinesociety.org/files/"

FILES = (
    # "February 2, 2025 - March 9, 2025"
    BASE + "Temp_20ft_01302025-03092025_22169464.dat",
    BASE + "Temp_40ft_01302025-03092025_22169467.dat",
    BASE + "Temp_80ft_01302025-03092025_22169469.dat",
    BASE + "JUSS_pH_02022025-03092025.txt",
    BASE + "JUSS_depth_temp_95ft_02022025-03092025.dat",
    BASE + "JUSS_current_02022025-03092025.txt",
    # "Mixed-Layer Data January 5 2025 - January 30 2025"
    BASE + "WIES_1ft_01052025-01302025_20894273.csv",
    BASE + "WIES_10ft_01052025-01302025_20733049.csv",
    BASE + "WIES_20ft_01052025-01302025_20894279.csv",
    BASE + "WIES_40ft_01052025-01302025_22129129.csv",
    BASE + "WIES_60ft_01052025-01302025_21292584.csv",
    # "April 27, 2024 - May 26, 2024"
    BASE + "Temp_40ft_04272024-05262024_20481390.csv",
    BASE + "Pressure_95ft_04272024-05262024_21511799.txt",
    # "Oct 13, 2024 - Jan 5, 2025"
    BASE + "thermograph_20ft_10132024-01052025_21894636.txt",
    BASE + "thermograph_40ft_10132024-01052025_21894635.txt",
    BASE + "thermograph_60ft_10132024-01052025_20894280.txt",
    BASE + "current_95ft_10132024-01052025_2108000.txt",
    # linked from each of the four headings above
    BASE + "Merged_Sci_Mooring_12042014-10202014.txt",
)

REPO = "https://github.com/cweber12/socal-bight-kelp-reference-catalog"

# Name the catalog and give the steward a way to reach us.
USER_AGENT = f"kelpcatalog/{SOURCE_ID} (+{REPO})"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def served_name(url: str) -> str:
    """The file name the URL's last path segment gives; the host sends no Content-Disposition."""
    name = Path(urllib.parse.unquote(urllib.parse.urlsplit(url).path.rsplit("/", 1)[-1])).name
    if name in ("", ".", ".."):
        raise RuntimeError(f"{url}: unusable served file name {name!r}")
    return name


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    content_type = headers.get("Content-Type") or ""
    if content_type.startswith("text/html") or body.lstrip()[:9].lower() == b"<!doctype":
        raise RuntimeError(
            f"{url}: body is HTML, not a data file "
            f"(Content-Type {content_type!r}, first bytes {body[:40]!r})"
        )
    name = served_name(url)
    manifest = {
        "url": url,
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "http_status": http_status,
        # What a repeat fetch records, not what it reproduces. No content_length - it
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
    # Fetch what can be fetched, then name every failure and exit non-zero, so a
    # directory missing files is never mistaken for a complete one.
    names = [served_name(url) for url in FILES]
    if len(set(names)) != len(names):
        raise SystemExit("two URLs in FILES share a file name")
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

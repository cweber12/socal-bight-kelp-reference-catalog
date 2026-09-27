"""Fetch the Channel Islands fish excretion deposit into data/raw/shrestha_fish_excretion/.

Run:  python src/fetch/shrestha_fish_excretion.py

The one file is downloaded unmodified and written beside a manifest carrying the url, the
time of the fetch, the sha256, the byte count, the HTTP status and the response headers a
repeat fetch records - content_type, last_modified and etag, null when the server sends
none. data/ is git-ignored and reproducible from this script, which is the record of the
fetch (CONTEXT.md, "Record format"). Standard library only.

URL is the download link Dryad's API gives version 328111 of doi:10.5061/dryad.k6djh9wgj,
the one version the API lists. On 2026-09-27 it answered HTTP 302 with a signed URL as its
Location, and that URL served a zip holding the version's four files. The manifest records
URL and not the Location. The host is datadryad.org; the access steps of
catalog/sources/shrestha_fish_excretion.md state what reading it as the second FETCHED
route (CONTEXT.md, "Vocabularies"), a route the steward names as where the source is to be
had, rests on.

URL's last segment is "download", so the zip is stored under the name the response's
Content-Disposition gives it, and its manifest is manifest_<that name>.json. A response
without one is refused.

The zip is assembled when it is asked for: on 2026-09-27 two requests about four minutes
apart were each served 56,245,597 bytes with two different SHA-256s, each member's
modification time the minute of its request. The zip's own SHA-256 is therefore a fact of
one fetch, and the host states neither a size nor a digest for it. What the host does
state is a size and a SHA-256 for each file of the version, at
https://datadryad.org/api/v2/versions/328111/files; FILES holds them as that listing gave
them on 2026-09-27. Whatever the status and the headers say, the zip must hold the members
FILES names and no others, each with that size and that digest, or it is not kept. The
members are read from the zip to be hashed and are not written out: what is held is the
zip as served.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

SOURCE_ID = "shrestha_fish_excretion"
USER_AGENT = f"kelpcatalog/{SOURCE_ID}"
URL = "https://datadryad.org/api/v2/versions/328111/download"
FILES = (
    (
        "README.md",
        "1a8b02349d7e896475403dbe88d4e0c481076857a1fb180a2e9d27e7e30fee93",
        5724,
    ),
    (
        "Shrestha_fish_excr_data_Channel_Islands_all.csv",
        "9f3d85a8b15e7180cdc62e82f3eb33a794b33b1f8b73871c0a9a5d2e6393295d",
        31436612,
    ),
    (
        "Shrestha_fish_excr_data_Channel_Islands_longterm_sites.csv",
        "79b06da4cd9b348cd72692bf9ecd51f12c9abc53f35fb84e7cb8534a7174cbb2",
        24786155,
    ),
    (
        "Shrestha_Fish_length-weight_conversion_table.csv",
        "1431e380bbad779149a733920a43a2d97a852e5de47bacc5305bc661f4c4efcb",
        7976,
    ),
)
CHUNK = 1 << 20

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def check_members(path: Path) -> None:
    """Raise unless the zip at path holds exactly the members FILES states."""
    stated = {name: (sha256, size) for name, sha256, size in FILES}
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if sorted(names) != sorted(stated):
            raise RuntimeError(f"{URL} served members {names}, where Dryad lists {list(stated)}")
        for name in names:
            sha256, size = hashlib.sha256(), 0
            with archive.open(name) as member:
                while chunk := member.read(CHUNK):
                    sha256.update(chunk)
                    size += len(chunk)
            found = (sha256.hexdigest(), size)
            if found != stated[name]:
                raise RuntimeError(
                    f"{URL} served {name} as {found[1]} bytes with SHA-256 {found[0]}, "
                    f"where Dryad states {stated[name][1]} and {stated[name][0]}"
                )


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download the zip into out_dir and write its manifest. Returns the manifest."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    out_dir.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=600) as response:
        http_status = response.status
        headers = response.headers
        # get_filename() sanitises nothing, and the value is server-supplied.
        name = headers.get_filename()
        if not name or name != Path(name).name or name in (".", ".."):
            raise RuntimeError(f"{url} named no file to store: {name!r}")
        part = out_dir / f"{name}.part"
        sha256, size = hashlib.sha256(), 0
        try:
            with part.open("wb") as out:
                while chunk := response.read(CHUNK):
                    out.write(chunk)
                    sha256.update(chunk)
                    size += len(chunk)
        except BaseException:
            part.unlink(missing_ok=True)
            raise
    try:
        check_members(part)
    except BaseException:
        part.unlink(missing_ok=True)
        raise
    manifest = {
        "url": url,
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "sha256": sha256.hexdigest(),
        "bytes": size,
        "http_status": http_status,
        # What a repeat fetch records, not what it reproduces. No content_length - it
        # duplicates bytes.
        "content_type": headers.get("Content-Type"),
        "last_modified": headers.get("Last-Modified"),
        "etag": headers.get("ETag"),
    }
    part.replace(out_dir / name)
    (out_dir / f"manifest_{name}.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    print(json.dumps(fetch(URL, OUT_DIR), indent=2))


if __name__ == "__main__":
    main()

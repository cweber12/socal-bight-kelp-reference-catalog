"""Fetch the giant kelp microsatellite deposit into data/raw/klingbeil_kelp_genotypes/.

Run:  python src/fetch/klingbeil_kelp_genotypes.py

The one file is downloaded unmodified and written beside a manifest carrying the url, the
time of the fetch, the sha256, the byte count, the HTTP status and the response headers a
repeat fetch records - content_type, last_modified and etag, null when the server sends
none. data/ is git-ignored and reproducible from this script, which is the record of the
fetch (CONTEXT.md, "Record format"). Standard library only.

URL is the download link Dryad's API gives version 248755 of doi:10.5061/dryad.nzs7h44v9,
the one version the API lists. On 2026-09-21 it answered HTTP 302 with a signed URL as its
Location, and that URL served a zip holding the version's two files. The manifest records
URL and not the Location. The host is datadryad.org; step 2 of `access` in
catalog/sources/klingbeil_kelp_genotypes.md states what reading it as the second FETCHED
route (CONTEXT.md, "Vocabularies"), a route the steward names as where the source is to be
had, rests on.

URL's last segment is "download", so the zip is stored under the name the response's
Content-Disposition gives it, and its manifest is manifest_<that name>.json. A response
without one is refused.

The zip is assembled when it is asked for: on 2026-09-21 three requests six seconds apart
were each served 176,604 bytes with three different SHA-256s, each member's modification
time within a second of the response's Date header, and two other requests were served
176,599 bytes. The zip's own SHA-256 and size are therefore facts of one fetch, and the
host states neither for it.
What the host does state is a size and a SHA-256 for each file of the version, at
https://datadryad.org/api/v2/versions/248755/files; FILES holds them as that listing gave
them on 2026-09-21. Whatever the status and the headers say, the zip must hold the members
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

SOURCE_ID = "klingbeil_kelp_genotypes"
USER_AGENT = f"kelpcatalog/{SOURCE_ID}"
URL = "https://datadryad.org/api/v2/versions/248755/download"
FILES = (
    (
        "README.md",
        "61c5826338ea7422ee172f2f95b42c0976ae9aec886b676771c0558c79f318bb",
        1438,
    ),
    (
        "Structure_before_and_after.Klingbeil2022.txt",
        "756933ec92efbd75632471c373c4755fd14e15c75b303756d5c9d2091cb1ec41",
        174743,
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
            body = archive.read(name)
            found = (hashlib.sha256(body).hexdigest(), len(body))
            if found != stated[name]:
                raise RuntimeError(
                    f"{URL} served {name} as {found[1]} bytes with SHA-256 {found[0]}, "
                    f"where Dryad states {stated[name][1]} and {stated[name][0]}"
                )


def fetch(url: str, out_dir: Path) -> dict[str, object]:
    """Download the zip into out_dir and write its manifest. Returns the manifest."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    out_dir.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=120) as response:
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

"""Fetch the San Diego giant kelp demography deposit into data/raw/parnell_kelp_demography/.

Run:  python src/fetch/parnell_kelp_demography.py

The one file is downloaded unmodified and written beside a manifest carrying the url, the
time of the fetch, the sha256, the byte count, the HTTP status and the response headers a
repeat fetch records - content_type, last_modified and etag, null when the server sends
none. data/ is git-ignored and reproducible from this script, which is the record of the
fetch (CONTEXT.md, "Record format"). Standard library only.

URL is the download link Dryad's API gives version 409846 of doi:10.5061/dryad.fttdz096d,
the one version the API lists. On 2026-10-01 it answered HTTP 302 with a signed URL as its
Location, and that URL served a zip holding the version's three files. The manifest
records URL and not the Location. The host is datadryad.org; the access steps of
catalog/sources/parnell_kelp_demography.md state what reading it as the second FETCHED
route (CONTEXT.md, "Vocabularies"), a route the steward names as where the source is to be
had, rests on.

URL's last segment is "download", so the zip is stored under the name the response's
Content-Disposition gives it, and its manifest is manifest_<that name>.json. A response
without one is refused.

The zip is assembled when it is asked for: on 2026-10-01 two requests about two seconds
apart were served 597,083 and 597,073 bytes with two different SHA-256s, each member's
modification time the minute of its request. The zip's own size and SHA-256 are therefore
facts of one fetch, and the host states neither for it. What the host does state is a size
and a SHA-256 for each file of the version, at
https://datadryad.org/api/v2/versions/409846/files; FILES holds them as that listing gave
them on 2026-10-01. Whatever the status and the headers say, the zip must hold the members
FILES names and no others, each with that size and that digest, or it is not kept. Because
the zip's own digest cannot be pinned, the file around the members is checked too: it must
begin with a local file header (the bytes 50 4B 03 04), carry no bytes before its first
member, and carry no archive comment, or it is not kept. The members are read from the zip
to be hashed and are not written out: what is held is the zip as served.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

SOURCE_ID = "parnell_kelp_demography"
USER_AGENT = f"kelpcatalog/{SOURCE_ID}"
URL = "https://datadryad.org/api/v2/versions/409846/download"
FILES = (
    (
        "AlgaeBoxData.RData",
        "44e2749ff885ae9e36f0e0c2d4db2d96c1d10ef7bf61d04baea246e57a07b064",
        388275,
    ),
    (
        "README.md",
        "9db9e8b832e64cd8aa10485ed6e19d60ee653303859012e732243fa955ac550a",
        3957,
    ),
    (
        "StipeData.RData",
        "9cc3e0227fe9a1f9e73488dc9269b1cc42d223a1aac161bfee62ad1fc326fe0c",
        204298,
    ),
)
CHUNK = 1 << 20
LOCAL_HEADER = b"PK\x03\x04"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def check_container(path: Path, archive: zipfile.ZipFile) -> None:
    """Raise unless the zip at path is nothing but its members: it begins with a local file
    header, no bytes stand before its first member, and it carries no archive comment."""
    with path.open("rb") as raw:
        head = raw.read(len(LOCAL_HEADER))
    if head != LOCAL_HEADER:
        raise RuntimeError(f"{URL} served a file beginning {head!r}, not a local file header")
    first = min((info.header_offset for info in archive.infolist()), default=None)
    if first != 0:
        raise RuntimeError(f"{URL} served {first} bytes before the zip's first member")
    if archive.comment:
        raise RuntimeError(f"{URL} served an archive comment of {len(archive.comment)} bytes")


def check_members(path: Path) -> None:
    """Raise unless the zip at path is nothing but its members (check_container) and holds
    exactly the members FILES states."""
    stated = {name: (sha256, size) for name, sha256, size in FILES}
    with zipfile.ZipFile(path) as archive:
        check_container(path, archive)
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

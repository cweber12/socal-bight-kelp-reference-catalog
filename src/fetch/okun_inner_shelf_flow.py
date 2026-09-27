"""Fetch the San Diego inner shelf flow deposit into data/raw/okun_inner_shelf_flow/.

Run:  python src/fetch/okun_inner_shelf_flow.py

The one file is downloaded unmodified and written beside a manifest carrying the url, the
time of the fetch, the sha256, the byte count, the HTTP status and the response headers a
repeat fetch records - content_type, last_modified and etag, null when the server sends
none. data/ is git-ignored and reproducible from this script, which is the record of the
fetch (CONTEXT.md, "Record format"). Standard library only.

URL is the download link Dryad's API gives version 360631 of doi:10.5061/dryad.x3ffbg7tk,
the version the dataset's API response links as its current one; the API lists two
versions, 334486 and 360631. On 2026-09-27 URL answered HTTP 302 with a signed URL as its
Location, and that URL served a zip holding the version's eighteen files. The manifest
records URL and not the Location. The host is datadryad.org; the access steps of
catalog/sources/okun_inner_shelf_flow.md state what reading it as the second FETCHED route
(CONTEXT.md, "Vocabularies"), a route the steward names as where the source is to be had,
rests on.

URL's last segment is "download", so the zip is stored under the name the response's
Content-Disposition gives it, and its manifest is manifest_<that name>.json. A response
without one is refused.

The zip is assembled when it is asked for: on 2026-09-27 two requests about five minutes
apart were served 24,192,611 and 24,192,581 bytes with two different SHA-256s, each
member's modification time the minute of its request. The zip's own size and SHA-256 are
therefore facts of one fetch, and the host states neither for it. What the host does
state is a size and a SHA-256 for each file of the version, at
https://datadryad.org/api/v2/versions/360631/files; FILES holds them as that listing gave
them on 2026-09-27. Whatever the status and the headers say, the zip must hold the members
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

SOURCE_ID = "okun_inner_shelf_flow"
USER_AGENT = f"kelpcatalog/{SOURCE_ID}"
URL = "https://datadryad.org/api/v2/versions/360631/download"
FILES = (
    (
        "Bathymetry_Profiles.mat",
        "8891872a789244777521c2f368a592f5ef037c3c00e42142205cc81f8844b1e8",
        25454,
    ),
    (
        "Quasi_Barotropic.mat",
        "92548e80fe50fee5fb7e158f6656e21ffe96bf8145fd6bb246d9d2bbd2023f4c",
        2378,
    ),
    (
        "README.md",
        "748855d4b094fc4075364408c77a04d12ffd56ff97190087acb6449d68e034cd",
        3861,
    ),
    (
        "RunsForPub_bathy2_strat1.mat",
        "db02e5a04ca397ce339ead9172f5427ae914528acbcacb863dba6949fbd66f00",
        2021725,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih1_is1.mat",
        "ff6c55cbe39e78c5f34feb62399d5785105e3662a8f8a6c87e1272dc64a9170e",
        8009,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih1_is2.mat",
        "a93e7651126af75d14a35b65daab0d93cb90b9ae4953ed0734c93671a14e9daa",
        7992,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih1_is4.mat",
        "7626f0d40b791975ce8616ee5dc9f51f3c8549f764c263d3c355979085d0cd9f",
        8022,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih2_is1.mat",
        "ad21c530fe8d2548417f9c5584eaf524c09cf3a817a2556ff2677aa20205ed0b",
        7473,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih2_is2.mat",
        "b98579c25fa5a56c9d20b74efbb15c577f6f76e8882e2ec5e8920eb11bb71e4c",
        7806,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih2_is3.mat",
        "9facf04fed6d5ee661ffbd88eaf8282e62e777a573fdccb272f8afba16be36d9",
        7914,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih2_is4.mat",
        "924552cd2bb80d343545684d6b0961ab36035ad79e5e57031855a32ea8a084d9",
        7696,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih3_is1.mat",
        "4e10a3377f248c9158080062825e93bcd4e1afd455cb699c9c27432f7561ff4d",
        7994,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih3_is2.mat",
        "4d2b0ffcda249ca402b9eec1ecace60536ff750cccba4a577138cd849d8dcc1c",
        8022,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih3_is3.mat",
        "ff65c69d11770c12c37889f281ed1463f3351708ab86d8bf5ef6cc1de5873284",
        7997,
    ),
    (
        "scatter_invisc_01_SoCal_2023_02_ih3_is4.mat",
        "4b6a07630e0530cdd86c57c1383d1558092cd102b373bb27243b7fca8ce12abc",
        8077,
    ),
    (
        "scatter_invisc_SoCal_February2025_Xsection_ih2_is1.mat",
        "94b18bd073b40057092a21f38f528925ca0e77aabf7b0b89ba4e2f1705d6812c",
        1768765,
    ),
    (
        "SD_IT_Current_Data.mat",
        "e531d6e9cff208c7bcd1df746599a934455c7576a73e74d65c7f2c1c07cfbc6c",
        20239579,
    ),
    (
        "Seasonal_N_2.mat",
        "fbfebe31862332c79aa8529b8cb31636ae8c002100e28577baccedf94212f619",
        37278,
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

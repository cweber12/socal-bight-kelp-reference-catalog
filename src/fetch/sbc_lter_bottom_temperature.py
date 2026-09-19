"""Fetch the SBC LTER reef bottom temperature table into data/raw/sbc_lter_bottom_temperature/.

Run:  python src/fetch/sbc_lter_bottom_temperature.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. This host sent no ETag on 2026-09-19. data/ is git-ignored and
reproducible from this script, which is the record of the fetch (CONTEXT.md, "Record
format"). Standard library only.

FILES holds PASTA identifiers, not URLs, each with the SHA-1 and the size DataONE's system
metadata stated for it on 2026-09-19; the identifier carries the package revision, 33.
EDI's own PASTA service answers HTTP 403 to an anonymous request for them, and the DataONE
member node EDI replicates to serves the same object under the same identifier
(catalog/sources/sbc_lter_bottom_temperature.md, `access`; CONTEXT.md, "Vocabularies", the
third FETCHED route). The URL fetched is MEMBER_NODE followed by the identifier
percent-encoded whole.

That URL's last segment is the encoded identifier, so the file is stored under the name
the server's Content-Disposition gives it, and its manifest is manifest_<that name>.json.
A response without one is refused.

The member node relays PASTA's answer under its own HTTP 200 and its own headers. On
2026-09-19, to the User-Agent "kelpcatalog/sbc_lter_bottom_temperature", which is this
script's id in the form noaa_oni.py sends, the body was a 162-byte nginx "403 Forbidden"
page beneath a Content-Length and a Content-Disposition that describe the table. So this
script sends a User-Agent naming the package instead, and believes neither the status nor
those headers: the body must have the SHA-1 and the size FILES gives, or nothing is kept.

The table is several hundred megabytes, so the body is streamed to <name>.part in chunks
and hashed as it arrives, and renamed once it has passed.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE_ID = "sbc_lter_bottom_temperature"
USER_AGENT = "kelpcatalog/knb-lter-sbc.13"
MEMBER_NODE = "https://gmn.lternet.edu/mn/v2/object/"
FILES = (
    (
        "https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/13/33/d707a45a2cd6eee1d016d99844d537da",
        "2c71847a7670e928800133c564aad85754c18bc6",
        582980514,
    ),
)
CHUNK = 1 << 20

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(identifier: str, sha1_stated: str, size_stated: int, out_dir: Path) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest."""
    url = MEMBER_NODE + urllib.parse.quote(identifier, safe="")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    out_dir.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=120) as response:
        http_status = response.status
        headers = response.headers
        # get_filename() sanitises nothing, and the value is server-supplied.
        name = headers.get_filename()
        if not name or name != Path(name).name or name in (".", ".."):
            raise SystemExit(f"{url} named no file to store: {name!r}")
        part = out_dir / f"{name}.part"
        sha256, sha1, size = hashlib.sha256(), hashlib.sha1(usedforsecurity=False), 0
        try:
            with part.open("wb") as out:
                while chunk := response.read(CHUNK):
                    out.write(chunk)
                    sha256.update(chunk)
                    sha1.update(chunk)
                    size += len(chunk)
        except BaseException:
            part.unlink(missing_ok=True)
            raise
    if sha1.hexdigest() != sha1_stated or size != size_stated:
        part.unlink()
        raise SystemExit(
            f"{url} did not return the file: {size} bytes with SHA-1 {sha1.hexdigest()}, "
            f"where DataONE states {size_stated} and {sha1_stated}"
        )
    manifest = {
        "url": url,
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "sha256": sha256.hexdigest(),
        "bytes": size,
        "http_status": http_status,
        # What a repeat fetch records, not what it reproduces: Last-Modified moves when
        # the steward updates the file. No content_length - it duplicates bytes.
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
    for identifier, sha1_stated, size_stated in FILES:
        print(json.dumps(fetch(identifier, sha1_stated, size_stated, OUT_DIR), indent=2))


if __name__ == "__main__":
    main()

"""Fetch the PISCO kelp forest community survey files into data/raw/pisco_kelp_forest/.

Run:  python src/fetch/pisco_kelp_forest.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. data/ is git-ignored and reproducible from this script, which is the
record of the fetch (CONTEXT.md, "Record format"). Standard library only.

FILES holds DataONE identifiers, not URLs, each with the SHA-256 and the size that the
PISCO member node's system metadata stated for it on 2026-09-20; they are the eight
entities the EML of doi:10.6085/AA/PISCO_kelpforest.1.11 lists, and each identifier
carries that revision. The host is data.piscoweb.org, the PISCO member node of DataONE;
steps 2 and 8 of `access` in catalog/sources/pisco_kelp_forest.md state what reading it
as the first FETCHED route (CONTEXT.md, "Vocabularies") rests on. The URL fetched is
MEMBER_NODE followed by the identifier percent-encoded whole.

That URL's last segment is the encoded identifier, so each file is stored under the name
the server's Content-Disposition gives it, and its manifest is manifest_<that name>.json;
on 2026-09-20 each of the eight responses carried one. A response without one is refused.

On that day the eight responses were sent with Transfer-Encoding chunked and no
Content-Length, so a body cut short does not show in the headers. Whatever the status
and the headers say, the body must have the SHA-256 and the size FILES gives, or it is
not kept. The digest checked is the one the manifest records.

The body is streamed to <name>.part in chunks and hashed as it arrives, and renamed once
it has passed. A failure part-way through FILES leaves some files on disk and others
missing: main() fetches what can be fetched, then names every failure and exits non-zero,
as src/fetch/sio_shore_stations.py does.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE_ID = "pisco_kelp_forest"
USER_AGENT = f"kelpcatalog/{SOURCE_ID}"
MEMBER_NODE = "https://data.piscoweb.org/metacat/d1/mn/v2/object/"
FILES = (
    (
        "doi:10.6085/AA/PISCO_kelpforest_swath.1.11",
        "47b33666ed06d4a2d0654405d768a7d0c2bbca37b2e26411e2c4393249e37dac",
        33316050,
    ),
    (
        "doi:10.6085/AA/PISCO_kelpforest_upc.1.11",
        "7357da5ed575735b3a315b94853e824048e2a44622379a966004bbc800dbaeff",
        20101670,
    ),
    (
        "doi:10.6085/AA/PISCO_kelpforest_sizefreq.1.11",
        "44e9c3db4534647af1619f01113e3a6ab1565377675a19f7d2eb5f4aca3464fa",
        2616775,
    ),
    (
        "doi:10.6085/AA/PISCO_kelpforest_fish.1.11",
        "a0d658cdd53bb6990db1b68cf4c9a4ca696a079e30b54f0f789cce0f018a5b34",
        68403795,
    ),
    (
        "doi:10.6085/AA/PISCO_kelpforest_quad.1.11",
        "5ce22da6764facc3bd045a632fd5bf556e76ab60c426183fbdf65b5d44d39525",
        4954171,
    ),
    (
        "doi:10.6085/AA/PISCO_kelpforest_taxon_table.1.11",
        "508bbefdc883d8e3fc9eb4c257c2254f1731a7d05380f05a3a946151532cd992",
        201464,
    ),
    (
        "doi:10.6085/AA/PISCO_kelpforest_site_table.1.11",
        "cf865f93a4137e49758c998c99de576fd74bf4f8cf660ab3638a8a589958ee04",
        1092929,
    ),
    (
        "doi:10.6085/AA/PISCO_kelpforest_methods.1.11",
        "88b47b30237bd9330a26d544a4ed1e7957df3d94fcd1e6b8c0dd06245f5a74b2",
        105090,
    ),
)
CHUNK = 1 << 20

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def fetch(
    identifier: str, sha256_stated: str, size_stated: int, out_dir: Path
) -> dict[str, object]:
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
    if sha256.hexdigest() != sha256_stated or size != size_stated:
        part.unlink()
        raise RuntimeError(
            f"{url} did not return the file: {size} bytes with SHA-256 {sha256.hexdigest()}, "
            f"where the member node states {size_stated} and {sha256_stated}"
        )
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
    failures: list[tuple[str, Exception]] = []
    for identifier, sha256_stated, size_stated in FILES:
        try:
            print(json.dumps(fetch(identifier, sha256_stated, size_stated, OUT_DIR), indent=2))
        except Exception as exc:  # noqa: BLE001 - every failure is reported below
            failures.append((identifier, exc))
            print(f"FAILED {identifier}: {exc}", file=sys.stderr)
    if failures:
        print(
            f"\n{len(failures)} of {len(FILES)} files did not fetch; {OUT_DIR} is incomplete:",
            file=sys.stderr,
        )
        for identifier, exc in failures:
            print(f"  {identifier}: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

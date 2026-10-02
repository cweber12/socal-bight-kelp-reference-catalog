"""Fetch the MLPA kelp forest monitoring files into data/raw/opc_mlpa_kelp_forest/.

Run:  python src/fetch/opc_mlpa_kelp_forest.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. data/ is git-ignored and reproducible from this script, which is the
record of the fetch (CONTEXT.md, "Record format"). Standard library only.

FILES holds DataONE identifiers, not URLs, each with the SHA-256 and the size that the
California Ocean Protection Council member node's system metadata stated for it on
2026-10-01; they are the seven entities the EML of doi:10.25494/P6/MLPA_kelpforest.12
lists, spelled as that node's system metadata spells them. The EML's own distribution
URLs for revision .12 carry the file extension inside the identifier (…_swath.10.csv),
and that spelling answered HTTP 404 from the node and from the DataONE resolver on
2026-10-01; the spelling here, which the previous revision's entities name in their
obsoletedBy elements, answered HTTP 200. The host is opc.dataone.org, the member node
urn:node:CA_OPC, which the EML's creators name as the distribution through the DataONE
resolver; the `access` steps of catalog/sources/opc_mlpa_kelp_forest.md state what
reading it as the second FETCHED route (CONTEXT.md, "Vocabularies") rests on. The URL
fetched is MEMBER_NODE followed by the identifier percent-encoded whole.

That URL's last segment is the encoded identifier, so each file is stored under the name
the server's Content-Disposition gives it, and its manifest is manifest_<that name>.json;
on 2026-10-01 each probed response carried one. A response without one is refused.

The responses carry no Content-Length, so a body cut short does not show in the headers.
Whatever the status and the headers say, the body must have the SHA-256 and the size
FILES gives, or it is not kept. The digest checked is the one the manifest records.

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

SOURCE_ID = "opc_mlpa_kelp_forest"
USER_AGENT = f"kelpcatalog/{SOURCE_ID}"
MEMBER_NODE = "https://opc.dataone.org/metacat/d1/mn/v2/object/"
FILES = (
    (
        "doi:10.25494/P6/MLPA_kelpforest_swath.10",
        "eb1a5615586f73cb83531efc2421424e0b9bd85213b13fb59de79df0f8fe7f34",
        41135852,
    ),
    (
        "doi:10.25494/P6/MLPA_kelpforest_upc.10",
        "42a095a2a72982b3aea8366920b86cf147a89d38c90e3c5fb083dd7d5c250e75",
        29835317,
    ),
    (
        "doi:10.25494/P6/MLPA_kelpforest_sizefreq.10",
        "33049ba91b050b6ce2e7302f8eea0fc9185aad7c8631db61d1dc11eaa270c463",
        9587148,
    ),
    (
        "doi:10.25494/P6/MLPA_kelpforest_fish.10",
        "0d6a11300f1d093694b17ae2f366f1d19e78669b1377b8a456da49ccb0b020ae",
        69409298,
    ),
    (
        "doi:10.25494/P6/MLPA_kelpforest_taxon_table.10",
        "54de86382a4cff6b689a76ecc91c997273f63227b859f9da23b1005049460707",
        501754,
    ),
    (
        "doi:10.25494/P6/MLPA_kelpforest_site_table.10",
        "e8b80d2dc350da0371e7f6e52ccb6921727725b86225b05991ef7eb658aa9aa4",
        1851410,
    ),
    (
        "doi:10.25494/P6/MLPA_kelpforest_methods.10",
        "317945d31d9876bc83421438c3835331dfbc8d784f7142034af17d653a392bb7",
        84001,
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

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
member or between one of its parts and the next, each part beginning where the one before
it ends (the parts being its members, each running from the local file header its central
directory entry places it at, through its name, extra field and compressed data of the
size that entry states, that data being either stored, and of the member's size, or
deflated, and one deflate stream ending at the data's last byte, to the end of its data
descriptor where it has one, that descriptor stating the CRC-32 and the sizes that entry
states; then its central directory; then its zip64 end of central directory record and
locator where it has them; then its end of central directory record), carry no archive
comment, and end where its end of central directory record ends, so that no bytes follow
it, or it is not kept. The members are read from the zip to be hashed and are not written
out: what is held is the zip as served.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import urllib.request
import zipfile
import zlib
from pathlib import Path
from typing import BinaryIO

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
DATA_DESCRIPTOR = b"PK\x07\x08"
END_RECORD = b"PK\x05\x06"
ZIP64_END_RECORD = b"PK\x06\x06"
ZIP64_LOCATOR = b"PK\x06\x07"
# A local file header is 30 bytes, then the member's name, then its extra field; the two lengths
# are the little-endian pairs at offsets 26 and 28, and bit 3 of the flag at offset 6 says a
# data descriptor follows the compressed data: an optional 4-byte signature, the CRC-32, then
# the compressed and uncompressed sizes as 4 bytes each or, in zip64 form, 8 bytes each.
LOCAL_HEADER_SIZE = 30
DESCRIPTOR_FLAG = 0x08
ZIP64_EXTRA_ID = 0x0001
# An end of central directory record is 22 bytes, then its comment; the comment length is
# the two little-endian bytes at offset 20, and the comment can be at most 65535 bytes. The
# central directory's size and offset are its 4-byte fields at offsets 12 and 16. A zip64 zip
# puts 0xFFFFFFFF there and carries the true values as the 8-byte fields at offsets 40 and 48
# of a zip64 end of central directory record, whose own size, less its first 12 bytes, is the
# 8-byte field at its offset 4; a 20-byte locator, which ends where the end record begins,
# gives that record's offset as the 8-byte field at its offset 8.
END_RECORD_SIZE = 22
END_RECORD_SEARCH = END_RECORD_SIZE + 0xFFFF
ZIP64_END_RECORD_SIZE = 56
ZIP64_LOCATOR_SIZE = 20

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def contiguous(ends: int, part: str, begins: int, next_part: str) -> None:
    """Raise unless `begins`, the byte at which next_part begins, is `ends`, where part ends."""
    if begins > ends:
        raise RuntimeError(f"{URL} served {begins - ends} bytes between {part} and {next_part}")
    if begins < ends:
        raise RuntimeError(
            f"{URL} served {next_part} beginning at byte {begins}, {ends - begins} bytes before "
            f"{part} ends"
        )


def check_stream(raw: BinaryIO, begins: int, info: zipfile.ZipInfo) -> None:
    """Raise unless the compressed data of the member info describes, which begins at byte `begins`
    and is of the size its central directory entry states, is either stored, and of the member's
    size, or deflated, and one deflate stream ending at the data's last byte."""
    if info.compress_type == zipfile.ZIP_STORED:
        surplus = info.compress_size - info.file_size
        if surplus:
            raise RuntimeError(
                f"{URL} served {info.filename} stored with {info.compress_size} bytes of data, "
                f"{abs(surplus)} bytes {'more' if surplus > 0 else 'fewer'} than its size of "
                f"{info.file_size}"
            )
        return
    if info.compress_type != zipfile.ZIP_DEFLATED:
        raise RuntimeError(
            f"{URL} served {info.filename} with compression method {info.compress_type} in its "
            f"central directory entry, neither stored (0) nor deflated (8)"
        )
    decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
    raw.seek(begins)
    left = info.compress_size
    try:
        while left and not decompressor.eof:
            chunk = raw.read(min(CHUNK, left))
            if not chunk:
                break
            left -= len(chunk)
            # The output is bounded and discarded: only where the stream ends is wanted. Output
            # that fills the bound can leave the stream's end inside zlib with no input left
            # over, so a full output asks for more as an unconsumed tail does.
            out = decompressor.decompress(chunk, CHUNK)
            while not decompressor.eof and (decompressor.unconsumed_tail or len(out) == CHUNK):
                out = decompressor.decompress(decompressor.unconsumed_tail, CHUNK)
    except zlib.error as exc:
        raise RuntimeError(
            f"{URL} served {info.filename} with compressed data that is not a deflate stream: {exc}"
        ) from exc
    if not decompressor.eof:
        raise RuntimeError(
            f"{URL} served {info.filename} with a deflate stream that does not end within the "
            f"{info.compress_size} bytes its central directory entry states"
        )
    surplus = len(decompressor.unused_data) + left
    if surplus:
        raise RuntimeError(
            f"{URL} served {info.filename} with {surplus} bytes after its deflate stream ends, "
            f"within the {info.compress_size} bytes its central directory entry states"
        )


def member_end(raw: BinaryIO, info: zipfile.ZipInfo) -> int:
    """Return the byte at which the member info describes ends: after its local file header, its
    name, its extra field and its compressed data, which must pass check_stream, and after its
    data descriptor when the flag in that header says one follows, which must state the CRC-32
    and the sizes the central directory states for the member."""
    raw.seek(info.header_offset)
    header = raw.read(LOCAL_HEADER_SIZE)
    if header[: len(LOCAL_HEADER)] != LOCAL_HEADER:
        raise RuntimeError(
            f"{URL} served no local file header at byte {info.header_offset}, where the central "
            f"directory places {info.filename}"
        )
    flag = int.from_bytes(header[6:8], "little")
    name_length = int.from_bytes(header[26:28], "little")
    extra_length = int.from_bytes(header[28:30], "little")
    begins = info.header_offset + LOCAL_HEADER_SIZE + name_length + extra_length
    check_stream(raw, begins, info)
    end = begins + info.compress_size
    if not flag & DESCRIPTOR_FLAG:
        return end
    # APPNOTE 4.3.9.2: when the local header's extra field carries the zip64 extended
    # information field (id 0x0001), the descriptor's sizes are 8 bytes each. Without it they
    # are read as 4 bytes first, because a 4-byte descriptor read as 8 bytes would match where
    # an empty member is followed by 8 zero bytes, and as 8 bytes after that, for a writer
    # that uses the 8-byte form without the field.
    raw.seek(info.header_offset + LOCAL_HEADER_SIZE + name_length)
    extra = raw.read(extra_length)
    widths, at = (4, 8), 0
    while at + 4 <= len(extra):
        field_id = int.from_bytes(extra[at : at + 2], "little")
        field_size = int.from_bytes(extra[at + 2 : at + 4], "little")
        if field_id == ZIP64_EXTRA_ID:
            widths = (8,)
        at += 4 + field_size
    raw.seek(end)
    descriptor = raw.read(len(DATA_DESCRIPTOR) + 20)
    if descriptor[: len(DATA_DESCRIPTOR)] == DATA_DESCRIPTOR:
        descriptor = descriptor[len(DATA_DESCRIPTOR) :]
        end += len(DATA_DESCRIPTOR)
    stated = (info.CRC, info.compress_size, info.file_size)
    for width in widths:
        fields = (
            int.from_bytes(descriptor[0:4], "little"),
            int.from_bytes(descriptor[4 : 4 + width], "little"),
            int.from_bytes(descriptor[4 + width : 4 + 2 * width], "little"),
        )
        if fields == stated:
            return end + 4 + 2 * width
    raise RuntimeError(
        f"{URL} served {info.filename} with a data descriptor that does not state the CRC-32 "
        f"{info.CRC:#010x} and the sizes {info.compress_size} and {info.file_size} its central "
        f"directory entry states"
    )


def check_container(path: Path, archive: zipfile.ZipFile) -> None:
    """Raise unless the zip at path is its parts and nothing else: it begins with a local file
    header; no bytes stand before its first member or between one of its parts and the next, each
    part beginning where the one before it ends (the parts being its members, each running from the
    local file header its central directory entry places it at, through its name, extra field and
    compressed data of the size that entry states, that data being either stored, and of the
    member's size, or deflated, and one deflate stream ending at the data's last byte, to the end of
    its data descriptor where it has one, that descriptor stating the CRC-32 and the sizes that
    entry states; then its central directory; then its zip64 end of central directory record and
    locator where it has them; then its end of central directory record); it carries no archive
    comment; and it ends where its end of central directory record ends, so no bytes follow that
    record. A member's extra field is the member's: it is read only for the zip64 id that sets the
    width of its data descriptor's sizes, and what else it holds is not checked."""
    size = path.stat().st_size
    with path.open("rb") as raw:
        head = raw.read(len(LOCAL_HEADER))
        if head != LOCAL_HEADER:
            raise RuntimeError(f"{URL} served a file beginning {head!r}, not a local file header")
        members = sorted(archive.infolist(), key=lambda info: info.header_offset)
        first = members[0].header_offset if members else None
        if first != 0:
            raise RuntimeError(f"{URL} served {first} bytes before the zip's first member")
        if archive.comment:
            raise RuntimeError(f"{URL} served an archive comment of {len(archive.comment)} bytes")
        raw.seek(max(0, size - END_RECORD_SEARCH))
        tail = raw.read()
        found = tail.rfind(END_RECORD)
        if found < 0:
            raise RuntimeError(f"{URL} served a file with no end of central directory record")
        end_record = size - len(tail) + found
        comment_length = int.from_bytes(tail[found + 20 : found + 22], "little")
        record_end = end_record + END_RECORD_SIZE + comment_length
        if record_end > size:
            raise RuntimeError(
                f"{URL} served an end of central directory record declaring a comment of "
                f"{comment_length} bytes, which would end at byte {record_end} of {size}"
            )
        if record_end < size:
            raise RuntimeError(
                f"{URL} served {size - record_end} bytes after the zip's end of central directory "
                f"record, which ends at byte {record_end} of {size}"
            )
        directory_size = int.from_bytes(tail[found + 12 : found + 16], "little")
        directory_offset = int.from_bytes(tail[found + 16 : found + 20], "little")
        records_begin, first_record = end_record, "the end of central directory record"
        raw.seek(max(0, end_record - ZIP64_LOCATOR_SIZE))
        locator = raw.read(ZIP64_LOCATOR_SIZE)
        if end_record >= ZIP64_LOCATOR_SIZE and locator[: len(ZIP64_LOCATOR)] == ZIP64_LOCATOR:
            zip64_offset = int.from_bytes(locator[8:16], "little")
            raw.seek(zip64_offset)
            zip64 = raw.read(ZIP64_END_RECORD_SIZE)
            if zip64[: len(ZIP64_END_RECORD)] != ZIP64_END_RECORD:
                raise RuntimeError(
                    f"{URL} served a zip64 end of central directory locator pointing at byte "
                    f"{zip64_offset}, where no zip64 end of central directory record begins"
                )
            zip64_end = zip64_offset + 12 + int.from_bytes(zip64[4:12], "little")
            contiguous(
                zip64_end,
                "the zip64 end of central directory record",
                end_record - ZIP64_LOCATOR_SIZE,
                "its locator",
            )
            directory_size = int.from_bytes(zip64[40:48], "little")
            directory_offset = int.from_bytes(zip64[48:56], "little")
            records_begin, first_record = zip64_offset, "the zip64 end of central directory record"
        contiguous(
            directory_offset + directory_size, "the central directory", records_begin, first_record
        )
        end = member_end(raw, members[0])
        for previous, info in zip(members, members[1:], strict=False):
            contiguous(
                end, f"member {previous.filename}", info.header_offset, f"member {info.filename}"
            )
            end = member_end(raw, info)
        contiguous(end, f"member {members[-1].filename}", directory_offset, "the central directory")


def check_members(path: Path) -> None:
    """Raise unless the zip at path passes check_container and holds exactly the members FILES
    states."""
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

"""Pull readable text out of a PDF whose text is glyph-index hex strings needing `/ToUnicode` CMaps.

    python pdftext_cmap.py <path.pdf>

Writes `<path.pdf>.txt` beside the PDF and prints the CMap, page and character counts. Reads
Flate-compressed and uncompressed streams both, and for each text run picks the CMap that decodes
it best. This is the extractor for subset-font PDFs where `pdftext_literal.py` returns nothing.
Standard library only.
"""

import re
import sys
import zlib

path = sys.argv[1]
raw = open(path, "rb").read()

objs = {}
for m in re.finditer(rb"(\d+)\s+0\s+obj(.*?)endobj", raw, re.S):
    objs[int(m.group(1))] = m.group(2)


def stream_of(body):
    m = re.search(rb"stream\r?\n", body)
    if not m:
        return None
    data = body[m.end() : body.rfind(b"endstream")]
    try:
        return zlib.decompress(data)
    except Exception:
        return data


cmaps = {}
for num, body in objs.items():
    data = stream_of(body)
    if not data or (b"beginbfchar" not in data and b"beginbfrange" not in data):
        continue
    cm = {}
    for blk in re.findall(rb"beginbfchar(.*?)endbfchar", data, re.S):
        for a, b in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            cm[int(a, 16)] = bytes.fromhex(b.decode()).decode("utf-16-be", "replace")
    for blk in re.findall(rb"beginbfrange(.*?)endbfrange", data, re.S):
        for a, b, c in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            lo, hi, dst = int(a, 16), int(b, 16), int(c, 16)
            for i in range(lo, min(hi, lo + 4096) + 1):
                cm[i] = chr(dst + i - lo)
    if cm:
        cmaps[num] = cm

merged = {}
for cm in cmaps.values():
    for k, v in cm.items():
        merged.setdefault(k, v)


def decode(codes, cm):
    return "".join(cm.get(c, "") for c in codes)


def score(s, n):
    if not s:
        return -1.0
    good = sum(c.isalnum() or c in " .,;:'\"()-/%" for c in s)
    return (good / len(s)) * (len(s) / max(n, 1))


TEXT_RUN = rb"\[((?:<[0-9A-Fa-f]+>|\((?:\\.|[^()\\])*\)|[-\d.]+|\s)+)\]\s*TJ|<([0-9A-Fa-f]+)>\s*Tj"

pages = []
for body in objs.values():
    data = stream_of(body)
    if not data or b"BT" not in data:
        continue
    runs = []
    for run in re.finditer(TEXT_RUN, data):
        blob = run.group(1) if run.group(1) else b"<" + (run.group(2) or b"") + b">"
        codes = []
        for h in re.findall(rb"<([0-9A-Fa-f]+)>", blob):
            h = h.decode()
            codes.extend(int(h[i : i + 2], 16) for i in range(0, len(h) - 1, 2))
        if len(codes) % 2 == 0 and codes:
            wide = [codes[i] * 256 + codes[i + 1] for i in range(0, len(codes), 2)]
        else:
            wide = []
        best, bs = "", -1.0
        for cand in ([wide] if wide else []) + [codes]:
            for cm in list(cmaps.values()) + [merged]:
                s = decode(cand, cm)
                sc = score(s, len(cand))
                if sc > bs:
                    best, bs = s, sc
        if best:
            runs.append(best)
    txt = " ".join(runs)
    if len(txt.strip()) > 20:
        pages.append(txt)

out = "\n\n---page---\n".join(pages)
open(path + ".txt", "w", encoding="utf-8").write(out)
print("CMAPS", len(cmaps), "PAGES", len(pages), "CHARS", len(out))

"""Pull readable text out of a PDF whose content streams carry literal `(...)` strings.

    python pdftext_literal.py <path.pdf>

Writes `<path.pdf>.txt` beside the PDF and prints the page and character counts. Skips image
streams and any Flate stream that does not decompress. For a PDF whose text is glyph-index hex
strings `<...>` — subset fonts, typically — this returns little or nothing: use `pdftext_cmap.py`.
Standard library only.
"""

import re
import sys
import zlib

path = sys.argv[1]
raw = open(path, "rb").read()

pieces = []
for m in re.finditer(rb"stream\r?\n", raw):
    start = m.end()
    end = raw.find(b"endstream", start)
    if end == -1:
        continue
    try:
        data = zlib.decompress(raw[start:end])
    except Exception:
        continue
    if b"BT" not in data or b"ET" not in data:
        continue
    words = []
    for t in re.finditer(rb"\((?:\\.|[^()\\])*\)\s*(?:Tj|TJ)|\((?:\\.|[^()\\])*\)", data):
        s = t.group(0)
        s = s[: s.rfind(b")") + 1]
        s = s[s.find(b"(") + 1 : -1]
        s = re.sub(rb"\\([()\\])", rb"\1", s)
        words.append(s.decode("latin-1"))
    text = "".join(words)
    letters = sum(c.isalpha() or c.isspace() or c in ".,;:'\"-()%$&/" for c in text)
    if len(text) > 40 and letters / max(len(text), 1) > 0.85:
        pieces.append(text)

out = "\n---page---\n".join(pieces)
open(path + ".txt", "w", encoding="utf-8").write(out)
print("PAGES", len(pieces), "CHARS", len(out))

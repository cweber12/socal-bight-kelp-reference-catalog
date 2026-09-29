"""Probe one URL and print the route record `review-source` step 4 asks for.

    python probe.py <url> [--once] [--ua <string>] [--save <path>]

Fetches the URL twice by default and prints one JSON object: a `fetches` list with one entry per
fetch, and two booleans, `same_final_url` and `same_sha256`, that say whether the two fetches
agreed. Two fetches are the point: a final URL that carries a per-request token while the bytes
stay identical, and an archive whose bytes vary per request, look the same after one fetch.

Each entry records, in this order: the URL asked for, the final URL after redirects, the status
code, the byte count, `Content-Type`, the first 8 bytes as hex and as ASCII, `Content-Disposition`,
`Last-Modified`, `ETag`, and the sha256 of the body. A 4xx or 5xx answer is recorded the same way,
body included, because a 403 page's bytes are evidence about the route.

`--ua` sets the User-Agent; the default names this skill. `--save` writes the first fetch's bytes to
the path given, unmodified. `--once` fetches once. Output is ASCII-only JSON, so it prints on a
cp1252 console. Standard library only.
"""

import hashlib
import json
import sys
import urllib.error
import urllib.request

DEFAULT_UA = "kelpcatalog/review-source"
TIMEOUT = 120


def probe(url, ua):
    request = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        response = urllib.request.urlopen(request, timeout=TIMEOUT)
    except urllib.error.HTTPError as error:
        response = error
    except urllib.error.URLError as error:
        return {"url": url, "error": str(error.reason)}, b""
    with response:
        body = response.read()
        headers = response.headers
        record = {
            "url": url,
            "final_url": response.geturl(),
            "status": response.status,
            "bytes": len(body),
            "content_type": headers.get("Content-Type"),
            "first_8_hex": body[:8].hex(),
            "first_8_ascii": body[:8].decode("ascii", "replace"),
            "content_disposition": headers.get("Content-Disposition"),
            "last_modified": headers.get("Last-Modified"),
            "etag": headers.get("ETag"),
            "sha256": hashlib.sha256(body).hexdigest(),
        }
    return record, body


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    url = argv[0]
    ua = DEFAULT_UA
    save = None
    times = 2
    rest = argv[1:]
    while rest:
        flag = rest.pop(0)
        if flag == "--once":
            times = 1
        elif flag == "--ua" and rest:
            ua = rest.pop(0)
        elif flag == "--save" and rest:
            save = rest.pop(0)
        else:
            print(f"unknown or incomplete argument: {flag}")
            return 2

    fetches = []
    for i in range(times):
        record, body = probe(url, ua)
        fetches.append(record)
        if i == 0 and save is not None and body:
            with open(save, "wb") as handle:
                handle.write(body)
            record["saved_to"] = save

    out = {"user_agent": ua, "fetches": fetches}
    if times == 2:
        out["same_final_url"] = fetches[0].get("final_url") == fetches[1].get("final_url")
        out["same_sha256"] = fetches[0].get("sha256") == fetches[1].get("sha256")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/bin/sh
# Hand the PostToolUse payload on stdin to advise.py, run by the interpreter that
# `gate.py` uses, so the ruff check sees the pinned ruff rather than PATH's.
#
# Silent no-op when there is no interpreter: a fresh clone has no `.venv`, a hook
# has no `skip_if`, and an advisory check that errors on every edit is one that
# gets switched off. Both layouts `CLAUDE.md` documents are tried, Windows first.
set -u
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
for python in "$root/.venv/Scripts/python.exe" "$root/.venv/bin/python"; do
    if [ -x "$python" ]; then
        exec "$python" "$root/.claude/hooks/advise.py" "$@"
    fi
done
exit 0

"""The one command that runs every gate.

Run:  python gate.py            (from the repo root, inside the venv)

Adding a gate is adding a row to GATES. Each gate returns (passed, message). The
runner prints one row per gate, prints a failing gate's own output beneath it, and
exits non-zero if any gate fails. Gates that need machine state a fresh clone lacks
declare skip_if and are skipped there - skipping is for the clone, not the author:
run this locally before every PR.

Today there is one gate. The plan (docs/prd/) says which ones come next and when.
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from kelpcatalog import check_catalog  # noqa: E402


@dataclass(frozen=True)
class Gate:
    name: str
    fn: Callable[[], tuple[bool, str]]
    skip_if: Callable[[], str | None] | None = None


def _run(cmd: list[str]) -> tuple[bool, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    return p.returncode == 0, (p.stdout or "") + (p.stderr or "")


def gate_unit() -> tuple[bool, str]:
    return _run(
        [sys.executable, "-m", "pytest", "-q", "--cov=src/kelpcatalog", "--cov-fail-under=90"]
    )


def gate_catalog_schema() -> tuple[bool, str]:
    """Every record parses, validates, and links only to records that exist."""
    catalog, problems = check_catalog(ROOT)
    counts = ", ".join(f"{len(v)} {k}" for k, v in catalog.records.items())
    if problems:
        return False, "\n".join(str(p) for p in problems) + f"\n({counts})"
    return True, counts


GATES: list[Gate] = [
    Gate("unit", gate_unit),
    Gate("catalog-schema", gate_catalog_schema),
]


def main() -> int:
    width = max(len(g.name) for g in GATES)
    failed = 0
    for gate in GATES:
        reason = gate.skip_if() if gate.skip_if else None
        if reason:
            print(f"{gate.name:<{width}}  SKIP  {reason}")
            continue
        ok, msg = gate.fn()
        status = "ok  " if ok else "FAIL"
        first = msg.strip().splitlines()[-1] if msg.strip() else ""
        print(f"{gate.name:<{width}}  {status}  {first}")
        if not ok:
            failed += 1
            print("\n".join("    " + line for line in msg.rstrip().splitlines()))
    print(f"\n{len(GATES) - failed}/{len(GATES)} gates passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

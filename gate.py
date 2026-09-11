"""The one command that runs every gate.

Run:  python gate.py            (from the repo root, inside the venv)

Adding a gate is adding a row to GATES. Each gate returns (passed, message). The
runner prints one row per gate, prints a failing gate's own output beneath it, and
exits non-zero if any gate fails. Gates that need machine state a fresh clone lacks
declare skip_if and are skipped there - skipping is for the clone, not the author:
run this locally before every PR.

CONTEXT.md, 'Gates', is the table of what each gate asserts and the schedule for the
ones not yet here. A row here that is not a row there is a gate nothing asked for.
"""

from __future__ import annotations

import subprocess
import sys
import traceback
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from kelpcatalog import check_catalog  # noqa: E402
from kelpcatalog.figure_provenance import check_figure_provenance  # noqa: E402
from kelpcatalog.outputs import check_outputs  # noqa: E402
from kelpcatalog.structure import check_structure  # noqa: E402


@dataclass(frozen=True)
class Gate:
    name: str
    fn: Callable[[], tuple[bool, str]]
    skip_if: Callable[[], str | None] | None = None


def _run(cmd: list[str]) -> tuple[bool, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    return p.returncode == 0, (p.stdout or "") + (p.stderr or "")


def gate_unit() -> tuple[bool, str]:
    """The suite, against CONTEXT.md's "the schema seams, ≥ 90 % coverage".

    `--cov-branch` measures branches as well as lines, so a module reported at 100% can no
    longer carry an untested branch, as one in `plan.py` did - the Parking lot entry from the
    audit of #41, folded in by #68. It re-measures every module against the same floor and
    moves none of them below it.

    `--cov=gate` puts this file under the same floor as the package. #68's goal names both
    halves of the gap - "Nothing in `tests/` imports it, and `--cov=src/kelpcatalog` does not
    reach it" - and closing only the first would leave the runner's coverage unmeasured, so
    tests deleted from `tests/test_gate.py` would cost nothing.
    """
    return _run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--cov=src/kelpcatalog",
            "--cov=gate",
            "--cov-branch",
            "--cov-fail-under=90",
        ]
    )


def gate_catalog_schema() -> tuple[bool, str]:
    """Every record parses, validates, and links only to records that exist."""
    catalog, problems = check_catalog(ROOT)
    counts = ", ".join(f"{len(v)} {k}" for k, v in catalog.records.items())
    if problems:
        return False, "\n".join(str(p) for p in problems) + f"\n({counts})"
    return True, counts


def gate_notebook_structure() -> tuple[bool, str]:
    """Every topic notebook has exactly the sections its sub-topic list requires, and the
    index lists every topic.

    Reads the committed notebooks, not the builder's output: a notebook edited by hand,
    or left behind by a sub-topic added to TOPICS, fails here. It does not check that a
    notebook's counts are current with the records, and no gate does - #48 re-executes a
    notebook, and re-execution never rebuilds a markdown cell from the records. A green
    row here says the sections are right and says nothing about what is in them.
    """
    sections, problems = check_structure(ROOT)
    counts = f"{len(sections)} notebooks, {sum(len(s) for s in sections.values())} sections"
    if problems:
        return False, "\n".join(str(p) for p in problems) + f"\n({counts})"
    return True, counts


def gate_notebook_outputs() -> tuple[bool, str]:
    """Committed notebooks carry outputs and no errors.

    Read as: every code cell carries outputs, and no output is an error - the reading
    adopted in docs/prd/topic-notebooks.md and argued in #45. A notebook with no code
    cells passes with nothing to check, which is all eleven today, because generated
    cells are markdown and the only code cell a notebook ever has is a figure (#47).
    The strict reading - every notebook carries outputs - would fail a topic notebook
    for not yet having a figure, which is a gate asserting content.

    Reads the committed notebooks, never a re-execution: that is #48, and not
    re-executing is why this row can run in CI while that one cannot.
    """
    cells, problems = check_outputs(ROOT)
    counts = f"{len(cells)} notebooks, {sum(len(c) for c in cells.values())} code cells"
    if problems:
        return False, "\n".join(str(p) for p in problems) + f"\n({counts})"
    return True, counts


def gate_figure_provenance() -> tuple[bool, str]:
    """Every figure cell carries a `provenance(...)` whose ids resolve.

    A figure cell is a code cell the builder did not generate; CONTEXT.md says figure
    cells are "never generated and never touched". The ids are read out of the committed
    cell's source with `ast` and resolved against the records, so this row never executes
    a notebook and runs in CI - which is also why an id has to be written out as a string
    rather than computed.

    It says nothing about what the cell *rendered*: a figure cell whose outputs carry no
    image passes here, and so does a `provenance()` naming nothing. Both were put to #46
    and both are answered in figure_provenance.py's docstring, where the Gates row they
    would each need is named.
    """
    cells, problems = check_figure_provenance(ROOT)
    counts = f"{len(cells)} notebooks, {sum(len(c) for c in cells.values())} figure cells"
    if problems:
        return False, "\n".join(str(p) for p in problems) + f"\n({counts})"
    return True, counts


def gate_lint() -> tuple[bool, str]:
    """`ruff check` and `ruff format --check`, the two commands CI's lint job runs.

    Without this row the module docstring's "the one command that runs every gate" was false:
    ruff ran only in CI, so a green `gate.py` was strictly weaker than a green CI - #68 records
    three PR bodies carrying that caveat by hand. Both commands run even when the first fails,
    so one run reports both.

    Run through `-m` rather than the `ruff` console script so the row uses the interpreter's
    own ruff rather than whatever is first on PATH. That, plus pinning `ruff` in the dev extra
    and pointing CI's lint job at that extra, is what makes "this row is green" and "CI's lint
    job is green" the same claim: before #68 the gate job installed `.[dev]` while the lint job
    installed the newest release, so a ruff that added a rule landed as a red CI on a PR that
    was green locally.
    """
    failed = []
    output = []
    for label, argv in (
        ("ruff check", ["check", "."]),
        ("ruff format --check", ["format", "--check", "."]),
    ):
        passed, out = _run([sys.executable, "-m", "ruff", *argv])
        if not passed:
            failed.append(label)
            output.append(out.rstrip())
    if failed:
        return False, "\n".join(output) + "\n" + " and ".join(failed) + " failed"
    return True, "ruff check and ruff format --check clean"


GATES: list[Gate] = [
    Gate("unit", gate_unit),
    Gate("catalog-schema", gate_catalog_schema),
    Gate("notebook-structure", gate_notebook_structure),
    Gate("notebook-outputs", gate_notebook_outputs),
    Gate("figure-provenance", gate_figure_provenance),
    Gate("lint", gate_lint),
]


def main() -> int:
    """Run every gate, print one row each, and exit non-zero if any failed.

    A gate that raises is reported as a failure rather than taking the run down, so the rows
    after it still run and the traceback arrives beneath its own row instead of replacing the
    whole report. `Exception`, not `BaseException`: a KeyboardInterrupt still stops the run.

    A skipped gate is not counted as a pass. It is not counted as a failure either - the
    module docstring says skipping "is for the clone, not the author", so a skip leaves the
    exit code alone and shows up as the gap between the passed count and the total.
    """
    width = max(len(g.name) for g in GATES)
    failed = 0
    skipped = 0
    for gate in GATES:
        reason = gate.skip_if() if gate.skip_if else None
        if reason:
            skipped += 1
            print(f"{gate.name:<{width}}  SKIP  {reason}")
            continue
        try:
            ok, msg = gate.fn()
        except Exception:
            ok, msg = False, traceback.format_exc()
        status = "ok  " if ok else "FAIL"
        first = msg.strip().splitlines()[-1] if msg.strip() else ""
        print(f"{gate.name:<{width}}  {status}  {first}")
        if not ok:
            failed += 1
            print("\n".join("    " + line for line in msg.rstrip().splitlines()))
    summary = f"\n{len(GATES) - failed - skipped}/{len(GATES)} gates passed"
    if skipped:
        summary += f", {skipped} skipped"
    print(summary)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

"""The committed notebooks, read back and checked for the outputs their code cells carry.

CONTEXT.md, "Gates": `notebook-outputs` asserts that "committed notebooks carry outputs and
no errors". This module is that assertion; gate.py's row is the two lines that print it.

Seams:
    check_outputs(root) -> (code cells checked, problems)   the whole of the gate

**The reading.** That sentence admits two, and the one adopted in
docs/prd/topic-notebooks.md, "Readings adopted", and argued in #45 is: *every code cell
carries outputs, and no output is an error*. A notebook with no code cells passes with
nothing to check - which is all eleven today, because generated cells are markdown
(CONTEXT.md, "Notebooks") and the only code cell a notebook ever has is a figure, the first
of which is #47. The strict reading - every *notebook* carries outputs - would fail a topic
notebook for not yet having a figure, and CONTEXT.md's own Gates preamble forbids that: "A
gate never fails because the catalog grew; counts are printed, not asserted."

So this row says nothing at all today, and is here for the moment after #47: CONTEXT.md
commits notebooks "with outputs so they read on GitHub without running", and a figure cell
committed without its outputs is a blank where the figure should be.

**Why a stderr stream is one of the failures.** An error output is the obvious half of "no
errors". A stderr stream is the other: it is how a kernel reports a problem that did not
raise, and the 6.2 spike (PRD finding 7) produced exactly that - a figure attempt whose sole
output was a stderr stream carrying the kernel's own PID path, `ipykernel_27100`, and no
image at all. That path differs on every run, so such a cell can never reproduce its
committed output and `notebook-fresh` (#48) would fail on it for good. stdout is not a
failure: a print() in a figure cell is output, which is what this row asks for.

**What it does not assert**, so that a reader does not take more from a green row than it
says. It never re-executes - that is #48, and not re-executing is why this row runs in CI
while that one cannot. It does not read what an output *contains*, only that one exists and
is not an error, so a figure whose committed PNG has gone stale passes here. It does not
check provenance (#46). And it does not assert that a notebook is **present**: CONTEXT.md
puts "every topic notebook" on `notebook-structure`, which reports a missing one, so
reporting it here as well would print one absence under two gate names. A file that is there
and cannot be read *is* reported, because this gate cannot then show that it carries
anything.

A gate reports; it does not fix. Nothing here writes.

nbformat is a dev dependency, so - like build.py and structure.py - this module is
deliberately not imported by `kelpcatalog/__init__.py`: `import kelpcatalog` must work in a
runtime install.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import nbformat
from nbformat import NotebookNode

from .generate import NOTEBOOKS_DIR
from .plan import INDEX_PATH, NOTEBOOK_PATHS
from .schema import TOPICS, Problem

# nbformat's own vocabulary for a cell and for the outputs it can hold.
CODE = "code"
ERROR = "error"
STREAM = "stream"
STDERR = "stderr"

NO_OUTPUTS = "carries no outputs"
UNREADABLE = "is not a notebook this gate can read"
NOTEBOOK_FIELD = "notebook"

# A message names a cell so a reader can go to it; a traceback or a multi-line warning
# belongs at the cell, not in the gate's output.
MESSAGE_CHARS = 120
ELLIPSIS = "…"


def _the_eleven() -> Iterator[str]:
    """Each notebook's path under the repo root.

    Derived from the same three public names `structure.py` derives its walk from, rather
    than from that module: the fact is `plan.py`'s, and the two gates ask different things
    of it. A third caller (#48) is the point at which one shared walk earns its keep.
    """
    yield f"{NOTEBOOKS_DIR}/{INDEX_PATH}"
    for topic in TOPICS:
        yield f"{NOTEBOOKS_DIR}/{NOTEBOOK_PATHS[topic]}"


def _inline(value: object) -> str:
    """One line of a message: whitespace collapsed, and never a whole traceback."""
    text = " ".join(str(value or "").split())
    return text if len(text) <= MESSAGE_CHARS else text[:MESSAGE_CHARS] + ELLIPSIS


def _name(cell: NotebookNode, position: int) -> str:
    """What a message calls the cell: its id, or where it sits when it has none.

    A notebook older than cell ids (nbformat_minor 4) reads back without them, and
    `nbformat.read` does not mint one. The cell is still a cell a reader has to be sent to.
    """
    return str(cell.get("id") or f"cell {position}")


def _code_cells(notebook: NotebookNode) -> list[tuple[str, NotebookNode]]:
    """(name, cell) for every code cell, in the order the notebook holds them.

    Code cells alone: a markdown cell has no `outputs` and never will, so a gate that read
    one would fail every notebook in the repo over the sections it is made of.
    """
    return [
        (_name(cell, position), cell)
        for position, cell in enumerate(notebook.cells)
        if cell.get("cell_type") == CODE
    ]


def _output_problem(output: NotebookNode) -> str | None:
    """Why this one output fails the gate, or None. See the module docstring on stderr."""
    kind = output.get("output_type")
    if kind == ERROR:
        return f"carries an error output: {_inline(output.get('ename'))}"
    if kind == STREAM and output.get("name") == STDERR:
        return f"carries a stderr stream: {_inline(output.get('text'))}"
    return None


def _cell_problems(cell: NotebookNode) -> list[str]:
    """Every way one code cell's outputs are wrong, in the order the cell holds them.

    Every output, not the first: a cell that plots and then raises carries the figure ahead
    of the traceback, so a gate that read `outputs[0]` would pass it.
    """
    outputs = list(cell.get("outputs") or [])
    if not outputs:
        return [NO_OUTPUTS]
    return [problem for problem in map(_output_problem, outputs) if problem is not None]


def check_outputs(root: Path) -> tuple[dict[str, list[str]], list[Problem]]:
    """The code cells each committed notebook holds, and every way their outputs are wrong.

    Counts are the caller's to print, never to assert: a gate never fails because the
    catalog grew (CONTEXT.md, "Gates").
    """
    root = Path(root)
    checked: dict[str, list[str]] = {}
    problems: list[Problem] = []
    for rel in _the_eleven():
        path = root / rel
        # is_file(), and no problem when it is false: a missing notebook is the structure
        # gate's to report (see the module docstring), and so is a directory standing where
        # one should be.
        if not path.is_file():
            continue
        try:
            notebook = nbformat.read(path, as_version=4)
        # Broad on purpose: the file is arbitrary bytes, and whatever a reader raises over
        # it is the one fact this gate has to report. A gate returns (passed, message); one
        # that raised would take gate.py down on exactly the hand-edited notebook it exists
        # to catch.
        except Exception as e:
            problems.append(Problem(rel, NOTEBOOK_FIELD, f"{UNREADABLE}: {e}"))
            continue
        cells = _code_cells(notebook)
        checked[rel] = [name for name, _ in cells]
        problems += [
            Problem(rel, name, message) for name, cell in cells for message in _cell_problems(cell)
        ]
    return checked, problems

"""The committed notebooks, re-executed and compared against the outputs they carry.

CONTEXT.md, "Gates": `notebook-fresh` asserts that "re-executing a notebook reproduces its
committed outputs (local; needs `data/` for figures)". This module is that assertion;
gate.py's row is the two lines that print it.

Seams:
    differences(committed, executed) -> [(cell, what differs)]   the comparison
    execute(notebook, folder) -> NotebookNode                    the run
    check_fresh(root) -> (cells re-executed, problems)           the whole of the gate
    skip_reason(root) -> str | None                              why it cannot run here

**What it catches, and what the others already catch.** A committed notebook's source and its
outputs are both just bytes in one file, and nothing about the file says whether the second
followed from the first. The other three notebook rows read those bytes, so each catches the
edits that make the bytes themselves wrong: `notebook-outputs` fails a code cell whose outputs
were deleted, or edited into an error or a stderr stream, and `figure-provenance` reads the
committed source with `ast`, so it fails a source edit that drops `provenance(...)` or mistypes
an id. What none of them can see is an edit that leaves well-formed bytes behind - an output
retyped into another plausible non-error output, or a source edit that still ends in a
resolvable `provenance(...)`. Those reproduce nothing and look like nothing, and running the
cells again is the only way to ask. That is why this row costs a kernel, and it is the only one
that does.

**Why it is local, and what `skip_if` means here.** PNG bytes depend on the platform and the
plotting stack, so a byte comparison cannot hold across the Ubuntu and Windows CI runners,
and `data/` is git-ignored - a fresh clone has nothing for a figure cell to load. CONTEXT.md
already scopes the row "local", `skip_reason` is that clause, and gate.py counts a skip apart
from a pass so that a run which never executed anything does not read like one that did. The
row skips in CI and the author runs it: gate.py's own docstring, "skipping is for the clone,
not the author: run this locally before every PR".

**The three fields compared**, per #48: `execution_count`, `outputs` and cell source. Not
`metadata.execution`, which `record_timing` fills with wall-clock times - a notebook executed
by hand in Jupyter records them and one this module executes does not, so comparing them
would report every hand-run notebook as stale. Code cells only: a markdown cell is never
executed and has nothing to reproduce.

**Notebook-level metadata is not compared at all**, which decides a question #48 does not
ask. Executing a notebook stamps `metadata.language_info` with the running machine's Python
patch version, and `11_ocean_climate` is committed carrying `kernelspec` alone because #47
stripped it. Whether a *committed* notebook may carry `language_info` is therefore a live
question - it is on the Parking lot, with the builder rather than a gate as the proposed
owner - and it is not this row's: CONTEXT.md's row quantifies over the outputs a
re-execution reproduces, and a row here that is not a row there is a gate nothing asked for
(gate.py's docstring). The comparison walks cells, so the key never enters it either way.

**What it does not assert**, so that a reader does not take more from a green row than it
says.

1. **Nothing about whether a figure is right.** The comparison is a re-execution against the
   committed outputs, so a cell that consistently draws the wrong thing reproduces itself
   exactly. The Parking lot carries five readings of what `figure-provenance` leaves open -
   an invented axis unit, an asserted title, a mark traced to a number computed in the cell -
   and this row closes none of them.
2. **Nothing about a generated markdown cell being current with the records.** Re-execution
   never rebuilds one: markdown cells are not executed, and the builder is what writes them.
   No row asserts it, which gate.py's `notebook-structure` docstring already says of itself.
3. **Nothing about a notebook that is absent.** A file that is not there has no outputs to
   reproduce, and this row's quantifier is the weakest of the four: CONTEXT.md writes it over
   "**a** notebook" where `notebook-structure` is "**every** topic notebook" and
   `figure-provenance` is "**every** figure cell". So the silence is better grounded here than
   the same silence is in `outputs.py`, which argued it from the absence of a clause rather
   than from a weaker one. `structure.py` does report a missing notebook, under the "every" its
   own row carries.

A gate reports; it does not fix. Nothing here writes - not into the repo and not into
`data/`, and a notebook found stale is reported rather than rewritten (#48: "Does not rewrite
a stale notebook - a gate reports"). Nor does it fetch: if `data/` is missing the row skips,
it does not go and get it.

`_the_eleven`, `_name` and `_code_cells` are a fourth copy of the walk `structure.py`,
`outputs.py` and `figure_provenance.py` each carry, derived like all three from the public
names in `plan.py` and `generate.py` rather than from any of them. Extracting one walk is on
the Parking lot, which has twice declined to do it inside a slice that adds a gate, and its
caveat still holds: `structure.py` reports a missing notebook and the other two deliberately
do not, so a merge has to decide that first.

nbclient and nbformat are dev dependencies, so - like build.py, structure.py, outputs.py and
figure_provenance.py - this module is deliberately not imported by `kelpcatalog/__init__.py`:
`import kelpcatalog` must work in a runtime install. It imports `DATA_DIR` from
`kelpcatalog.notebook`, which is the directory `load()` reaches into - so the row skips on the
absence of the directory a figure cell loads from, and not on the absence of the file itself.
A `data/` that exists and holds nothing satisfies the predicate: the row then runs, the figure
cell raises inside the kernel, and the failure names the exception rather than pretending the
notebook is stale (`_raised_now`). Closing the gap at the predicate instead would mean knowing
which files each figure will ask for before running it, which is what 6.5's `data-lock.json`
makes possible and nothing here can do. Found by the audit of PR #71.

Two consequences of that, stated because neither is visible from the row's wording. The verdict
depends on what `data/` *holds*, not only on whether it is there, and those bytes are living
data: `noaa_oni`'s `oni.ascii.txt` gains a row each month, and the committed figure plots every
row it finds - so re-fetching turns this row red on an unchanged commit, and refreshing `data/`
obliges you to re-commit the figure. And running `gate.py` now executes whatever code the
committed notebooks carry, unsandboxed, on any machine holding a `data/`; that follows from
CONTEXT.md's row and is not avoidable while the row exists, but it is a change in what running
the gate means. Both are on the Parking lot as part of one Gates-table question.
"""

from __future__ import annotations

import copy
from collections.abc import Iterator
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbformat import NotebookNode

from .generate import NOTEBOOKS_DIR
from .notebook import DATA_DIR
from .plan import INDEX_PATH, NOTEBOOK_PATHS
from .schema import TOPICS, Problem

# nbformat's own vocabulary for the cell and output fields this gate compares.
CODE = "code"
SOURCE = "source"
EXECUTION_COUNT = "execution_count"
OUTPUTS = "outputs"
OUTPUT_TYPE = "output_type"
ERROR = "error"
ENAME = "ename"
EVALUE = "evalue"

# A message names a cell so a reader can go to it; a traceback or a paragraph-long evalue
# belongs at the cell, not in the gate's output. The same cap `outputs.py` uses.
MESSAGE_CHARS = 120
ELLIPSIS = "…"

NOTEBOOK_FIELD = "notebook"

SOURCE_DIFFERS = "was not the source that was executed"
UNREADABLE = "is not a notebook this gate can read"
NOT_EXECUTED = "could not be re-executed"

# Why the row cannot run here. `data/` is git-ignored and reproducible from `src/fetch/`
# (CONTEXT.md, "Record format"), so a fresh clone and every CI runner has none, and a figure
# cell that loads a catalogued file by id has nothing to load.
NO_DATA = f"no {DATA_DIR}/, which a figure cell loads its file from"

# Seconds one cell may take. nbclient's own default is no timeout at all, which would leave a
# cell waiting on a prompt or a dead server hanging `gate.py` with nothing printed and no way
# back but Ctrl-C. Generous against what is here - the whole of `check_fresh` over the
# committed tree, kernel start included, measured at 1.5 s - because a figure that fetches or
# reads a large file is a slow cell rather than a broken one, and a gate that failed one would
# be wrong. A run that does hit it is reported, not raised: see check_fresh.
TIMEOUT = 300


def _cleared(notebook: NotebookNode) -> NotebookNode:
    """A copy with every code cell's outputs and execution count thrown away.

    A copy because `NotebookClient` mutates the notebook it is handed, and the committed one
    is the other half of the comparison. Cleared because a run that was handed the committed
    outputs could pass by giving them back: nothing a kernel executes comes from them, so
    dropping them costs nothing and makes the comparison a reproduction rather than an echo.
    """
    fresh = copy.deepcopy(notebook)
    for _, cell in _code_cells(fresh):
        cell[OUTPUTS] = []
        cell[EXECUTION_COUNT] = None
    return fresh


def execute(notebook: NotebookNode, folder: Path) -> NotebookNode:
    """The notebook run from `folder`, with its outputs replaced by what the kernel produced.

    `record_timing=False`, the condition the 6.2 spike found byte-identical runs under (PRD
    finding 7): with it on, nbclient stamps a wall-clock `metadata.execution` into every
    executed cell and no two runs match.

    `folder` is the notebook's own directory, because that is where Jupyter runs it -
    `notebook.py`: "a notebook runs with its own folder as the working directory - two levels
    under the root for a topic notebook". `load()` walks up from the working directory to find
    `catalog/`, so the repo root would resolve the figure too; it is the wrong choice because a
    cell reaching for a relative path would then work under this gate and not under Jupyter,
    and the gate would be the one that is wrong.

    No `kernel_name`: nbclient then reads the notebook's own `metadata.kernelspec`, which the
    builder writes onto any notebook holding a figure (`build.KERNEL`). A notebook is
    re-executed under the kernel it declares.

    `allow_errors=True`, so a cell that has started raising produces an error output instead of
    an exception out of the gate, and the comparison then reports it against whatever that cell
    committed. Without it the run stops at the first such cell and the rest of the notebook is
    never reached. A traceback is an output like any other here, and a difference message names
    fields and never their values, so it does not land in the gate's report.
    """
    client = NotebookClient(
        _cleared(notebook),
        timeout=TIMEOUT,
        allow_errors=True,
        record_timing=False,
        resources={"metadata": {"path": str(folder)}},
    )
    return client.execute()


def _the_eleven() -> Iterator[str]:
    """Each notebook's path under the repo root."""
    yield f"{NOTEBOOKS_DIR}/{INDEX_PATH}"
    for topic in TOPICS:
        yield f"{NOTEBOOKS_DIR}/{NOTEBOOK_PATHS[topic]}"


def _name(cell: NotebookNode, position: int) -> str:
    """What a message calls the cell: its id, or where it sits when it has none."""
    return str(cell.get("id") or f"cell {position}")


def _code_cells(notebook: NotebookNode) -> list[tuple[str, NotebookNode]]:
    """(name, cell) for every code cell, in the order the notebook holds them."""
    return [
        (_name(cell, position), cell)
        for position, cell in enumerate(notebook.cells)
        if cell.get("cell_type") == CODE
    ]


def _differing_keys(committed: NotebookNode, executed: NotebookNode) -> list[str]:
    """The fields of one output that the two do not agree on, in a fixed order."""
    return sorted(key for key in {*committed, *executed} if committed.get(key) != executed.get(key))


def _inline(value: object) -> str:
    """One line of a message: whitespace collapsed, and never a whole traceback."""
    text = " ".join(str(value or "").split())
    return text if len(text) <= MESSAGE_CHARS else text[:MESSAGE_CHARS] + ELLIPSIS


def _raised_now(committed: list, executed: list) -> str | None:
    """The error the re-execution hit that the committed outputs do not carry, or None.

    The cause rather than the symptom, and it is reported ahead of everything else because
    the symptom arrives first otherwise: an error output changes the output *count*, so a
    cell that raised would be reported as "re-executes with 1 outputs, not the committed 2"
    - a sentence a reader cannot act on, and one indistinguishable from a notebook that is
    merely stale. The audit of PR #71 measured exactly that against a `data/` that exists
    and holds nothing: `load()` raises inside the kernel, and the exception naming the
    missing directory sat inside the output this gate declines to print.

    The asymmetry is the whole of the claim - an error on the re-executed side that the
    committed side does not carry - and nothing here says a committed notebook may not hold
    an error output. When both sides carry one, the ordinary field comparison decides it.

    `evalue` as well as `ename`, capped: "FileNotFoundError" says a file is missing and
    `evalue` says which, which is the difference between a message that ends the search and
    one that starts it.
    """
    if any(output.get(OUTPUT_TYPE) == ERROR for output in committed):
        return None
    raised = next((output for output in executed if output.get(OUTPUT_TYPE) == ERROR), None)
    if raised is None:
        return None
    return (
        "re-executes to an error the committed outputs do not carry: "
        f"{_inline(raised.get(ENAME))}: {_inline(raised.get(EVALUE))}"
    )


def _output_difference(committed: list, executed: list) -> str | None:
    """The first way this cell's outputs are not what re-execution produced, or None.

    The first, not all of them: the notebook is one click away, and a cell whose outputs
    have moved is read there rather than diffed here. Field names, never values - a
    `display_data` carries a PNG as one base64 string, and a gate row is not where that
    belongs. The one exception is an error that is new, above: there the value is the cause.
    """
    raised = _raised_now(committed, executed)
    if raised is not None:
        return raised
    if len(committed) != len(executed):
        return f"re-executes with {len(executed)} outputs, not the committed {len(committed)}"
    for position, (before, after) in enumerate(zip(committed, executed, strict=True)):
        keys = _differing_keys(before, after)
        if keys:
            kind = before.get(OUTPUT_TYPE)
            return f"output {position} ({kind}) differs in {', '.join(keys)}"
    return None


def _cell_differences(committed: NotebookNode, executed: NotebookNode) -> list[str]:
    """Every way one code cell's re-execution is not what it carries.

    The three fields #48 names - `execution_count`, `outputs` and cell source - and not
    `metadata.execution`, which `record_timing` stamps with wall-clock times: a notebook
    executed by hand in Jupyter records them and one this gate executes does not, and
    comparing them would report every such notebook as stale.
    """
    messages = []
    if committed.get(SOURCE) != executed.get(SOURCE):
        messages.append(SOURCE_DIFFERS)
    if committed.get(EXECUTION_COUNT) != executed.get(EXECUTION_COUNT):
        messages.append(
            f"re-executes as {EXECUTION_COUNT} {executed.get(EXECUTION_COUNT)}, "
            f"not the committed {committed.get(EXECUTION_COUNT)}"
        )
    outputs = _output_difference(
        list(committed.get(OUTPUTS) or []), list(executed.get(OUTPUTS) or [])
    )
    if outputs is not None:
        messages.append(outputs)
    return messages


def differences(committed: NotebookNode, executed: NotebookNode) -> list[tuple[str, str]]:
    """(cell, what differs) for every code cell whose re-execution is not what is committed.

    Code cells alone, paired by the order they sit in. A markdown cell is never executed
    and carries no `outputs` or `execution_count`, so comparing one would report its
    absence of both against every notebook in the repo.

    A count mismatch is reported once, against the notebook: with the counts unequal there
    is no pairing to name a cell from, and a comparator that zipped them would drop the
    unpaired cells in silence.
    """
    before = _code_cells(committed)
    after = _code_cells(executed)
    if len(before) != len(after):
        return [
            (
                NOTEBOOK_FIELD,
                f"re-executes with {len(after)} code cells, not the committed {len(before)}",
            )
        ]
    return [
        (name, message)
        for (name, first), (_, second) in zip(before, after, strict=True)
        for message in _cell_differences(first, second)
    ]


def skip_reason(root: Path) -> str | None:
    """Why `notebook-fresh` cannot run against this tree, or None.

    `gate.py`'s `skip_if`, and the repo's first real one. CONTEXT.md scopes this row "local;
    needs `data/` for figures", and `data/` is the whole of the condition: it is git-ignored,
    so a fresh clone and every CI runner lacks it and a figure cell has nothing to load.

    A skip is not a pass - `gate.py` counts it separately - and it is not a fetch either.
    #48: "if `data/` is missing the gate skips, it does not go and get it."
    """
    return None if (Path(root) / DATA_DIR).is_dir() else NO_DATA


def check_fresh(root: Path) -> tuple[dict[str, list[str]], list[Problem]]:
    """The code cells re-executed in each committed notebook, and every way they differ.

    Counts are the caller's to print, never to assert: a gate never fails because the
    catalog grew (CONTEXT.md, "Gates").

    A notebook holding no code cell is walked and not executed. There is nothing in it for a
    kernel to reproduce, so the verdict is the same either way and a kernel is what costs
    time here - ten of the eleven are in that state today, because generated cells are
    markdown and the only code cell a notebook ever has is a figure.

    A notebook is mapped to the cells that were re-executed and compared, so one that could
    not be read or could not be run counts nothing: the row's number is what was checked, not
    what was walked past.
    """
    root = Path(root)
    checked: dict[str, list[str]] = {}
    problems: list[Problem] = []
    for rel in _the_eleven():
        path = root / rel
        # is_file(), and no problem when it is false: a file that is not there has no outputs
        # for this row to reproduce, and neither does a directory standing where a notebook
        # should be. `structure.py` does report a missing notebook, as its own choice - not a
        # division of labour CONTEXT.md draws (see outputs.py).
        if not path.is_file():
            continue
        try:
            committed = nbformat.read(path, as_version=4)
        # Broad on purpose: the file is arbitrary bytes, and whatever a reader raises over it
        # is the one fact this gate has to report. A gate returns (passed, message); one that
        # raised would take gate.py down on exactly the hand-edited notebook it exists to
        # catch.
        except Exception as e:
            problems.append(Problem(rel, NOTEBOOK_FIELD, f"{UNREADABLE}: {e}"))
            continue
        checked[rel] = []
        cells = _code_cells(committed)
        if not cells:
            continue
        try:
            executed = execute(committed, path.parent)
        # Broad for the same reason, and the ways are several: a kernel the notebook names
        # that is not installed, one that dies mid-run, a cell that outlives TIMEOUT. The
        # class name is kept because "No such kernel named python3" alone does not say what
        # kind of failure it was.
        except Exception as e:
            message = f"{NOT_EXECUTED}: {type(e).__name__}: {e}"
            problems.append(Problem(rel, NOTEBOOK_FIELD, message))
            continue
        checked[rel] = [name for name, _ in cells]
        problems += [
            Problem(rel, name, message) for name, message in differences(committed, executed)
        ]
    return checked, problems

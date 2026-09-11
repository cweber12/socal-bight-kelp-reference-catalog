"""The committed notebooks, read back and checked for the citation each figure cell carries.

CONTEXT.md, "Gates": `figure-provenance` asserts that "every figure cell carries a
`provenance(...)` whose ids resolve". This module is that assertion; gate.py's row is the
two lines that print it.

Seams:
    check_figure_provenance(root) -> (figure cells checked, problems)   the whole of the gate

**What a figure cell is.** A code cell that does not carry the builder's `kelpcatalog:
generated` marker. CONTEXT.md says "figure cells are never generated and never touched",
so a generated cell is not one; and its notebook shape names no other kind of code cell -
sections 1 to 5 are generated markdown, and section 2 ends "then any figures". That is a
reading of the shape rather than a sentence CONTEXT.md prints, and it is the reading this
gate takes: a code cell that is not generated is a figure cell and must carry a citation.
Today the question is moot, because the builder emits markdown cells only and no notebook
carries a code cell at all (the first is #47).

**It reads the cell's source, never its outputs and never a run.** The ids are parsed out
of the committed text with `ast`, which is why this row can run in CI: there is no kernel
there, and there is none in this repo yet. Two consequences are worth stating rather than
leaving to be discovered. An id has to be *written out* as a string for the gate to see
it, so a computed id list is reported rather than passed - a gate that reads source can
only check what is written. And the check that the call comes last is the same fact as the
caption *appearing*: a cell's value is its last expression's, so a `provenance(...)` with a
statement after it renders nothing at all. It is not the same fact as the caption appearing
*under* the figure, which is CONTEXT.md's word and which this gate does not secure - see
`notebook.Provenance` on the output order a kernel would actually write, which is #47's to
settle against a running one.

**What it does not assert**, so that a reader does not take more from a green row than it
says. Two questions were put to this slice and both are answered *no*, because CONTEXT.md's
row states its assertion in full and a row here that is not a row there is a gate nothing
asked for (gate.py's docstring). Neither is deferred to another gate: no row asserts
either today, so closing one means amending CONTEXT.md's Gates table, and both are on the
Parking lot as that.

1. **A figure cell whose outputs carry no image passes** (#46's comment, from #45). A cell
   whose sole output is a `stream` satisfies `notebook-outputs` too, so a figure that
   silently stopped plotting reads on GitHub as a caption with nothing above it and
   `gate.py` stays green - the shape PRD finding 7 records the 6.2 spike producing. It is
   not closed here for the reason above, and for a second: matplotlib is not installed,
   nothing in this repo has ever been executed, and a check written today could only be
   tested against a hand-built output dict standing in for what a kernel emits. #47 is
   where the first real committed figure output exists to write it against.
2. **A `provenance()` naming nothing passes.** It carries a call, and its zero ids
   resolve. CONTEXT.md's "The rule" is the ground for failing it - "every mark on the
   figure traces to a record or a printed equation, and a `provenance(...)` caption under
   the figure says which", and a caption naming nothing says nothing - but that is the
   rule's ground, not the row's, so it is the same amendment as the first.

It also does not check *where* a figure sits: the ids resolve identically under the wrong
heading, so renaming a sub-topic relocates a figure silently. That is on the Parking lot
too, filed before this slice.

A gate reports; it does not fix. Nothing here writes.

nbformat is a dev dependency, so - like build.py, structure.py and outputs.py - this
module is deliberately not imported by `kelpcatalog/__init__.py`. `kelpcatalog.notebook`,
which a notebook imports and which defines the call this gate matches, is the other half
of the same split: it depends on nothing but the standard library and the schema.
"""

from __future__ import annotations

import ast
from collections.abc import Iterator
from pathlib import Path

import nbformat
from nbformat import NotebookNode

from .build import is_generated
from .generate import NOTEBOOKS_DIR
from .notebook import EQUATION_SEP, EQUATIONS, PROVENANCE, REFERENCES, SOURCES
from .plan import INDEX_PATH, NOTEBOOK_PATHS
from .schema import TOPICS, Catalog, Problem, load_catalog

CODE = "code"
NOTEBOOK_FIELD = "notebook"

# IPython's own syntax, which is not Python: a line magic or a shell escape is a
# SyntaxError to ast.parse, and a cell magic hands the whole cell to something other than
# the Python compiler. The first two are blanked and the cell read without them; the third
# leaves nothing this gate can read.
LINE_MAGIC = ("%", "!")
CELL_MAGIC = "%%"

KEYWORDS = (SOURCES, REFERENCES, EQUATIONS)
NAMED = ", ".join(f"{name}=" for name in KEYWORDS[:-1]) + f" and {KEYWORDS[-1]}="

NO_PROVENANCE = f"does not end in {PROVENANCE}(...)"
UNREADABLE_CELL = "is not Python this gate can read"
CELL_MAGIC_MESSAGE = f"opens with a cell magic, so it {UNREADABLE_CELL}"
POSITIONAL = f"names its ids positionally; {PROVENANCE}(...) takes {NAMED}"
UNPACKED = f"unpacks its keywords; {PROVENANCE}(...) must name {NAMED}"
UNREADABLE_NOTEBOOK = "is not a notebook this gate can read"


def _the_eleven() -> Iterator[str]:
    """Each notebook's path under the repo root.

    The third derivation of this walk, after `structure.py` and `outputs.py`, and derived
    like both from the three public names in `plan.py` and `generate.py` rather than from
    either module: the fact is the plan's, and the three gates ask different things of it.
    Extracting one walk is on the Parking lot, which named #48 as the third caller before
    this slice arrived ahead of it; it is a refactor across two shipped gates, so it is not
    folded into this one.
    """
    yield f"{NOTEBOOKS_DIR}/{INDEX_PATH}"
    for topic in TOPICS:
        yield f"{NOTEBOOKS_DIR}/{NOTEBOOK_PATHS[topic]}"


def _name(cell: NotebookNode, position: int) -> str:
    """What a message calls the cell: its id, or where it sits when it has none.

    A notebook older than cell ids (nbformat_minor 4) reads back without them, and
    `nbformat.read` does not mint one. The cell is still a cell a reader has to be sent to.
    """
    return str(cell.get("id") or f"cell {position}")


def _figure_cells(notebook: NotebookNode) -> list[tuple[str, NotebookNode]]:
    """(name, cell) for every figure cell, in the order the notebook holds them."""
    return [
        (_name(cell, position), cell)
        for position, cell in enumerate(notebook.cells)
        if cell.get("cell_type") == CODE and not is_generated(cell)
    ]


def _is_magic(line: str) -> bool:
    """Whether this line is IPython's rather than Python's."""
    return line.lstrip().startswith(LINE_MAGIC)


def _without_magics(source: str) -> str:
    """The cell's source with IPython's line magics and shell escapes blanked out.

    Blanked rather than dropped so that a line number in a SyntaxError still points at the
    line a reader would count to.
    """
    return "\n".join("" if _is_magic(line) else line for line in source.splitlines())


def _parse(source: str) -> tuple[ast.Module | None, str | None]:
    """The cell as a syntax tree, or why it could not be read.

    Plain Python first, and a cell that parses that way is never looked at again: a `%` or
    a `!` inside a string is then a string, not a magic, and blanking the line it sits on
    would corrupt the cell to no purpose. Only a cell that does *not* parse can be IPython,
    and that is the only one the rest of this reaches.

    A `%%` line is a cell magic, which hands the whole cell to something that is not the
    Python compiler - so there is nothing here to read - and it is legal only as the first
    line. One below the first is broken IPython, which is equally unreadable, so the search
    is over every line: blanking such a line as though it were a line magic made the rest
    of the cell parse and pass. Found by the audit of PR #67.
    """
    try:
        return ast.parse(source), None
    except SyntaxError:
        pass
    if any(line.lstrip().startswith(CELL_MAGIC) for line in source.splitlines()):
        return None, CELL_MAGIC_MESSAGE
    try:
        return ast.parse(_without_magics(source)), None
    # The message comes from the second parse, not the first: the first failed on a line
    # this gate has since accounted for, so its "invalid syntax" would point at a magic
    # that is not the problem.
    except SyntaxError as e:
        return None, f"{UNREADABLE_CELL}: {e.msg}"


def _callee(call: ast.Call) -> str | None:
    """The trailing name of what is being called: `provenance` or `nb.provenance`."""
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return None


def _magic_below(source: str, line: int) -> bool:
    """Whether any line of the source past `line` (1-indexed) is IPython's.

    The trailing half of "ends with". A magic is blanked before the cell is parsed, so the
    tree cannot see one standing after the last statement - and IPython runs it after the
    call, which makes the cell's value the magic's rather than the caption's. Checked
    against the source as written, which is the only place it survives.
    """
    return any(_is_magic(text) for text in source.splitlines()[line:])


def _the_call(tree: ast.Module, source: str) -> ast.Call | None:
    """The `provenance(...)` the cell ends with, or None if it does not end with one.

    Last, because a cell's value is its last expression's: a call with a statement after
    it, or one whose value is assigned, renders no caption under the plot. A comment after
    it is not a statement and displaces nothing; a magic is neither, and is handled above.
    """
    if not tree.body:
        return None
    last = tree.body[-1]
    if not isinstance(last, ast.Expr) or not isinstance(last.value, ast.Call):
        return None
    if _callee(last.value) != PROVENANCE or _magic_below(source, last.end_lineno or 0):
        return None
    return last.value


def _ids(call: ast.Call) -> tuple[dict[str, list[str]], list[str]]:
    """The ids the call names, by keyword, and every way the call cannot be read.

    `ast.literal_eval` rather than reading the nodes: a list of string literals is exactly
    what it evaluates, and anything it refuses is something this gate cannot check.
    """
    found: dict[str, list[str]] = {}
    problems: list[str] = []
    if call.args:
        problems.append(POSITIONAL)
    for keyword in call.keywords:
        if keyword.arg is None:
            problems.append(UNPACKED)
            continue
        if keyword.arg not in KEYWORDS:
            problems.append(f"{PROVENANCE}(...) takes no {keyword.arg!r} keyword")
            continue
        try:
            value = ast.literal_eval(keyword.value)
        except (ValueError, SyntaxError):
            value = None
        if not isinstance(value, (list, tuple)) or not all(isinstance(v, str) for v in value):
            problems.append(f"{keyword.arg}= must be a list of strings written out, not computed")
            continue
        found[keyword.arg] = list(value)
    return found, problems


def _equations_on(citekey: str, catalog: Catalog) -> set[str] | None:
    """The equation ids a reference record prints, or None if there is no such record."""
    for record in catalog.records["references"]:
        if record.id == citekey:
            return {
                str(entry["id"])
                for entry in record.data.get("equations") or []
                if isinstance(entry, dict) and "id" in entry
            }
    return None


def _equation_problem(equation_id: str, catalog: Catalog) -> str | None:
    """Why an `equations` id resolves to nothing, or None.

    An equation hangs off the reference that prints it (`equations: list of {id,
    as_printed, where}`), so the id names both: `<citekey>/<equation id>`.
    """
    citekey, separator, equation = equation_id.partition(EQUATION_SEP)
    if not separator or not citekey or not equation or EQUATION_SEP in equation:
        return f"{equation_id!r} must be <citekey>{EQUATION_SEP}<equation id>"
    printed = _equations_on(citekey, catalog)
    if printed is None:
        return f"{citekey!r} is not a reference record"
    if equation not in printed:
        return f"{equation!r} is not an equation on {citekey!r}"
    return None


def _resolve_problems(found: dict[str, list[str]], catalog: Catalog) -> list[str]:
    """Every id in the call that resolves to no record, in the order the call names them."""
    problems: list[str] = []
    for source_id in found.get(SOURCES, []):
        if source_id not in catalog.ids("sources"):
            problems.append(f"{source_id!r} is not a source record")
    for citekey in found.get(REFERENCES, []):
        if citekey not in catalog.ids("references"):
            problems.append(f"{citekey!r} is not a reference record")
    for equation_id in found.get(EQUATIONS, []):
        problem = _equation_problem(equation_id, catalog)
        if problem is not None:
            problems.append(problem)
    return problems


def _cell_problems(cell: NotebookNode, catalog: Catalog) -> list[str]:
    """Every way one figure cell's citation is wrong, in the order a reader meets them."""
    source = str(cell.get("source") or "")
    tree, unreadable = _parse(source)
    if tree is None:
        return [unreadable] if unreadable else []
    call = _the_call(tree, source)
    if call is None:
        return [NO_PROVENANCE]
    found, problems = _ids(call)
    return problems + _resolve_problems(found, catalog)


def check_figure_provenance(root: Path) -> tuple[dict[str, list[str]], list[Problem]]:
    """The figure cells each committed notebook holds, and every way their citations are wrong.

    Counts are the caller's to print, never to assert: a gate never fails because the
    catalog grew (CONTEXT.md, "Gates"). Records that do not parse are not in the catalog
    and their ids do not resolve here; `catalog-schema` is the row that diagnoses them.
    """
    root = Path(root)
    catalog, _ = load_catalog(root)
    checked: dict[str, list[str]] = {}
    problems: list[Problem] = []
    for rel in _the_eleven():
        path = root / rel
        # is_file(), and no problem when it is false: a file that is not there carries no
        # figure cell for this row to assert about, and neither does a directory standing
        # where a notebook should be. `structure.py` does report a missing notebook, as
        # its own choice - not a division of labour CONTEXT.md draws (see outputs.py).
        if not path.is_file():
            continue
        try:
            notebook = nbformat.read(path, as_version=4)
        # Broad on purpose: the file is arbitrary bytes, and whatever a reader raises over
        # it is the one fact this gate has to report. A gate returns (passed, message); one
        # that raised would take gate.py down on exactly the hand-edited notebook it exists
        # to catch.
        except Exception as e:
            problems.append(Problem(rel, NOTEBOOK_FIELD, f"{UNREADABLE_NOTEBOOK}: {e}"))
            continue
        cells = _figure_cells(notebook)
        checked[rel] = [name for name, _ in cells]
        problems += [
            Problem(rel, name, message)
            for name, cell in cells
            for message in _cell_problems(cell, catalog)
        ]
    return checked, problems

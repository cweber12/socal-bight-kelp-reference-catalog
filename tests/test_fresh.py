"""Tests for the notebook-fresh gate: what re-executing a committed notebook produces.

Three kinds of test, and the split is about what each can witness.

**The comparator** (`differences`) is pure and is tested against hand-built cells. Two of its
arms cannot be reached through `check_fresh` at all - a differing source, and a differing
number of code cells - because what the gate executes is a copy of what it compares against.
They are tested here because this is the only place they can be.

**The execution path** is tested against notebooks a kernel really ran. A hand-built output
would prove nothing here: the whole question this gate asks is whether a kernel reproduces
what is committed, and an output nobody executed has no answer to it. The notebooks are tiny
(`1 + 1`), so they need a kernel but no `data/`, and they run in CI.

**The committed tree** is the one thing that needs `data/`, because `11_ocean_climate`'s
figure cell loads a catalogued file. Those tests are skipped without it, exactly as the gate
row is. The skip condition is written out here rather than imported from `kelpcatalog.fresh`,
so a `skip_reason` that stopped looking at `data/` would strand these tests as skipped rather
than move both sides together.
"""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

from kelpcatalog import fresh
from kelpcatalog.build import write_notebook
from kelpcatalog.fresh import (
    NO_DATA,
    NOT_EXECUTED,
    NOTEBOOK_FIELD,
    UNREADABLE,
    check_fresh,
    differences,
    execute,
    skip_reason,
)
from kelpcatalog.generate import NOTEBOOKS_DIR
from kelpcatalog.plan import INDEX_PATH, NOTEBOOK_PATHS
from kelpcatalog.schema import TOPICS

ROOT = Path(__file__).parents[1]

OCEAN_CLIMATE = NOTEBOOK_PATHS["ocean-climate"]

# The gate's own skip condition, typed out rather than imported - see the module docstring.
needs_data = pytest.mark.skipif(
    not (ROOT / "data").is_dir(), reason="the committed figure loads a catalogued file"
)

KERNEL = {"display_name": "Python 3", "language": "python", "name": "python3"}


def rel(path: str) -> str:
    return f"{NOTEBOOKS_DIR}/{path}"


# --- the comparator --------------------------------------------------------------------


def a_cell(source: str = "1 + 1", outputs=(), execution_count=1, **metadata):
    cell = new_code_cell(source, outputs=list(outputs), execution_count=execution_count)
    cell.metadata.update(metadata)
    return cell


def a_result(text: str = "2"):
    return new_output("execute_result", data={"text/plain": text}, execution_count=1)


def a_notebook(*cells):
    notebook = new_notebook(cells=list(cells))
    notebook.metadata[KERNELSPEC] = dict(KERNEL)
    return notebook


KERNELSPEC = "kernelspec"


def test_a_cell_that_re_executes_to_what_it_carries_has_no_differences():
    cell = a_cell(outputs=[a_result()])

    assert differences(a_notebook(cell), a_notebook(copy.deepcopy(cell))) == []


def test_a_committed_output_edited_by_hand_is_named_with_its_cell_and_its_key():
    committed = a_cell(outputs=[a_result("3")])
    executed = a_cell(outputs=[a_result("2")])

    assert differences(a_notebook(committed), a_notebook(executed)) == [
        (committed.id, "output 0 (execute_result) differs in data")
    ]


def test_a_cell_that_re_executes_to_a_different_number_of_outputs_says_so():
    committed = a_cell(outputs=[a_result()])
    executed = a_cell(outputs=[a_result(), a_result("4")])

    (_, message) = differences(a_notebook(committed), a_notebook(executed))[0]

    assert message == "re-executes with 2 outputs, not the committed 1"


def test_a_cell_that_re_executes_under_a_different_count_says_so():
    committed = a_cell(outputs=[a_result()], execution_count=7)
    executed = a_cell(outputs=[a_result()], execution_count=1)

    (_, message) = differences(a_notebook(committed), a_notebook(executed))[0]

    assert message == "re-executes as execution_count 1, not the committed 7"


def test_a_source_that_differs_from_the_one_executed_says_so():
    """Unreachable through `check_fresh` - see the module docstring - and the one arm of the
    comparison that names no output, because nothing was run from the committed text."""
    committed = a_cell(source="1 + 1", outputs=[a_result()])
    executed = a_cell(source="2 + 2", outputs=[a_result()])

    (_, message) = differences(a_notebook(committed), a_notebook(executed))[0]

    assert message == "was not the source that was executed"


def test_a_cell_carrying_execution_timings_compares_equal_to_one_without():
    """`record_timing` stamps wall-clock times into `metadata.execution`, so a notebook run
    by hand in Jupyter carries them and one this gate executes does not. #48: do not compare
    `metadata.execution`."""
    timings = {"iopub.status.idle": "2026-09-11T00:00:00Z"}
    committed = a_cell(outputs=[a_result()], execution=timings)
    executed = a_cell(outputs=[a_result()])

    assert differences(a_notebook(committed), a_notebook(executed)) == []


def test_a_notebook_that_re_executes_to_a_different_number_of_code_cells_says_so():
    """The other arm `check_fresh` cannot reach. Reported once, against the notebook rather
    than a cell: with the counts unequal there is no pairing to name a cell from, and a
    comparator that zipped them would silently drop the unpaired ones."""
    committed = a_notebook(a_cell(), a_cell())
    executed = a_notebook(a_cell())

    assert differences(committed, executed) == [
        (NOTEBOOK_FIELD, "re-executes with 1 code cells, not the committed 2")
    ]


def test_markdown_cells_are_not_compared():
    """A markdown cell has no outputs and is never executed, so it has nothing to reproduce.
    Counting it would also break the pairing: the committed and executed notebooks agree on
    it by construction, but a comparator over every cell would report its absent
    `execution_count` as a difference."""
    committed = a_notebook(new_markdown_cell("# a heading"), a_cell(outputs=[a_result()]))
    executed = a_notebook(new_markdown_cell("# a heading"), a_cell(outputs=[a_result()]))

    assert differences(committed, executed) == []


def test_a_cell_with_no_id_is_named_by_where_it_sits():
    """A notebook older than cell ids reads back without them, and `nbformat.read` does not
    mint one. The cell is still a cell a reader has to be sent to."""
    committed = a_notebook(a_cell(outputs=[a_result("3")]))
    executed = a_notebook(a_cell(outputs=[a_result("2")]))
    for notebook in (committed, executed):
        notebook.cells[0].pop("id", None)

    (name, _) = differences(committed, executed)[0]

    assert name == "cell 0"


# --- executing ---------------------------------------------------------------------------
#
# A kernel really runs here. Every notebook below is `1 + 1` and `os.getcwd()`, so it needs a
# kernel but no `data/`, and one module-scoped execution serves the whole section: starting a
# kernel is the expensive thing in this file, and these tests all ask about one run.

CWD_CELL = "import os; os.getcwd()"

# What the committed cell wrongly claims `1 + 1` produced. A kernel that were handed the
# committed outputs and gave them back would return this.
STALE = "99"


def a_written_notebook(folder: Path):
    """A notebook on disk whose first cell carries an output no kernel would produce."""
    notebook = a_notebook(a_cell("1 + 1", outputs=[a_result(STALE)]), a_cell(CWD_CELL, outputs=()))
    write_notebook(notebook, folder / "probe.ipynb")
    return notebook


@pytest.fixture(scope="module")
def one_execution(tmp_path_factory):
    """(the notebook as committed, what `execute` made of it, the folder it ran in)."""
    folder = tmp_path_factory.mktemp("executed")
    committed = a_written_notebook(folder)
    return committed, execute(copy.deepcopy(committed), folder), folder


def test_execute_returns_what_the_kernel_produced(one_execution):
    _, executed, _ = one_execution

    cell = executed.cells[0]

    assert cell.execution_count == 1
    assert [output.data["text/plain"] for output in cell.outputs] == ["2"]


def test_execute_discards_the_outputs_it_is_given_rather_than_handing_them_back(one_execution):
    """A gate that handed the committed outputs to the executor and compared what came back
    could pass on an executor that echoed them. Nothing is executed from those bytes, so they
    are cleared first and the comparison is against a run that never saw them."""
    committed, executed, _ = one_execution

    assert committed.cells[0].outputs[0].data["text/plain"] == STALE
    assert executed.cells[0].outputs[0].data["text/plain"] != STALE


def test_execute_runs_in_the_folder_it_is_given(one_execution):
    """CONTEXT.md puts a topic notebook two levels under the root and `notebook.py` says "a
    notebook runs with its own folder as the working directory". Asserted as a path equality:
    `tmp_path` carries this test's own name, so a substring check would pass on the path."""
    _, executed, folder = one_execution

    printed = executed.cells[1].outputs[0].data["text/plain"]

    assert Path(printed.strip("'\"")).resolve() == folder.resolve()


def test_execute_records_no_timings(one_execution):
    """`record_timing=False`. With it on, every executed cell carries a wall-clock
    `metadata.execution` and no two runs ever match."""
    _, executed, _ = one_execution

    assert [cell.metadata.get("execution") for cell in executed.cells] == [None, None]


def test_execute_leaves_the_notebook_it_is_given_alone(one_execution):
    """`NotebookClient` mutates the notebook it is handed. The committed one is the other
    half of the comparison, so a gate that handed it over would compare it with itself and
    pass on anything."""
    committed, _, _ = one_execution

    assert committed.cells[0].outputs[0].data["text/plain"] == STALE
    assert committed.cells[1].outputs == []


# --- the walk ----------------------------------------------------------------------------


@pytest.fixture(scope="module")
def as_this_gate_runs_it(tmp_path_factory):
    """A one-cell notebook whose outputs a kernel really produced, timings off."""
    folder = tmp_path_factory.mktemp("committed")
    return execute(a_notebook(a_cell("1 + 1", outputs=())), folder)


@pytest.fixture(scope="module")
def as_jupyter_would(tmp_path_factory):
    """The same notebook executed the way Jupyter executes one: with timings recorded."""
    folder = tmp_path_factory.mktemp("jupyter")
    notebook = a_notebook(a_cell("1 + 1", outputs=()))
    client = NotebookClient(notebook, resources={"metadata": {"path": str(folder)}})
    return client.execute()


def a_repo(tmp_path: Path, notebook, path: str = OCEAN_CLIMATE) -> Path:
    """A repo root holding one notebook, at a path the gate walks.

    One notebook, not eleven: executing a notebook costs a kernel, and the ten that are not
    there carry nothing for this row to assert about.
    """
    write_notebook(notebook, tmp_path / NOTEBOOKS_DIR / path)
    return tmp_path


def problems(root: Path):
    return check_fresh(root)[1]


def test_a_notebook_whose_committed_outputs_re_execute_unchanged_passes(
    tmp_path, as_this_gate_runs_it
):
    root = a_repo(tmp_path, copy.deepcopy(as_this_gate_runs_it))

    checked, found = check_fresh(root)

    assert found == [], "\n".join(str(p) for p in found)
    assert checked == {rel(OCEAN_CLIMATE): [as_this_gate_runs_it.cells[0].id]}


def test_a_committed_output_edited_by_hand_fails_and_names_the_cell(tmp_path, as_this_gate_runs_it):
    committed = copy.deepcopy(as_this_gate_runs_it)
    committed.cells[0].outputs[0].data["text/plain"] = "3"
    root = a_repo(tmp_path, committed)

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert problem.field == committed.cells[0].id
    # On the message, not on str(problem): tmp_path carries this test's own name.
    assert problem.message == "output 0 (execute_result) differs in data"


def test_a_source_edited_without_re_executing_fails(tmp_path, as_this_gate_runs_it):
    """The committed outputs are the old source's. Nothing about the file says so - the
    source and its outputs are both just bytes - so only a re-execution finds it."""
    committed = copy.deepcopy(as_this_gate_runs_it)
    committed.cells[0].source = "2 + 2"
    root = a_repo(tmp_path, committed)

    (problem,) = problems(root)

    assert problem.field == committed.cells[0].id
    assert problem.message == "output 0 (execute_result) differs in data"


def test_a_notebook_executed_by_hand_in_jupyter_is_not_reported_as_stale(
    tmp_path, as_jupyter_would
):
    """The timings are real here, not hand-written: this fixture went through a kernel with
    `record_timing` left at nbclient's default, which is what Jupyter does."""
    assert as_jupyter_would.cells[0].metadata["execution"], "the fixture must carry timings"

    assert problems(a_repo(tmp_path, copy.deepcopy(as_jupyter_would))) == []


def test_a_notebook_with_no_code_cells_is_walked_and_never_executed(tmp_path, monkeypatch):
    """Ten of the eleven hold no code cell today, and a kernel is the expensive thing here.
    A notebook with nothing to execute reproduces its nothing whatever a kernel would do."""
    monkeypatch.setattr(
        fresh, "execute", lambda *a, **k: pytest.fail("a notebook with no code cells was executed")
    )
    root = a_repo(tmp_path, a_notebook(new_markdown_cell("# a heading")))

    checked, found = check_fresh(root)

    assert found == []
    assert checked == {rel(OCEAN_CLIMATE): []}


def test_a_notebook_that_cannot_be_executed_is_reported_against_the_notebook(
    tmp_path, monkeypatch, as_this_gate_runs_it
):
    """A kernel that is not installed, one that dies, a cell that runs past the timeout. A
    gate returns a verdict; one that raised would take `gate.py` down on exactly the notebook
    it exists to report on."""

    def boom(notebook, folder):
        raise RuntimeError("No such kernel named python3")

    monkeypatch.setattr(fresh, "execute", boom)
    root = a_repo(tmp_path, copy.deepcopy(as_this_gate_runs_it))

    checked, (problem,) = check_fresh(root)

    assert problem.field == NOTEBOOK_FIELD
    assert problem.message == f"{NOT_EXECUTED}: RuntimeError: No such kernel named python3"
    assert checked == {rel(OCEAN_CLIMATE): []}, "nothing was re-executed, so nothing is counted"


def test_a_notebook_that_cannot_be_read_is_reported_against_the_notebook(tmp_path):
    path = tmp_path / NOTEBOOKS_DIR / OCEAN_CLIMATE
    path.parent.mkdir(parents=True)
    path.write_text("not a notebook", encoding="utf-8")

    checked, (problem,) = check_fresh(tmp_path)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert problem.field == NOTEBOOK_FIELD
    assert problem.message.startswith(UNREADABLE)
    assert checked == {}


def test_a_missing_notebook_carries_nothing_to_check(tmp_path):
    assert check_fresh(tmp_path) == ({}, [])


def test_a_topic_whose_notebook_is_not_generated_is_walked_and_skipped(
    tmp_path, monkeypatch, as_this_gate_runs_it
):
    """The walk grows with TOPICS, and a path with no file behind it is skipped in silence."""
    monkeypatch.setitem(TOPICS, "sea-level", ())
    monkeypatch.setitem(NOTEBOOK_PATHS, "sea-level", "1_physical_environment/15_sea_level.ipynb")
    root = a_repo(tmp_path, copy.deepcopy(as_this_gate_runs_it))

    checked, found = check_fresh(root)

    assert found == []
    assert set(checked) == {rel(OCEAN_CLIMATE)}


# --- the committed tree ------------------------------------------------------------------


@pytest.fixture(scope="module")
def the_committed_tree():
    """The gate run against the real repo, once. This is the expensive call in the file -
    it starts a kernel and re-draws the committed figure - and both tests below read it."""
    return check_fresh(ROOT)


@needs_data
def test_the_committed_notebooks_re_execute_to_what_they_carry(the_committed_tree):
    """Needs `data/`, because `11_ocean_climate`'s figure cell loads a catalogued file -
    which is the whole of why CONTEXT.md scopes this row local.

    The paths, not `len(checked) == 11`: a count is blind to a walk that grows. The
    re-executed cell count is deliberately not asserted - it goes up with the next figure.
    """
    checked, found = the_committed_tree

    assert found == [], "\n".join(str(p) for p in found)
    assert set(checked) == {rel(INDEX_PATH), *(rel(p) for p in NOTEBOOK_PATHS.values())}


@needs_data
def test_the_committed_figure_notebook_is_the_one_that_is_re_executed(the_committed_tree):
    """Stated rather than left to the reader: ten of the eleven hold no code cell, so a green
    row over eleven notebooks is a green row over one execution."""
    checked, _ = the_committed_tree

    assert {path for path, cells in checked.items() if cells} == {rel(OCEAN_CLIMATE)}


# --- skipping ----------------------------------------------------------------------------


def test_there_is_no_reason_to_skip_when_data_is_there(tmp_path):
    (tmp_path / "data").mkdir()

    assert skip_reason(tmp_path) is None


def test_the_reason_to_skip_is_that_data_is_not_there(tmp_path):
    """`data/` is git-ignored, so a fresh clone and every CI runner has none."""
    assert skip_reason(tmp_path) == NO_DATA


def test_a_file_called_data_is_not_a_data_directory(tmp_path):
    (tmp_path / "data").write_text("", encoding="utf-8")

    assert skip_reason(tmp_path) == NO_DATA

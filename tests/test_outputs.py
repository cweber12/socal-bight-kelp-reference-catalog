"""Tests for the notebook-outputs gate: what a committed notebook's code cells carry.

The gate reads `notebooks/`, so every test below writes a notebook to disk and asks what
the gate says about the file. The notebooks are constructed here with `nbformat.v4`
rather than committed as fixture `.ipynb` files, and the reason is particular to this
gate: the builder emits markdown cells and no outputs at all, so there is no builder run
that produces a code cell carrying an error, a stderr stream or an empty `outputs` list.
A committed fixture would therefore be hand-written JSON, and hand-written JSON is a
weaker witness than `nbformat.v4.new_output`, which is the same constructor nbformat
validates against. `a_repo` validates each notebook before it is written.

That buys less than it sounds like, and the limit belongs here rather than in a reader's
head: validating shows nbformat would *accept* a shape, not that a kernel *emits* it. The v4
schema types a stream's `name` as a bare string with no enum, so `name: "STDERR"` and
`name: ""` both validate, neither is anything Jupyter writes, and this gate passes both.
Nothing here can close that gap while the repo has no kernel in it - `nbclient` and
`ipykernel` arrive with #48.
"""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import (
    new_code_cell,
    new_markdown_cell,
    new_notebook,
    new_output,
    new_raw_cell,
)

from kelpcatalog.build import write_notebook
from kelpcatalog.generate import NOTEBOOKS_DIR
from kelpcatalog.outputs import MESSAGE_CHARS, check_outputs
from kelpcatalog.plan import INDEX_PATH, NOTEBOOK_PATHS
from kelpcatalog.schema import TOPICS

ROOT = Path(__file__).parents[1]

OCEAN_CLIMATE = NOTEBOOK_PATHS["ocean-climate"]


def rel(path: str) -> str:
    return f"{NOTEBOOKS_DIR}/{path}"


def problems(root: Path):
    return check_outputs(root)[1]


# --- the committed tree --------------------------------------------------------------


def test_the_committed_notebooks_pass_and_are_read_back_by_path():
    # Green here is vacuous today and the gate row says so out loud - it prints "11
    # notebooks, 0 code cells", because generated cells are markdown and the first figure
    # is #47. The code-cell count is deliberately not asserted: it goes up when #47 lands.
    #
    # The paths, not `len(checked) == 11`: a count is blind to a walk that *grows*. A topic
    # added to TOPICS and NOTEBOOK_PATHS whose notebook has not been generated is skipped
    # silently, which leaves the count at eleven and this test green. NOTEBOOK_PATHS rather
    # than TOPICS, so the expectation is not read off the same name the walk iterates;
    # test_plan.py pins the two against each other.
    checked, found = check_outputs(ROOT)

    assert found == [], "\n".join(str(p) for p in found)
    assert set(checked) == {rel(INDEX_PATH), *(rel(p) for p in NOTEBOOK_PATHS.values())}


def test_a_topic_whose_notebook_is_not_generated_is_walked_and_skipped(monkeypatch):
    # The hazard the test above is written against, stated rather than left implicit: the
    # walk grows with TOPICS, and a path with no file behind it is skipped in silence. The
    # count is eleven either way, so only an assertion on the paths notices.
    monkeypatch.setitem(TOPICS, "sea-level", ())
    monkeypatch.setitem(NOTEBOOK_PATHS, "sea-level", "1_physical_environment/15_sea_level.ipynb")

    checked, found = check_outputs(ROOT)

    assert found == []
    assert len(checked) == 11
    assert rel(NOTEBOOK_PATHS["sea-level"]) not in checked


# --- constructing a notebook the gate will read ---------------------------------------


def a_code_cell(source: str = "provenance()", outputs=(), execution_count=1):
    return new_code_cell(source, outputs=list(outputs), execution_count=execution_count)


def an_error(ename: str = "ZeroDivisionError"):
    return new_output(
        "error", ename=ename, evalue="division by zero", traceback=["Traceback…", "…"]
    )


def a_stream(name: str, text: str):
    return new_output("stream", name=name, text=text)


def a_display():
    return new_output("display_data", data={"text/plain": "<Figure size 640x480>"})


def a_repo(tmp_path: Path, *cells, path: str = OCEAN_CLIMATE, minor: int | None = None) -> Path:
    """A repo root holding one notebook, at a path the gate walks.

    One notebook, not eleven: the gate reports on the notebooks that are there, and the ten
    that are not carry nothing for it to assert about - pinned below by
    `test_a_missing_notebook_carries_nothing_to_check`. So each test here holds only the
    cells it is about.
    """
    notebook = new_notebook(cells=list(cells))
    if minor is not None:
        # A notebook older than cell ids. nbformat writes and reads it without minting
        # one, so the cell reaches the gate unnamed.
        notebook.nbformat_minor = minor
        for cell in notebook.cells:
            cell.pop("id", None)
    # The witness that these constructions are shapes nbformat would accept. A test that
    # exercised an invalid notebook would prove nothing about a notebook Jupyter wrote.
    nbformat.validate(notebook)
    write_notebook(notebook, tmp_path / NOTEBOOKS_DIR / path)
    return tmp_path


# --- what fails ------------------------------------------------------------------------


def test_a_code_cell_with_no_outputs_fails_and_names_the_notebook_and_the_cell(tmp_path: Path):
    cell = a_code_cell()
    root = a_repo(tmp_path, cell)

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert problem.field == cell.id
    # On the message, not on str(problem): tmp_path carries this test's own name, so a
    # message quoting an absolute path could spell almost anything.
    assert "no outputs" in problem.message


def test_a_cell_carrying_an_error_output_fails_and_names_the_cell(tmp_path: Path):
    cell = a_code_cell(outputs=[an_error()])
    root = a_repo(tmp_path, cell)

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert problem.field == cell.id
    assert problem.message.startswith("carries an error output")
    assert "ZeroDivisionError" in problem.message


def test_a_cell_whose_output_is_a_stderr_stream_fails(tmp_path: Path):
    # #45: the spike showed a warning carrying a per-run kernel PID path
    # (`ipykernel_27100`), which differs on every re-execution and would break #48.
    cell = a_code_cell(outputs=[a_stream("stderr", "…/ipykernel_27100/1234.py:3: UserWarning")])
    root = a_repo(tmp_path, cell)

    (problem,) = problems(root)

    assert problem.field == cell.id
    assert problem.message.startswith("carries a stderr stream")
    assert "ipykernel_27100" in problem.message


def test_a_long_multi_line_warning_is_reported_on_one_line(tmp_path: Path):
    # gate.py prints a failing gate's whole output, so a cell whose stderr is forty lines
    # of warning would bury the other rows. The message points at the cell; the text is at
    # the cell. MESSAGE_CHARS builds the input rather than being asserted against, so this
    # keeps exercising truncation whatever the cap is set to.
    text = "a warning\nover several lines\n" * MESSAGE_CHARS
    root = a_repo(tmp_path, a_code_cell(outputs=[a_stream("stderr", text)]))

    (problem,) = problems(root)

    assert "\n" not in problem.message
    assert len(problem.message) < len(text)
    assert problem.message.endswith("…")


# --- what passes -----------------------------------------------------------------------


def test_a_notebook_of_markdown_cells_only_passes(tmp_path: Path):
    root = a_repo(tmp_path, new_markdown_cell("# ocean-climate"), new_markdown_cell("## salinity"))

    assert problems(root) == []


def test_a_code_cell_that_carries_an_output_passes(tmp_path: Path):
    # The positive control: without it every assertion above would still hold for a gate
    # that failed every code cell it met.
    root = a_repo(tmp_path, a_code_cell(outputs=[a_display()]))

    assert problems(root) == []


def test_a_stdout_stream_is_not_an_error(tmp_path: Path):
    # A print() in a figure cell is output, not a failure. Only stderr is treated as one.
    root = a_repo(tmp_path, a_code_cell(outputs=[a_stream("stdout", "1950 to 2026\n")]))

    assert problems(root) == []


def test_a_raw_cell_is_not_a_code_cell(tmp_path: Path):
    raw = new_raw_cell("no outputs here")
    root = a_repo(tmp_path, raw)

    checked, found = check_outputs(root)

    assert found == []
    assert checked[rel(OCEAN_CLIMATE)] == []


def test_a_code_cell_with_no_source_still_needs_an_output(tmp_path: Path):
    # An empty code cell produces nothing when run, so it can never satisfy the rule; the
    # fix is to delete the cell. Exempting it would be the gate deciding what a notebook
    # may contain, which is more than CONTEXT.md's row asks of it.
    root = a_repo(tmp_path, a_code_cell(source="", execution_count=None))

    (problem,) = problems(root)

    assert problem.message == "carries no outputs"


# --- every failure is reported, not the first ------------------------------------------


def test_an_error_output_is_reported_even_beside_a_good_one(tmp_path: Path):
    # A cell that plots and then raises carries the figure first and the traceback after,
    # so a gate that looked only at outputs[0] would pass it.
    cell = a_code_cell(outputs=[a_display(), an_error()])
    root = a_repo(tmp_path, cell)

    (problem,) = problems(root)

    assert problem.field == cell.id
    assert problem.message.startswith("carries an error output")


def test_every_bad_code_cell_in_a_notebook_is_reported(tmp_path: Path):
    empty, failed, good = (
        a_code_cell(),
        a_code_cell(outputs=[an_error()]),
        a_code_cell(outputs=[a_display()]),
    )
    root = a_repo(tmp_path, empty, new_markdown_cell("## heatwaves"), failed, good)

    found = problems(root)

    assert [p.field for p in found] == [empty.id, failed.id]


def test_every_bad_notebook_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_code_cell())
    a_repo(tmp_path, a_code_cell(), path=INDEX_PATH)

    assert sorted(p.path for p in problems(root)) == [rel(INDEX_PATH), rel(OCEAN_CLIMATE)]


# --- what the gate reads back ----------------------------------------------------------


def test_it_reads_back_the_code_cells_it_checked(tmp_path: Path):
    first, second = a_code_cell(outputs=[a_display()]), a_code_cell(outputs=[a_display()])
    root = a_repo(tmp_path, new_markdown_cell("# ocean-climate"), first, second)

    checked, _ = check_outputs(root)

    assert checked[rel(OCEAN_CLIMATE)] == [first.id, second.id]


def test_a_cell_older_than_cell_ids_is_named_by_its_position(tmp_path: Path):
    # nbformat_minor 4 has no cell id, and `nbformat.read` does not mint one. The cell is
    # still a cell a message has to point at, so it is named by where it sits.
    root = a_repo(tmp_path, new_markdown_cell("# ocean-climate"), a_code_cell(), minor=4)

    (problem,) = problems(root)

    assert problem.field == "cell 1"


# --- a notebook the gate cannot read ---------------------------------------------------


def test_a_notebook_that_cannot_be_read_fails_and_names_it(tmp_path: Path):
    # A gate returns (passed, message); one that raised would take gate.py down on exactly
    # the hand-edited notebook it exists to catch.
    root = a_repo(tmp_path, a_code_cell(outputs=[a_display()]))
    (root / NOTEBOOKS_DIR / OCEAN_CLIMATE).write_text("{ not json", encoding="utf-8")

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert problem.field == "notebook"
    # Written out, and over bytes that do not themselves contain it: nbformat quotes the
    # file's own content back in its error, so a file reading "not a notebook" makes an
    # `in problem.message` assertion pass on the file rather than on the gate. That is
    # what it did here until a mutation sweep changed this string and nothing failed.
    assert problem.message.startswith("is not a notebook this gate can read")
    assert "JSON" in problem.message


def test_a_missing_notebook_carries_nothing_to_check(tmp_path: Path):
    # This row is about what committed notebooks carry, and a file that is not there
    # carries nothing. Not because CONTEXT.md assigns the absence to `notebook-structure`:
    # that row quantifies over the notebooks that exist too, and `structure.py` reporting a
    # missing one is its own choice. See the module docstring.
    checked, found = check_outputs(tmp_path)

    assert found == []
    assert checked == {}


def test_a_directory_where_a_notebook_should_be_is_not_read(tmp_path: Path):
    # `is_file()`, not `exists()`: a directory holds no code cells, so it carries nothing
    # for this row to assert about, exactly as a missing file does.
    root = a_repo(tmp_path, a_code_cell(outputs=[a_display()]))
    target = root / NOTEBOOKS_DIR / OCEAN_CLIMATE
    target.unlink()
    target.mkdir()

    assert problems(root) == []

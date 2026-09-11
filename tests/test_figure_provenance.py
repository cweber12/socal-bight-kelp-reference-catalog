"""Tests for the figure-provenance gate: the citation a committed figure cell carries.

The gate reads `notebooks/` and `catalog/`, so every test below writes both to disk and
asks what the gate says about the files. It never executes a notebook and never imports
one: the ids are read out of the cell's *source text*, so the fixtures are cell sources,
and a cell that would raise when run is checked here exactly as one that would not.

The notebooks are constructed with `nbformat.v4` rather than committed as fixture
`.ipynb` files, for the same reason `tests/test_outputs.py` gives: the builder emits
markdown cells only, so no builder run produces a figure cell at all, and a committed
fixture would be hand-written JSON. `a_repo` validates each notebook before writing it.

What that buys, stated so a reader does not take more: `nbformat.validate` shows the
notebook is a shape nbformat accepts, and says nothing about whether a kernel would emit
the cell's outputs - this gate reads no outputs, so the question does not arise here the
way it does for `notebook-outputs`. What it *cannot* show is that the cell sources below
are ones #47 will write, because nothing in this repo has been executed and `matplotlib`
is not installed. The plotting lines in these fixtures are stand-ins, and the gate never
looks at them.
"""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import (
    new_code_cell,
    new_markdown_cell,
    new_notebook,
    new_raw_cell,
)

from kelpcatalog.build import write_notebook
from kelpcatalog.figure_provenance import check_figure_provenance
from kelpcatalog.generate import NOTEBOOKS_DIR
from kelpcatalog.plan import INDEX_PATH, NOTEBOOK_PATHS
from kelpcatalog.schema import TOPICS

ROOT = Path(__file__).parents[1]

OCEAN_CLIMATE = NOTEBOOK_PATHS["ocean-climate"]

# A stand-in for whatever #47 plots. The gate reads the last statement and nothing else,
# so what stands above it only has to be Python.
PLOT = "plt.plot([1, 2])"


def rel(path: str) -> str:
    return f"{NOTEBOOKS_DIR}/{path}"


def problems(root: Path):
    return check_figure_provenance(root)[1]


def messages(root: Path) -> list[str]:
    return [p.message for p in problems(root)]


# --- the committed tree --------------------------------------------------------------


def test_the_committed_notebooks_pass_and_are_read_back_by_path():
    # Green here is vacuous today and the gate row says so out loud - it prints "11
    # notebooks, 0 figure cells", because all eleven are markdown only and the first
    # figure is #47. The figure-cell count is deliberately not asserted: it goes up then.
    #
    # The paths, not `len(checked) == 11`: a count is blind to a walk that *grows*. A
    # topic added to TOPICS and NOTEBOOK_PATHS whose notebook has not been generated is
    # skipped silently, which leaves the count at eleven and this test green.
    checked, found = check_figure_provenance(ROOT)

    assert found == [], "\n".join(str(p) for p in found)
    assert set(checked) == {rel(INDEX_PATH), *(rel(p) for p in NOTEBOOK_PATHS.values())}


def test_a_topic_whose_notebook_is_not_generated_is_walked_and_skipped(monkeypatch):
    monkeypatch.setitem(TOPICS, "sea-level", ())
    monkeypatch.setitem(NOTEBOOK_PATHS, "sea-level", "1_physical_environment/15_sea_level.ipynb")

    checked, found = check_figure_provenance(ROOT)

    assert found == []
    assert rel(NOTEBOOK_PATHS["sea-level"]) not in checked


# --- building a repo the gate will read -----------------------------------------------


def a_source_record(source_id: str) -> str:
    return f"---\nid: {source_id}\n---\n"


def a_reference_record(citekey: str, *equations: str) -> str:
    """A reference record, with one `equations` entry per id given.

    The three keys CONTEXT.md gives an equation entry - `id`, `as_printed`, `where` - are
    written out; the gate reads only `id`, and a record holding the other two is the
    record `catalog-schema` requires.
    """
    lines = [f"---\ncitekey: {citekey}\nyear: 2022"]
    if equations:
        lines.append("equations:")
        for equation in equations:
            lines.append(f"  - id: {equation}\n    as_printed: y = mx + b\n    where: eq. 1, p. 4")
    return "\n".join([*lines, "---\n"])


def a_catalog(root: Path, sources=("noaa_oni",), references=(("gillett2022", "eq3"),)) -> None:
    """`catalog/sources/` and `catalog/references/`, holding just enough to resolve ids.

    `references` is a tuple per record: the citekey, then the equation ids it prints.
    """
    (root / "catalog" / "sources").mkdir(parents=True, exist_ok=True)
    (root / "catalog" / "references").mkdir(parents=True, exist_ok=True)
    for source_id in sources:
        path = root / "catalog" / "sources" / f"{source_id}.md"
        path.write_text(a_source_record(source_id), encoding="utf-8")
    for citekey, *equations in references:
        path = root / "catalog" / "references" / f"{citekey}.md"
        path.write_text(a_reference_record(citekey, *equations), encoding="utf-8")


def a_figure_cell(call: str = 'provenance(sources=["noaa_oni"])', above: str = PLOT):
    return new_code_cell(f"{above}\n{call}" if above else call)


def a_generated_cell(source: str, code: bool = False):
    """A cell the builder wrote. CONTEXT.md's own spelling of the marker, written out:
    `Generated cells are marked in cell metadata (kelpcatalog: generated)`."""
    cell = new_code_cell(source) if code else new_markdown_cell(source)
    cell.metadata["kelpcatalog"] = "generated"
    return cell


def a_repo(tmp_path: Path, *cells, path: str = OCEAN_CLIMATE, minor: int | None = None, **catalog):
    """A repo root holding one notebook at a path the gate walks, and a catalog.

    One notebook, not eleven: the gate reports on the notebooks that are there, and the
    ten that are not carry nothing for it to assert about - pinned below by
    `test_a_missing_notebook_carries_nothing_to_check`.
    """
    notebook = new_notebook(cells=list(cells))
    if minor is not None:
        # A notebook older than cell ids. nbformat writes and reads it without minting
        # one, so the cell reaches the gate unnamed.
        notebook.nbformat_minor = minor
        for cell in notebook.cells:
            cell.pop("id", None)
    nbformat.validate(notebook)
    write_notebook(notebook, tmp_path / NOTEBOOKS_DIR / path)
    a_catalog(tmp_path, **catalog)
    return tmp_path


# --- what passes ---------------------------------------------------------------------


def test_a_figure_cell_whose_ids_resolve_is_no_problem(tmp_path: Path):
    # The positive control: without it every assertion below would still hold for a gate
    # that failed every figure cell it met.
    call = (
        'provenance(sources=["noaa_oni"], references=["gillett2022"], '
        'equations=["gillett2022/eq3"])'
    )
    root = a_repo(tmp_path, a_figure_cell(call))

    assert problems(root) == []


def test_provenance_may_be_reached_through_a_module_name(tmp_path: Path):
    # `import kelpcatalog.notebook as nb` then `nb.provenance(...)` ends in the same call.
    root = a_repo(tmp_path, a_figure_cell('nb.provenance(sources=["noaa_oni"])'))

    assert problems(root) == []


def test_a_call_spread_over_several_lines_is_read(tmp_path: Path):
    root = a_repo(
        tmp_path,
        a_figure_cell('provenance(\n    sources=["noaa_oni"],\n    references=["gillett2022"],\n)'),
    )

    assert problems(root) == []


def test_a_tuple_of_ids_is_read_like_a_list(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell('provenance(sources=("noaa_oni",))'))

    assert problems(root) == []


def test_a_line_magic_does_not_make_a_cell_unreadable(tmp_path: Path):
    # A notebook cell is IPython source, not Python: `%matplotlib inline` is a SyntaxError
    # to `ast.parse`, and a gate that reported it would fail whatever #47 writes.
    root = a_repo(
        tmp_path,
        a_figure_cell(above=f"%matplotlib inline\nimport matplotlib.pyplot as plt\n{PLOT}"),
    )

    assert problems(root) == []


def test_a_shell_escape_does_not_make_a_cell_unreadable(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell(above=f"!echo building\n{PLOT}"))

    assert problems(root) == []


def test_provenance_naming_nothing_passes(tmp_path: Path):
    # The decision, pinned: CONTEXT.md's row is "every figure cell carries a
    # `provenance(...)` whose ids resolve", and an empty call carries one whose (zero) ids
    # resolve. Failing it would be the gate asserting more than the row. The question is
    # on the Parking lot as a question about the row's wording - see the module docstring.
    root = a_repo(tmp_path, a_figure_cell("provenance()"))

    assert problems(root) == []


# --- what is not a figure cell --------------------------------------------------------


def test_a_markdown_cell_is_not_a_figure_cell(tmp_path: Path):
    root = a_repo(tmp_path, new_markdown_cell("## upwelling-enso\n\nno provenance here"))

    checked, found = check_figure_provenance(root)

    assert found == []
    assert checked[rel(OCEAN_CLIMATE)] == []


def test_a_raw_cell_is_not_a_figure_cell(tmp_path: Path):
    root = a_repo(tmp_path, new_raw_cell("no provenance here either"))

    assert problems(root) == []


def test_a_generated_code_cell_is_not_a_figure_cell(tmp_path: Path):
    # CONTEXT.md: "figure cells are never generated and never touched", so a cell carrying
    # the builder's marker is not one. No builder writes a code cell today; the gate does
    # not have to know that to be right about it.
    root = a_repo(tmp_path, a_generated_cell("# a count line, one day", code=True))

    checked, found = check_figure_provenance(root)

    assert found == []
    assert checked[rel(OCEAN_CLIMATE)] == []


# --- the cell must end in the call ----------------------------------------------------


def test_a_code_cell_that_does_not_end_in_provenance_is_reported(tmp_path: Path):
    cell = a_figure_cell(call=PLOT, above="")
    root = a_repo(tmp_path, cell)

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert problem.field == cell.id
    # On the message, not on str(problem): tmp_path carries this test's own name, so a
    # message quoting an absolute path could spell almost anything.
    assert problem.message == "does not end in provenance(...)"


def test_a_statement_after_the_call_is_reported(tmp_path: Path):
    # Not last means not displayed: the cell's value is the last expression's, so a
    # provenance() with anything after it renders no caption at all.
    root = a_repo(tmp_path, a_figure_cell('provenance(sources=["noaa_oni"])\nprint("done")'))

    assert messages(root) == ["does not end in provenance(...)"]


def test_a_call_whose_value_is_assigned_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell('caption = provenance(sources=["noaa_oni"])'))

    assert messages(root) == ["does not end in provenance(...)"]


def test_a_cell_that_ends_in_a_different_call_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell("plt.show()"))

    assert messages(root) == ["does not end in provenance(...)"]


def test_an_empty_code_cell_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell(call="", above=""))

    assert messages(root) == ["does not end in provenance(...)"]


def test_a_call_on_something_that_is_not_a_name_is_reported(tmp_path: Path):
    # `captions["figure"](...)` is a call whose callee is a subscript, so it has no name to
    # match against. Reported rather than reached for: a gate that read `.id` off whatever
    # it found would raise here, and gate.py's runner has no `try`.
    root = a_repo(tmp_path, a_figure_cell('captions["figure"](sources=["noaa_oni"])'))

    assert messages(root) == ["does not end in provenance(...)"]


def test_the_name_without_its_parentheses_is_reported(tmp_path: Path):
    # `provenance` rather than `provenance(...)`: the cell ends in an expression that is
    # not a call, which displays the function object and no caption. It also stands for
    # every cell ending in a bare expression - a name, a string, a subscript - which is
    # the shape that reaches the gate's `isinstance(..., ast.Call)` guard.
    root = a_repo(tmp_path, a_figure_cell("provenance"))

    assert messages(root) == ["does not end in provenance(...)"]


# --- the ids must resolve -------------------------------------------------------------


def test_a_source_id_that_resolves_to_no_record_is_reported(tmp_path: Path):
    cell = a_figure_cell('provenance(sources=["not_a_record"])')
    root = a_repo(tmp_path, cell)

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert problem.field == cell.id
    assert problem.message == "'not_a_record' is not a source record"


def test_a_reference_id_that_resolves_to_no_record_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell('provenance(references=["notaref2020"])'))

    assert messages(root) == ["'notaref2020' is not a reference record"]


def test_an_equation_id_not_listed_on_its_reference_is_reported(tmp_path: Path):
    # The reference resolves and the equation does not: the record prints eq3, not eq9.
    root = a_repo(tmp_path, a_figure_cell('provenance(equations=["gillett2022/eq9"])'))

    assert messages(root) == ["'eq9' is not an equation on 'gillett2022'"]


def test_an_equation_id_on_a_reference_that_lists_none_is_reported(tmp_path: Path):
    root = a_repo(
        tmp_path,
        a_figure_cell('provenance(equations=["gillett2022/eq3"])'),
        references=(("gillett2022",),),
    )

    assert messages(root) == ["'eq3' is not an equation on 'gillett2022'"]


def test_a_reference_whose_equations_entry_is_malformed_does_not_take_the_gate_down(
    tmp_path: Path,
):
    # `load_catalog` parses and does not validate, so a record `catalog-schema` would
    # reject still reaches this gate. An `equations` list holding a bare string, or a
    # mapping with no `id`, must be read as printing no equation rather than raising:
    # gate.py's runner has no `try`, and a gate that raised would take the whole run down.
    root = a_repo(tmp_path, a_figure_cell('provenance(equations=["gillett2022/eq3"])'))
    (root / "catalog" / "references" / "gillett2022.md").write_text(
        "---\ncitekey: gillett2022\nyear: 2022\nequations:\n  - eq3\n  - where: p. 4\n---\n",
        encoding="utf-8",
    )

    assert messages(root) == ["'eq3' is not an equation on 'gillett2022'"]


def test_an_equation_id_naming_no_reference_record_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell('provenance(equations=["notaref2020/eq3"])'))

    assert messages(root) == ["'notaref2020' is not a reference record"]


def test_an_equation_id_that_names_no_reference_at_all_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell('provenance(equations=["eq3"])'))

    assert messages(root) == ["'eq3' must be <citekey>/<equation id>"]


def test_an_equation_id_with_an_empty_half_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell('provenance(equations=["gillett2022/"])'))

    assert messages(root) == ["'gillett2022/' must be <citekey>/<equation id>"]


def test_an_equation_id_with_two_separators_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell('provenance(equations=["gillett2022/eq3/a"])'))

    assert messages(root) == ["'gillett2022/eq3/a' must be <citekey>/<equation id>"]


def test_a_call_the_gate_half_cannot_read_still_has_its_other_ids_resolved(tmp_path: Path):
    # A cell with a keyword the call does not take *and* a typo'd id: both are reported.
    # Returning the first family alone would hide the typo behind the keyword, and the
    # author would fix one, re-run, and meet the other.
    call = 'provenance(tables=["oni"], sources=["nope"])'
    root = a_repo(tmp_path, a_figure_cell(call))

    assert messages(root) == [
        "provenance(...) takes no 'tables' keyword",
        "'nope' is not a source record",
    ]


def test_every_unresolvable_id_in_one_call_is_reported(tmp_path: Path):
    # Not the first: a cell citing three records with two typos has to name both.
    call = 'provenance(sources=["noaa_oni", "nope"], references=["alsonope2020"])'
    root = a_repo(tmp_path, a_figure_cell(call))

    assert messages(root) == [
        "'nope' is not a source record",
        "'alsonope2020' is not a reference record",
    ]


# --- the ids must be written out where the gate can read them -------------------------


def test_ids_that_are_computed_rather_than_written_out_are_reported(tmp_path: Path):
    # The gate reads source text, so it can only check what is written. A cell that built
    # its id list at runtime would pass a gate that shrugged at it.
    root = a_repo(tmp_path, a_figure_cell("provenance(sources=[which_source()])"))

    assert messages(root) == ["sources= must be a list of strings written out, not computed"]


def test_a_variable_standing_for_the_ids_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell("provenance(sources=ids)"))

    assert messages(root) == ["sources= must be a list of strings written out, not computed"]


def test_a_bare_string_instead_of_a_list_is_reported(tmp_path: Path):
    # `sources="noaa_oni"` is a string the runtime would iterate character by character.
    root = a_repo(tmp_path, a_figure_cell('provenance(sources="noaa_oni")'))

    assert messages(root) == ["sources= must be a list of strings written out, not computed"]


def test_a_non_string_id_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell("provenance(sources=[1950])"))

    assert messages(root) == ["sources= must be a list of strings written out, not computed"]


def test_a_positional_id_list_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell('provenance(["noaa_oni"])'))

    assert messages(root) == [
        "names its ids positionally; provenance(...) takes sources=, references= and equations="
    ]


def test_unpacked_keywords_are_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell("provenance(**cited)"))

    assert messages(root) == [
        "unpacks its keywords; provenance(...) must name sources=, references= and equations="
    ]


def test_a_keyword_provenance_does_not_take_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell('provenance(tables=["oni"])'))

    assert messages(root) == ["provenance(...) takes no 'tables' keyword"]


# --- a cell the gate cannot read ------------------------------------------------------


def test_a_cell_that_is_not_python_is_reported(tmp_path: Path):
    cell = a_figure_cell(call="provenance(sources=[", above="")
    root = a_repo(tmp_path, cell)

    (problem,) = problems(root)

    assert problem.field == cell.id
    # Written out, and over source that does not itself contain the phrase: a parser
    # quotes its input back in its error, so an `in` assertion over a cell reading
    # "is not Python" would pass on the cell rather than on the gate.
    assert problem.message.startswith("is not Python this gate can read")


def test_a_cell_magic_is_reported(tmp_path: Path):
    # `%%capture` and friends hand the whole cell to something that is not the Python
    # compiler, so the gate cannot say what the cell ends in. Reported rather than
    # skipped: a figure cell that silently stopped being checked is the worse failure.
    root = a_repo(tmp_path, a_figure_cell(above='%%capture\nprovenance(sources=["noaa_oni"])'))

    assert messages(root) == ["opens with a cell magic, so it is not Python this gate can read"]


# --- every failure is reported, not the first -----------------------------------------


def test_every_bad_figure_cell_in_a_notebook_is_reported(tmp_path: Path):
    bad, good, worse = (
        a_figure_cell(call=PLOT, above=""),
        a_figure_cell(),
        a_figure_cell('provenance(sources=["nope"])'),
    )
    root = a_repo(tmp_path, bad, new_markdown_cell("## heatwaves"), good, worse)

    assert [p.field for p in problems(root)] == [bad.id, worse.id]


def test_every_bad_notebook_is_reported(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell(call=PLOT, above=""))
    a_repo(tmp_path, a_figure_cell(call=PLOT, above=""), path=INDEX_PATH)

    assert sorted(p.path for p in problems(root)) == [rel(INDEX_PATH), rel(OCEAN_CLIMATE)]


# --- what the gate reads back ---------------------------------------------------------


def test_it_reads_back_the_figure_cells_it_checked(tmp_path: Path):
    first, second = a_figure_cell(), a_figure_cell()
    root = a_repo(tmp_path, new_markdown_cell("# ocean-climate"), first, second)

    checked, _ = check_figure_provenance(root)

    assert checked[rel(OCEAN_CLIMATE)] == [first.id, second.id]


def test_a_cell_older_than_cell_ids_is_named_by_its_position(tmp_path: Path):
    root = a_repo(
        tmp_path, new_markdown_cell("# ocean-climate"), a_figure_cell(call=PLOT, above=""), minor=4
    )

    (problem,) = problems(root)

    assert problem.field == "cell 1"


# --- a notebook the gate cannot read --------------------------------------------------


def test_a_notebook_that_cannot_be_read_is_reported_and_named(tmp_path: Path):
    # A gate returns (passed, message); one that raised would take gate.py down on
    # exactly the hand-edited notebook it exists to catch.
    root = a_repo(tmp_path, a_figure_cell())
    (root / NOTEBOOKS_DIR / OCEAN_CLIMATE).write_text("{ not json", encoding="utf-8")

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert problem.field == "notebook"
    assert problem.message.startswith("is not a notebook this gate can read")
    assert "JSON" in problem.message


def test_a_missing_notebook_carries_nothing_to_check(tmp_path: Path):
    a_catalog(tmp_path)

    checked, found = check_figure_provenance(tmp_path)

    assert found == []
    assert checked == {}


def test_a_directory_where_a_notebook_should_be_is_not_read(tmp_path: Path):
    root = a_repo(tmp_path, a_figure_cell())
    target = root / NOTEBOOKS_DIR / OCEAN_CLIMATE
    target.unlink()
    target.mkdir()

    assert problems(root) == []


def test_a_repo_with_no_catalog_resolves_no_id(tmp_path: Path):
    # The gate loads the catalog to resolve against; a root with none resolves nothing,
    # and every id in a figure cell is then unresolvable rather than silently fine.
    notebook = new_notebook(cells=[a_figure_cell()])
    write_notebook(notebook, tmp_path / NOTEBOOKS_DIR / OCEAN_CLIMATE)

    assert messages(tmp_path) == ["'noaa_oni' is not a source record"]

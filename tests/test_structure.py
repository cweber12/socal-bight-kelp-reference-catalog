"""Tests for the notebook-structure gate: the sections a committed notebook must hold.

The gate reads `notebooks/`, never the builder's output, so every test below mutates a
written notebook the way a hand-edit would and asks what the gate says about the file on
disk. The tree is generated into tmp_path from the miniature repo test_build.py uses:
eleven fixture notebooks per case would be eleven files to rewrite every time a heading
changed, and it is the mutation, not the tree, that each test is about.

The one thing that cannot be checked that way is the expected list itself - a gate whose
expectations came from the builder would agree with a builder that had drifted - so the
ten sections of 11_ocean_climate are typed out here and read back from the committed
notebook, as test_build.py types out the same list one level up.
"""

from __future__ import annotations

from pathlib import Path

import nbformat
import pytest
from nbformat.v4 import new_code_cell, new_markdown_cell

from kelpcatalog.build import GENERATED, GENERATED_KEY, write_notebook
from kelpcatalog.generate import NOTEBOOKS_DIR, generate
from kelpcatalog.plan import INDEX_PATH, NOTEBOOK_PATHS
from kelpcatalog.schema import TOPICS
from kelpcatalog.structure import check_structure

ROOT = Path(__file__).parents[1]
FIXTURE = Path(__file__).parent / "fixtures" / "notebook"

OCEAN_CLIMATE = NOTEBOOK_PATHS["ocean-climate"]

# CONTEXT.md, "Notebooks": the question, one section per sub-topic in TOPICS order, then
# the three fixed ones. Typed out rather than derived, because deriving it is what the
# code under test does.
OCEAN_CLIMATE_SECTIONS = [
    "# ocean-climate",
    "## temperature",
    "## salinity",
    "## nutrients",
    "## upwelling-enso",
    "## heatwaves",
    "## oxygen-ph",
    "## General",
    "## Not held",
    "## Reviewed and not included",
]


def a_repo(tmp_path: Path) -> Path:
    """A repo root whose notebooks/ holds the eleven, every one of them right."""
    generate(FIXTURE, into=tmp_path / NOTEBOOKS_DIR)
    return tmp_path


def read(root: Path, path: str):
    return nbformat.read(root / NOTEBOOKS_DIR / path, as_version=4)


def rewrite(root: Path, path: str, notebook) -> None:
    write_notebook(notebook, root / NOTEBOOKS_DIR / path)


def problems(root: Path):
    return check_structure(root)[1]


def a_generated_cell(source: str):
    cell = new_markdown_cell(source)
    cell.metadata[GENERATED_KEY] = GENERATED
    return cell


def rel(path: str) -> str:
    return f"{NOTEBOOKS_DIR}/{path}"


# --- the committed tree --------------------------------------------------------------


def test_the_committed_notebooks_pass_and_are_counted():
    sections, found = check_structure(ROOT)

    assert found == [], "\n".join(str(p) for p in found)
    assert len(sections) == 11


def test_it_reads_back_the_sections_the_committed_ocean_climate_notebook_holds():
    sections, _ = check_structure(ROOT)

    assert sections[rel(OCEAN_CLIMATE)] == OCEAN_CLIMATE_SECTIONS


def test_a_generated_tree_passes(tmp_path: Path):
    assert problems(a_repo(tmp_path)) == []


# --- a topic notebook's sections ------------------------------------------------------


def test_a_missing_section_fails_and_names_the_notebook_and_the_section(tmp_path: Path):
    root = a_repo(tmp_path)
    notebook = read(root, OCEAN_CLIMATE)
    notebook.cells = [c for c in notebook.cells if c.id != "kelpcatalog-subtopic-heatwaves"]
    rewrite(root, OCEAN_CLIMATE, notebook)

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert "heatwaves" in str(problem)
    assert "missing" in str(problem)


def test_a_section_for_a_sub_topic_that_is_not_in_topics_fails(tmp_path: Path):
    root = a_repo(tmp_path)
    notebook = read(root, OCEAN_CLIMATE)
    notebook.cells.insert(2, a_generated_cell("## sea-level"))
    rewrite(root, OCEAN_CLIMATE, notebook)

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert "sea-level" in str(problem)
    # Named as the extra it is: an inserted section also shifts every section below it,
    # and "out of order" would send a reader looking in the wrong place.
    assert "not a section" in problem.message


def test_sections_out_of_topics_order_fail(tmp_path: Path):
    root = a_repo(tmp_path)
    notebook = read(root, OCEAN_CLIMATE)
    notebook.cells[1], notebook.cells[2] = notebook.cells[2], notebook.cells[1]
    rewrite(root, OCEAN_CLIMATE, notebook)

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert "order" in str(problem)


def test_the_same_section_twice_fails(tmp_path: Path):
    root = a_repo(tmp_path)
    notebook = read(root, OCEAN_CLIMATE)
    notebook.cells.insert(2, a_generated_cell("## temperature"))
    rewrite(root, OCEAN_CLIMATE, notebook)

    (problem,) = problems(root)

    assert "temperature" in str(problem)
    assert "twice" in str(problem)


def test_a_sub_topic_added_to_topics_without_regenerating_fails(monkeypatch):
    # How a new sub-topic gets its section: CONTEXT.md, "Topics do not decide what is
    # admitted". The gate reads the committed notebooks, so adding the row and not
    # regenerating is a failure, not a silent gap.
    monkeypatch.setitem(TOPICS, "ocean-climate", (*TOPICS["ocean-climate"], "sea-level"))

    _, found = check_structure(ROOT)

    assert [p for p in found if p.path == rel(OCEAN_CLIMATE) and "sea-level" in str(p)]


# --- what is not a section ------------------------------------------------------------


@pytest.mark.parametrize("path", [OCEAN_CLIMATE, INDEX_PATH], ids=["topic", "index"])
def test_a_cell_without_the_generated_marker_is_not_a_section(tmp_path: Path, path: str):
    # A figure cell deliberately carries no marker (#47), and a heading over one is not a
    # section that has gone missing.
    root = a_repo(tmp_path)
    notebook = read(root, path)
    notebook.cells.insert(1, new_markdown_cell("## Canopy against temperature"))
    notebook.cells.insert(2, new_code_cell("# a comment, not a heading\nprovenance()"))
    rewrite(root, path, notebook)

    assert problems(root) == []


def test_a_line_that_opens_no_heading_is_not_a_section(tmp_path: Path):
    # CommonMark wants the space after the hashes. `#kelp` is prose, and a gate that read
    # it as a section would fail a notebook over a record's own words.
    root = a_repo(tmp_path)
    notebook = read(root, OCEAN_CLIMATE)
    notebook.cells[1].source += "\n\n#kelp\n"
    rewrite(root, OCEAN_CLIMATE, notebook)

    assert problems(root) == []


def test_a_generated_code_cell_holds_no_sections(tmp_path: Path):
    # `#` opens a comment in code and a heading in markdown, so a section is read from
    # markdown alone.
    root = a_repo(tmp_path)
    notebook = read(root, OCEAN_CLIMATE)
    cell = new_code_cell("# temperature")
    cell.metadata[GENERATED_KEY] = GENERATED
    notebook.cells.insert(1, cell)
    rewrite(root, OCEAN_CLIMATE, notebook)

    assert problems(root) == []


# --- the index ------------------------------------------------------------------------


def test_an_index_that_does_not_list_every_topic_fails(tmp_path: Path):
    root = a_repo(tmp_path)
    notebook = read(root, INDEX_PATH)
    dropped = "canyon-dynamics"
    for cell in notebook.cells:
        cell.source = cell.source.replace(f"### [{dropped}]({NOTEBOOK_PATHS[dropped]})\n", "")
    rewrite(root, INDEX_PATH, notebook)

    (problem,) = problems(root)

    assert problem.path == rel(INDEX_PATH)
    assert dropped in str(problem)


def test_a_topic_added_to_topics_is_listed_by_the_index_only_after_a_regeneration(monkeypatch):
    # A new topic is a row in CONTEXT.md, an entry in schema.py and one in plan.py; the
    # eleventh notebook and the index's entry for it arrive with the regeneration.
    monkeypatch.setitem(TOPICS, "sea-level", ())
    monkeypatch.setitem(NOTEBOOK_PATHS, "sea-level", "1_physical_environment/15_sea_level.ipynb")

    _, found = check_structure(ROOT)

    assert [p for p in found if p.path == rel(INDEX_PATH) and "sea-level" in str(p)]


# --- a notebook the gate cannot read --------------------------------------------------


def test_a_missing_notebook_fails_and_names_it(tmp_path: Path):
    root = a_repo(tmp_path)
    (root / NOTEBOOKS_DIR / OCEAN_CLIMATE).unlink()

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    # On the message, not on str(problem): tmp_path carries this test's own name, so an
    # OS error quoting the absolute path would spell "missing" whatever went wrong.
    assert problem.message.startswith("the notebook is missing")


def test_a_notebook_that_cannot_be_read_fails_and_names_it(tmp_path: Path):
    # A gate that raised here would break gate.py's contract - (passed, message) - on
    # exactly the hand-edited notebook it exists to catch.
    root = a_repo(tmp_path)
    (root / NOTEBOOKS_DIR / OCEAN_CLIMATE).write_text("not a notebook\n", encoding="utf-8")

    (problem,) = problems(root)

    assert problem.path == rel(OCEAN_CLIMATE)
    assert "not a notebook" in problem.message


def test_a_tree_with_no_notebooks_fails_once_per_notebook(tmp_path: Path):
    _, found = check_structure(tmp_path)

    assert len(found) == 11


# --- what the module advertises, pinned -----------------------------------------------
#
# Added after the audit of PR #62: each of these passed when it was written, and each
# kills a mutant that survived the whole suite before it existed.


@pytest.mark.parametrize(
    "written",
    ["## heatwaves ##", "##   heatwaves  ", "## heatwaves   ###"],
    ids=["closing-hashes", "loose-spacing", "both"],
)
def test_a_heading_is_read_past_its_cosmetic_whitespace(tmp_path: Path, written: str):
    # HEADING_RE's tolerance is deliberate - a hand-edited notebook should not fail this
    # gate over spacing CommonMark ignores - and nothing pinned it.
    root = a_repo(tmp_path)
    notebook = read(root, OCEAN_CLIMATE)
    cell = next(c for c in notebook.cells if c.id == "kelpcatalog-subtopic-heatwaves")
    cell.source = written + cell.source[len("## heatwaves") :]
    rewrite(root, OCEAN_CLIMATE, notebook)

    assert problems(root) == []


def test_a_directory_where_a_notebook_should_be_reads_as_missing(tmp_path: Path):
    # `is_file()`, not `exists()`: a directory at a notebook's path holds no sections, so
    # "missing" is what a reader needs to be told.
    root = a_repo(tmp_path)
    target = root / NOTEBOOKS_DIR / OCEAN_CLIMATE
    target.unlink()
    target.mkdir()

    (problem,) = problems(root)

    assert problem.message.startswith("the notebook is missing")


def test_a_sub_topic_named_like_a_fixed_section_is_reported_rather_than_raised(monkeypatch):
    # A gate returns (passed, message). This is the one shape that reaches the ordering
    # branch with the two lists agreeing as far as the notebook runs.
    monkeypatch.setitem(TOPICS, "ocean-climate", (*TOPICS["ocean-climate"], "General"))

    _, found = check_structure(ROOT)

    assert [p for p in found if p.path == rel(OCEAN_CLIMATE)]


def test_hashes_with_no_text_open_no_section(tmp_path: Path):
    # A heading needs text. Without this, `##` alone reads as a section named nothing,
    # which would then be reported as a section the topic does not have.
    root = a_repo(tmp_path)
    notebook = read(root, OCEAN_CLIMATE)
    notebook.cells[1].source += "\n\n##   \n"
    rewrite(root, OCEAN_CLIMATE, notebook)

    assert problems(root) == []

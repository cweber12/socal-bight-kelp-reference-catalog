"""Tests for the entry point: one command, eleven notebooks.

This is the command #49 will point `add-source` at and the command a reviewer runs to
check that a notebook is current, so what it must not do is the point of it: rebuilding a
notebook from records alone would delete a figure cell the first time one exists. Every
assertion below is at the byte level, because that is the level the property lives at -
`git status` clean after a regeneration - and the level nbformat's repair-on-serialize
shows up at.

The two-process check is the one that catches anything drawn rather than derived. A set
or a dict keyed by anything unordered iterates differently at a different PYTHONHASHSEED,
and one process cannot tell: Python fixes the seed once, at start-up.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import warnings
from pathlib import Path

import nbformat
import pytest
from nbformat.v4 import new_code_cell, new_markdown_cell, new_output

from kelpcatalog.generate import NOTEBOOKS_DIR, generate, main
from kelpcatalog.plan import INDEX_PATH, NOTEBOOK_PATHS

ROOT = Path(__file__).parents[1]
FIXTURE = Path(__file__).parent / "fixtures" / "notebook"

THE_ELEVEN = {INDEX_PATH, *NOTEBOOK_PATHS.values()}


def tree(directory: Path) -> dict[str, bytes]:
    """Every file under the directory, keyed by its path relative to it."""
    return {
        p.relative_to(directory).as_posix(): p.read_bytes()
        for p in sorted(directory.rglob("*"))
        if p.is_file()
    }


def a_figure_cell(source: str = "provenance(sources=['shore_temp'])"):
    cell = new_code_cell(source)
    cell.outputs = [new_output("display_data", data={"text/plain": "<Figure>"})]
    cell.execution_count = 1
    return cell


# --- what it writes ----------------------------------------------------------------


def test_it_writes_the_eleven_paths_the_plan_names(tmp_path: Path):
    written = generate(FIXTURE, into=tmp_path)

    assert {p.relative_to(tmp_path).as_posix() for p in written} == THE_ELEVEN
    assert set(tree(tmp_path)) == THE_ELEVEN
    assert len(THE_ELEVEN) == 11


def test_it_defaults_to_the_notebooks_directory_under_the_root(tmp_path: Path):
    (tmp_path / "catalog").mkdir()

    written = generate(tmp_path)

    assert {p.relative_to(tmp_path).as_posix() for p in written} == {
        f"{NOTEBOOKS_DIR}/{path}" for path in THE_ELEVEN
    }


def test_every_written_notebook_is_valid_and_carries_no_metadata(tmp_path: Path):
    for path in generate(FIXTURE, into=tmp_path):
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        # #56: metadata is carried through from `existing`, never invented, so a
        # notebook that has never held a figure has none - no kernelspec (#47/#48).
        assert nb.metadata == {}, path
        assert [c for c in nb.cells if c.cell_type == "code"] == [], path


def test_every_written_notebook_is_committed_with_lf(tmp_path: Path):
    # .gitattributes is `* text=auto eol=lf`, and nbformat.write would open the file in
    # text mode - so on Windows the same notebook would be different bytes.
    for path in generate(FIXTURE, into=tmp_path):
        raw = path.read_bytes()
        assert b"\r\n" not in raw, path
        assert raw.endswith(b"\n") and not raw.endswith(b"\n\n"), path


def test_it_generates_the_real_catalog(tmp_path: Path):
    generate(ROOT, into=tmp_path)
    assert set(tree(tmp_path)) == THE_ELEVEN


# --- regenerating -------------------------------------------------------------------


def test_regenerating_with_no_record_change_leaves_every_file_byte_identical(tmp_path: Path):
    generate(FIXTURE, into=tmp_path)
    before = tree(tmp_path)

    generate(FIXTURE, into=tmp_path)

    assert tree(tmp_path) == before


def test_regenerating_the_real_catalog_leaves_every_file_byte_identical(tmp_path: Path):
    generate(ROOT, into=tmp_path)
    before = tree(tmp_path)
    generate(ROOT, into=tmp_path)
    assert tree(tmp_path) == before


@pytest.mark.parametrize("path", sorted(THE_ELEVEN))
def test_a_figure_cell_survives_a_regeneration(tmp_path: Path, path: str):
    # The whole point of #42's merge, and the trap this entry point can fall into: a
    # regeneration that called the builder without `existing` would delete the figure the
    # first time one existed, and nothing would say so. Asserted for all eleven, the
    # index included, because a loop that read one of them back and not the others would
    # pass a test that checked only the topic notebooks.
    generate(FIXTURE, into=tmp_path)
    target = tmp_path / path
    nb = nbformat.read(target, as_version=4)
    figure = a_figure_cell()
    nb.cells.insert(1, figure)
    nbformat.write(nb, target)
    before = nbformat.read(target, as_version=4).cells[1]

    generate(FIXTURE, into=tmp_path)

    kept = [c for c in nbformat.read(target, as_version=4).cells if c.cell_type == "code"]
    assert kept == [before], path


def test_a_regeneration_over_a_hand_edited_notebook_settles_after_one_pass(tmp_path: Path):
    # A cell nbformat had to repair - one with no id - gets a derived id on the first
    # rebuild and is stable from then on, so a second regeneration changes no bytes.
    generate(FIXTURE, into=tmp_path)
    target = tmp_path / INDEX_PATH
    nb = nbformat.read(target, as_version=4)
    note = new_markdown_cell("Hand-written, not generated.")
    del note["id"]
    nb.cells.insert(1, note)
    with warnings.catch_warnings():
        # nbformat warns as it writes the id-less cell this test exists to hand the
        # builder. The warning is the setup's, not the builder's - and the builder
        # triggering one is what test_writing_a_built_notebook_asks_nbformat_to_repair
        # _nothing pins.
        warnings.simplefilter("ignore")
        nbformat.write(nb, target)

    generate(FIXTURE, into=tmp_path)
    once = tree(tmp_path)
    generate(FIXTURE, into=tmp_path)

    assert tree(tmp_path) == once
    assert "Hand-written, not generated." in target.read_text(encoding="utf-8")


# --- two processes, two hash seeds --------------------------------------------------


def generate_in_a_new_process(root: Path, into: Path, seed: str) -> None:
    env = {**os.environ, "PYTHONHASHSEED": seed, "PYTHONUTF8": "1"}
    code = (
        "import sys, pathlib;"
        "sys.path.insert(0, sys.argv[1]);"
        "from kelpcatalog.generate import generate;"
        "generate(pathlib.Path(sys.argv[2]), into=pathlib.Path(sys.argv[3]))"
    )
    subprocess.run(
        [sys.executable, "-c", code, str(ROOT / "src"), str(root), str(into)],
        env=env,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


@pytest.mark.parametrize("root", [FIXTURE, ROOT], ids=["fixture", "real"])
def test_two_processes_at_different_hash_seeds_write_the_same_bytes(tmp_path: Path, root: Path):
    # Python fixes PYTHONHASHSEED once at start-up, so a builder that iterated a set
    # somewhere would still be self-consistent within one process and could pass every
    # test above. This is the check that catches it.
    first, second = tmp_path / "0", tmp_path / "1"
    generate_in_a_new_process(root, first, "0")
    generate_in_a_new_process(root, second, "12345")

    assert tree(first) == tree(second)


# --- the command ---------------------------------------------------------------------


def test_the_module_runs_as_a_command_and_names_what_it_wrote(tmp_path: Path):
    (tmp_path / "catalog").mkdir()
    result = subprocess.run(
        [sys.executable, "-m", "kelpcatalog.generate"],
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUTF8": "1"},
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    assert result.returncode == 0, result.stderr
    assert set(tree(tmp_path / NOTEBOOKS_DIR)) == THE_ELEVEN
    assert INDEX_PATH in result.stdout
    assert "11 notebooks" in result.stdout


def test_main_regenerates_the_repo_it_is_run_from(tmp_path: Path, monkeypatch, capsys):
    (tmp_path / "catalog").mkdir()
    monkeypatch.chdir(tmp_path)

    assert main() == 0

    out = capsys.readouterr().out
    assert set(tree(tmp_path / NOTEBOOKS_DIR)) == THE_ELEVEN
    assert all(f"{NOTEBOOKS_DIR}/{path}" in out for path in THE_ELEVEN)


def test_main_refuses_a_directory_that_is_not_a_repo_root(tmp_path: Path, monkeypatch, capsys):
    # notebooks/ under whatever directory the command happened to be run from is a
    # footgun with no gate to catch it, so the command says where it expects to stand.
    monkeypatch.chdir(tmp_path)

    assert main() == 1

    assert not (tmp_path / NOTEBOOKS_DIR).exists()
    assert "catalog" in capsys.readouterr().err


def test_it_refuses_to_render_a_catalog_that_does_not_validate(tmp_path: Path):
    # A record that does not parse is a record the builder cannot render, and eleven
    # notebooks written from a half-loaded catalog would look like eleven good ones.
    (tmp_path / "catalog" / "sources").mkdir(parents=True)
    (tmp_path / "catalog" / "sources" / "broken.md").write_text("no frontmatter\n", "utf-8")

    with pytest.raises(ValueError, match="does not validate"):
        generate(tmp_path, into=tmp_path / "out")

    assert not (tmp_path / "out").exists()


# --- the committed figure ------------------------------------------------------------
#
# #47's third "Done when" - "a builder regeneration leaves the figure cell byte-identical"
# - asserted against the notebook that actually holds one, rather than against a figure
# cell a test built. The tests above insert one into the fixture tree and are the general
# property; these two are the committed artifact, outputs and all.

FIGURE_NOTEBOOK = NOTEBOOK_PATHS["ocean-climate"]
FIGURE_CELL_ID = "figure-oni-anomaly"


def code_cells(path: Path) -> dict[str, str]:
    """Every code cell of the notebook, serialized, keyed by id.

    Serialized because that is the level "byte-identical" lives at, and keyed by id
    rather than counted because a count is blind to a collection that grows: a second
    figure would leave `len(...) == 1` failing for the wrong reason and a set comparison
    saying exactly what arrived.
    """
    notebook = nbformat.read(path, as_version=4)
    return {
        cell.id: json.dumps(cell, sort_keys=True)
        for cell in notebook.cells
        if cell.cell_type == "code"
    }


def test_regenerating_the_committed_notebooks_leaves_the_figure_cell_byte_identical(
    tmp_path: Path,
):
    # The committed tree is copied in first, because that is what a regeneration in the
    # repo meets: generate() reads each notebook back and merges over it, and a run into
    # an empty directory would build from records alone and hold no figure at all.
    shutil.copytree(ROOT / NOTEBOOKS_DIR, tmp_path, dirs_exist_ok=True)
    before = code_cells(tmp_path / FIGURE_NOTEBOOK)
    assert set(before) == {FIGURE_CELL_ID}, "the committed ONI figure cell is gone"

    generate(ROOT, into=tmp_path)

    assert code_cells(tmp_path / FIGURE_NOTEBOOK) == before


def test_the_committed_figure_commits_its_caption_under_its_figure(tmp_path: Path):
    # CONTEXT.md says the caption sits *under* the figure ("The rule"; "Notebooks"), and
    # no gate secures it: `figure-provenance` reads the cell's source and never its
    # outputs, so a cell that dropped its `plt.show()` would publish the figure from
    # matplotlib's post_execute hook - after the caption - and stay green while reading
    # on GitHub with the citation above the plot it cites. Measured in #47; this is the
    # only thing standing on the order.
    cell = next(
        c
        for c in nbformat.read(ROOT / NOTEBOOKS_DIR / FIGURE_NOTEBOOK, as_version=4).cells
        if c.id == FIGURE_CELL_ID
    )

    kinds = [output.output_type for output in cell.outputs]

    assert kinds == ["display_data", "execute_result"]
    assert "image/png" in cell.outputs[0].data
    assert "text/markdown" in cell.outputs[1].data

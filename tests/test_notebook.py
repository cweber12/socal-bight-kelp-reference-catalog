"""Tests for the figure runtime: what a figure cell calls.

`kelpcatalog.notebook` is the one module in this package a *notebook* imports, so these
tests import it the way a figure cell would and never go through `gate.py`. Two things
follow from that and shape everything below.

`provenance(...)` is pure. It renders a caption from the ids it is handed and resolves
nothing, so there is no test here for an id that names no record: resolving is the
`figure-provenance` gate's, in `tests/test_figure_provenance.py`, and the reason the
split is that way round is in `notebook.py`'s docstring.

`load()` is not. It reads `data/raw/<id>/`, which is git-ignored, so every test builds
its own tree under `tmp_path` and none reads the repo's. That is not only a CI
requirement - `data/` is absent there - it is what lets a test hold five files for
`sio_shore_stations` without five ZIP archives in the fixture. The counts the fixtures
use (1 for `noaa_oni`, 2 for `calcofi`, 5 for `sio_shore_stations`) are the shape
measured in this machine's `data/` on 2026-09-10; the PR body records the same run
against the real tree, which no test can reach.
"""

from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest

from kelpcatalog.notebook import (
    EQUATION_SEP,
    EQUATIONS,
    PROVENANCE,
    REFERENCES,
    SOURCES,
    Provenance,
    load,
    provenance,
)

# The shape of `data/raw/` measured on 2026-09-10, one entry per catalogued source.
MEASURED = {"noaa_oni": 1, "calcofi": 2, "sio_shore_stations": 5}


# --- the caption ---------------------------------------------------------------------


def test_provenance_renders_a_caption_naming_the_source():
    caption = provenance(sources=["noaa_oni"])._repr_markdown_()

    assert "noaa_oni" in caption


def test_the_whole_caption_written_out():
    # The one test that pins the shape rather than asking what is in it. CONTEXT.md
    # specifies no caption format, so every character here is this module's choice - which
    # is the reason to pin it in one visible place: emptying the label or the separator
    # left every other assertion in this file green until this test existed. Written out
    # as a literal rather than assembled from the constants, so a rename shows up here.
    caption = provenance(
        sources=["noaa_oni", "calcofi"],
        references=["gillett2022"],
        equations=["gillett2022/eq3"],
    )._repr_markdown_()

    assert caption == (
        "**Provenance** — sources: `noaa_oni` · `calcofi` · references: `gillett2022` · "
        "equations: `gillett2022/eq3`"
    )


def test_the_caption_names_every_id_it_is_given():
    caption = provenance(
        sources=["noaa_oni", "calcofi"],
        references=["gillett2022"],
        equations=["gillett2022/eq3"],
    )._repr_markdown_()

    for named in ("noaa_oni", "calcofi", "gillett2022", "gillett2022/eq3"):
        assert named in caption


def test_a_group_with_no_ids_is_left_out_of_the_caption():
    # Written out rather than taken from the constants: a caption that renamed its
    # labels along with them would still pass a test that read them from the module.
    caption = provenance(sources=["noaa_oni"])._repr_markdown_()

    assert "sources" in caption
    assert "references" not in caption
    assert "equations" not in caption


def test_a_caption_naming_nothing_says_so_rather_than_rendering_an_empty_line():
    # `provenance()` is not a failure here and is not one at the gate either - see
    # figure_provenance.py's docstring on what the row asserts - so it has to render
    # something a reader can see.
    caption = provenance()._repr_markdown_()

    assert caption.strip() != ""
    assert "nothing named" in caption


def test_the_caption_is_what_str_gives():
    citation = provenance(sources=["noaa_oni"])

    assert str(citation) == citation._repr_markdown_()


def test_ids_must_be_named_by_keyword():
    # Keyword-only, so that the gate reading a call's source and the runtime executing it
    # read the same three names. A positional list would have an order only the signature
    # states, and the gate would have to transcribe it.
    with pytest.raises(TypeError):
        provenance(["noaa_oni"])  # type: ignore[misc]


def test_the_keywords_the_gate_looks_for_are_the_ones_the_signature_takes():
    # The gate reads `sources=`, `references=` and `equations=` out of a cell's source
    # text by these three names. If the signature and the constants drift, a figure cell
    # that runs fails the gate, or one that fails the gate runs.
    taken = tuple(inspect.signature(provenance).parameters)

    assert taken == (SOURCES, REFERENCES, EQUATIONS)


def test_the_call_a_figure_cell_ends_with_is_spelled_provenance():
    # Both ends of the same fact written out, because the gate matches this name against
    # a cell's source and nothing else would notice a rename.
    assert PROVENANCE == "provenance"
    assert provenance.__name__ == PROVENANCE


def test_an_equation_id_names_its_reference_ahead_of_the_separator():
    assert EQUATION_SEP == "/"
    assert f"gillett2022{EQUATION_SEP}eq3" == "gillett2022/eq3"


def test_a_citation_is_hashable_and_holds_the_ids_it_was_given():
    citation = provenance(sources=["noaa_oni"], references=["gillett2022"])

    assert citation == Provenance(("noaa_oni",), ("gillett2022",), ())
    assert {citation}  # frozen, so a cell that returns one can be put in a set


# --- building a repo load() will read ------------------------------------------------


def a_source_record(source_id: str) -> str:
    """The smallest frontmatter `load_catalog` reads an id out of.

    `load()` asks the catalog whether an id is a source, and `load_catalog` parses rather
    than validates, so the fields a record needs to *validate* are beside the point here
    and would put a second copy of the schema in this file. `catalog-schema` is the gate
    over the real records.
    """
    return f"---\nid: {source_id}\n---\n"


def a_repo(tmp_path: Path, *source_ids: str, fetched: dict[str, list[str]] | None = None) -> Path:
    """A repo root holding source records, and `data/raw/<id>/` for what was fetched.

    `fetched` maps a source id to the file names its fetch wrote. Each lands beside a
    `manifest_<name>.json`, which is the convention the fetch scripts in `src/fetch/`
    follow and the one `load()` resolves through until the lock arrives.
    """
    sources = tmp_path / "catalog" / "sources"
    sources.mkdir(parents=True)
    for source_id in source_ids:
        (sources / f"{source_id}.md").write_text(a_source_record(source_id), encoding="utf-8")
    for source_id, names in (fetched or {}).items():
        into = tmp_path / "data" / "raw" / source_id
        into.mkdir(parents=True)
        for name in names:
            (into / name).write_bytes(b"payload")
            a_manifest(into, name)
    return tmp_path


def a_manifest(into: Path, name: str, **extra: object) -> Path:
    """The manifest a fetch writes beside its payload.

    The keys are the ones the three fetch scripts write; `calcofi`'s also carries
    `content_type`, `last_modified` and `etag`, so the set is not fixed and `load()` must
    not read it. What `load()` does read is the manifest's own *file name*, which is the
    only place the local file name is recorded.
    """
    manifest = into / f"manifest_{name}.json"
    manifest.write_text(
        json.dumps(
            {
                "url": f"https://example.invalid/{name}",
                "sha256": "0" * 64,
                "bytes": 7,
                "fetched_at": "2026-09-10T00:00:00-07:00",
                "http_status": 200,
                **extra,
            }
        ),
        encoding="utf-8",
    )
    return manifest


# --- what load() reaches --------------------------------------------------------------


@pytest.mark.parametrize("source_id, count", sorted(MEASURED.items()))
def test_load_reaches_every_file_a_source_holds(tmp_path: Path, source_id: str, count: int):
    # The multi-file case the issue names: a signature returning a single Path could not
    # express two of these three, and a test that exercised only `noaa_oni` would not
    # notice. Parametrised over all three so the single-file source is the special case
    # rather than the shape the tests are written around.
    names = [f"{source_id}_{n}.txt" for n in range(count)]
    root = a_repo(tmp_path, source_id, fetched={source_id: names})

    files = load(source_id, root=root)

    assert sorted(files) == sorted(names)
    assert all(path.is_file() for path in files.values())


def test_load_is_keyed_by_file_name_so_a_caller_can_pick_one(tmp_path: Path):
    # `calcofi` holds a cast file and a bottle file, which are different data; a figure
    # has to be able to say which it plots. A list would make that an index, and nothing
    # in the catalog states an order for the files.
    root = a_repo(
        tmp_path, "calcofi", fetched={"calcofi": ["siocalcofiHydroCast.csv", "bottle.csv"]}
    )

    files = load("calcofi", root=root)

    assert files["siocalcofiHydroCast.csv"].read_bytes() == b"payload"
    assert files["siocalcofiHydroCast.csv"].name == "siocalcofiHydroCast.csv"


def test_load_iterates_in_a_fixed_order_whatever_the_directory_gives(tmp_path: Path, monkeypatch):
    # A figure that iterates the mapping must plot the same series on every machine, so
    # `load` imposes an order rather than passing the directory's through. The listing is
    # reversed here because the filesystem's own order cannot be chosen and NTFS returns
    # names sorted: without this, dropping the sort from `load` survives the suite on
    # Windows and is caught only on the Ubuntu half of CI. Verified by sweeping it.
    names = ["c.txt", "a.txt", "b.txt"]
    root = a_repo(tmp_path, "sio_shore_stations", fetched={"sio_shore_stations": names})
    listing = Path.glob
    monkeypatch.setattr(
        Path, "glob", lambda self, pattern: reversed(sorted(listing(self, pattern)))
    )

    files = load("sio_shore_stations", root=root)

    assert list(files) == ["a.txt", "b.txt", "c.txt"]


def test_load_orders_names_that_differ_only_in_case_the_same_way_everywhere(tmp_path: Path):
    # The order must be the *file names'*, not the Paths'. `sorted()` over Path objects
    # compares a case-folded form on Windows and the raw string on POSIX, so this set
    # comes back `_x, a, B` here and `B, _x, a` on the Ubuntu half of CI - and #48 compares
    # committed bytes, which would then never agree on both. Found by the audit of PR #67.
    #
    # Three names chosen so that case changes the order without changing identity: `B`
    # sorts before `_` and `a` by code point and after both when folded. A pair like
    # `A.csv`/`a.csv` cannot be the fixture - a case-insensitive filesystem holds one file
    # for the two, and the test would silently measure two files instead of three.
    names = ["B.csv", "a.csv", "_x.csv"]
    root = a_repo(tmp_path, "calcofi", fetched={"calcofi": names})

    files = load("calcofi", root=root)

    assert list(files) == ["B.csv", "_x.csv", "a.csv"]


def test_load_ignores_a_file_no_manifest_names(tmp_path: Path):
    # The stale-file case: `load()` resolves through the manifests, not the listing, so a
    # payload left behind by an earlier fetch is not handed to a figure as current.
    root = a_repo(tmp_path, "noaa_oni", fetched={"noaa_oni": ["oni.ascii.txt"]})
    (root / "data" / "raw" / "noaa_oni" / "oni.ascii.old.txt").write_bytes(b"stale")

    files = load("noaa_oni", root=root)

    assert list(files) == ["oni.ascii.txt"]


def test_load_does_not_hand_back_the_manifests_themselves(tmp_path: Path):
    root = a_repo(tmp_path, "noaa_oni", fetched={"noaa_oni": ["oni.ascii.txt"]})

    files = load("noaa_oni", root=root)

    assert not any(name.startswith("manifest_") for name in files)


def test_load_finds_the_repo_root_from_the_working_directory(tmp_path: Path, monkeypatch):
    # A notebook runs with its own folder as the working directory, two levels under the
    # root, so a figure cell calls `load("noaa_oni")` with no root at all.
    root = a_repo(tmp_path, "noaa_oni", fetched={"noaa_oni": ["oni.ascii.txt"]})
    here = root / "notebooks" / "1_physical_environment"
    here.mkdir(parents=True)
    monkeypatch.chdir(here)

    assert list(load("noaa_oni")) == ["oni.ascii.txt"]


# --- what load() raises ---------------------------------------------------------------


def test_load_raises_for_an_id_that_is_not_a_source_record(tmp_path: Path):
    root = a_repo(tmp_path, "noaa_oni", fetched={"noaa_oni": ["oni.ascii.txt"]})

    with pytest.raises(KeyError) as raised:
        load("not_a_record", root=root)

    # On a phrase the path cannot spell: tmp_path is named after this test, so an
    # assertion on "not_a_record" alone would pass on the directory name.
    assert "is not a source record" in str(raised.value)


def test_load_raises_when_there_is_no_data_directory(tmp_path: Path):
    # A fresh clone has none - `data/` is git-ignored - and the figure-bearing notebook
    # is committed with its outputs, so a reader never needs to run it.
    root = a_repo(tmp_path, "noaa_oni")

    with pytest.raises(FileNotFoundError) as raised:
        load("noaa_oni", root=root)

    assert "git-ignored" in str(raised.value)
    assert "fetch_script" in str(raised.value)


def test_load_raises_when_a_source_has_been_catalogued_but_not_fetched(tmp_path: Path):
    root = a_repo(tmp_path, "noaa_oni", "calcofi", fetched={"calcofi": ["cast.csv"]})

    with pytest.raises(FileNotFoundError) as raised:
        load("noaa_oni", root=root)

    assert "nothing fetched" in str(raised.value)


def test_load_raises_when_a_source_directory_holds_no_manifest(tmp_path: Path):
    root = a_repo(tmp_path, "noaa_oni")
    (root / "data" / "raw" / "noaa_oni").mkdir(parents=True)

    with pytest.raises(FileNotFoundError) as raised:
        load("noaa_oni", root=root)

    assert "nothing fetched" in str(raised.value)


def test_load_raises_when_a_manifest_names_a_file_that_is_not_there(tmp_path: Path):
    # The half-fetch: the manifest was written and the payload was not, or was deleted
    # afterwards. Handing back a Path that does not exist would push the failure into the
    # figure, where it reads as a plotting bug.
    root = a_repo(tmp_path, "noaa_oni", fetched={"noaa_oni": ["oni.ascii.txt"]})
    (root / "data" / "raw" / "noaa_oni" / "oni.ascii.txt").unlink()

    with pytest.raises(FileNotFoundError) as raised:
        load("noaa_oni", root=root)

    assert "named by a manifest" in str(raised.value)


def test_load_raises_when_the_working_directory_is_under_no_repo(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(FileNotFoundError) as raised:
        load("noaa_oni")

    # Both halves, written out around the path in the middle. This is the first module in
    # the repo whose messages a person reads rather than a gate, and the remediation clause
    # is the half that tells them what to do: a sweep rewrote it and the whole suite stayed
    # green until this assertion existed. Found by the audit of PR #67.
    message = str(raised.value)
    assert message.startswith("no catalog/ at or above ")
    assert message.endswith(
        "run a notebook from inside the repo, or name the root with load(source_id, root=...)."
    )

"""Tests for the builder: records in, one topic notebook out.

The fixture is tests/fixtures/notebook/ - a miniature repo, like the schema fixtures, so
check_catalog() runs on it unchanged. It carries what the real catalog does not yet have
and the builder must still render: a reference, an exclusion, a source that fits no
sub-topic, a source that is not held, and two sources in one section under different
region tags. The real catalog is exercised too, at the end, but it reaches four of the
builder's paths and no more.

Two properties fail quietly and so are asserted on serialized JSON rather than on
NotebookNode objects: two builds of the same catalog are identical, and a cell the
builder did not generate comes through untouched.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

from kelpcatalog import Catalog, Record, check_catalog
from kelpcatalog.build import (
    COVERAGE_CHARS,
    EMPTY_CELL,
    GENERATED,
    GENERATED_KEY,
    build_topic,
    write_notebook,
)
from kelpcatalog.plan import TOPIC_QUESTIONS
from kelpcatalog.schema import TOPICS

ROOT = Path(__file__).parents[1]
FIXTURES = Path(__file__).parent / "fixtures"

# The nine sections CONTEXT.md, "Notebooks", requires of 11_ocean_climate: one per
# sub-topic in TOPICS order, then the three fixed ones.
OCEAN_CLIMATE_SECTIONS = [
    "temperature",
    "salinity",
    "nutrients",
    "upwelling-enso",
    "heatwaves",
    "oxygen-ph",
    "General",
    "Not held",
    "Reviewed and not included",
]

# One generated cell per section, its id derived from the section's identity so a rebuild
# that changes no record changes no byte. Typed out here rather than imported: an id that
# silently changed would take every notebook's diff with it.
OCEAN_CLIMATE_CELL_IDS = [
    "kelpcatalog-overview",
    "kelpcatalog-subtopic-temperature",
    "kelpcatalog-subtopic-salinity",
    "kelpcatalog-subtopic-nutrients",
    "kelpcatalog-subtopic-upwelling-enso",
    "kelpcatalog-subtopic-heatwaves",
    "kelpcatalog-subtopic-oxygen-ph",
    "kelpcatalog-general",
    "kelpcatalog-not-held",
    "kelpcatalog-reviewed",
]


def a_catalog(case: str = "notebook") -> Catalog:
    catalog, problems = check_catalog(FIXTURES / case)
    assert problems == [], "\n".join(map(str, problems))
    return catalog


def an_empty_catalog() -> Catalog:
    return Catalog(root=FIXTURES / "notebook")


def headings(nb, level: int = 2) -> list[str]:
    marker = "#" * level + " "
    return [
        line[len(marker) :]
        for cell in nb.cells
        for line in cell.source.splitlines()
        if line.startswith(marker)
    ]


def sections(nb) -> dict[str, str]:
    """Each generated cell's source, keyed by its heading."""
    out = {}
    for cell in nb.cells:
        head = next((ln for ln in cell.source.splitlines() if ln.startswith("## ")), None)
        if head is not None:
            out[head[3:]] = cell.source
    return out


def generated(nb) -> list:
    return [c for c in nb.cells if c.metadata.get(GENERATED_KEY) == GENERATED]


# --- the fixture -------------------------------------------------------------------


def test_the_notebook_fixture_is_a_valid_catalog():
    catalog = a_catalog()
    assert {r.id for r in catalog.records["sources"]} == {
        "shore_temp",
        "global_index",
        "bare_climate",
        "ask_first",
        "elsewhere",
    }
    assert {r.id for r in catalog.records["references"]} == {
        "andrews2020",
        "brooks2019",
        "carter2018",
    }
    assert len(catalog.records["excluded"]) == 2


# --- the five sections CONTEXT.md specifies ----------------------------------------


def test_the_notebook_has_every_section_in_order():
    nb = build_topic("ocean-climate", a_catalog())
    assert headings(nb) == OCEAN_CLIMATE_SECTIONS


def test_section_one_prints_the_question_verbatim():
    nb = build_topic("ocean-climate", a_catalog())
    assert TOPIC_QUESTIONS["ocean-climate"] in nb.cells[0].source
    assert headings(nb, level=1) == ["ocean-climate"]


def test_section_one_counts_the_topics_sources_and_references():
    # Four of the fixture's five sources carry an ocean-climate tag; `elsewhere` does
    # not. Two of its three references do; carter2018 does not.
    nb = build_topic("ocean-climate", a_catalog())
    assert "4 sources" in nb.cells[0].source
    assert "2 references" in nb.cells[0].source


def test_section_one_carries_a_region_by_subtopic_table():
    # A row per region in use, in the notebook's region order, and a column per section
    # a source can land in - the sub-topics, and General for a bare tag. The counts are
    # the fixture's: shore_temp under temperature and salinity, ask_first under
    # nutrients, all three tagged scb; global_index under temperature, tagged global;
    # bare_climate under General.
    overview = build_topic("ocean-climate", a_catalog()).cells[0].source
    assert overview.splitlines()[-4:] == [
        "| region | temperature | salinity | nutrients | upwelling-enso | heatwaves"
        " | oxygen-ph | General |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
        "| Southern California Bight | 1 | 1 | 1 | 0 | 0 | 0 | 1 |",
        "| No regional bound | 1 | 0 | 0 | 0 | 0 | 0 | 0 |",
    ]


@pytest.mark.parametrize("topic", list(TOPICS))
def test_every_topic_has_every_section_even_with_no_sources(topic: str):
    # Eight of the ten topics have no sources at all today, and the notebook-structure
    # gate (#43) asserts the sections regardless.
    nb = build_topic(topic, an_empty_catalog())
    assert headings(nb) == [
        *TOPICS[topic],
        "General",
        "Not held",
        "Reviewed and not included",
    ]


def test_an_unknown_topic_raises_and_says_so():
    # TOPICS[topic] would raise a bare KeyError a few frames in; the guard is there to
    # name what went wrong, so the message is what this pins.
    with pytest.raises(KeyError, match="unknown topic"):
        build_topic("kelp-genomics", a_catalog())


# --- which section a source lands in -----------------------------------------------


def test_a_subtopic_source_renders_in_its_sections_and_no_other():
    body = sections(build_topic("ocean-climate", a_catalog()))
    assert "shore_temp" in body["temperature"]
    assert "shore_temp" in body["salinity"]
    for name in ("nutrients", "upwelling-enso", "heatwaves", "oxygen-ph", "General"):
        assert "shore_temp" not in body[name], name


def test_a_bare_topic_source_renders_under_general_only():
    body = sections(build_topic("ocean-climate", a_catalog()))
    assert "bare_climate" in body["General"]
    for name in OCEAN_CLIMATE_SECTIONS:
        if name != "General":
            assert "bare_climate" not in body[name], name


def test_a_source_of_another_topic_renders_nowhere():
    nb = build_topic("ocean-climate", a_catalog())
    assert "elsewhere" not in "\n".join(c.source for c in nb.cells)


def test_regions_group_in_the_notebooks_own_order():
    # global sorts last and is headed "No regional bound" (#40), so the Bight-wide
    # source leads the section and the unbounded one follows.
    temperature = sections(build_topic("ocean-climate", a_catalog()))["temperature"]
    scb = temperature.index("Southern California Bight")
    unbounded = temperature.index("No regional bound")
    assert scb < unbounded
    assert temperature.index("shore_temp") < temperature.index("global_index")


# --- the sources table -------------------------------------------------------------


def test_the_sources_table_has_the_columns_context_md_names():
    temperature = sections(build_topic("ocean-climate", a_catalog()))["temperature"]
    header = next(ln for ln in temperature.splitlines() if ln.startswith("| id |"))
    assert [c.strip() for c in header.strip("|").split("|")] == [
        "id",
        "title",
        "steward",
        "status",
        "tier",
        "coverage",
        "link",
    ]


def test_the_id_links_to_the_record():
    temperature = sections(build_topic("ocean-climate", a_catalog()))["temperature"]
    assert "[shore_temp](../../catalog/sources/shore_temp.md)" in temperature


def test_the_link_column_prefers_the_doi():
    temperature = sections(build_topic("ocean-climate", a_catalog()))["temperature"]
    assert "https://doi.org/10.5555/shore.temp" in temperature
    # global_index has no doi, so its url is the link.
    assert "https://example.org/index.txt" in temperature


def test_coverage_is_truncated_and_the_record_carries_the_rest():
    catalog = a_catalog()
    full = next(r for r in catalog.records["sources"] if r.id == "shore_temp").data["coverage"]
    assert len(full) > COVERAGE_CHARS, "the fixture must have coverage worth truncating"
    temperature = sections(build_topic("ocean-climate", catalog))["temperature"]
    assert full not in temperature
    assert full[:60] in temperature
    row = next(ln for ln in temperature.splitlines() if ln.startswith("| [shore_temp]"))
    coverage_cell = row.strip("|").split("|")[5].strip()
    assert coverage_cell.endswith("…")
    assert len(coverage_cell) <= COVERAGE_CHARS + 1
    # And it cuts on a word boundary: what is kept is a prefix of the field ending
    # where a word ends, not eight letters into "beginning".
    kept = coverage_cell.removesuffix("…")
    assert full.startswith(kept)
    assert not full[len(kept)].isalnum()


def test_a_source_stating_no_coverage_renders_an_empty_cell():
    nutrients = sections(build_topic("ocean-climate", a_catalog()))["nutrients"]
    row = next(ln for ln in nutrients.splitlines() if ln.startswith("| [ask_first]"))
    cells = [c.strip() for c in row.strip("|").split("|")]
    assert cells[5] == "—"
    assert cells[6] == "—"  # url and doi are both null: nothing to link to


def test_an_empty_section_says_so_rather_than_printing_an_empty_table():
    body = sections(build_topic("ocean-climate", a_catalog()))
    assert "| id |" not in body["heatwaves"]
    assert "No sources" in body["heatwaves"]


# --- references --------------------------------------------------------------------


def test_a_reference_renders_in_its_subtopic_section():
    body = sections(build_topic("ocean-climate", a_catalog()))
    assert "andrews2020" in body["temperature"]
    assert "Andrews A (2020)" in body["temperature"]
    for name in OCEAN_CLIMATE_SECTIONS:
        if name != "temperature":
            assert "andrews2020" not in body[name], name


def test_a_bare_topic_reference_renders_under_general():
    body = sections(build_topic("ocean-climate", a_catalog()))
    assert "brooks2019" in body["General"]


def test_a_reference_of_another_topic_renders_nowhere():
    nb = build_topic("ocean-climate", a_catalog())
    assert "carter2018" not in "\n".join(c.source for c in nb.cells)


# --- not held, and reviewed and not included ---------------------------------------


def test_not_held_and_on_request_sources_carry_their_human_task():
    not_held = sections(build_topic("ocean-climate", a_catalog()))["Not held"]
    assert "ask_first" in not_held
    assert "H1" in not_held


def test_a_not_held_source_also_appears_in_its_subtopic_table():
    # CONTEXT.md puts NOT HELD and ON REQUEST sources in section 4 and does not say
    # whether they also appear in section 2. This PR reads section 2's table as holding
    # every source tagged with the sub-topic - the status and tier columns are there to
    # say which - and section 4 as repeating them with the one field the table has no
    # column for. See the PR body.
    nutrients = sections(build_topic("ocean-climate", a_catalog()))["nutrients"]
    assert "ask_first" in nutrients
    assert "ON REQUEST" in nutrients


def test_a_held_source_is_not_in_the_not_held_section():
    not_held = sections(build_topic("ocean-climate", a_catalog()))["Not held"]
    assert "shore_temp" not in not_held


def test_exclusions_render_for_their_topic_only():
    reviewed = sections(build_topic("ocean-climate", a_catalog()))["Reviewed and not included"]
    assert "bight-adjacent-2026" in reviewed
    assert "Baja California site" in reviewed
    assert "off-topic-2026" not in reviewed


# --- generated cells ---------------------------------------------------------------


def test_the_generated_marker_is_the_one_context_md_names():
    # CONTEXT.md, "Notebooks": "Generated cells are marked in cell metadata
    # (`kelpcatalog: generated`)". Every other assertion imports these symbols,
    # so nothing else holds them to the prose.
    assert (GENERATED_KEY, GENERATED) == ("kelpcatalog", "generated")


def test_every_cell_the_builder_writes_is_marked_generated():
    nb = build_topic("ocean-climate", a_catalog())
    assert generated(nb) == list(nb.cells)
    assert all(c.cell_type == "markdown" for c in nb.cells)


def test_cell_ids_are_derived_from_section_identity():
    nb = build_topic("ocean-climate", a_catalog())
    assert [c.id for c in nb.cells] == OCEAN_CLIMATE_CELL_IDS


@pytest.mark.parametrize("topic", list(TOPICS))
def test_a_topics_cell_ids_are_unique(topic: str):
    ids = [c.id for c in build_topic(topic, an_empty_catalog()).cells]
    assert len(ids) == len(set(ids))
    assert len(ids) == len(TOPICS[topic]) + 4


def test_two_builds_of_the_same_catalog_are_identical():
    # nbformat.v4.new_markdown_cell assigns a random id per call, so this is the
    # assertion that a builder letting nbformat choose would fail - and it fails on the
    # serialized JSON, where the id lives, not on the NotebookNode.
    catalog = a_catalog()
    first = json.dumps(build_topic("ocean-climate", catalog), sort_keys=True)
    second = json.dumps(build_topic("ocean-climate", catalog), sort_keys=True)
    assert first == second


def test_a_rebuild_over_its_own_output_is_identical():
    catalog = a_catalog()
    once = build_topic("ocean-climate", catalog)
    twice = build_topic("ocean-climate", catalog, existing=once)
    assert json.dumps(twice, sort_keys=True) == json.dumps(once, sort_keys=True)


# --- the merge ---------------------------------------------------------------------
#
# CONTEXT.md: "figure cells are never generated and never touched". A pure build from
# records alone holds no figure cell, so writing one over the committed notebook would
# delete #47's figure in silence.


def a_figure_cell():
    # The outputs must be NotebookNodes, not plain dicts: nbformat reads them by
    # attribute as it serializes. Nothing wrote a figure cell to disk until the merge
    # was asserted at the byte level, so this was wrong and nothing said so.
    cell = new_code_cell("provenance(sources=['shore_temp'])")
    cell.outputs = [new_output("display_data", data={"text/plain": "<Figure>"})]
    cell.execution_count = 1
    return cell


def test_a_figure_cell_survives_a_rebuild_byte_for_byte():
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    figure = a_figure_cell()
    at = 1 + OCEAN_CLIMATE_SECTIONS.index("temperature") + 1
    existing.cells.insert(at, figure)
    before = json.dumps(figure, sort_keys=True)

    rebuilt = build_topic("ocean-climate", catalog, existing=existing)

    assert json.dumps(rebuilt.cells[at], sort_keys=True) == before
    assert len(rebuilt.cells) == len(OCEAN_CLIMATE_CELL_IDS) + 1


def test_a_figure_cell_holds_its_place_when_the_records_change():
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    at = 1 + OCEAN_CLIMATE_SECTIONS.index("temperature") + 1
    existing.cells.insert(at, a_figure_cell())
    # The catalog loses every source: the temperature cell's text changes, its identity
    # does not, and the figure stays under it.
    thinner = Catalog(root=catalog.root)
    thinner.records["regions"] = catalog.records["regions"]

    rebuilt = build_topic("ocean-climate", thinner, existing=existing)

    assert rebuilt.cells[at].cell_type == "code"
    assert "No sources" in rebuilt.cells[at - 1].source


def test_a_cell_above_the_first_generated_cell_is_kept_there():
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    note = new_markdown_cell("Hand-written, not generated.")
    existing.cells.insert(0, note)

    rebuilt = build_topic("ocean-climate", catalog, existing=existing)

    assert rebuilt.cells[0].source == "Hand-written, not generated."
    assert rebuilt.cells[1].id == "kelpcatalog-overview"


def test_a_kept_cell_whose_section_is_gone_is_not_lost():
    # A generated cell the plan no longer produces - a sub-topic CONTEXT.md drops -
    # takes no figure with it. The cell beneath it falls to the last surviving section
    # above it, or to the top of the notebook when there is none, as here.
    catalog = a_catalog()
    existing = new_notebook()
    stale = new_markdown_cell("## a sub-topic that no longer exists")
    stale.id = "kelpcatalog-subtopic-gone"
    stale.metadata[GENERATED_KEY] = GENERATED
    existing.cells = [stale, a_figure_cell()]

    rebuilt = build_topic("ocean-climate", catalog, existing=existing)

    assert [c.cell_type for c in rebuilt.cells].count("code") == 1
    assert "kelpcatalog-subtopic-gone" not in [c.id for c in rebuilt.cells]


def test_the_notebooks_own_metadata_survives():
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    existing.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3"}

    rebuilt = build_topic("ocean-climate", catalog, existing=existing)

    assert rebuilt.metadata["kernelspec"]["name"] == "python3"


def test_the_builder_does_not_mutate_the_notebook_it_was_given():
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    existing.cells.insert(0, new_markdown_cell("Hand-written, not generated."))
    before = json.dumps(existing, sort_keys=True)

    build_topic("ocean-climate", catalog, existing=existing)

    assert json.dumps(existing, sort_keys=True) == before


# --- the writer --------------------------------------------------------------------


def test_write_notebook_round_trips_and_ends_in_one_newline(tmp_path: Path):
    import nbformat

    nb = build_topic("ocean-climate", a_catalog())
    path = tmp_path / "1_physical_environment" / "11_ocean_climate.ipynb"
    write_notebook(nb, path)

    raw = path.read_bytes()
    assert b"\r\n" not in raw, ".gitattributes commits every file with LF"
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert json.dumps(nbformat.read(path, as_version=4), sort_keys=True) == json.dumps(
        nb, sort_keys=True
    )


def test_two_writes_of_the_same_notebook_are_the_same_bytes(tmp_path: Path):
    catalog = a_catalog()
    first, second = tmp_path / "a.ipynb", tmp_path / "b.ipynb"
    write_notebook(build_topic("ocean-climate", catalog), first)
    write_notebook(build_topic("ocean-climate", catalog), second)
    assert first.read_bytes() == second.read_bytes()


# --- the real catalog --------------------------------------------------------------


def test_every_topic_builds_from_the_real_catalog():
    catalog, problems = check_catalog(ROOT)
    assert problems == [], "\n".join(map(str, problems))
    for topic in TOPICS:
        nb = build_topic(topic, catalog)
        assert headings(nb) == [
            *TOPICS[topic],
            "General",
            "Not held",
            "Reviewed and not included",
        ]


def test_the_real_catalogs_only_bare_topic_tag_lands_under_general():
    # noaa_oni carries bare `waves-storms-sediment`; it is the whole of that notebook's
    # General section, and 11_ocean_climate's is empty.
    catalog, _ = check_catalog(ROOT)
    assert "noaa_oni" in sections(build_topic("waves-storms-sediment", catalog))["General"]
    assert "No sources" in sections(build_topic("ocean-climate", catalog))["General"]


def test_a_not_held_source_with_no_human_task_renders_an_empty_cell():
    # human_task is optional (CONTEXT.md, sources), and section 4 lists NOT HELD and
    # ON REQUEST sources "with their human_task". Built in memory rather than added to
    # the fixture, as test_schema.py builds a record for a single rule: one field is
    # what differs from ask_first.
    catalog = Catalog(root=FIXTURES / "notebook")
    catalog.records["regions"] = [
        Record("regions", "catalog/regions/scb.md", {"id": "scb", "name": "The Bight"})
    ]
    catalog.records["sources"] = [
        Record(
            "sources",
            "catalog/sources/no_task.md",
            {
                "id": "no_task",
                "title": "A source nobody has asked for yet",
                "steward": "A steward",
                "status": "NOT PUBLIC",
                "tier": "NOT HELD",
                "topics": ["ocean-climate/heatwaves"],
                "regions": ["scb"],
                "human_task": None,
            },
        )
    ]
    not_held = sections(build_topic("ocean-climate", catalog))["Not held"]
    row = next(ln for ln in not_held.splitlines() if ln.startswith("| [no_task]"))
    assert [c.strip() for c in row.strip("|").split("|")][5] == "—"


def test_an_on_request_source_lands_in_not_held_whatever_its_tier():
    # CONTEXT.md, section 4: "NOT HELD and ON REQUEST sources". NOT HELD is a tier and
    # ON REQUEST a status, so the section is the union of the two. ask_first is both, so
    # it cannot tell the two halves apart; this record is ON REQUEST and holds bytes.
    catalog = Catalog(root=FIXTURES / "notebook")
    catalog.records["regions"] = [
        Record("regions", "catalog/regions/scb.md", {"id": "scb", "name": "The Bight"})
    ]
    catalog.records["sources"] = [
        Record(
            "sources",
            "catalog/sources/asked_and_got.md",
            {
                "id": "asked_and_got",
                "title": "Casts released after a request",
                "steward": "A steward",
                "status": "ON REQUEST",
                "tier": "FETCHED",
                "topics": ["ocean-climate/heatwaves"],
                "regions": ["scb"],
                "human_task": "H3",
            },
        )
    ]
    body = sections(build_topic("ocean-climate", catalog))
    assert "asked_and_got" in body["Not held"]
    assert "asked_and_got" in body["heatwaves"]


# --- the writer, and the ids that reach it -----------------------------------------
#
# Every determinism assertion above is on `json.dumps(build_topic(...))`, and the one
# byte-level assertion builds with existing=None. That left the merge path unasserted at
# the byte level - which is the level #44's "regenerating a clean tree changes no bytes"
# and #47's "the figure cell is byte-identical" actually live at, and the level where
# nbformat's repair-on-serialize shows up.


def cells_of(row: str) -> list[str]:
    """A table row's cells, splitting on the pipes that are not escaped."""
    swapped = row.replace(r"\|", "\x00")
    return [c.strip().replace("\x00", r"\|") for c in swapped.strip("|").split("|")]


def written(nb, path: Path) -> bytes:
    write_notebook(nb, path)
    return path.read_bytes()


def test_two_writes_through_the_merge_are_the_same_bytes(tmp_path: Path):
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    existing.cells.insert(2, a_figure_cell())

    def build():
        return build_topic("ocean-climate", catalog, existing=existing)

    assert written(build(), tmp_path / "a.ipynb") == written(build(), tmp_path / "b.ipynb")


def test_a_kept_cell_with_no_id_gets_a_derived_one(tmp_path: Path):
    # nbformat.read leaves cells id-less below nbformat_minor 5, and nbformat.writes then
    # mints a random id as it serializes - so one build is different bytes on every write.
    catalog = a_catalog()
    existing = new_notebook()
    existing.nbformat_minor = 4
    generated_cell = new_markdown_cell("## temperature")
    generated_cell.id = "kelpcatalog-subtopic-temperature"
    generated_cell.metadata[GENERATED_KEY] = GENERATED
    figure = a_figure_cell()
    del figure["id"]
    existing.cells = [generated_cell, figure]

    def build():
        return build_topic("ocean-climate", catalog, existing=existing)

    kept = next(c for c in build().cells if c.cell_type == "code")
    assert kept.id == "kelpcatalog-kept-2"
    assert written(build(), tmp_path / "a.ipynb") == written(build(), tmp_path / "b.ipynb")


def test_a_kept_cell_that_copied_a_generated_id_gets_a_derived_one(tmp_path: Path):
    # The reachable half: #47's workflow is to copy a generated cell and drop the marker.
    # nbformat.writes emits DuplicateCellId and renumbers it, randomly, on every write.
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    squatter = new_markdown_cell("hand-written, carrying a generated cell's id")
    squatter.id = "kelpcatalog-overview"
    existing.cells.append(squatter)

    def build():
        return build_topic("ocean-climate", catalog, existing=existing)

    ids = [c.id for c in build().cells]
    assert len(ids) == len(set(ids))
    assert ids.count("kelpcatalog-overview") == 1
    assert written(build(), tmp_path / "a.ipynb") == written(build(), tmp_path / "b.ipynb")


def test_writing_a_built_notebook_asks_nbformat_to_repair_nothing(tmp_path: Path):
    # The sharpest statement of the two above: a repair is what mints the random value,
    # so the property is that a built notebook never triggers one.
    import warnings

    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    squatter = new_markdown_cell("x")
    squatter.id = "kelpcatalog-overview"
    orphan = new_markdown_cell("y")
    del orphan["id"]
    existing.cells += [squatter, orphan]
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        write_notebook(
            build_topic("ocean-climate", catalog, existing=existing), tmp_path / "n.ipynb"
        )


def test_a_minted_id_that_is_already_taken_is_minted_again():
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    holder = new_markdown_cell("holds the name a later position would mint")
    holder.id = "kelpcatalog-kept-1"
    orphan = new_markdown_cell("needs a name")
    del orphan["id"]
    existing.cells = [holder, orphan, *existing.cells]

    ids = [c.id for c in build_topic("ocean-climate", catalog, existing=existing).cells]
    assert len(ids) == len(set(ids))
    assert "kelpcatalog-kept-1" in ids and "kelpcatalog-kept-1x" in ids


def test_a_kept_cell_with_an_id_of_its_own_keeps_it():
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    existing.cells.insert(2, a_figure_cell())
    kept_id = existing.cells[2].id
    assert build_topic("ocean-climate", catalog, existing=existing).cells[2].id == kept_id


def test_the_result_shares_no_objects_with_the_notebook_it_was_given():
    # test_the_builder_does_not_mutate_the_notebook_it_was_given passes without the
    # deepcopies, because build_topic never writes through the alias. This is the
    # property those deepcopies are actually for.
    catalog = a_catalog()
    existing = build_topic("ocean-climate", catalog)
    existing.cells.insert(0, new_markdown_cell("hand-written"))
    existing.metadata["kernelspec"] = {"name": "python3"}

    rebuilt = build_topic("ocean-climate", catalog, existing=existing)

    assert rebuilt.cells[0] is not existing.cells[0]
    assert rebuilt.metadata is not existing.metadata
    assert rebuilt.metadata["kernelspec"] is not existing.metadata["kernelspec"]


# --- a record's prose is not markdown ----------------------------------------------


def a_source_record(**overrides) -> Catalog:
    """One region and one source, built in memory so that a single field is what differs."""
    catalog = Catalog(root=FIXTURES / "notebook")
    catalog.records["regions"] = [
        Record("regions", "catalog/regions/scb.md", {"id": "scb", "name": "The Bight"})
    ]
    data = {
        "id": "p",
        "title": "A source",
        "steward": "A steward",
        "status": "VERIFIED",
        "tier": "FETCHED",
        "topics": ["ocean-climate/temperature"],
        "regions": ["scb"],
        "url": None,
        "doi": None,
        "coverage": None,
    }
    data.update(overrides)
    catalog.records["sources"] = [Record("sources", "catalog/sources/p.md", data)]
    return catalog


def a_row(catalog: Catalog, section: str = "temperature") -> list[str]:
    body = sections(build_topic("ocean-climate", catalog))[section]
    return cells_of(next(ln for ln in body.splitlines() if ln.startswith("| [p]")))


def test_a_pipe_in_a_field_does_not_split_the_row():
    row = a_row(a_source_record(title="Temperature | salinity"))
    assert len(row) == 7
    assert row[1] == r"Temperature \| salinity"


def test_a_pipe_in_a_url_does_not_split_the_row():
    # No record carries one today. ArcGIS REST query URLs put a pipe in outFields, and
    # this catalog already has an ArcGIS-backed portal in view, so "today" is the claim.
    row = a_row(a_source_record(url="https://ex.org/query?outFields=a|b"))
    assert len(row) == 7
    assert row[6] == r"[link](https://ex.org/query?outFields=a\|b)"


def test_a_newline_in_a_field_does_not_break_the_table():
    row = a_row(a_source_record(title="A title\nover two lines"))
    assert len(row) == 7
    assert row[1] == "A title over two lines"


def test_an_empty_string_renders_as_an_absent_value():
    assert a_row(a_source_record(steward=""))[2] == EMPTY_CELL


def test_truncation_leaves_no_trailing_punctuation_before_the_ellipsis():
    assert a_row(a_source_record(coverage="word, " * 40))[5].endswith("word…")


def test_the_link_columns_anchor_is_the_doi_or_the_word_link():
    # One rule for all three tables: the doi where there is one - short, and the string a
    # reader copies - else the word `link`, which keeps a 116-character URL out of a cell.
    assert a_row(a_source_record(doi="10.5555/x", url="https://ex.org/"))[6] == (
        "[10.5555/x](https://doi.org/10.5555/x)"
    )
    assert a_row(a_source_record(url="https://ex.org/"))[6] == "[link](https://ex.org/)"
    assert a_row(a_source_record())[6] == EMPTY_CELL


def test_one_source_and_one_reference_are_counted_in_the_singular():
    catalog = a_source_record()
    catalog.records["references"] = [
        Record(
            "references",
            "catalog/references/andrews2020.md",
            {"citekey": "andrews2020", "ref": "R", "topics": ["ocean-climate"]},
        )
    ]
    assert "1 source · 1 reference" in build_topic("ocean-climate", catalog).cells[0].source


def test_a_topic_with_no_sources_states_the_count_once():
    overview = build_topic("canyon-dynamics", an_empty_catalog()).cells[0].source
    assert "0 sources · 0 references" in overview
    assert "No sources" not in overview
    assert "| region |" not in overview, "no matrix, not an empty one"


def test_sources_sort_by_id_whatever_order_the_catalog_holds_them_in():
    # load_catalog walks a sorted directory, so a loaded catalog cannot reach this; the
    # builder is pure and must not depend on the order it is handed records in.
    catalog = a_source_record()
    given = catalog.records["sources"][0]
    catalog.records["sources"] = [
        given,
        Record("sources", "catalog/sources/a.md", {**given.data, "id": "a"}),
    ]
    temperature = sections(build_topic("ocean-climate", catalog))["temperature"]
    assert temperature.index("[a](") < temperature.index("[p](")


# --- regions ------------------------------------------------------------------------


def test_a_source_tagging_two_regions_renders_under_each_in_region_order():
    # This records what the builder does, not a decision: whether a source with two region
    # tags repeats in every group or renders once is parked on #5, and no current source
    # carries two. The test is here so #44 cannot commit the opposite by accident.
    temperature = sections(
        build_topic("ocean-climate", a_source_record(regions=["global", "scb"]))
    )["temperature"]
    assert temperature.count("| [p](") == 2
    assert temperature.index("The Bight") < temperature.index("No regional bound")


def test_a_region_named_twice_renders_once_and_agrees_with_the_matrix():
    # `regions: [scb, scb]` is a record the schema accepts today (a bug filed against
    # schema.py under CLAUDE.md rule 3). Whatever the schema comes to allow, a source is
    # one source: two identical rows in one table against a matrix that counts one would
    # be the notebook contradicting itself inside a single cell.
    nb = build_topic("ocean-climate", a_source_record(regions=["scb", "scb"]))
    assert sections(nb)["temperature"].count("| [p](") == 1
    assert "| The Bight | 1 |" in nb.cells[0].source

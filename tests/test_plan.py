"""Tests for the notebook plan: the facts CONTEXT.md's "Notebooks" section states as
prose, held as data the builder can read.

Nothing here parses CONTEXT.md - CLAUDE.md forbids a parser for any prose file, and the
gap that leaves (nothing checks CONTEXT.md against the code) is parked on #5. So the
strings CONTEXT.md prints verbatim are typed out again below, from the file, and asserted
equal to the plan's. Two independent transcriptions agreeing is the check; it is the same
shape as test_schema.py's test_ocean_climate_carries_salinity_in_notebook_order.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kelpcatalog.plan import (
    GROUP_FOLDERS,
    INDEX_PATH,
    NO_REGIONAL_BOUND,
    NOTEBOOK_PATHS,
    TOPIC_QUESTIONS,
    region_heading,
    region_sort_key,
)
from kelpcatalog.schema import GLOBAL_REGION, GROUPS, TOPICS, Catalog, Record

# --- the ten questions -------------------------------------------------------------
#
# Typed from CONTEXT.md, "Topics: the ten questions", the third column, top to bottom.

CONTEXT_QUESTIONS = {
    "ocean-climate": (
        "What thermal, salinity, nutrient, oxygen and pH climate are the beds exposed to, "
        "and how is it trending?"
    ),
    "canyon-dynamics": (
        "How much cool, nutrient-rich water do canyon internal tides deliver, and when?"
    ),
    "waves-storms-sediment": (
        "When do swells and storms remove kelp, and what is the sand doing at the bed margins?"
    ),
    "substrate": "Where is the rock, how complex is it, and what does that predict?",
    "canopy": "How has surface canopy extent changed since 1911, bed by bed?",
    "bed-state": "What are the kelp and its community doing on the reef, where, and since when?",
    "grazers-predators-competitors": (
        "What sets urchin and competitor pressure on the beds, and what holds it in check?"
    ),
    "recruitment-connectivity": (
        "How do spores, larvae and genes move between beds, and what does that mean for recovery?"
    ),
    "water-quality-harvest": (
        "What do discharges, runoff, power plants and kelp harvest do to the beds?"
    ),
    "restoration-mitigation": (
        "What has been tried to restore or offset kelp loss, and what did it do?"
    ),
}


def every_topic_has_a_question() -> None:
    """The assertion two tests share: the one below, and the one that breaks it."""
    assert set(TOPIC_QUESTIONS) == set(TOPICS), (
        "every topic asks a question; CONTEXT.md's ten-questions table is the authority"
    )


def test_every_topic_has_a_question_and_it_is_verbatim():
    every_topic_has_a_question()
    assert TOPIC_QUESTIONS == CONTEXT_QUESTIONS


def test_a_topic_with_no_question_fails(monkeypatch: pytest.MonkeyPatch):
    # The plan cannot silently fall behind CONTEXT.md: adding a topic without adding its
    # question breaks the test above rather than rendering a notebook with no question.
    monkeypatch.setitem(TOPICS, "kelp-genomics", ())
    with pytest.raises(AssertionError):
        every_topic_has_a_question()


@pytest.mark.parametrize("topic", list(TOPICS))
def test_every_question_is_a_question(topic: str):
    assert TOPIC_QUESTIONS[topic].endswith("?")


# --- the eleven notebooks ----------------------------------------------------------


def test_every_topic_has_a_notebook_path():
    assert set(NOTEBOOK_PATHS) == set(TOPICS)


def test_the_eleven_paths_are_distinct():
    paths = [INDEX_PATH, *NOTEBOOK_PATHS.values()]
    assert len(paths) == 11
    assert len(set(paths)) == 11


@pytest.mark.parametrize("group, topics", list(GROUPS.items()))
def test_a_notebook_sits_in_its_group_folder(group: str, topics: tuple[str, ...]):
    for topic in topics:
        folder, _, name = NOTEBOOK_PATHS[topic].partition("/")
        assert folder == GROUP_FOLDERS[group]
        assert name.endswith(".ipynb")


@pytest.mark.parametrize("group, topics", list(GROUPS.items()))
def test_a_notebook_is_numbered_by_group_then_position(group: str, topics: tuple[str, ...]):
    # CONTEXT.md, "Notebooks": 1_physical_environment/11_ocean_climate. The folder carries
    # the group's number and the file repeats it, then the topic's place in the group.
    group_number = GROUP_FOLDERS[group].split("_")[0]
    for position, topic in enumerate(topics, start=1):
        number, _, stem = Path(NOTEBOOK_PATHS[topic]).stem.partition("_")
        assert number == f"{group_number}{position}"
        assert stem == topic.replace("-", "_")


def test_the_index_is_notebook_zero():
    assert INDEX_PATH == "00_index.ipynb"


def test_group_folders_cover_every_group():
    assert set(GROUP_FOLDERS) == set(GROUPS)


# --- the region order --------------------------------------------------------------


def test_the_region_order_issue_41_states():
    unsorted = [
        "global",
        "scb.islands.northern",
        "scb.mainland.san-diego",
        "scb",
        "scb.mainland.ventura",
    ]
    assert sorted(unsorted, key=region_sort_key) == [
        "scb",
        "scb.mainland.ventura",
        "scb.mainland.san-diego",
        "scb.islands.northern",
        "global",
    ]


def test_the_whole_tree_runs_depth_first():
    # A node, then all its descendants, before the next sibling; siblings in the order
    # CONTEXT.md lists them; islands, which it does not order, by id; global last.
    tree = [
        "scb",
        "scb.mainland",
        "scb.mainland.santa-barbara",
        "scb.mainland.ventura",
        "scb.mainland.los-angeles",
        "scb.mainland.orange",
        "scb.mainland.san-diego",
        "scb.islands",
        "scb.islands.northern",
        "scb.islands.northern.anacapa",
        "scb.islands.northern.santa-cruz",
        "scb.islands.southern",
        "scb.islands.southern.san-clemente",
        "scb.islands.southern.santa-catalina",
        "global",
    ]
    assert sorted(reversed(tree), key=region_sort_key) == tree


def test_a_county_sorts_before_the_islands_it_is_not_listed_with():
    # The tree is numbered by level, which would put scb.islands (level 2) before the
    # counties (level 3). The traversal, not the numbering, fixes the order.
    unsorted = ["scb.islands", "scb.mainland.santa-barbara", "scb.mainland.san-diego"]
    assert sorted(unsorted, key=region_sort_key) == [
        "scb.mainland.santa-barbara",
        "scb.mainland.san-diego",
        "scb.islands",
    ]


def test_islands_within_a_group_sort_by_id():
    unsorted = [
        "scb.islands.northern.santa-rosa",
        "scb.islands.northern.anacapa",
        "scb.islands.northern.san-miguel",
    ]
    assert sorted(unsorted, key=region_sort_key) == [
        "scb.islands.northern.anacapa",
        "scb.islands.northern.san-miguel",
        "scb.islands.northern.santa-rosa",
    ]


def test_global_sorts_last_not_first():
    assert region_sort_key(GLOBAL_REGION) > region_sort_key("scb")
    assert region_sort_key(GLOBAL_REGION) > region_sort_key("scb.islands.southern.santa-barbara")


@pytest.mark.parametrize(
    "region_id",
    [
        "3",  # a bed id: level 4 of the tree, but not a region id
        "leichter2023.point-loma",  # a site id: level 5, and it would split into segments
        "",
        "scbb",  # not a node; the root is scb and an id splits on "."
        "pacific",
    ],
)
def test_a_region_id_with_no_place_in_the_order_raises(region_id: str):
    with pytest.raises(ValueError):
        region_sort_key(region_id)


# --- region headings ---------------------------------------------------------------


def a_catalog(*regions: tuple[str, str]) -> Catalog:
    catalog = Catalog(root=Path("."))
    catalog.records["regions"] = [
        Record("regions", f"catalog/regions/{rid}.md", {"id": rid, "name": name})
        for rid, name in regions
    ]
    return catalog


def test_global_is_headed_no_regional_bound_with_no_region_record():
    assert region_heading(GLOBAL_REGION, a_catalog()) == "No regional bound"
    assert NO_REGIONAL_BOUND == "No regional bound"


def test_a_group_heading_is_its_nodes_name():
    catalog = a_catalog(("scb", "Southern California Bight"))
    assert region_heading("scb", catalog) == "Southern California Bight"


def test_a_heading_needs_the_region_record():
    # The order holds for a node before its record exists (6.3); the heading does not,
    # and a source cannot tag a region that has no record, so this cannot be reached
    # from the catalog. It raises rather than inventing a name.
    with pytest.raises(KeyError):
        region_heading("scb.mainland.ventura", a_catalog())

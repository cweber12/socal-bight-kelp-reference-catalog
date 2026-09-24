"""Schema tests. One valid and one invalid fixture per record type, plus the rules
that need more than one record to fail: unresolved links and duplicate ids.

Fixtures live in tests/fixtures/<case>/catalog/<kind>/*.md so a case is a whole
miniature repo and check_catalog() runs on it unchanged.

The last two sections come from a mutation sweep - disable one rule in schema.py, run
the suite, see whether anything fails - and pin the rules it found undefended: one
named test per conditional rule, then every field of every record type dropped and
mistyped, table-driven over RULES.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest

from kelpcatalog import check_catalog, parse_record, split_topic, topic_problem, validate
from kelpcatalog.schema import (
    GROUPS,
    HELD_TIERS,
    KINDS,
    RULES,
    STATUS,
    TABLE_TIERS,
    TIER,
    TOPICS,
    Catalog,
    Record,
)

FIXTURES = Path(__file__).parent / "fixtures"


def problems_of(case: str) -> list[str]:
    _, problems = check_catalog(FIXTURES / case)
    return [f"{p.field}: {p.message}" for p in problems]


# --- parsing -----------------------------------------------------------------------


def test_parse_requires_frontmatter():
    rec, probs = parse_record("id: x\n", "sources")
    assert rec is None
    assert probs[0].field == "frontmatter"


def test_parse_rejects_prose_body():
    text = "---\nid: x\n---\nThis bed is interesting because...\n"
    rec, probs = parse_record(text, "sources")
    assert rec is None
    assert probs[0].field == "body"


def test_parse_accepts_trailing_whitespace_only():
    rec, probs = parse_record("---\nid: x\n---\n\n  \n", "sources")
    assert rec is not None and probs == []


def test_parse_unknown_kind():
    rec, probs = parse_record("---\nid: x\n---\n", "notebooks")
    assert rec is None and probs[0].field == "kind"


def test_parse_frontmatter_must_be_mapping():
    rec, probs = parse_record("---\n- a\n- b\n---\n", "sources")
    assert rec is None and probs[0].field == "frontmatter"


# --- the valid miniature catalog ---------------------------------------------------


def test_valid_catalog_has_no_problems():
    catalog, problems = check_catalog(FIXTURES / "valid")
    assert problems == [], "\n".join(map(str, problems))
    for kind in KINDS:
        assert catalog.records[kind], f"valid fixture should contain a {kind} record"


def test_empty_catalog_is_valid(tmp_path: Path):
    for kind in KINDS:
        (tmp_path / "catalog" / kind).mkdir(parents=True)
    catalog, problems = check_catalog(tmp_path)
    assert problems == []
    assert not list(catalog.all())


# --- one invalid record per type ---------------------------------------------------


def test_invalid_source_reports_each_problem_once():
    probs = problems_of("invalid_source")
    assert "title: required field is missing" in probs
    assert "status: must be one of ('VERIFIED', 'PATTERN', 'NOT PUBLIC', 'ON REQUEST')" in probs
    assert "notes: unknown field; CONTEXT.md lists the allowed ones" in probs
    assert not any(p.startswith("id:") for p in probs)
    assert len([p for p in probs if p.startswith("title:")]) == 1, "one report per problem"


def test_missing_field_is_not_reported_twice():
    # 'status' missing entirely: reported as missing, not also as 'must be one of'
    text = "---\nid: x\n---\n"
    rec, _ = parse_record(text, "beds", "catalog/beds/x.md")
    assert rec is not None
    status_reports = [p for p in validate(rec) if p.field == "status"]
    assert [p.message for p in status_reports] == ["required field is missing"]


def test_fetched_source_needs_retrieved_and_script():
    probs = problems_of("invalid_tier")
    assert "retrieved: required when tier is FETCHED" in probs
    assert "fetch_script: required when tier is FETCHED" in probs


def test_transcribed_source_needs_provenance_and_file():
    probs = problems_of("invalid_transcribed")
    assert any(p.startswith("transcribed_from: required") for p in probs)
    assert any(p.startswith("file: required") for p in probs)


def test_invalid_reference():
    probs = problems_of("invalid_reference")
    assert "doi: a reference needs a doi or a url" in probs
    assert any(p.startswith("citekey: does not match") for p in probs)
    assert "topics: unknown topic 'kelp'" in probs


def test_invalid_excluded_missing_reason():
    assert "reason: required field is missing" in problems_of("invalid_excluded")


def test_invalid_region_parent_unresolved():
    assert "parent: 'scb.mainland' is not a region record" in problems_of("invalid_region")


def test_invalid_bed_status_and_region():
    probs = problems_of("invalid_bed")
    assert any(p.startswith("status: must be one of ('Open'") for p in probs)
    assert "region: 'scb.mainland.san-diego' is not a region record" in probs


def test_invalid_site_reports_each_problem_once():
    # CONTEXT.md, sites: bed is not a field; lat and lon are str, as printed; defined_by's
    # reference is a references/ record; retrieved is a date or null (#174).
    probs = problems_of("invalid_site")
    assert "bed: unknown field; CONTEXT.md lists the allowed ones" in probs
    assert "lat: expected str" in probs
    assert "defined_by.reference: 'nobody2020' is not a reference record" in probs
    assert "retrieved: expected date?" in probs
    assert len(probs) == 4, probs


def test_site_coordinates_load_byte_for_byte_as_printed():
    # CONTEXT.md, sites: lat*, lon* are str, as printed - DMS glyphs included. The fixture
    # carries the glyphs klingbeil's Table 2 prints (#176), so this reads the file through
    # load_catalog rather than a literal through parse_record.
    catalog, problems = check_catalog(FIXTURES / "valid")
    assert problems == []
    site = next(r for r in catalog.records["sites"] if r.id == "leichter2023.point-loma")
    assert site.data["lat"] == "32°41’24”N"
    assert site.data["lon"] == "117°16’12”W"


# --- cross-record rules ------------------------------------------------------------


def test_id_must_match_filename():
    assert "id: must equal the file name ('mismatch')" in problems_of("invalid_filename")


def test_duplicate_ids_across_kinds_are_allowed_but_within_a_kind_are_not():
    probs = problems_of("duplicate_id")
    assert any(p.startswith("id: duplicates catalog/sources/") for p in probs)


def test_unresolved_links_are_named():
    probs = problems_of("unresolved_links")
    assert "regions: 'scb.islands' is not a region record" in probs
    assert "references: 'nobody2020' is not a reference record" in probs
    assert "defined_by.source: 'nobody_2020' is not a source record" in probs


def test_global_is_an_allowed_region_without_a_record():
    catalog, problems = check_catalog(FIXTURES / "valid")
    src = next(r for r in catalog.records["sources"] if r.id == "noaa_oni")
    assert "global" in src.data["regions"]
    assert validate(src, catalog) == []


def test_validate_without_catalog_skips_links_only():
    catalog, _ = check_catalog(FIXTURES / "unresolved_links")
    src = catalog.records["sources"][0]
    assert validate(src, None) == []
    assert validate(src, catalog) != []


@pytest.mark.parametrize("topic", list(TOPICS))
def test_topic_vocabulary_is_kebab_case(topic: str):
    assert topic == topic.lower() and " " not in topic
    for sub in TOPICS[topic]:
        assert sub == sub.lower() and " " not in sub and "/" not in sub


def test_every_topic_belongs_to_exactly_one_group():
    placed = [t for group in GROUPS.values() for t in group]
    assert sorted(placed) == sorted(TOPICS), (
        "GROUPS and TOPICS disagree; CONTEXT.md is the authority"
    )
    assert len(placed) == len(set(placed))


@pytest.mark.parametrize(
    "tag, why",
    [
        ("ocean-climate", None),
        ("ocean-climate/heatwaves", None),
        ("ocean-climate/salinity", None),
        ("ocean-climate/nope", "unknown sub-topic 'nope' for 'ocean-climate'"),
        ("nope/heatwaves", "unknown topic 'nope'"),
        ("ocean-climate/heatwaves/extra", "malformed topic tag 'ocean-climate/heatwaves/extra'"),
        ("", "topic must be a non-empty string"),
    ],
)
def test_topic_tags_and_subtopics(tag: str, why: str | None):
    assert topic_problem(tag) == why


def test_ocean_climate_carries_salinity_in_notebook_order():
    # The tuple is the notebook's section order (CONTEXT.md, "Sub-topics"), so salinity
    # reads second, next to temperature: the other half of a shoreline hydrographic record.
    assert TOPICS["ocean-climate"] == (
        "temperature",
        "salinity",
        "nutrients",
        "upwelling-enso",
        "heatwaves",
        "oxygen-ph",
    )


def test_split_topic():
    assert split_topic("canopy/satellite") == ("canopy", "satellite")
    assert split_topic("canopy") == ("canopy", None)


def test_subtopic_tag_validates_in_a_record():
    catalog, problems = check_catalog(FIXTURES / "valid")
    oni = next(r for r in catalog.records["sources"] if r.id == "noaa_oni")
    assert "ocean-climate/upwelling-enso" in oni.data["topics"]
    assert problems == []


def test_excluded_records_may_carry_topics_but_need_not():
    catalog, problems = check_catalog(FIXTURES / "valid")
    ex = catalog.records["excluded"][0]
    assert ex.data["topics"] == ["bed-state/diver-surveys"]
    assert problems == []
    rec, _ = parse_record(
        "---\nslug: x\nreviewed: 2026-01-01\nwhat: w\nreason: r\n---\n",
        "excluded",
        "catalog/excluded/x.md",
    )
    assert rec is not None and validate(rec) == []


def test_catalog_ids_helper():
    c = Catalog(root=Path("."))
    assert c.ids("sources") == set()


# --- rules CONTEXT.md states, one test each ----------------------------------------
#
# Each of the nine below is a record that validate() accepted before this section
# existed. CONTEXT.md is the authority, so accepting them was the bug. The records are
# built inline rather than as fixtures: with no catalog, validate() runs every rule
# except the link checks, so one wrong field yields exactly one problem.


def reports(problems: list[Any]) -> list[tuple[str, str]]:
    return [(p.field, p.message) for p in problems]


def a_source(**overrides: Any) -> Record:
    """A NOT HELD source that validates; each override mutates one field."""
    data: dict[str, Any] = {
        "id": "x",
        "title": "A source",
        "steward": "A steward",
        "url": None,
        "status": "NOT PUBLIC",
        "tier": "NOT HELD",
        "access": ["Ask the program PI"],
        "license": "not stated",
        "variables": [],
        "retrieved": None,
        "topics": ["bed-state"],
        "regions": ["scb"],
    }
    data.update(overrides)
    return Record("sources", "catalog/sources/x.md", data)


def a_transcribed_source(**overrides: Any) -> Record:
    transcribed: dict[str, Any] = {
        "status": "VERIFIED",
        "tier": "TRANSCRIBED",
        "file": "catalog/tables/x.csv",
        "transcribed_from": {"reference": "konotchick2012", "table": "Table 1", "page": "p. 2"},
    }
    return a_source(**(transcribed | overrides))


def a_fetched_source(**overrides: Any) -> Record:
    fetched: dict[str, Any] = {
        "status": "VERIFIED",
        "tier": "FETCHED",
        "url": "https://origin.cpc.ncep.noaa.gov/oni.ascii.txt",
        "retrieved": "2026-09-07",
        "fetch_script": "src/fetch/oni.py",
    }
    return a_source(**(fetched | overrides))


def a_derived_source(**overrides: Any) -> Record:
    """A DERIVED source that validates: a table a committed script wrote from catalogued
    inputs (CONTEXT.md, "Vocabularies", tier). The script and the first input exist in
    tests/fixtures/valid, so it also validates against valid_catalog()."""
    derived: dict[str, Any] = {
        "status": "VERIFIED",
        "tier": "DERIVED",
        "access": [
            "Run src/derive/bed_region.py; it wrote catalog/tables/bed_region.csv, 1 row, "
            "2026-09-22"
        ],
        "variables": ["bed", "region"],
        "file": "catalog/tables/bed_region.csv",
        "derived_from": {
            "inputs": ["noaa_oni", "catalog/sites/"],
            "script": "src/derive/bed_region.py",
            "parameters": {"predicate": "intersects", "crs": "EPSG:3310", "tolerance": 0},
        },
        "topics": [],
    }
    return a_source(**(derived | overrides))


def derived_from(**overrides: Any) -> dict[str, Any]:
    """a_derived_source()'s provenance map with one key changed or, for None, dropped."""
    base: dict[str, Any] = dict(a_derived_source().data["derived_from"])
    for key, value in overrides.items():
        if value is None:
            del base[key]
        else:
            base[key] = value
    return base


SOURCE_OF_TIER = {
    "FETCHED": a_fetched_source,
    "TRANSCRIBED": a_transcribed_source,
    "DERIVED": a_derived_source,
    "NOT HELD": a_source,
}


def a_source_of(status: str, tier: str) -> Record:
    """A source whose tier-specific fields are all in order, so the status/tier
    pairing is the only thing left that can be wrong."""
    return SOURCE_OF_TIER[tier](status=status, tier=tier)


def test_every_tier_has_a_builder():
    # A fifth tier arrives with a fixture, or the parametrised tests below skip it. The two
    # sets are stated as literals because the tests over them are parametrised over them:
    # a member dropped from the constant would drop its cases, not fail them (PR #185, F5).
    assert set(SOURCE_OF_TIER) == set(TIER)
    assert HELD_TIERS == ("FETCHED", "TRANSCRIBED", "DERIVED")
    assert TABLE_TIERS == ("TRANSCRIBED", "DERIVED")


def a_reference(**overrides: Any) -> Record:
    data: dict[str, Any] = {
        "citekey": "konotchick2012",
        "ref": "Konotchick T et al. (2012) Estuarine, Coastal and Shelf Science 106:85-92",
        "doi": "10.1016/j.ecss.2012.04.026",
        "year": 2012,
        "topics": ["ocean-climate"],
    }
    data.update(overrides)
    return Record("references", "catalog/references/konotchick2012.md", data)


def an_excluded(**overrides: Any) -> Record:
    data: dict[str, Any] = {
        "slug": "example-excluded-2026",
        "reviewed": "2026-09-05",
        "what": "Example et al. 2026, a study at a site outside the Bight",
        "reason": "Baja California site, not the Southern California Bight",
    }
    data.update(overrides)
    return Record("excluded", "catalog/excluded/example-excluded-2026.md", data)


def a_region(**overrides: Any) -> Record:
    data: dict[str, Any] = {
        "id": "scb.mainland.san-diego",
        "name": "San Diego County",
        "parent": "scb.mainland",
        "defined_by": {"source": "kelp_surveys", "where": "Study area"},
    }
    data.update(overrides)
    return Record("regions", f"catalog/regions/{data['id']}.md", data)


def a_bed(**overrides: Any) -> Record:
    data: dict[str, Any] = {
        "id": "3",
        "cdfw_bed": 3,
        "name": "A bed",
        "status": "Open",
        "region": "scb.mainland.san-diego",
        "defined_by": "https://filelib.wildlife.ca.gov/Public/R7_MR/BIOLOGICAL/Kelp/",
    }
    data.update(overrides)
    return Record("beds", f"catalog/beds/{data['id']}.md", data)


def a_site(**overrides: Any) -> Record:
    data: dict[str, Any] = {
        "id": "leichter2023.point-loma",
        "program": "leichter2023",
        "name": "Point Loma mooring",
        "key": "PL",
        "lat": "32.69",
        "lon": "-117.27",
        "datum": None,
        "defined_by": {"source": "kelp_surveys", "where": "Table 1"},
        "retrieved": None,
    }
    data.update(overrides)
    return Record("sites", f"catalog/sites/{data['id']}.md", data)


def test_source_needs_at_least_one_region():
    # CONTEXT.md, sources: regions* ... list of region ids or `global`, >= 1
    assert validate(a_source()) == []
    assert reports(validate(a_source(regions=[]))) == [("regions", "at least one region")]


@pytest.mark.parametrize("tier", TABLE_TIERS)
def test_a_table_writing_tier_needs_a_file_under_catalog_tables(tier: str):
    # CONTEXT.md, sources: file ... required when TRANSCRIBED or DERIVED; a file under
    # `catalog/tables/`. The two tiers that write a table there are one set (#17 reads
    # it for the reverse check), so one test over the set.
    build = SOURCE_OF_TIER[tier]
    assert validate(build()) == []
    assert reports(validate(build(file=None))) == [
        ("file", f"required when tier is {tier} (catalog/tables/...)")
    ]
    assert reports(validate(build(file="data/tables/x.csv"))) == [
        ("file", "must be a file under catalog/tables/")
    ]


HOLDS_CONTENT = "status", "PATTERN cannot hold content; tier is {}"


@pytest.mark.parametrize("status", STATUS)
def test_not_held_admits_every_status(status: str):
    # CONTEXT.md, "Vocabularies": "Holding nothing excludes nothing, because a route can be
    # exercised without its bytes being kept, so a NOT HELD record carries whichever of the
    # four its own access steps support" - the sentence runs on to say that PATTERN there
    # means nobody here has tried the route. VERIFIED is among the four:
    # sbc_lter_landsat_canopy exercised its route by reading enough of the entity to show
    # that it opens.
    assert validate(a_source_of(status, "NOT HELD")) == []


@pytest.mark.parametrize("tier", HELD_TIERS)
@pytest.mark.parametrize("status", [s for s in STATUS if s != "PATTERN"])
def test_held_content_admits_every_status_but_pattern(status: str, tier: str):
    # CONTEXT.md, "Vocabularies": holding content excludes PATTERN and nothing else - it
    # does "not compel VERIFIED, because NOT PUBLIC and ON REQUEST state what a stranger
    # faces whatever is held here". DERIVED holds content too - the route to a derived
    # table is running its script - so #94 put it in the same exception and no other.
    assert validate(a_source_of(status, tier)) == []


@pytest.mark.parametrize("tier", HELD_TIERS)
def test_pattern_cannot_hold_content(tier: str):
    # CONTEXT.md, "Vocabularies": "Holding content means the route was exercised, so
    # FETCHED, TRANSCRIBED and DERIVED exclude PATTERN" - the sentence goes on to say they
    # do not compel VERIFIED, which test_held_content_admits_every_status_but_pattern
    # covers. One constraint, so one problem, and it names both fields.
    field, message = HOLDS_CONTENT
    assert reports(validate(a_source_of("PATTERN", tier))) == [(field, message.format(tier))]


def test_region_consortium_is_a_list_of_consortia():
    # CONTEXT.md, regions: consortium (list of RNKSC / CRKSC, non-empty only when
    # parent is scb.mainland). kelp.sccwrp.org splits Orange County between the two
    # and leaves Santa Barbara County to neither, so one value cannot state it.
    assert validate(a_region()) == []
    assert validate(a_region(consortium=["RNKSC"])) == []
    orange = a_region(id="scb.mainland.orange", name="Orange County", consortium=["RNKSC", "CRKSC"])
    assert validate(orange) == []
    santa_barbara = a_region(
        id="scb.mainland.santa-barbara", name="Santa Barbara County", consortium=[]
    )
    assert validate(santa_barbara) == []

    assert reports(validate(a_region(consortium=["SCCWRP"]))) == [
        ("consortium", "must be one of ('RNKSC', 'CRKSC')")
    ]
    assert reports(validate(a_region(consortium="RNKSC"))) == [("consortium", "expected list[str]")]
    assert reports(validate(a_region(consortium=None))) == [("consortium", "expected list[str]")]
    assert reports(validate(a_region(id="scb", parent=None, consortium=["RNKSC"]))) == [
        ("consortium", "non-empty only when parent is scb.mainland")
    ]


def test_human_task_is_an_h_number():
    # CONTEXT.md, sources: human_task ... an `H<n>` id
    assert validate(a_source(human_task="H2")) == []
    assert validate(a_source(human_task=None)) == []
    assert reports(validate(a_source(human_task="2"))) == [("human_task", r"does not match ^H\d+$")]


def test_license_stated_at_is_a_place_or_null():
    # CONTEXT.md, sources: license_stated_at is "str or null". The field is named here, not read
    # from RULES: the typed sweep below cannot tell "str?" from "str", and a list built from
    # RULES would drop the field with its "?".
    stated_at = "NWS Disclaimer, https://www.weather.gov/disclaimer"
    assert validate(a_source(license_stated_at=stated_at)) == []
    assert validate(a_source(license_stated_at=None)) == []


# --- site_key: where a source's own data keys its sites (#175) ---------------------
#
# CONTEXT.md, sources: site_key is a list of {file, column?, lat_column?, lon_column?},
# every value as the source's own metadata names it. The shape is checked here and
# nothing else: whether `file` names a held file is the lock's question (6.5), and no
# record carries the field yet (#175's non-goal).

SITE_KEY_SHAPES = {
    "file": [{"file": "bb4003017c_1_1.zip"}],
    "column": [{"file": "Bottom_temp_all_years_20260129.csv", "column": "SITE"}],
    "column+coords": [
        {
            "file": "PISCO_kelpforest_site_table.1.11.csv",
            "column": "site",
            "lat_column": "latitude",
            "lon_column": "longitude",
        }
    ],
    "coords": [{"file": "stations.csv", "lat_column": "lat", "lon_column": "lon"}],
}


@pytest.mark.parametrize("value", SITE_KEY_SHAPES.values(), ids=SITE_KEY_SHAPES.keys())
def test_site_key_admits_each_shape_the_row_describes(value: list[dict[str, str]]):
    # {file} alone is the same shape with three absent keys, not a shape of its own.
    assert validate(a_fetched_source(site_key=value)) == []


def test_site_key_absent_or_empty_says_nothing():
    # CONTEXT.md, sources: "Absent or empty says nothing about the source" - both validate,
    # as `sites: []` does, whatever the tier. No fixture carries site_key, so each
    # fixture's own validation is the absent case.
    for tier, build in SOURCE_OF_TIER.items():
        assert "site_key" not in build().data and validate(build()) == [], tier
        assert validate(build(site_key=[])) == [], tier


def test_site_key_is_non_empty_only_when_fetched():
    # CONTEXT.md, sources: one entry per file fetch_script stores that keys its rows by site,
    # "so non-empty only when FETCHED" - a NOT HELD record holds no file to name, and a table under
    # catalog/tables/ is the record's `file`, not one fetch_script stores.
    entry = [{"file": "Bottom_temp_all_years_20260129.csv", "column": "SITE"}]
    for tier, build in SOURCE_OF_TIER.items():
        expected = (
            [] if tier == "FETCHED" else [("site_key", "non-empty only when tier is FETCHED")]
        )
        assert reports(validate(build(site_key=entry))) == expected, tier


def test_site_key_null_inside_an_entry_is_absent():
    # add-source step 3 writes null for a scalar that does not apply, and a site's defined_by
    # reads an explicit null as absent; an entry does the same, so a fill can show every key.
    entry = {"file": "a.csv", "column": "SITE", "lat_column": None, "lon_column": None}
    assert validate(a_fetched_source(site_key=[entry])) == []
    assert reports(validate(a_fetched_source(site_key=[{"file": None}]))) == [
        ("site_key[0].file", "required field is missing")
    ]


def test_site_key_entry_must_be_a_mapping():
    # A bare string names a column and not the file it is a column of.
    assert reports(validate(a_fetched_source(site_key=["SITE"]))) == [
        ("site_key", "expected list[site_key]")
    ]


def test_site_key_entry_needs_a_file():
    # The second entry is the one reported, by its index.
    entries = [{"file": "sites.csv"}, {"column": "SITE"}]
    assert reports(validate(a_fetched_source(site_key=entries))) == [
        ("site_key[1].file", "required field is missing")
    ]


@pytest.mark.parametrize("half", ["lat_column", "lon_column"])
def test_site_key_lat_and_lon_columns_come_together(half: str):
    # A coordinate is a pair; one column of it locates nothing.
    entry = {"file": "sites.csv", half: "x"}
    assert reports(validate(a_fetched_source(site_key=[entry]))) == [
        ("site_key[0]", "lat_column and lon_column come together")
    ]


def test_site_key_entry_names_only_the_keys_the_row_lists():
    # The record-level "unknown field" problem, one level down: a key the row does not list
    # would otherwise pass silently, a misspelt lon_column among them.
    entry = {"file": "sites.csv", "station_column": "site"}
    assert reports(validate(a_fetched_source(site_key=[entry]))) == [
        ("site_key[0].station_column", "unknown key; CONTEXT.md lists the allowed ones")
    ]


def test_site_key_values_are_non_empty_strings():
    entry = {"file": "sites.csv", "column": ""}
    assert reports(validate(a_fetched_source(site_key=[entry]))) == [
        ("site_key[0].column", "expected str")
    ]


# --- citations: the citations a source prints for itself (#180) --------------------
#
# CONTEXT.md, sources: citations is a list of {as_printed, stated_at}, no other key, and
# the row names no tier. The shape is checked here and nothing else: whether an entry is
# the text as the source prints it is the audit's question, and no record carries
# the field yet (#180's non-goal).

# The two keys, as a literal: the tests below parametrize over this tuple, and a member
# dropped from the constant would drop its cases, not fail them (PR #185, F5).
CITE_KEYS = ("as_printed", "stated_at")

A_CITATION = {
    "as_printed": "Gillett, D.J., W. Enright, and J.B. Walker. 2022. A title.",
    "stated_at": "Foreword, printed page ii",
}

# Entries drafted from real sources, one per kind of bytes the catalog holds - HTML,
# JSON inside HTML, JSON, PDF - by the steps each stated_at names (PR #191's body,
# "Entries the cell admits"). None is committed to a record. cinp_kfm is NOT HELD: its
# profile prints two that differ for what url and doi name, and the list holds each.
IRMA_STEPS = (
    "in the JSON literal the HTML of https://irma.nps.gov/DataStore/Reference/Profile/2318436 "
    "passes to NPSDataStoreReferenceCoreModel.modelSerialize(...), its JSON string escapes "
    "decoded, each <a> element removed with the <img> inside it and nothing put in its place, "
    "and each run of whitespace replaced by one space (retrieved 2026-09-23)"
)
CINP_KFM_CITATIONS = [
    {
        "as_printed": (
            "Gabara SS and Others. 2026. Kelp Forest Monitoring at Channel Islands National "
            "Park (CHIS) by the Mediterranean Coast Inventory and Monitoring Network (MEDN) "
            "1982-2025 : Data Package. National Park Service. Fort Collins CO "
            "https://doi.org/10.57830/2318436"
        ),
        "stated_at": f"DisplayCitation {IRMA_STEPS}",
    },
    {
        "as_printed": (
            "Gabara SS , Chan KM , Whitaker S, Kushner D, Joshua S, Pandori LL , Woods DJ . "
            "2026. Kelp Forest Monitoring at Channel Islands National Park (CHIS) by the "
            "Mediterranean Coast Inventory and Monitoring Network (MEDN) 1982-2025 : Data "
            "Package. National Park Service. Fort Collins CO https://doi.org/10.57830/2318436"
        ),
        "stated_at": f"AllContactsDisplayCitation {IRMA_STEPS}",
    },
]
SIO_CITATIONS = [
    {
        "as_printed": (
            "Carter, Melissa L.; Flick, Reinhard E.; Terrill, Eric; Beckhaus, Elena C.; Martin, "
            "Kayla; Fey, Connie L.; Walker, Patricia W.; Largier, John L.; McGowan, John A. "
            "(2022). Shore Stations Program Data Archive: Current and historical coastal ocean "
            "temperature and salinity measurements from California stations. UC San Diego "
            "Library Digital Collections. https://doi.org/10.6075/J0S75GHD"
        ),
        "stated_at": (
            "the Cite This Work field of https://library.ucsd.edu/dc/collection/bb4719748r, the "
            "text of its one <p> with the <a> element's tags removed and its text kept, and "
            "leading and trailing whitespace trimmed (retrieved 2026-09-23)"
        ),
    },
]
KLINGBEIL_CITATIONS = [
    {
        "as_printed": (
            "Alberto, Filipe (2023). Macrocystis pyrifera before (2008) and after (2018-19) "
            "microsatellite data in Structure format [Dataset]. Dryad. "
            "https://doi.org/10.5061/dryad.nzs7h44v9"
        ),
        "stated_at": (
            'the <p id="dataset-citation"> in the HTML of '
            "https://datadryad.org/dataset/doi:10.5061/dryad.nzs7h44v9, the <a> element's tags "
            "removed and its text kept; and the body parameter of the same page's one mailto: "
            "share link, percent-decoded, between its 'Citation: ' label and its "
            "'Abstract: ' tail (retrieved 2026-09-23)"
        ),
    },
]
CDFW_KELP_ESR_CITATIONS = [
    {
        "as_printed": (
            "California Department of Fish and Wildlife. 2021. Giant Kelp and Bull Kelp, "
            "Macrocystis pyrifera and Nereocystis luetkeana, Enhanced Status Report."
        ),
        "stated_at": (
            "footer.citation in each of the seven held payloads, one and the same value in "
            "each, by the three steps the record's access states: the tags removed with "
            "nothing put in their place, the character entities resolved, each run of "
            "whitespace replaced by one space (held copy retrieved 2026-09-15)"
        ),
    },
]
SCCWRP_TR1289_CITATIONS = [
    {
        "as_printed": (
            "Gillett, D.J., W. Enright, and J.B. Walker. 2022. Southern California Bight 2018 "
            "Regional Monitoring Program: Volume III. Benthic Infauna. Technical Report 1289. "
            "Southern California Coastal Water Research Project. Costa Mesa, CA."
        ),
        "stated_at": (
            'Foreword, printed page iii (PDF page 5), under "The proper citation for this '
            'report is:", its three lines joined with one space (held copy retrieved '
            "2026-09-15)"
        ),
    },
]
DRAFTED_CITATIONS = {
    "cinp_kfm": (a_source, CINP_KFM_CITATIONS),
    "sio_shore_stations": (a_fetched_source, SIO_CITATIONS),
    "klingbeil_kelp_genotypes": (a_fetched_source, KLINGBEIL_CITATIONS),
    "cdfw_kelp_esr": (a_fetched_source, CDFW_KELP_ESR_CITATIONS),
    "sccwrp_tr1289": (a_fetched_source, SCCWRP_TR1289_CITATIONS),
}


@pytest.mark.parametrize("build, entries", DRAFTED_CITATIONS.values(), ids=DRAFTED_CITATIONS.keys())
def test_citations_admit_the_entries_drafted_from_real_sources(
    build: Any, entries: list[dict[str, str]]
):
    # A cell is checked against the records it will admit (PR #186, F1), on a fixture of
    # each record's own tier.
    assert validate(build(citations=entries)) == []


def test_citations_absent_or_empty_validate_on_every_tier():
    # CONTEXT.md, sources: "Absent or empty means none entered" - both validate, whatever
    # the tier. No fixture carries citations, so each fixture's own validation is the
    # absent case.
    for tier, build in SOURCE_OF_TIER.items():
        assert "citations" not in build().data and validate(build()) == [], tier
        assert validate(build(citations=[])) == [], tier


def test_citations_are_admitted_on_every_tier():
    # The row names no tier, unlike site_key's: a NOT HELD profile prints a citation as
    # readily as a held file does (cinp_kfm), so a tier condition would be a rule the row
    # lacks.
    for tier, build in SOURCE_OF_TIER.items():
        assert validate(build(citations=[A_CITATION])) == [], tier


def test_citations_entry_must_be_a_mapping():
    # A bare string is a citation with nowhere it was printed.
    assert reports(validate(a_source(citations=[A_CITATION["as_printed"]]))) == [
        ("citations", "expected list[cite]")
    ]


@pytest.mark.parametrize("key", CITE_KEYS)
def test_citations_entry_needs_each_key(key: str):
    # The second entry is the one reported, by its index.
    entries = [A_CITATION, {k: v for k, v in A_CITATION.items() if k != key}]
    assert reports(validate(a_source(citations=entries))) == [
        (f"citations[1].{key}", "required field is missing")
    ]


def test_citations_entry_names_only_the_keys_the_row_lists():
    # The record-level "unknown field" problem, one level down: a key the row does not
    # list would otherwise pass silently.
    entry = {**A_CITATION, "style": "ESIP"}
    assert reports(validate(a_source(citations=[entry]))) == [
        ("citations[0].style", "unknown key; CONTEXT.md lists the allowed ones")
    ]


@pytest.mark.parametrize("key", CITE_KEYS)
def test_citations_values_are_non_empty_strings(key: str):
    entry = {**A_CITATION, key: ""}
    assert reports(validate(a_source(citations=[entry]))) == [
        (f"citations[0].{key}", "expected str")
    ]


# --- variables: the named columns or fields of a source's data files (#90) ----------
#
# CONTEXT.md, sources: an entry is {name, description, unit, file?}, no other key, and
# until #182 an entry may be a str instead, one form to a list. The shape is checked here
# and nothing else: whether a `description` or a `unit` is what the source states for that
# column is the audit's question, and no record carries a map yet (#90's non-goal).
#
# The fixture is FETCHED throughout, because the row gives NOT HELD the empty list: a
# field's default fixture may be the tier that cannot carry it (PR #189, F2). No gate ties
# `variables` to the tier today, and adding one is not this slice's.

# The three keys every entry carries, as a literal: the tests below parametrize over this
# tuple, and a member dropped from the constant would drop its cases, not fail them (PR
# #185, F5). `file` is the fourth key and the optional one, so it is not in here.
VARIABLE_KEYS = ("name", "description", "unit")
# The two the row lets a record write as null, where the source states none.
VARIABLE_NULLABLE_KEYS = ("description", "unit")

A_VARIABLE = {"name": "temp_c", "description": "Water temperature", "unit": "degree Celsius"}

# Entries drafted from two records' own text - the two cases the Parking lot left S1 to
# settle (#5 issuecomment-5805925619 and its correction, issuecomment-5806181504). Neither
# is committed to a record. `description` is null in both because neither record's own text
# states one; which text a description quotes is the migration's question (rows M4, M5 and
# M8 of docs/prd/re-entry.md), not this slice's.

# catalog/sources/pisco_kelp_forest.md:104-106 states the 76 names as the union of seven
# tables' attributeNames and `size`'s unit as "number" in one table and "centimeter" in
# another. One statement per entry, each `file` naming the file that states it - one `unit`
# per entry cannot hold both.
PISCO_SIZE_VARIABLES = [
    {
        "name": "size",
        "description": None,
        "unit": "number",
        "file": ["PISCO_kelpforest_swath.1.11.csv"],
    },
    {
        "name": "size",
        "description": None,
        "unit": "centimeter",
        "file": ["PISCO_kelpforest_sizefreq.1.11.csv"],
    },
]

# catalog/sources/calcofi.md:52-56 states that five columns - time, latitude, longitude,
# cst_cnt and sta_id - appear in both of its files. Each is one entry whose `file` names
# both, stated once. The units are the two files' unit rows, which that cell says each file
# carries; the two that state none are null. The file names are the names src/fetch's
# script stored them under.
CALCOFI_FILES = [
    "siocalcofiHydroCast_d677_9801_7f83.csv",
    "siocalcofiHydroBottle_d677_9801_7f83.csv",
]
CALCOFI_SHARED_VARIABLES = [
    {"name": "time", "description": None, "unit": "UTC", "file": CALCOFI_FILES},
    {"name": "latitude", "description": None, "unit": "degrees_north", "file": CALCOFI_FILES},
    {"name": "longitude", "description": None, "unit": "degrees_east", "file": CALCOFI_FILES},
    {"name": "cst_cnt", "description": None, "unit": None, "file": CALCOFI_FILES},
    {"name": "sta_id", "description": None, "unit": None, "file": CALCOFI_FILES},
]
DRAFTED_VARIABLES = {
    "pisco_kelp_forest": PISCO_SIZE_VARIABLES,
    "calcofi": CALCOFI_SHARED_VARIABLES,
}


@pytest.mark.parametrize("entries", DRAFTED_VARIABLES.values(), ids=DRAFTED_VARIABLES.keys())
def test_variables_admit_the_entries_drafted_from_two_records(entries: list[dict[str, Any]]):
    # A cell is checked against the records it will admit (PR #186, F1). Both records are
    # FETCHED; the drafts are in the PR body and in no record.
    assert validate(a_fetched_source(variables=entries)) == []


def test_variables_entry_must_be_a_mapping_or_a_string():
    # Until #182 both forms validate, and one list holds one of them: a list that mixes
    # them is the half-migrated record, and it fails at the field rather than per entry.
    assert validate(a_fetched_source(variables=["campus", "method"])) == []
    assert validate(a_fetched_source(variables=[A_VARIABLE])) == []
    # A blank string names no column, as `list[str]` has it everywhere else in the table.
    assert reports(validate(a_fetched_source(variables=["campus", "  "]))) == [
        ("variables", "expected list[variable]")
    ]
    assert reports(validate(a_fetched_source(variables=["campus", A_VARIABLE]))) == [
        ("variables", "expected list[variable]")
    ]
    assert reports(validate(a_fetched_source(variables=[A_VARIABLE, "campus"]))) == [
        ("variables", "expected list[variable]")
    ]


def test_variables_string_entries_and_the_empty_list_validate_on_every_tier():
    # #90, Done when: "existing string-shaped records still validate". The empty list is
    # what the row gives NOT HELD and what four records carry on main.
    for tier, build in SOURCE_OF_TIER.items():
        assert validate(build(variables=["campus", "method"])) == [], tier
        assert validate(build(variables=[])) == [], tier


def test_the_derived_fixture_keeps_its_two_string_entries():
    # The row's "the CSV's columns when DERIVED" is unchanged by this slice, and the
    # fixture that carries it is the one a later migration would move.
    assert a_derived_source().data["variables"] == ["bed", "region"]
    assert validate(a_derived_source()) == []


def test_the_string_shaped_records_in_the_catalog_still_validate():
    # The catalog itself, not a fixture. The string-shaped records are counted rather than
    # pinned to a number, so a record migrated under #182's rows does not fail this test.
    # On main at 95dbac3 all 19 sources are string-shaped, 369 entries in all, 4 of them
    # the empty list.
    catalog, problems = check_catalog(ROOT)
    assert problems == []
    string_shaped = [
        rec
        for rec in catalog.records["sources"]
        if all(isinstance(e, str) for e in rec.data["variables"])
    ]
    assert string_shaped, "no string-shaped record left for this test to check"
    for rec in string_shaped:
        assert validate(rec, catalog) == [], rec.path


@pytest.mark.parametrize("key", VARIABLE_KEYS)
def test_variables_entry_needs_each_of_the_three_keys(key: str):
    # The second entry is the one reported, by its index. null is allowed for two of the
    # three; absent is allowed for none of them.
    entries = [A_VARIABLE, {k: v for k, v in A_VARIABLE.items() if k != key}]
    assert reports(validate(a_fetched_source(variables=entries))) == [
        (f"variables[1].{key}", "required field is missing")
    ]


def test_variables_entry_names_only_the_keys_the_row_lists():
    # The record-level "unknown field" problem, one level down: a key the row does not
    # list would otherwise pass silently. `units` is the plural a record could reach for.
    entry = {**A_VARIABLE, "units": "cm"}
    assert reports(validate(a_fetched_source(variables=[entry]))) == [
        ("variables[0].units", "unknown key; CONTEXT.md lists the allowed ones")
    ]


@pytest.mark.parametrize("value", [None, ""])
def test_variables_name_is_never_null_or_blank(value: Any):
    # The row: a column the source names nowhere is no entry (#90, Decision; #5
    # issuecomment-5761453102, klingbeil's two unnamed columns), so `name` has no null.
    entry = {**A_VARIABLE, "name": value}
    assert reports(validate(a_fetched_source(variables=[entry]))) == [
        ("variables[0].name", "expected str")
    ]


@pytest.mark.parametrize("key", VARIABLE_NULLABLE_KEYS)
def test_variables_description_and_unit_may_be_null(key: str):
    # "null where it states none" - the row's answer to the non-goal "do not invent
    # descriptions or units".
    assert validate(a_fetched_source(variables=[{**A_VARIABLE, key: None}])) == []


@pytest.mark.parametrize("key", VARIABLE_NULLABLE_KEYS)
def test_variables_description_and_unit_are_not_blank_strings(key: str):
    # A blank string is neither what the source states nor the null that says it states
    # none.
    assert reports(validate(a_fetched_source(variables=[{**A_VARIABLE, key: ""}]))) == [
        (f"variables[0].{key}", "expected str?")
    ]


def test_variables_file_is_a_list_of_file_names():
    # The row: `file` names the files an entry is stated for. A bare string is the shape a
    # record reaches for when only one file states it; the list is what a shared column
    # needs, so there is one form here too.
    entry = {**A_VARIABLE, "file": "siocalcofiHydroCast_d677_9801_7f83.csv"}
    assert reports(validate(a_fetched_source(variables=[entry]))) == [
        ("variables[0].file", "expected list[str]")
    ]
    assert reports(validate(a_fetched_source(variables=[{**A_VARIABLE, "file": [""]}]))) == [
        ("variables[0].file", "expected list[str]")
    ]


def test_variables_file_is_optional():
    # `file` is the one optional key: absent and an explicit null both say the entry names
    # no file, as a key written as null is absent in site_key and in a site's defined_by.
    assert validate(a_fetched_source(variables=[A_VARIABLE])) == []
    assert validate(a_fetched_source(variables=[{**A_VARIABLE, "file": None}])) == []


@pytest.mark.parametrize("bad", ["leichter2023", "leichter2023.point.loma", "leichter2023."])
def test_site_id_is_program_dot_site(bad: str):
    # CONTEXT.md, sites: id* (`<program>.<site>`, equals file name)
    assert validate(a_site()) == []
    assert reports(validate(a_site(id=bad))) == [
        ("id", "must be <program>.<site>, both parts non-empty")
    ]


def test_site_required_fields_are_pinned():
    # CONTEXT.md, sites: the starred rows. Stated as a literal because the sweep at the end
    # of this file is parametrised over RULES: a field flipped to optional would drop its
    # own case, not fail it (PR #185 F5; audit of PR #186, F5).
    required = tuple(name for name, (req, _) in RULES["sites"].items() if req)
    assert required == ("id", "program", "name", "key", "lat", "lon", "defined_by")


def test_site_carries_no_bed():
    # CONTEXT.md, sites: the schema has no bed field (#174); the region a site's
    # coordinates fall in is computed, a DERIVED table's (#177), and the record has no
    # field for it.
    assert reports(validate(a_site(bed=None))) == [
        ("bed", "unknown field; CONTEXT.md lists the allowed ones")
    ]


def test_site_lat_and_lon_are_strings_as_printed():
    # CONTEXT.md, sites: lat*, lon* are str, as the document prints them. A float is what
    # the value looks like once converted, and converting it is kept off the record.
    assert validate(a_site(lat="34.400275", lon="-119.842")) == []
    assert validate(a_site(lat="34°2’34.56”N", lon="119° 50’ 31.2” W")) == []
    assert reports(validate(a_site(lat=32.69))) == [("lat", "expected str")]
    assert reports(validate(a_site(lon=-117.27))) == [("lon", "expected str")]


def test_site_defined_by_names_exactly_one_document():
    # CONTEXT.md, sites: defined_by* is exactly one of {source, where} or {reference, where}
    # - the document that prints the coordinates. A bare string is the old shape.
    assert validate(a_site(defined_by={"reference": "klingbeil2022", "where": "Table 2"})) == []
    assert reports(validate(a_site(defined_by="10.3389/fmars.2023.1007789"))) == [
        ("defined_by", "expected map")
    ]
    both = {"source": "kelp_surveys", "reference": "klingbeil2022", "where": "Table 2"}
    assert reports(validate(a_site(defined_by=both))) == [
        ("defined_by", "names both source and reference; exactly one")
    ]
    assert reports(validate(a_site(defined_by={"where": "Table 2"}))) == [
        ("defined_by", "names neither source nor reference; exactly one")
    ]
    # A limb written as an explicit null is absent, the way the fixtures write datum and
    # retrieved: it neither counts as named nor is looked up (audit of PR #186, F3).
    one_null = {"source": None, "reference": "klingbeil2022", "where": "Table 2"}
    assert validate(a_site(defined_by=one_null)) == []
    assert reports(validate(a_site(defined_by={"source": None, "where": "Table 2"}))) == [
        ("defined_by", "names neither source nor reference; exactly one")
    ]
    for db in ({"source": "kelp_surveys"}, {"source": "kelp_surveys", "where": ""}):
        assert reports(validate(a_site(defined_by=db))) == [("defined_by.where", "expected str")]
    assert reports(validate(a_site(defined_by={"reference": "", "where": "Table 2"}))) == [
        ("defined_by.reference", "expected str")
    ]


def test_site_defined_by_must_resolve():
    # CONTEXT.md, "Gates": catalog-schema links only to records that exist. Each limb
    # resolves into its own directory: source into sources/, reference into references/.
    catalog = valid_catalog()
    assert validate(a_site(defined_by={"source": "kelp_surveys", "where": "x"}), catalog) == []
    assert validate(a_site(defined_by={"reference": "konotchick2012", "where": "x"}), catalog) == []
    assert reports(validate(a_site(defined_by={"source": "nobody", "where": "x"}), catalog)) == [
        ("defined_by.source", "'nobody' is not a source record")
    ]
    absent = {"reference": "nobody2020", "where": "x"}
    assert reports(validate(a_site(defined_by=absent), catalog)) == [
        ("defined_by.reference", "'nobody2020' is not a reference record")
    ]
    # A source citekey is not a reference, and the reverse; the limb names the directory.
    crossed = {"reference": "kelp_surveys", "where": "x"}
    assert reports(validate(a_site(defined_by=crossed), catalog)) == [
        ("defined_by.reference", "'kelp_surveys' is not a reference record")
    ]


def test_site_retrieved_is_a_date_or_null():
    # CONTEXT.md, sites: retrieved is date or null - the rule it follows on a source (#95's
    # site half, moved here by #174). Optional: the table marks it with no `*`.
    assert validate(a_site(retrieved="2026-09-23")) == []
    assert validate(a_site(retrieved=None)) == []
    dropped = {k: v for k, v in a_site().data.items() if k != "retrieved"}
    assert validate(Record("sites", "catalog/sites/leichter2023.point-loma.md", dropped)) == []
    assert reports(validate(a_site(retrieved="not-a-date"))) == [("retrieved", "expected date?")]


def test_site_datum_is_a_string_or_null():
    # CONTEXT.md, sites: datum is str or null, where the program states one. Named here
    # for the same reason as license_stated_at: the sweep cannot tell "str?" from "str".
    assert validate(a_site(datum="WGS84")) == []
    assert validate(a_site(datum=None)) == []
    dropped = {k: v for k, v in a_site().data.items() if k != "datum"}
    assert validate(Record("sites", "catalog/sites/leichter2023.point-loma.md", dropped)) == []


def test_bed_id_is_its_cdfw_bed_number():
    # CONTEXT.md, beds: id* (the bed number as a string, equals file name)
    assert validate(a_bed()) == []
    assert reports(validate(a_bed(cdfw_bed=4))) == [("id", "must equal cdfw_bed ('4')")]


# --- a record directory holds only records -----------------------------------------


def test_unexpected_file_under_a_record_directory_is_reported():
    # CONTEXT.md, "Record format": a record is one markdown file. Globbing for *.md
    # skipped anything else in silence, so a record saved as catalog/sources/stray.yaml
    # - the wrong extension, the content still YAML - left the gate green without it.
    _, problems = check_catalog(FIXTURES / "unexpected_file")
    assert [(p.path, p.field, p.message) for p in problems] == [
        ("catalog/sources/stray.yaml", "file", "unexpected file; catalog/sources/ holds *.md")
    ]


def test_gitkeep_and_transcribed_tables_are_not_unexpected():
    # .gitkeep holds an empty record directory in git, and catalog/tables/ holds the
    # transcribed and derived CSVs by design; neither is a stray. The equality above says they are
    # silent - this says the fixture still contains them to be silent about.
    tree = FIXTURES / "unexpected_file"
    assert (tree / "catalog" / "beds" / ".gitkeep").is_file()
    assert (tree / "catalog" / "tables" / "parnell2005_table1.csv").is_file()


# --- the conditional rules a mutation sweep found undefended ------------------------
#
# Sweep: disable one rule in schema.py, run the suite, see whether anything fails. A
# mutant that survives is a rule no test defends. Nine of the survivors were the
# conditional and cross-record rules below - each a rule CONTEXT.md states that a
# record could break in silence. One named test each; the per-field survivors are the
# table-driven pair at the end of this file.
#
# The five that need a repo on disk - a fetch script, a transcribed table, a bed, a
# site, a reference to resolve against - validate against tests/fixtures/valid, which
# is already a whole miniature repo, rather than a fixture tree of their own.


def valid_catalog() -> Catalog:
    catalog, problems = check_catalog(FIXTURES / "valid")
    assert problems == [], "\n".join(map(str, problems))
    return catalog


def test_tier_must_come_from_the_vocabulary():
    # CONTEXT.md, "Vocabularies": tier is FETCHED, TRANSCRIBED, DERIVED or NOT HELD.
    # status had this test from the start; tier did not, so 'FETCHD' validated.
    assert validate(a_source(tier="NOT HELD")) == []
    assert reports(validate(a_source(tier="FETCHD"))) == [("tier", f"must be one of {TIER}")]


def test_topics_needs_at_least_one_tag():
    # CONTEXT.md, sources and references: topics* ... >= 1. A source that fits no topic
    # means adding a topic, never an empty list.
    assert reports(validate(a_source(topics=[]))) == [("topics", "at least one topic")]
    assert reports(validate(a_reference(topics=[]))) == [("topics", "at least one topic")]
    # excluded.topics is optional, so an empty list there is not the same failure.
    assert validate(an_excluded(topics=[])) == []


def test_fetch_script_must_exist_in_the_repo():
    # CONTEXT.md, sources: fetch_script ... required when FETCHED; must exist in the
    # repo. A record naming a script nobody wrote does not reproduce the fetch.
    catalog = valid_catalog()
    assert validate(a_fetched_source(fetch_script="src/fetch/noaa_oni.py"), catalog) == []
    assert ("fetch_script", "src/fetch/nope.py does not exist in the repo") in reports(
        validate(a_fetched_source(fetch_script="src/fetch/nope.py"), catalog)
    )


@pytest.mark.parametrize("tier", TABLE_TIERS)
def test_a_table_writing_tier_s_file_must_exist_in_the_repo(tier: str):
    # CONTEXT.md, sources: file ... required when TRANSCRIBED or DERIVED; a file under
    # catalog/tables/. That the path is under catalog/tables/ has a test above; that
    # the file is actually there had none.
    catalog = valid_catalog()
    build = SOURCE_OF_TIER[tier]
    assert validate(build(file="catalog/tables/parnell2005_table1.csv"), catalog) == []
    assert ("file", "catalog/tables/nope.csv does not exist in the repo") in reports(
        validate(build(file="catalog/tables/nope.csv"), catalog)
    )


def test_not_held_source_has_no_retrieved_date():
    # CONTEXT.md, sources: retrieved ... null when NOT HELD. Nothing was retrieved, so
    # a date here states a fetch that did not happen.
    assert validate(a_source(retrieved=None)) == []
    assert reports(validate(a_source(retrieved="2026-09-07"))) == [
        ("retrieved", "must be null when tier is NOT HELD")
    ]


def test_not_held_source_names_no_fetch_script():
    # CONTEXT.md, tier: NOT HELD is "nothing local", and fetch_script is required when
    # FETCHED - a NOT HELD record naming one describes a fetch it did not make.
    assert validate(a_source(fetch_script=None)) == []
    assert reports(validate(a_source(fetch_script="src/fetch/noaa_oni.py"))) == [
        ("fetch_script", "must be absent when tier is NOT HELD")
    ]


def test_source_beds_must_resolve():
    # CONTEXT.md, "Gates": catalog-schema links only to records that exist. regions and
    # references were tested; beds and sites were not.
    catalog = valid_catalog()
    assert validate(a_source(beds=["3"]), catalog) == []
    assert ("beds", "'99' is not a bed record") in reports(validate(a_source(beds=["99"]), catalog))


def test_source_sites_must_resolve():
    catalog = valid_catalog()
    assert validate(a_source(sites=["leichter2023.point-loma"]), catalog) == []
    assert ("sites", "'leichter2023.nowhere' is not a site record") in reports(
        validate(a_source(sites=["leichter2023.nowhere"]), catalog)
    )


def test_transcribed_from_reference_must_resolve():
    # CONTEXT.md, sources: transcribed_from {reference, table, page} - the reference is
    # the printed page the values were typed from, so it has to be a record here.
    catalog = valid_catalog()
    held = a_transcribed_source(file="catalog/tables/parnell2005_table1.csv")
    assert validate(held, catalog) == []
    absent = a_transcribed_source(
        file="catalog/tables/parnell2005_table1.csv",
        transcribed_from={"reference": "nobody2020", "table": "Table 1", "page": "p. 2"},
    )
    assert ("transcribed_from.reference", "'nobody2020' is not a reference record") in reports(
        validate(absent, catalog)
    )


# --- the DERIVED tier (#94) ---------------------------------------------------------
#
# CONTEXT.md, "Vocabularies", tier: DERIVED is a table under catalog/tables/ that a
# committed script wrote from inputs the catalog already holds. Its provenance is one
# map, derived_from {inputs, script, parameters}, the shape transcribed_from has for
# the other tier that writes a table there.

DERIVED_FROM_REQUIRED = ("derived_from", "required: {inputs, script, parameters} when DERIVED")


def test_derived_source_validates_end_to_end():
    # tests/fixtures/valid holds one: the record, the CSV it names and the script.
    catalog = valid_catalog()
    rec = next(r for r in catalog.records["sources"] if r.data["tier"] == "DERIVED")
    assert rec.data["derived_from"]["script"] == "src/derive/bed_region.py"
    assert rec.data["topics"] == []
    assert validate(rec, catalog) == []


def test_derived_source_needs_its_provenance_map():
    # #94: "a DERIVED record with no script is a problem". The script lives in the map,
    # and a map missing any of its three keys is reported once, as the map.
    assert validate(a_derived_source()) == []
    assert reports(validate(a_derived_source(derived_from=None))) == [DERIVED_FROM_REQUIRED]
    for key in ("inputs", "script", "parameters"):
        dropped = a_derived_source(derived_from=derived_from(**{key: None}))
        assert reports(validate(dropped)) == [DERIVED_FROM_REQUIRED], key


def test_derived_from_is_not_required_of_the_other_tiers():
    # The map is DERIVED's; a FETCHED or TRANSCRIBED record carries it as null, as
    # noaa_oni carries transcribed_from.
    for tier in TIER:
        if tier != "DERIVED":
            assert validate(SOURCE_OF_TIER[tier](derived_from=None)) == [], tier


def test_derived_script_must_exist_in_the_repo():
    # CONTEXT.md, sources: derived_from ... script, a path that exists in the repo. The
    # same rule fetch_script has: a script nobody committed reproduces nothing.
    catalog = valid_catalog()
    assert validate(a_derived_source(), catalog) == []
    nope = a_derived_source(derived_from=derived_from(script="src/derive/nope.py"))
    assert reports(validate(nope, catalog)) == [
        ("derived_from.script", "src/derive/nope.py does not exist in the repo")
    ]
    assert reports(validate(a_derived_source(derived_from=derived_from(script=5)))) == [
        ("derived_from.script", "expected str")
    ]


def test_derived_inputs_resolve_to_a_source_or_a_record_directory():
    # #94, amended 2026-09-22: an input is a source record, a record directory, or a
    # held file a source record's field names; one that resolves to none of the three
    # is a problem. The third kind enters the list as its record's id - the file has no
    # id of its own - so the list holds source ids and record directories.
    catalog = valid_catalog()
    for inputs in (
        ["noaa_oni"],
        ["catalog/sites/"],
        ["parnell2005_table1"],
        ["bed_region"],
        ["noaa_oni", "catalog/sites/", "parnell2005_table1"],
        *([f"catalog/{kind}/"] for kind in KINDS),
    ):
        rec = a_derived_source(derived_from=derived_from(inputs=inputs))
        assert validate(rec, catalog) == [], inputs
    unresolved = "'{}' is neither a source record nor a record directory"
    for bad in ("nobody", "catalog/tables/", "data/raw/noaa_oni/", "sites"):
        rec = a_derived_source(derived_from=derived_from(inputs=["noaa_oni", bad]))
        assert reports(validate(rec, catalog)) == [
            ("derived_from.inputs", unresolved.format(bad))
        ], bad


def test_derived_inputs_named_by_id_hold_content():
    # CONTEXT.md, tier: "A source named as an input holds content ... a NOT HELD record holds
    # nothing to read." kelp_surveys in the valid fixture is NOT HELD / NOT PUBLIC; a hand-
    # carried file entered that way must not come back in as a script's input (#185, F4).
    catalog = valid_catalog()
    rec = a_derived_source(derived_from=derived_from(inputs=["kelp_surveys"]))
    assert reports(validate(rec, catalog)) == [
        ("derived_from.inputs", "'kelp_surveys' holds nothing to read; its tier is NOT HELD")
    ]


def test_derived_inputs_are_a_non_empty_list_of_strings():
    # "a deterministic index over pinned catalogued inputs": an index over nothing is
    # not one, and an input that is not a name resolves to nothing.
    assert reports(validate(a_derived_source(derived_from=derived_from(inputs=[])))) == [
        ("derived_from.inputs", "at least one input")
    ]
    for wrong in ("noaa_oni", [""], [{"source": "noaa_oni"}]):
        rec = a_derived_source(derived_from=derived_from(inputs=wrong))
        assert reports(validate(rec)) == [("derived_from.inputs", "expected list[str]")], wrong


def test_derived_parameters_are_a_mapping():
    # "with the parameters that change its answer recorded": a mapping, named
    # parameter to value. An empty one states that the script has none.
    assert validate(a_derived_source(derived_from=derived_from(parameters={}))) == []
    rec = a_derived_source(derived_from=derived_from(parameters="intersects, EPSG:3310"))
    assert reports(validate(rec)) == [("derived_from.parameters", "expected map")]


def test_derived_source_carries_no_topics():
    # CONTEXT.md, sources: topics ... >= 1; [] when DERIVED. A join key answers none of
    # the ten questions, so it renders in no topic notebook; tagging one would place a
    # table of keys under a question it does not answer.
    assert validate(a_derived_source(topics=[])) == []
    assert reports(validate(a_derived_source(topics=["canopy"]))) == [
        ("topics", "must be [] when tier is DERIVED")
    ]
    # The >= 1 rule stands for every other tier.
    for tier in TIER:
        if tier != "DERIVED":
            rec = SOURCE_OF_TIER[tier](topics=[])
            assert reports(validate(rec)) == [("topics", "at least one topic")], tier


def test_derived_source_needs_no_transcribed_from():
    # CONTEXT.md, sources: transcribed_from ... required when TRANSCRIBED - and only
    # then. Its reference link-checks into references/, which a computed table has no
    # business naming (#94, "Why not TRANSCRIBED").
    assert "transcribed_from" not in a_derived_source().data
    assert validate(a_derived_source(transcribed_from=None)) == []


def test_region_defined_by_is_a_source_and_a_locator():
    # CONTEXT.md, regions: defined_by* {source, where} - the record that draws the boundary
    # and where in it. A bare string is the shape #104 retires; a map missing either half
    # is not a citation.
    assert validate(a_region()) == []
    assert reports(validate(a_region(defined_by="http://kelp.sccwrp.org/"))) == [
        ("defined_by", "expected map")
    ]
    assert reports(validate(a_region(defined_by={"source": "kelp_surveys"}))) == [
        ("defined_by", "required: {source, where}")
    ]
    assert reports(validate(a_region(defined_by={"where": "Study area"}))) == [
        ("defined_by", "required: {source, where}")
    ]
    assert reports(validate(a_region(defined_by={"source": "kelp_surveys", "where": ""}))) == [
        ("defined_by", "required: {source, where}")
    ]


def test_region_defined_by_source_must_resolve():
    # CONTEXT.md, "Gates": catalog-schema links only to records that exist; the source half
    # is a link, as transcribed_from.reference is.
    catalog = valid_catalog()
    assert validate(a_region(), catalog) == []
    absent = a_region(defined_by={"source": "nobody", "where": "Study area"})
    assert reports(validate(absent, catalog)) == [
        ("defined_by.source", "'nobody' is not a source record")
    ]
    # A source half that is missing, blank or not a string is reported once, by the shape
    # check, not also as a link to a record that could never exist (audit of PR #116, F3).
    for db in (
        {"where": "Study area"},
        {"source": "", "where": "x"},
        {"source": 123, "where": "x"},
    ):
        half = a_region(defined_by=db)
        assert reports(validate(half, catalog)) == [("defined_by", "required: {source, where}")]


def test_bed_defined_by_stays_a_bare_string():
    # #104 reached regions and #174 sites; beds are #83, frozen. A bed's defined_by is
    # still the string CONTEXT.md's beds row describes.
    assert isinstance(a_bed().data["defined_by"], str) and validate(a_bed()) == []


# --- every field of every record type, dropped and mistyped ------------------------
#
# The same sweep left 88 per-field mutants alive: most fields had no test that omitted
# or mistyped them. Table-driven over RULES rather than 88 fixtures, so a field added
# to RULES arrives with both tests already written, and a field whose rule CONTEXT.md
# changes fails here rather than going unnoticed.

BUILDERS = {
    "sources": a_source,
    "references": a_reference,
    "excluded": an_excluded,
    "regions": a_region,
    "beds": a_bed,
    "sites": a_site,
}

# One value of the wrong type per type RULES uses. Each is the kind of thing a record
# actually gets wrong: a bare string where a list belongs, a quoted number, a mapping
# flattened to prose.
WRONG_VALUE: dict[str, Any] = {
    "str": 5,
    "str?": 5,
    "int": "2012",
    "float": "32.69",
    "date": 5,
    "date?": 5,
    "map": "SCCWRP Tech. Rep. 1289, Methods, Study Design",
    "map?": "reference, table, page",
    "list[str]": "one string, not a list",
    "list[topic]": "bed-state",
    "list[eq]": ["not a mapping"],
    "list[site_key]": ["SITE"],
    "list[cite]": ["A. Author. 2020. A title."],
    # A half-migrated record: one form to a list (CONTEXT.md, sources, `variables`).
    "list[variable]": ["campus", {"name": "method", "description": None, "unit": None}],
}

FIELD_RULES = [(k, n, r, t) for k, fields in RULES.items() for n, (r, t) in fields.items()]
REQUIRED_FIELDS = [(k, n) for k, n, required, _ in FIELD_RULES if required]
TYPED_FIELDS = [(k, n, t) for k, n, _, t in FIELD_RULES]


def a_valid(kind: str) -> Record:
    rec = BUILDERS[kind]()
    assert validate(rec) == [], (
        f"the base {kind} record must be valid, or the mutated field is not what failed"
    )
    return rec


@pytest.mark.parametrize(
    "kind, name", REQUIRED_FIELDS, ids=[f"{k}.{n}" for k, n in REQUIRED_FIELDS]
)
def test_every_required_field_is_required(kind: str, name: str):
    rec = a_valid(kind)
    dropped = Record(kind, rec.path, {k: v for k, v in rec.data.items() if k != name})
    assert (name, "required field is missing") in reports(validate(dropped))


@pytest.mark.parametrize(
    "kind, name, typ", TYPED_FIELDS, ids=[f"{k}.{n}" for k, n, _ in TYPED_FIELDS]
)
def test_every_field_is_typed(kind: str, name: str, typ: str):
    assert typ in WRONG_VALUE, f"RULES uses {typ!r}; add a value of the wrong type for it"
    rec = a_valid(kind)
    mistyped = Record(kind, rec.path, {**rec.data, name: WRONG_VALUE[typ]})
    assert (name, f"expected {typ}") in reports(validate(mistyped))


# --- the island region nodes (#88) --------------------------------------------------

ROOT = Path(__file__).parents[1]

ISLANDS = (
    "scb.islands.anacapa",
    "scb.islands.san-clemente",
    "scb.islands.san-miguel",
    "scb.islands.san-nicolas",
    "scb.islands.santa-barbara",
    "scb.islands.santa-catalina",
    "scb.islands.santa-cruz",
    "scb.islands.santa-rosa",
)


def test_the_islands_are_eight_nodes_under_scb_islands_each_citing_the_regulation():
    # CONTEXT.md, "The region tree", level 3: eight nodes directly under scb.islands, with
    # no group level between; CCR Title 14 s165.5(k)(2) prints the island on every island
    # bed, and gathers them under the heading "(2) Channel Island administrative kelp beds",
    # which is what scb.islands is defined by (#123).
    catalog, problems = check_catalog(ROOT)
    assert problems == []
    regions = {rec.id: rec.data for rec in catalog.records["regions"]}
    assert regions["scb.islands"]["parent"] == "scb"
    assert regions["scb.islands"]["defined_by"]["source"] == "ccr_t14_165_5"
    islands = sorted(rid for rid, d in regions.items() if d["parent"] == "scb.islands")
    assert tuple(islands) == ISLANDS
    for rid in ISLANDS:
        assert regions[rid]["defined_by"]["source"] == "ccr_t14_165_5", rid
        assert "(k)(2)" in regions[rid]["defined_by"]["where"], rid
    # The regulation prints "Anacapa Islands" and "Santa Barbara Island"; name is as stated.
    assert regions["scb.islands.anacapa"]["name"] == "Anacapa Islands"
    assert regions["scb.islands.santa-barbara"]["name"] == "Santa Barbara Island"
    # consortium is a county's attribute: non-empty only when parent is scb.mainland.
    for rid in ("scb.islands", *ISLANDS):
        assert not regions[rid].get("consortium"), rid


def test_the_island_locators_partition_the_regulation_s_channel_island_beds():
    # The transcriptions cannot be checked in CI (data/ is git-ignored), but three
    # internal properties can be, and they catch a swapped name, a widened bed range or a
    # moved paragraph (audit of PR #117, F2): the nine names are distinct; each island's
    # `where` quotes its own name; and the eight `where`s' bed numbers partition 101-118
    # and their paragraph letters partition (A)-(R), the whole of s165.5(k)(2).
    catalog, _ = check_catalog(ROOT)
    regions = {rec.id: rec.data for rec in catalog.records["regions"]}
    nine = ["scb.islands", *ISLANDS]
    assert len({regions[rid]["name"] for rid in nine}) == len(nine)
    beds: list[int] = []
    letters: list[str] = []
    for rid in ISLANDS:
        where = regions[rid]["defined_by"]["where"]
        assert f'"{regions[rid]["name"]}"' in where, rid
        m = re.search(r"paragraphs? \(([A-Z])\)(?:-\(([A-Z])\))?", where)
        assert m, rid
        letters += [chr(c) for c in range(ord(m[1]), ord(m[2] or m[1]) + 1)]
        m = re.search(r"beds? (\d+)(?:-(\d+))?", where)
        assert m, rid
        beds += range(int(m[1]), int(m[2] or m[1]) + 1)
    assert sorted(beds) == list(range(101, 119)) and len(beds) == 18
    assert sorted(letters) == [chr(c) for c in range(ord("A"), ord("R") + 1)]


def test_the_notebook_region_order_lists_the_eight_islands_by_id():
    from kelpcatalog.plan import region_sort_key

    catalog, _ = check_catalog(ROOT)
    ids = [rec.id for rec in catalog.records["regions"] if rec.data["parent"] == "scb.islands"]
    assert sorted(ids, key=region_sort_key) == sorted(ids) == list(ISLANDS)

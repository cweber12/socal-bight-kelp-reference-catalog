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


def test_invalid_site_lat_type_and_bed():
    probs = problems_of("invalid_site")
    assert "lat: expected float" in probs
    assert "bed: '3' is not a bed record" in probs


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
        "bed": None,
        "lat": 32.69,
        "lon": -117.27,
        "defined_by": "10.3389/fmars.2023.1007789",
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


@pytest.mark.parametrize("bad", ["leichter2023", "leichter2023.point.loma", "leichter2023."])
def test_site_id_is_program_dot_site(bad: str):
    # CONTEXT.md, sites: id* (`<program>.<site>`, equals file name)
    assert validate(a_site()) == []
    assert reports(validate(a_site(id=bad))) == [
        ("id", "must be <program>.<site>, both parts non-empty")
    ]


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


def test_bed_and_site_defined_by_stay_bare_strings():
    # #104 reaches regions only; beds and sites are #83, frozen. Their defined_by is still
    # the string CONTEXT.md's beds and sites rows describe.
    assert isinstance(a_bed().data["defined_by"], str) and validate(a_bed()) == []
    assert isinstance(a_site().data["defined_by"], str) and validate(a_site()) == []


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

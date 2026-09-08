"""Schema tests. One valid and one invalid fixture per record type, plus the rules
that need more than one record to fail: unresolved links and duplicate ids.

Fixtures live in tests/fixtures/<case>/catalog/<kind>/*.md so a case is a whole
miniature repo and check_catalog() runs on it unchanged.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from kelpcatalog import check_catalog, parse_record, split_topic, topic_problem, validate
from kelpcatalog.schema import GROUPS, KINDS, TOPICS, Catalog, Record

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
        ("ocean-climate/nope", "unknown sub-topic 'nope' for 'ocean-climate'"),
        ("nope/heatwaves", "unknown topic 'nope'"),
        ("ocean-climate/heatwaves/extra", "malformed topic tag 'ocean-climate/heatwaves/extra'"),
        ("", "topic must be a non-empty string"),
    ],
)
def test_topic_tags_and_subtopics(tag: str, why: str | None):
    assert topic_problem(tag) == why


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
# Each of the six below is a record that validate() accepted before this section
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


def a_region(**overrides: Any) -> Record:
    data: dict[str, Any] = {
        "id": "scb.mainland.san-diego",
        "name": "San Diego County",
        "parent": None,
        "defined_by": "http://kelp.sccwrp.org/",
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


def test_transcribed_file_must_be_under_catalog_tables():
    # CONTEXT.md, sources: file ... a file under `catalog/tables/`
    assert validate(a_transcribed_source()) == []
    assert reports(validate(a_transcribed_source(file="data/tables/x.csv"))) == [
        ("file", "must be a file under catalog/tables/")
    ]


def test_region_consortium_is_a_closed_vocabulary():
    # CONTEXT.md, regions: consortium (`RNKSC` or `CRKSC`, counties only)
    assert validate(a_region()) == []
    assert validate(a_region(consortium="RNKSC")) == []
    assert validate(a_region(consortium="CRKSC")) == []
    assert validate(a_region(consortium=None)) == []
    assert reports(validate(a_region(consortium="SCCWRP"))) == [
        ("consortium", "must be one of ('RNKSC', 'CRKSC')")
    ]


def test_human_task_is_an_h_number():
    # CONTEXT.md, sources: human_task ... an `H<n>` id
    assert validate(a_source(human_task="H2")) == []
    assert validate(a_source(human_task=None)) == []
    assert reports(validate(a_source(human_task="2"))) == [("human_task", r"does not match ^H\d+$")]


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

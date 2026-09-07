"""Schema tests. One valid and one invalid fixture per record type, plus the rules
that need more than one record to fail: unresolved links and duplicate ids.

Fixtures live in tests/fixtures/<case>/catalog/<kind>/*.md so a case is a whole
miniature repo and check_catalog() runs on it unchanged.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from kelpcatalog import check_catalog, parse_record, split_topic, topic_problem, validate
from kelpcatalog.schema import GROUPS, KINDS, TOPICS, Catalog

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

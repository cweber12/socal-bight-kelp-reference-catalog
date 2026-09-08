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

from pathlib import Path
from typing import Any

import pytest

from kelpcatalog import check_catalog, parse_record, split_topic, topic_problem, validate
from kelpcatalog.schema import GROUPS, KINDS, RULES, STATUS, TIER, TOPICS, Catalog, Record

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
# Each of the seven below is a record that validate() accepted before this section
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


def a_source_of(status: str, tier: str) -> Record:
    """A source whose tier-specific fields are all in order, so the status/tier
    pairing is the only thing left that can be wrong."""
    builders = {
        "FETCHED": a_fetched_source,
        "TRANSCRIBED": a_transcribed_source,
        "NOT HELD": a_source,
    }
    return builders[tier](status=status, tier=tier)


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


VERIFIED_BY_TIER = ("status", "VERIFIED requires tier FETCHED or TRANSCRIBED; tier is NOT HELD")


@pytest.mark.parametrize("status", [s for s in STATUS if s != "VERIFIED"])
def test_not_held_admits_every_status_but_verified(status: str):
    # CONTEXT.md, tier: NOT HELD is "nothing local", so its status is one of the three
    # that do not claim the route was exercised.
    assert validate(a_source_of(status, "NOT HELD")) == []


def test_verified_status_requires_fetched_or_transcribed_tier():
    # CONTEXT.md, status: VERIFIED means the route was exercised - fetched on the
    # retrieved date, or a printed page in hand. A NOT HELD record holds nothing and
    # names no fetch, so nothing here could have verified it.
    assert validate(a_source_of("VERIFIED", "FETCHED")) == []
    assert validate(a_source_of("VERIFIED", "TRANSCRIBED")) == []
    # Stated from the status end: VERIFIED on a record that holds nothing.
    assert reports(validate(a_source(status="VERIFIED"))) == [VERIFIED_BY_TIER]
    # And from the tier end: NOT HELD on a record that claims VERIFIED. One constraint,
    # so one problem, and it names both fields.
    assert reports(
        validate(a_transcribed_source(tier="NOT HELD", file=None, transcribed_from=None))
    ) == [VERIFIED_BY_TIER]


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
    # transcribed CSVs by design; neither is a stray. The equality above says they are
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
    # CONTEXT.md, "Vocabularies": tier is FETCHED, TRANSCRIBED or NOT HELD. status had
    # this test from the start; tier did not, so 'FETCHD' validated.
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


def test_transcribed_file_must_exist_in_the_repo():
    # CONTEXT.md, sources: file ... required when TRANSCRIBED; a file under
    # catalog/tables/. That the path is under catalog/tables/ has a test above; that
    # the file is actually there had none.
    catalog = valid_catalog()
    held = a_transcribed_source(file="catalog/tables/parnell2005_table1.csv")
    assert validate(held, catalog) == []
    assert ("file", "catalog/tables/nope.csv does not exist in the repo") in reports(
        validate(a_transcribed_source(file="catalog/tables/nope.csv"), catalog)
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

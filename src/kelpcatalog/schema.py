"""Load and validate catalog records.

A record is a markdown file whose entire content is a YAML frontmatter block. The
body below the frontmatter must be empty: records hold structured facts, not prose
(see CONTEXT.md, "The rule"). The record type is the directory it lives in.

Seams:
    parse_record(text, kind, path) -> Record       pure; takes a string
    validate(record, catalog) -> list[Problem]     pure given a loaded catalog
    load_catalog(root) -> Catalog                  thin directory walk
    check_catalog(root) -> (Catalog, list[Problem]) what gate.py calls

Every field's rule is stated once, in RULES below, and CONTEXT.md carries the same
table in prose. If the two disagree, CONTEXT.md wins and this file is wrong.
"""

from __future__ import annotations

import datetime as dt
import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

KINDS = ("sources", "references", "excluded", "regions", "beds", "sites")

STATUS = ("VERIFIED", "PATTERN", "NOT PUBLIC", "ON REQUEST")
TIER = ("FETCHED", "TRANSCRIBED", "NOT HELD")
BED_STATUS = ("Open", "Closed", "Leasable", "Lease Only")
# Topics and their sub-topics, in notebook order. CONTEXT.md "Topics" is the authority;
# the group each topic belongs to is in GROUPS. A topic tag is "<topic>" or
# "<topic>/<subtopic>".
TOPICS: dict[str, tuple[str, ...]] = {
    "ocean-climate": ("temperature", "nutrients", "upwelling-enso", "heatwaves", "oxygen-ph"),
    "canyon-dynamics": ("internal-tides", "canyon-circulation", "observations"),
    "waves-storms-sediment": ("swell-climate", "storms", "sediment-sand", "beach-coupling"),
    "substrate": ("rock-mapping", "relief-rugosity", "artificial-substrate"),
    "canopy": ("aerial-surveys", "satellite", "historical-baselines", "persistence"),
    "bed-state": ("diver-surveys", "community", "invasives", "mpas"),
    "grazers-predators-competitors": (
        "urchins",
        "predators",
        "grazing-fishes",
        "drift-algae",
        "competitors",
    ),
    "recruitment-connectivity": ("spore-dispersal", "larval-transport", "settlement", "genetics"),
    "water-quality-harvest": (
        "discharges-outfalls",
        "runoff-sedimentation",
        "power-plants",
        "kelp-harvest",
        "fishing-pressure",
    ),
    "restoration-mitigation": ("outplanting", "urchin-removal", "artificial-reefs", "kelp-farms"),
}
GROUPS: dict[str, tuple[str, ...]] = {
    "physical-environment": (
        "ocean-climate",
        "canyon-dynamics",
        "waves-storms-sediment",
        "substrate",
    ),
    "kelp-and-community": (
        "canopy",
        "bed-state",
        "grazers-predators-competitors",
        "recruitment-connectivity",
    ),
    "human-uses-management": ("water-quality-harvest", "restoration-mitigation"),
}
GLOBAL_REGION = "global"


def split_topic(tag: str) -> tuple[str, str | None]:
    """'ocean-climate/heatwaves' -> ('ocean-climate', 'heatwaves'); bare tag -> (tag, None)."""
    topic, _, sub = tag.partition("/")
    return topic, (sub or None)


def topic_problem(tag: str) -> str | None:
    """Why a topic tag is invalid, or None if it is valid."""
    if not isinstance(tag, str) or not tag:
        return "topic must be a non-empty string"
    if tag.count("/") > 1:
        return f"malformed topic tag {tag!r}"
    topic, sub = split_topic(tag)
    if topic not in TOPICS:
        return f"unknown topic {topic!r}"
    if sub is not None and sub not in TOPICS[topic]:
        return f"unknown sub-topic {sub!r} for {topic!r}"
    return None


ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
CITEKEY_RE = re.compile(r"^[a-z][a-z0-9]*\d{4}[a-z]?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.S)


@dataclass(frozen=True)
class Problem:
    path: str
    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.field}: {self.message}"


def _id_field(kind: str) -> str:
    return "citekey" if kind == "references" else "slug" if kind == "excluded" else "id"


@dataclass(frozen=True)
class Record:
    kind: str
    path: str
    data: dict[str, Any]

    @property
    def id(self) -> str:
        value = self.data.get(_id_field(self.kind))
        return str(value) if value is not None else ""


@dataclass
class Catalog:
    root: Path
    records: dict[str, list[Record]] = field(default_factory=lambda: {k: [] for k in KINDS})

    def ids(self, kind: str) -> set[str]:
        return {r.id for r in self.records[kind] if r.id}

    def all(self) -> Iterable[Record]:
        for kind in KINDS:
            yield from self.records[kind]


# --- field rules -------------------------------------------------------------------
#
# Each rule: (required, type). Types: "str", "str?" (str or null), "int", "float",
# "date", "date?", "list[str]", "list[topic]", "list[eq]".

RULES: dict[str, dict[str, tuple[bool, str]]] = {
    "sources": {
        "id": (True, "str"),
        "title": (True, "str"),
        "steward": (True, "str"),
        "url": (True, "str?"),
        "doi": (False, "str?"),
        "status": (True, "str"),
        "tier": (True, "str"),
        "access": (True, "list[str]"),
        "format": (False, "str?"),
        "license": (True, "str"),
        "variables": (True, "list[str]"),
        "coverage": (False, "str?"),
        "coverage_stated_at": (False, "str?"),
        "retrieved": (True, "date?"),
        "fetch_script": (False, "str?"),
        "file": (False, "str?"),
        "transcribed_from": (False, "map?"),
        "topics": (True, "list[topic]"),
        "regions": (True, "list[str]"),
        "beds": (False, "list[str]"),
        "sites": (False, "list[str]"),
        "references": (False, "list[str]"),
        "human_task": (False, "str?"),
    },
    "references": {
        "citekey": (True, "str"),
        "ref": (True, "str"),
        "doi": (False, "str?"),
        "url": (False, "str?"),
        "year": (True, "int"),
        "equations": (False, "list[eq]"),
        "topics": (True, "list[topic]"),
    },
    "excluded": {
        "slug": (True, "str"),
        "reviewed": (True, "date"),
        "what": (True, "str"),
        "reason": (True, "str"),
        "url": (False, "str?"),
        "doi": (False, "str?"),
        "topics": (False, "list[topic]"),
    },
    "regions": {
        "id": (True, "str"),
        "name": (True, "str"),
        "parent": (True, "str?"),
        "defined_by": (True, "str"),
        "consortium": (False, "str?"),
    },
    "beds": {
        "id": (True, "str"),
        "cdfw_bed": (True, "int"),
        "name": (True, "str"),
        "status": (True, "str"),
        "region": (True, "str"),
        "aliases": (False, "list[str]"),
        "defined_by": (True, "str"),
    },
    "sites": {
        "id": (True, "str"),
        "program": (True, "str"),
        "name": (True, "str"),
        "bed": (True, "str?"),
        "lat": (True, "float"),
        "lon": (True, "float"),
        "defined_by": (True, "str"),
    },
}


def _is_date(value: Any) -> bool:
    if isinstance(value, dt.date):
        return True
    return isinstance(value, str) and bool(DATE_RE.match(value))


def _type_ok(value: Any, kind: str) -> bool:
    if kind.endswith("?") and value is None:
        return True
    base = kind.rstrip("?")
    if base == "str":
        return isinstance(value, str) and value.strip() != ""
    if base == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if base == "float":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if base == "date":
        return _is_date(value)
    if base == "map":
        return isinstance(value, dict)
    if base == "list[str]":
        return isinstance(value, list) and all(isinstance(v, str) and v.strip() for v in value)
    if base == "list[topic]":
        return isinstance(value, list) and all(isinstance(v, str) for v in value)
    if base == "list[eq]":
        return isinstance(value, list) and all(
            isinstance(e, dict) and {"id", "as_printed", "where"} <= set(e) for e in value
        )
    return False


# --- parsing -----------------------------------------------------------------------


def parse_record(
    text: str, kind: str, path: str = "<string>"
) -> tuple[Record | None, list[Problem]]:
    """Split frontmatter from body; the body must be empty."""
    if kind not in KINDS:
        return None, [Problem(path, "kind", f"unknown record kind {kind!r}")]
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, [Problem(path, "frontmatter", "file must begin with a '---' YAML block")]
    raw, body = m.group(1), m.group(2)
    if body.strip():
        return None, [
            Problem(path, "body", "records carry no prose; move facts into fields or drop them")
        ]
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:  # pragma: no cover - message text varies by version
        return None, [Problem(path, "frontmatter", f"YAML error: {e}")]
    if not isinstance(data, dict):
        return None, [Problem(path, "frontmatter", "frontmatter must be a mapping")]
    return Record(kind, path, data), []


# --- validation --------------------------------------------------------------------


def _shape_problems(rec: Record) -> tuple[list[Problem], set[str]]:
    """Missing, mistyped and unknown fields. Also returns the names of fields that
    are missing or mistyped, so later checks skip them instead of reporting twice."""
    rules = RULES[rec.kind]
    out: list[Problem] = []
    bad: set[str] = set()
    for name, (required, typ) in rules.items():
        if name not in rec.data:
            if required:
                out.append(Problem(rec.path, name, "required field is missing"))
                bad.add(name)
            continue
        if not _type_ok(rec.data[name], typ):
            out.append(Problem(rec.path, name, f"expected {typ}"))
            bad.add(name)
    for name in rec.data:
        if name not in rules:
            out.append(Problem(rec.path, name, "unknown field; CONTEXT.md lists the allowed ones"))
    return out, bad


def _vocab_problems(rec: Record, bad: set[str]) -> list[Problem]:
    d, p = rec.data, rec.path
    out: list[Problem] = []
    if rec.kind == "sources":
        if "status" not in bad and d.get("status") not in STATUS:
            out.append(Problem(p, "status", f"must be one of {STATUS}"))
        if "tier" not in bad and d.get("tier") not in TIER:
            out.append(Problem(p, "tier", f"must be one of {TIER}"))
    if rec.kind == "beds" and "status" not in bad and d.get("status") not in BED_STATUS:
        out.append(Problem(p, "status", f"must be one of {BED_STATUS}"))
    if "topics" in d and "topics" not in bad:
        if not d["topics"] and RULES[rec.kind]["topics"][0]:
            out.append(Problem(p, "topics", "at least one topic"))
        for t in d["topics"]:
            why = topic_problem(t)
            if why:
                out.append(Problem(p, "topics", why))
    return out


def _id_problems(rec: Record) -> list[Problem]:
    stem = Path(rec.path).stem
    rid = rec.id
    out: list[Problem] = []
    key = _id_field(rec.kind)
    if not rid:
        return out  # already reported as missing
    if rid != stem:
        out.append(Problem(rec.path, key, f"must equal the file name ({stem!r})"))
    pattern = CITEKEY_RE if rec.kind == "references" else ID_RE
    if not pattern.match(rid):
        out.append(Problem(rec.path, key, f"does not match {pattern.pattern}"))
    return out


def _tier_problems(rec: Record, root: Path | None, bad: set[str]) -> list[Problem]:
    if rec.kind != "sources" or "tier" in bad:
        return []
    d, p = rec.data, rec.path
    out: list[Problem] = []
    tier = d.get("tier")
    if tier == "FETCHED":
        for f in ("url", "retrieved", "fetch_script"):
            if not d.get(f):
                out.append(Problem(p, f, "required when tier is FETCHED"))
        script = d.get("fetch_script")
        if root is not None and isinstance(script, str) and not (root / script).exists():
            out.append(Problem(p, "fetch_script", f"{script} does not exist in the repo"))
    elif tier == "TRANSCRIBED":
        tf = d.get("transcribed_from")
        if not isinstance(tf, dict) or not {"reference", "table", "page"} <= set(tf):
            out.append(
                Problem(
                    p, "transcribed_from", "required: {reference, table, page} when TRANSCRIBED"
                )
            )
        if not d.get("file"):
            out.append(Problem(p, "file", "required when tier is TRANSCRIBED (catalog/tables/...)"))
        elif root is not None and not (root / str(d["file"])).exists():
            out.append(Problem(p, "file", f"{d['file']} does not exist in the repo"))
    elif tier == "NOT HELD":
        if d.get("retrieved") is not None:
            out.append(Problem(p, "retrieved", "must be null when tier is NOT HELD"))
        if d.get("fetch_script"):
            out.append(Problem(p, "fetch_script", "must be absent when tier is NOT HELD"))
    return out


def _link_problems(rec: Record, catalog: Catalog, bad: set[str]) -> list[Problem]:
    d, p = rec.data, rec.path
    out: list[Problem] = []

    def check(
        fieldname: str, values: Iterable[str], kind: str, extra: set[str] | None = None
    ) -> None:
        if fieldname.split(".")[0] in bad:
            return
        known = catalog.ids(kind) | (extra or set())
        for v in values:
            if v not in known:
                out.append(Problem(p, fieldname, f"{v!r} is not a {kind[:-1]} record"))

    if rec.kind == "sources":
        check("regions", d.get("regions") or [], "regions", {GLOBAL_REGION})
        check("beds", d.get("beds") or [], "beds")
        check("sites", d.get("sites") or [], "sites")
        check("references", d.get("references") or [], "references")
        tf = d.get("transcribed_from")
        if isinstance(tf, dict) and "reference" in tf:
            check("transcribed_from.reference", [str(tf["reference"])], "references")
    if rec.kind == "regions" and d.get("parent") is not None:
        check("parent", [str(d["parent"])], "regions")
    if rec.kind == "beds":
        check("region", [str(d.get("region"))], "regions")
    if rec.kind == "sites" and d.get("bed") is not None:
        check("bed", [str(d["bed"])], "beds")
    if rec.kind == "references" and not (d.get("doi") or d.get("url")):
        out.append(Problem(p, "doi", "a reference needs a doi or a url"))
    return out


def validate(rec: Record, catalog: Catalog | None = None) -> list[Problem]:
    """Every problem with one record. Cross-record checks need a catalog."""
    out, bad = _shape_problems(rec)
    out += _vocab_problems(rec, bad)
    out += _id_problems(rec)
    out += _tier_problems(rec, catalog.root if catalog else None, bad)
    if catalog is not None:
        out += _link_problems(rec, catalog, bad)
    return out


def _duplicate_problems(catalog: Catalog) -> list[Problem]:
    out: list[Problem] = []
    seen: dict[tuple[str, str], str] = {}
    for rec in catalog.all():
        if not rec.id:
            continue
        key = (rec.kind, rec.id)
        if key in seen:
            out.append(Problem(rec.path, "id", f"duplicates {seen[key]}"))
        else:
            seen[key] = rec.path
    return out


# --- loading -----------------------------------------------------------------------


def load_catalog(root: Path) -> tuple[Catalog, list[Problem]]:
    """Read every record under root/catalog/<kind>/. Parse problems are returned, not raised."""
    catalog = Catalog(root=root)
    problems: list[Problem] = []
    base = root / "catalog"
    for kind in KINDS:
        for path in sorted((base / kind).glob("*.md")):
            rel = path.relative_to(root).as_posix()
            rec, probs = parse_record(path.read_text(encoding="utf-8"), kind, rel)
            problems += probs
            if rec is not None:
                catalog.records[kind].append(rec)
    return catalog, problems


def check_catalog(root: Path) -> tuple[Catalog, list[Problem]]:
    """Load, then validate every record against the whole catalog."""
    catalog, problems = load_catalog(root)
    for rec in catalog.all():
        problems += validate(rec, catalog)
    problems += _duplicate_problems(catalog)
    return catalog, problems

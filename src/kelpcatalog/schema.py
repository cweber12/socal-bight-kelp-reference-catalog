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
# Every directory under catalog/ and the one extension its files carry: records are
# markdown, and catalog/tables/ holds the transcribed and derived CSVs (CONTEXT.md,
# "Record format"). .gitkeep is how git holds an empty one, so it is not a stray.
RECORD_DIRS: dict[str, str] = {**dict.fromkeys(KINDS, ".md"), "tables": ".csv"}
KEEP_FILE = ".gitkeep"

STATUS = ("VERIFIED", "PATTERN", "NOT PUBLIC", "ON REQUEST")
TIER = ("FETCHED", "TRANSCRIBED", "DERIVED", "NOT HELD")
# CONTEXT.md, "Vocabularies": "Holding content means the route was exercised", so these
# three exclude PATTERN; NOT HELD, holding nothing, excludes nothing.
HELD_TIERS = ("FETCHED", "TRANSCRIBED", "DERIVED")
# CONTEXT.md, "Record format": the tiers whose record names a file under catalog/tables/,
# and so require `file`. #17's reverse check reads this set rather than naming a tier.
TABLE_TIERS = ("TRANSCRIBED", "DERIVED")
# CONTEXT.md, sources: derived_from {inputs, script, parameters}, DERIVED's provenance,
# the shape transcribed_from has for the other tier that writes a table.
DERIVED_FROM_KEYS = ("inputs", "script", "parameters")
BED_STATUS = ("Open", "Closed", "Leasable", "Lease Only")
CONSORTIUM = ("RNKSC", "CRKSC")
# Topics and their sub-topics, in notebook order. CONTEXT.md "Topics" is the authority;
# the group each topic belongs to is in GROUPS. A topic tag is "<topic>" or
# "<topic>/<subtopic>".
TOPICS: dict[str, tuple[str, ...]] = {
    "ocean-climate": (
        "temperature",
        "salinity",
        "nutrients",
        "upwelling-enso",
        "heatwaves",
        "oxygen-ph",
    ),
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
# The consortium boundary runs through Orange County, so consortium is a list, and it is
# an attribute of a county - a node whose parent is the mainland. CONTEXT.md, region tree.
MAINLAND_REGION = "scb.mainland"


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
HUMAN_TASK_RE = re.compile(r"^H\d+$")

# Tables live in one place, so a record cannot point at data/ (git-ignored) or at a
# file outside the catalog.
TABLES_DIR = "catalog/tables/"

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
# "date", "date?", "map", "map?", "list[str]", "list[topic]", "list[eq]",
# "list[site_key]".

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
        "license_stated_at": (False, "str?"),
        "variables": (True, "list[str]"),
        "coverage": (False, "str?"),
        "coverage_stated_at": (False, "str?"),
        "retrieved": (True, "date?"),
        "fetch_script": (False, "str?"),
        "file": (False, "str?"),
        "transcribed_from": (False, "map?"),
        "derived_from": (False, "map?"),
        "topics": (True, "list[topic]"),
        "regions": (True, "list[str]"),
        "beds": (False, "list[str]"),
        "sites": (False, "list[str]"),
        "site_key": (False, "list[site_key]"),
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
        "defined_by": (True, "map"),
        "consortium": (False, "list[str]"),
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
    # CONTEXT.md, "sites/<id>.md": key is str, spelled as that table's `key` row says; lat
    # and lon are str, as the document prints them - converting them is kept off the
    # record; no region field - the region a site falls in is computed, so a DERIVED
    # table's (#177).
    "sites": {
        "id": (True, "str"),
        "program": (True, "str"),
        "name": (True, "str"),
        "key": (True, "str"),
        "lat": (True, "str"),
        "lon": (True, "str"),
        "datum": (False, "str?"),
        "defined_by": (True, "map"),
        "retrieved": (False, "date?"),
    },
}
# CONTEXT.md, sites: defined_by is exactly one of {source, where} or {reference, where} -
# the document that prints the coordinates, resolved into sources/ or references/.
SITE_DEFINED_BY_LIMBS = ("source", "reference")
# CONTEXT.md, sources: a site_key entry is {file, column?, lat_column?, lon_column?}, the
# two coordinate columns together or neither.
SITE_KEY_KEYS = ("file", "column", "lat_column", "lon_column")
SITE_KEY_COORDS = ("lat_column", "lon_column")


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
    if base == "list[site_key]":
        return isinstance(value, list) and all(isinstance(e, dict) for e in value)
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
        if "regions" not in bad and not d.get("regions"):
            out.append(Problem(p, "regions", "at least one region"))
        task = d.get("human_task")
        if "human_task" not in bad and isinstance(task, str) and not HUMAN_TASK_RE.match(task):
            out.append(Problem(p, "human_task", f"does not match {HUMAN_TASK_RE.pattern}"))
        if "site_key" not in bad:
            out += _site_key_problems(rec)
    if rec.kind == "beds" and "status" not in bad and d.get("status") not in BED_STATUS:
        out.append(Problem(p, "status", f"must be one of {BED_STATUS}"))
    if rec.kind == "regions" and "defined_by" not in bad:
        # CONTEXT.md, regions: defined_by {source, where} - the record that draws the
        # boundary and a locator within it, the shape transcribed_from has. Beds still
        # carry a string here (#83).
        db = d["defined_by"]
        if not all(isinstance(db.get(k), str) and db[k].strip() for k in ("source", "where")):
            out.append(Problem(p, "defined_by", "required: {source, where}"))
    if rec.kind == "sites" and "defined_by" not in bad:
        out += _site_defined_by_problems(rec)
    if rec.kind == "regions" and "consortium" not in bad:
        con = d.get("consortium") or []
        for c in con:
            if c not in CONSORTIUM:
                out.append(Problem(p, "consortium", f"must be one of {CONSORTIUM}"))
        if con and "parent" not in bad and d.get("parent") != MAINLAND_REGION:
            out.append(Problem(p, "consortium", f"non-empty only when parent is {MAINLAND_REGION}"))
    if "topics" in d and "topics" not in bad:
        # CONTEXT.md, sources: topics >= 1, and [] when DERIVED - a join key answers none
        # of the ten questions. _tier_problems reports a DERIVED record that carries one.
        required = RULES[rec.kind]["topics"][0] and d.get("tier") != "DERIVED"
        if not d["topics"] and required:
            out.append(Problem(p, "topics", "at least one topic"))
        for t in d["topics"]:
            why = topic_problem(t)
            if why:
                out.append(Problem(p, "topics", why))
    return out


def _site_key_problems(rec: Record) -> list[Problem]:
    """The shape of each site_key entry (CONTEXT.md, sources): `file`, a non-empty string;
    `column`, `lat_column` and `lon_column` optional, the last two together; no other key.
    A key written as an explicit null is absent, as in a site's defined_by. Each entry is
    reported by its index. Whether `file` names a held file is the lock's question
    (milestone 6.5), not this one's; whether the record's tier holds one is _tier_problems'."""
    p = rec.path
    out: list[Problem] = []
    for i, raw in enumerate(rec.data.get("site_key") or []):
        at = f"site_key[{i}]"
        entry = {k: v for k, v in raw.items() if v is not None}
        if "file" not in entry:
            out.append(Problem(p, f"{at}.file", "required field is missing"))
        for k, v in entry.items():
            if k not in SITE_KEY_KEYS:
                why = "unknown key; CONTEXT.md lists the allowed ones"
                out.append(Problem(p, f"{at}.{k}", why))
            elif not _type_ok(v, "str"):
                out.append(Problem(p, f"{at}.{k}", "expected str"))
        if sum(k in entry for k in SITE_KEY_COORDS) == 1:
            out.append(Problem(p, at, "lat_column and lon_column come together"))
    return out


def _site_defined_by_named(db: dict[str, Any]) -> list[str]:
    """Which of source and reference a site's defined_by names. A key written as an
    explicit null is absent, as the fixtures write datum and retrieved."""
    return [k for k in SITE_DEFINED_BY_LIMBS if db.get(k) is not None]


def _site_defined_by_limb(db: dict[str, Any]) -> str | None:
    """The one limb a site's defined_by names, or None when it names both or neither."""
    named = _site_defined_by_named(db)
    return named[0] if len(named) == 1 else None


def _site_defined_by_problems(rec: Record) -> list[Problem]:
    """The shape of a site's defined_by (CONTEXT.md, sites): exactly one of {source, where}
    or {reference, where}. Naming both, or neither, is one problem each; a limb or a
    `where` that is not a non-empty string is reported by its own name. Whether the
    limb resolves is the link pass's question."""
    db, p = rec.data["defined_by"], rec.path
    named = _site_defined_by_named(db)
    if len(named) == 2:
        return [Problem(p, "defined_by", "names both source and reference; exactly one")]
    if not named:
        return [Problem(p, "defined_by", "names neither source nor reference; exactly one")]
    out: list[Problem] = []
    for k in (named[0], "where"):
        if not _type_ok(db.get(k), "str"):
            out.append(Problem(p, f"defined_by.{k}", "expected str"))
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
    if rec.kind == "sites":
        program, _, site = rid.partition(".")
        if rid.count(".") != 1 or not program or not site:
            out.append(Problem(rec.path, key, "must be <program>.<site>, both parts non-empty"))
    if rec.kind == "beds":
        bed = rec.data.get("cdfw_bed")
        if isinstance(bed, int) and not isinstance(bed, bool) and rid != str(bed):
            out.append(Problem(rec.path, key, f"must equal cdfw_bed ({str(bed)!r})"))
    return out


def _tier_problems(rec: Record, root: Path | None, bad: set[str]) -> list[Problem]:
    if rec.kind != "sources" or "tier" in bad:
        return []
    d, p = rec.data, rec.path
    out: list[Problem] = []
    tier = d.get("tier")
    # CONTEXT.md, "Vocabularies": status and tier are independent but for one exception -
    # "Holding content means the route was exercised, so FETCHED, TRANSCRIBED and DERIVED
    # exclude PATTERN". The converse does not hold: holding nothing excludes nothing,
    # because a route can be exercised without its bytes being kept.
    if tier in HELD_TIERS and d.get("status") == "PATTERN":
        out.append(Problem(p, "status", f"PATTERN cannot hold content; tier is {tier}"))
    if tier in TABLE_TIERS:
        if not d.get("file"):
            out.append(Problem(p, "file", f"required when tier is {tier} (catalog/tables/...)"))
        elif not str(d["file"]).replace("\\", "/").startswith(TABLES_DIR):
            out.append(Problem(p, "file", f"must be a file under {TABLES_DIR}"))
        elif root is not None and not (root / str(d["file"])).exists():
            out.append(Problem(p, "file", f"{d['file']} does not exist in the repo"))
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
    elif tier == "DERIVED" and "derived_from" not in bad:
        out += _derived_from_problems(rec, root)
        if d.get("topics"):
            out.append(Problem(p, "topics", "must be [] when tier is DERIVED"))
    if tier != "FETCHED" and d.get("site_key"):
        # CONTEXT.md, sources: site_key names files fetch_script stores, so only a FETCHED
        # record has one to name.
        out.append(Problem(p, "site_key", "non-empty only when tier is FETCHED"))
    if tier == "NOT HELD":
        if d.get("retrieved") is not None:
            out.append(Problem(p, "retrieved", "must be null when tier is NOT HELD"))
        if d.get("fetch_script"):
            out.append(Problem(p, "fetch_script", "must be absent when tier is NOT HELD"))
    return out


def _derived_from_problems(rec: Record, root: Path | None) -> list[Problem]:
    """The shape of a DERIVED record's provenance (CONTEXT.md, sources, `derived_from`):
    inputs, a non-empty list of names; script, a path that exists in the repo;
    parameters, a mapping. Whether each input resolves is the link pass's question."""
    d, p = rec.data, rec.path
    df = d.get("derived_from")
    if not isinstance(df, dict) or not set(DERIVED_FROM_KEYS) <= set(df):
        return [Problem(p, "derived_from", "required: {inputs, script, parameters} when DERIVED")]
    out: list[Problem] = []
    if not _type_ok(df["inputs"], "list[str]"):
        out.append(Problem(p, "derived_from.inputs", "expected list[str]"))
    elif not df["inputs"]:
        out.append(Problem(p, "derived_from.inputs", "at least one input"))
    script = df["script"]
    if not _type_ok(script, "str"):
        out.append(Problem(p, "derived_from.script", "expected str"))
    elif root is not None and not (root / script).exists():
        out.append(Problem(p, "derived_from.script", f"{script} does not exist in the repo"))
    if not _type_ok(df["parameters"], "map"):
        out.append(Problem(p, "derived_from.parameters", "expected map"))
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
        df = d.get("derived_from")
        if isinstance(df, dict) and _type_ok(df.get("inputs"), "list[str]"):
            # CONTEXT.md, "Vocabularies", tier: an input is a source record or a record
            # directory; a held file enters the list as the id of the record whose field
            # names it. So the set is source ids plus catalog/<kind>/ for every kind.
            directories = {f"catalog/{kind}/" for kind in KINDS}
            # "A source named as an input holds content": the script reads what the record
            # holds, and a NOT HELD record holds nothing to read.
            tier_of = {r.id: r.data.get("tier") for r in catalog.records["sources"]}
            for v in df["inputs"]:
                if v in directories:
                    continue
                if v not in tier_of:
                    why = f"{v!r} is neither a source record nor a record directory"
                elif tier_of[v] not in HELD_TIERS:
                    why = f"{v!r} holds nothing to read; its tier is {tier_of[v]}"
                else:
                    continue
                out.append(Problem(p, "derived_from.inputs", why))
    if rec.kind == "regions":
        if d.get("parent") is not None:
            check("parent", [str(d["parent"])], "regions")
        db = d.get("defined_by")
        src = db.get("source") if isinstance(db, dict) else None
        if isinstance(src, str) and src.strip():  # else the shape check has reported it
            check("defined_by.source", [src], "sources")
    if rec.kind == "beds":
        check("region", [str(d.get("region"))], "regions")
    if rec.kind == "sites" and "defined_by" not in bad:
        # Each limb resolves into its own directory; a limb the shape check reported
        # (not a non-empty string, or not exactly one named) is not looked up.
        db = d["defined_by"]
        limb = _site_defined_by_limb(db)
        if limb is not None and _type_ok(db[limb], "str"):
            check(f"defined_by.{limb}", [db[limb]], f"{limb}s")
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
    """Read every record under root/catalog/<kind>/. Parse problems are returned, not raised.

    The directories are listed rather than globbed: a file the directory should not hold -
    a record saved as .yaml, say - is reported, never read.
    """
    catalog = Catalog(root=root)
    problems: list[Problem] = []
    base = root / "catalog"
    for dirname, ext in RECORD_DIRS.items():
        directory = base / dirname
        if not directory.is_dir():
            continue
        for path in sorted(directory.iterdir()):
            if not path.is_file() or path.name == KEEP_FILE:
                continue
            rel = path.relative_to(root).as_posix()
            if path.suffix != ext:
                problems.append(
                    Problem(rel, "file", f"unexpected file; catalog/{dirname}/ holds *{ext}")
                )
                continue
            if dirname not in KINDS:
                continue  # catalog/tables/ holds tables, not records
            rec, probs = parse_record(path.read_text(encoding="utf-8"), dirname, rel)
            problems += probs
            if rec is not None:
                catalog.records[dirname].append(rec)
    return catalog, problems


def check_catalog(root: Path) -> tuple[Catalog, list[Problem]]:
    """Load, then validate every record against the whole catalog."""
    catalog, problems = load_catalog(root)
    for rec in catalog.all():
        problems += validate(rec, catalog)
    problems += _duplicate_problems(catalog)
    return catalog, problems

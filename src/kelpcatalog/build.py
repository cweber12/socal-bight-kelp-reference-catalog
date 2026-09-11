"""Records in, one topic notebook out.

CONTEXT.md, "Notebooks", states the shape: five sections in a fixed order, generated
cells marked in cell metadata, figure cells never generated and never touched. This
module renders the first and preserves the second.

Seams:
    build_topic(topic, catalog, existing) -> NotebookNode   pure; no disk, no clock
    write_notebook(nb, path)                                a thin writer

`existing` is what makes "never touched" true. A build from records alone holds no
figure cell, so writing one over the committed notebook would delete the figure in
silence. build_topic therefore rewrites the cells carrying `kelpcatalog: generated` and
carries every other cell through, in place, byte for byte.

A notebook holds no facts. Every string below is one of four kinds: a record's own field,
a heading CONTEXT.md prints, a count - which CONTEXT.md permits a notebook to compute - or a
piece of the table furniture that carries no fact at all ("_No sources._", the column header
"region", the em dash for an absent value, the ellipsis on a truncation).

nbformat is a dev dependency, so this module is deliberately not imported by
`kelpcatalog/__init__.py`: `import kelpcatalog` must work in a runtime install.
"""

from __future__ import annotations

import copy
from pathlib import Path

import nbformat
from nbformat import NotebookNode
from nbformat.v4 import new_markdown_cell, new_notebook

from .plan import NOTEBOOK_PATHS, TOPIC_QUESTIONS, region_heading, region_sort_key
from .schema import GROUPS, TOPICS, Catalog, Record, split_topic

# --- what marks a generated cell ---------------------------------------------------
#
# CONTEXT.md: "Generated cells are marked in cell metadata (`kelpcatalog: generated`)".

GENERATED_KEY = "kelpcatalog"
GENERATED = "generated"

# nbformat's own word for a code cell. A figure cell is one the builder did not generate:
# CONTEXT.md says figure cells are "never generated and never touched", and the notebook
# shape names no other kind of code cell.
CODE = "code"

# --- the kernel a figure is executed by --------------------------------------------
#
# CONTEXT.md, "Notebooks": notebooks are "committed with outputs so they read on GitHub
# without running", and a figure cell's outputs exist only because a kernel produced them.
# Notebook metadata is the only place a notebook can name the kernel that does it, so the
# builder writes one the moment the assembled notebook holds a figure cell - rather than a
# hand-added kernelspec, which survives a regeneration *over* a notebook (metadata is
# carried through) but not a build from records alone, where a figure would be lost with
# it. #47's first comment is the argument in full.
#
# The values are notebook furniture and carry no fact about any source. `python3` is the
# name ipykernel registers itself under - `ipykernel/kernelspec.py` builds it as
# `"python%i" % sys.version_info[0]`, so it is the major version and not a fixed string,
# and it is what a venv with ipykernel in it offers. nbclient reads it from here when it
# is handed a notebook and no kernel name (`nbclient/client.py`: `self.nb.metadata.get(
# "kernelspec", {}).get("name")`), which is how #48 will re-execute one.
#
# One direction only. A notebook that holds a figure gains this; one that has lost its
# last figure keeps whatever metadata it had, because carrying `existing.metadata`
# through unchanged is what stops the builder from deleting something a reader put there.
KERNELSPEC = "kernelspec"
KERNEL = {"display_name": "Python 3", "language": "python", "name": "python3"}

# Cell ids are derived from the section's identity, never generated: nbformat's
# new_markdown_cell assigns a random id per call, so a builder that let it choose would
# rewrite every id - and so every byte of the file - on a rebuild that changed no record.
# The prefix keeps a derived id from ever colliding with a hand-authored cell's, and the
# two families ("subtopic-" and the fixed names) keep a sub-topic called "general" from
# colliding with the General section.
ID_PREFIX = "kelpcatalog-"
OVERVIEW_ID = f"{ID_PREFIX}overview"
GENERAL_ID = f"{ID_PREFIX}general"
NOT_HELD_ID = f"{ID_PREFIX}not-held"
REVIEWED_ID = f"{ID_PREFIX}reviewed"

# The three sections CONTEXT.md names in prose; the sub-topic sections are headed by the
# tag itself, which is the only name CONTEXT.md gives them.
GENERAL = "General"
NOT_HELD = "Not held"
REVIEWED = "Reviewed and not included"

# --- the coverage column -----------------------------------------------------------
#
# CONTEXT.md names the column `coverage` and is silent on what fills it, so the builder
# chooses; this is the whole of that choice. The field is prose as the source states it -
# 243, 1067 and 1596 characters in the three records held on 2026-09-09 - and a source
# renders once per sub-topic it is tagged with, so 11_ocean_climate would carry 9299
# characters of it, 6393 of them the same text again. Truncated here it carries 1249.
# The cut falls on a word boundary, and the id in the first column links to the record,
# where GitHub renders the whole field as a table: nothing is lost, only moved.
#
# The alternative, measured so the next reader need not re-derive it: at 300 the notebook
# carries 2283 characters and two of the three records show a span rather than one, because
# noaa_oni's 243-character field then renders whole. 160 is kept because chasing spans is
# self-defeating - PRD finding 2 is that these records state no span a rule can extract - so
# the column is a pointer at either length, and the cheaper pointer is the better one.
#
# One constant, one function: the day a record holds a span field that "The rule" admits,
# the column renders that field and both go.
COVERAGE_CHARS = 160
ELLIPSIS = "…"
EMPTY_CELL = "—"

SOURCE_COLUMNS = ("id", "title", "steward", "status", "tier", "coverage", "link")
NOT_HELD_COLUMNS = ("id", "title", "steward", "status", "tier", "human_task")
EXCLUDED_COLUMNS = ("slug", "what", "reason", "reviewed", "link")

LINK_TEXT = "link"

NO_SOURCES = "_No sources._"
NO_REFERENCES = "_No references._"
NO_EXCLUSIONS = "_Nothing reviewed and not included._"

# CONTEXT.md, "Vocabularies": NOT HELD is a tier, ON REQUEST a status. Section 4 is the
# union of the two, so a record that is either lands there.
NOT_HELD_TIER = "NOT HELD"
ON_REQUEST_STATUS = "ON REQUEST"


# --- reading records ---------------------------------------------------------------


def _tags(rec: Record) -> list[str]:
    return list(rec.data.get("topics") or [])


def _regions(rec: Record) -> list[str]:
    """The distinct regions a record tags, in the order it lists them.

    Distinct because a source is one source: `regions: [scb, scb]` is a record the schema
    accepts today, and iterating it as written renders the source twice in one table while
    section 1's matrix, which counts sources, counts it once. The record is malformed
    either way - see the bug filed against schema.py - but the grouping is right here
    regardless of what the schema comes to allow.
    """
    return list(dict.fromkeys(rec.data.get("regions") or []))


def _carries(rec: Record, topic: str, sub: str | None) -> bool:
    """Whether a record carries exactly this section's tag: `<topic>/<sub>`, or the bare
    `<topic>` when sub is None. A bare tag places a source under General, never under a
    sub-topic (CONTEXT.md, "Sub-topics")."""
    return any(split_topic(tag) == (topic, sub) for tag in _tags(rec))


def _in_topic(rec: Record, topic: str) -> bool:
    return any(split_topic(tag)[0] == topic for tag in _tags(rec))


def _of_topic(catalog: Catalog, kind: str, topic: str) -> list[Record]:
    return [r for r in catalog.records[kind] if _in_topic(r, topic)]


def _section_records(catalog: Catalog, kind: str, topic: str, sub: str | None) -> list[Record]:
    return sorted((r for r in catalog.records[kind] if _carries(r, topic, sub)), key=lambda r: r.id)


def _not_held(rec: Record) -> bool:
    return rec.data.get("tier") == NOT_HELD_TIER or rec.data.get("status") == ON_REQUEST_STATUS


# --- markdown --------------------------------------------------------------------


def _escape_pipes(text: str) -> str:
    """A pipe ends a table cell unless it is escaped, and GFM honours the escape inside
    an inline span - so a link's destination needs it as much as its text does."""
    return text.replace("|", r"\|")


def _inline(value: object) -> str:
    """A record's value as one table cell: whitespace collapsed, pipes escaped."""
    if value is None or value == "":
        return EMPTY_CELL
    return _escape_pipes(" ".join(str(value).split()))


def _truncate(text: str, limit: int = COVERAGE_CHARS) -> str:
    """The coverage column's one rendering decision. See COVERAGE_CHARS above."""
    if len(text) <= limit:
        return text
    cut = text[:limit].rstrip()
    space = cut.rfind(" ")
    if space > 0:
        cut = cut[:space]
    return cut.rstrip(" ,;:.") + ELLIPSIS


def _link(text: str, target: str | None) -> str:
    if not target:
        return EMPTY_CELL
    return f"[{_inline(text)}]({_escape_pipes(str(target))})"


def _table(columns: tuple[str, ...], rows: list[list[str]]) -> list[str]:
    head = "| " + " | ".join(columns) + " |"
    rule = "| " + " | ".join("---" for _ in columns) + " |"
    return [head, rule, *("| " + " | ".join(r) + " |" for r in rows)]


def _record_link(topic: str, kind: str, record_id: str) -> str:
    """A record is one click from the table that truncates it. The notebook sits at
    notebooks/<group folder>/<file>, so the hops up are counted from its own path."""
    up = "../" * (1 + NOTEBOOK_PATHS[topic].count("/"))
    return f"{up}catalog/{kind}/{record_id}.md"


def _external_link(rec: Record) -> str:
    """Link out of a table: the doi where the record has one, else the url.

    CONTEXT.md names the `link` column and says nothing about which of the two to prefer;
    the preference is #42's. The anchor text is the doi, which is short and is the string
    a reader copies, or the word "link", which keeps a 116-character URL out of a table
    cell. One rule, used by all three tables.
    """
    doi = rec.data.get("doi")
    if doi:
        return _link(str(doi), f"https://doi.org/{doi}")
    return _link(LINK_TEXT, rec.data.get("url"))


# --- the sources table -------------------------------------------------------------


def _source_row(topic: str, rec: Record) -> list[str]:
    d = rec.data
    coverage = d.get("coverage")
    return [
        _link(rec.id, _record_link(topic, "sources", rec.id)),
        _inline(d.get("title")),
        _inline(d.get("steward")),
        _inline(d.get("status")),
        _inline(d.get("tier")),
        _truncate(_inline(coverage)) if coverage else EMPTY_CELL,
        _external_link(rec),
    ]


def _sources_by_region(topic: str, sources: list[Record], catalog: Catalog) -> list[str]:
    """Grouped by region, in the notebook's own region order (#40, plan.region_sort_key).

    A source tagging more than one region renders under each of them. Whether it should,
    or should render once, is parked on #5; no current source carries two, so nothing
    observable turns on it yet. This is what the builder does today, and a test records
    it so that #44 cannot commit the opposite by accident - the test pins the behaviour,
    not the parked decision.
    """
    if not sources:
        return [NO_SOURCES]
    grouped: dict[str, list[Record]] = {}
    for rec in sources:
        for region in _regions(rec):
            grouped.setdefault(region, []).append(rec)
    lines: list[str] = []
    for region in sorted(grouped, key=region_sort_key):
        lines += ["", f"### {region_heading(region, catalog)}", ""]
        lines += _table(SOURCE_COLUMNS, [_source_row(topic, r) for r in grouped[region]])
    return lines[1:]  # the section heading already left a blank line


# --- references --------------------------------------------------------------------


def _references(topic: str, references: list[Record]) -> list[str]:
    """Every rendering of a reference goes through here.

    Today a reference record is a citation - citekey, ref, doi/url, year - so a section
    renders a bibliography. A `findings` field holding what a study states, verbatim with
    its page or section, is decided but not landed; when it lands this list becomes a
    table, and this is the one function that changes.
    """
    if not references:
        return [NO_REFERENCES]
    return [
        f"- **{rec.id}** {_inline(rec.data.get('ref'))} {_external_link(rec)}" for rec in references
    ]


# --- the five sections -------------------------------------------------------------


def _counted(n: int, noun: str) -> str:
    return f"{n} {noun}" if n == 1 else f"{n} {noun}s"


def _matrix(topic: str, catalog: Catalog, sources: list[Record]) -> list[str]:
    """The small region x sub-topic table of section 1.

    General is a column beside the sub-topics because it is a section beside them: a
    bare tag places a source there, and a matrix of sub-topics alone would show an empty
    row for a source the notebook does render.
    """
    subs: list[str | None] = [*TOPICS[topic], None]
    regions = sorted({r for rec in sources for r in _regions(rec)}, key=region_sort_key)

    def count(region: str, sub: str | None) -> str:
        return str(sum(1 for r in sources if _carries(r, topic, sub) and region in _regions(r)))

    rows = [
        [_inline(region_heading(region, catalog)), *(count(region, s) for s in subs)]
        for region in regions
    ]
    return _table(("region", *TOPICS[topic], GENERAL), rows)


def _counts(sources: list[Record], references: list[Record]) -> str:
    """The count line, printed by a topic notebook and by the index's entry for it.

    One function because the two must agree: a reader who follows the index's link must
    not find a different number at the other end.
    """
    return f"{_counted(len(sources), 'source')} · {_counted(len(references), 'reference')}"


def _overview(topic: str, catalog: Catalog) -> str:
    sources = _of_topic(catalog, "sources", topic)
    references = _of_topic(catalog, "references", topic)
    lines = [
        f"# {topic}",
        "",
        f"> {TOPIC_QUESTIONS[topic]}",
        "",
        _counts(sources, references),
    ]
    # No matrix when there is nothing to put in it: the count above already says so, and
    # "0 sources" followed by "_No sources._" states one thing twice.
    if sources:
        lines += ["", *_matrix(topic, catalog, sources)]
    return "\n".join(lines)


def _subtopic(topic: str, sub: str, catalog: Catalog) -> str:
    lines = [f"## {sub}", ""]
    lines += _sources_by_region(topic, _section_records(catalog, "sources", topic, sub), catalog)
    lines += ["", *_references(topic, _section_records(catalog, "references", topic, sub))]
    return "\n".join(lines)


def _general(topic: str, catalog: Catalog) -> str:
    lines = [f"## {GENERAL}", ""]
    lines += _sources_by_region(topic, _section_records(catalog, "sources", topic, None), catalog)
    lines += ["", *_references(topic, _section_records(catalog, "references", topic, None))]
    return "\n".join(lines)


def _not_held_section(topic: str, catalog: Catalog) -> str:
    sources = sorted(
        (r for r in _of_topic(catalog, "sources", topic) if _not_held(r)), key=lambda r: r.id
    )
    lines = [f"## {NOT_HELD}", ""]
    if not sources:
        return "\n".join([*lines, NO_SOURCES])
    rows = [
        [
            _link(rec.id, _record_link(topic, "sources", rec.id)),
            _inline(rec.data.get("title")),
            _inline(rec.data.get("steward")),
            _inline(rec.data.get("status")),
            _inline(rec.data.get("tier")),
            _inline(rec.data.get("human_task")),
        ]
        for rec in sources
    ]
    return "\n".join([*lines, *_table(NOT_HELD_COLUMNS, rows)])


def _reviewed(topic: str, catalog: Catalog) -> str:
    excluded = sorted(_of_topic(catalog, "excluded", topic), key=lambda r: r.id)
    lines = [f"## {REVIEWED}", ""]
    if not excluded:
        return "\n".join([*lines, NO_EXCLUSIONS])
    rows = [
        [
            _link(rec.id, _record_link(topic, "excluded", rec.id)),
            _inline(rec.data.get("what")),
            _inline(rec.data.get("reason")),
            _inline(rec.data.get("reviewed")),
            _external_link(rec),
        ]
        for rec in excluded
    ]
    return "\n".join([*lines, *_table(EXCLUDED_COLUMNS, rows)])


def _sections(topic: str, catalog: Catalog) -> list[tuple[str, str]]:
    """Every generated cell of a topic notebook: (derived id, markdown). Every section
    exists whether or not it holds anything (CONTEXT.md, "Notebooks"; gate #43)."""
    out = [(OVERVIEW_ID, _overview(topic, catalog))]
    out += [(f"{ID_PREFIX}subtopic-{sub}", _subtopic(topic, sub, catalog)) for sub in TOPICS[topic]]
    out.append((GENERAL_ID, _general(topic, catalog)))
    out.append((NOT_HELD_ID, _not_held_section(topic, catalog)))
    out.append((REVIEWED_ID, _reviewed(topic, catalog)))
    return out


# --- the index ---------------------------------------------------------------------
#
# CONTEXT.md, "Notebooks": `00_index.ipynb  group -> topic -> sub-topic counts; topic x
# region matrix`. Both halves read the catalog the topic notebooks read, so a source
# carrying a bare topic tag is counted here where its notebook renders it - under
# General - and a sub-topic breakdown without a General row would drop it. That is the
# defect #59 fixed in section 1's own matrix, one level up.
#
# The index's headings are the keys themselves - `physical-environment`, `ocean-climate`
# - as a topic notebook's are. CONTEXT.md's ten-questions table prints a group's name in
# prose ("Physical environment"), but the notebooks head every section with the tag, and
# a display name for each group would be a fourth transcription of CONTEXT.md to keep in
# step. The one rendering choice here is the link on a topic's heading, which is
# NOTEBOOK_PATHS' value and nothing else: the index sits at notebooks/00_index.ipynb, so
# a topic notebook's path is already relative to it.

INDEX_TITLE = "Index"
MATRIX_HEADING = "topic × region"
TOPIC_COLUMN = "topic"
SUBTOPIC_COLUMNS = ("sub-topic", "sources", "references")

INDEX_OVERVIEW_ID = f"{ID_PREFIX}index-overview"
INDEX_GROUP_ID = f"{ID_PREFIX}index-group-"
INDEX_MATRIX_ID = f"{ID_PREFIX}index-matrix"


def _index_overview(catalog: Catalog) -> str:
    return "\n".join(
        [
            f"# {INDEX_TITLE}",
            "",
            _counts(catalog.records["sources"], catalog.records["references"]),
        ]
    )


def _index_group(group: str, catalog: Catalog) -> str:
    """One group: each of its topics, its counts, and its sub-topics' counts.

    A topic with no sources is listed with its zeros rather than left out. The empty
    rows are the ingestion worklist, and CONTEXT.md's `notebook-structure` gate puts the
    every-topic obligation on the index.
    """
    lines = [f"## {group}"]
    for topic in GROUPS[group]:
        subs: list[str | None] = [*TOPICS[topic], None]
        rows = [
            [
                sub if sub is not None else GENERAL,
                str(len(_section_records(catalog, "sources", topic, sub))),
                str(len(_section_records(catalog, "references", topic, sub))),
            ]
            for sub in subs
        ]
        lines += [
            "",
            f"### [{topic}]({NOTEBOOK_PATHS[topic]})",
            "",
            _counts(_of_topic(catalog, "sources", topic), _of_topic(catalog, "references", topic)),
            "",
            *_table(SUBTOPIC_COLUMNS, rows),
        ]
    return "\n".join(lines)


def _index_matrix(catalog: Catalog) -> str:
    """Every topic against every region tag in use, `global` included.

    A row per topic whether or not it holds anything, so the matrix is the same shape
    from one PR to the next and a gap reads as a column of zeros. With no region tag in
    use it degenerates to the topic list rather than disappearing, which is the one thing
    CONTEXT.md's gate asks the index for.
    """
    sources = catalog.records["sources"]
    regions = sorted({r for rec in sources for r in _regions(rec)}, key=region_sort_key)

    def count(topic: str, region: str) -> str:
        return str(sum(1 for r in sources if _in_topic(r, topic) and region in _regions(r)))

    columns = (TOPIC_COLUMN, *(_inline(region_heading(r, catalog)) for r in regions))
    rows = [[topic, *(count(topic, region) for region in regions)] for topic in TOPICS]
    return "\n".join([f"## {MATRIX_HEADING}", "", *_table(columns, rows)])


def _index_sections(catalog: Catalog) -> list[tuple[str, str]]:
    """Every generated cell of the index: (derived id, markdown)."""
    out = [(INDEX_OVERVIEW_ID, _index_overview(catalog))]
    out += [(f"{INDEX_GROUP_ID}{group}", _index_group(group, catalog)) for group in GROUPS]
    out.append((INDEX_MATRIX_ID, _index_matrix(catalog)))
    return out


# --- building ----------------------------------------------------------------------


def is_generated(cell: NotebookNode) -> bool:
    return (cell.get("metadata") or {}).get(GENERATED_KEY) == GENERATED


def is_figure(cell: NotebookNode) -> bool:
    """A code cell the builder did not generate - CONTEXT.md's "figure cells".

    One definition, here beside `is_generated`, because two modules ask it of the same
    cells and must agree: the builder, to decide whether a notebook needs a kernelspec,
    and `figure_provenance.py`, to decide what carries a citation.
    """
    return cell.get("cell_type") == CODE and not is_generated(cell)


def _generated_cell(cell_id: str, source: str) -> NotebookNode:
    cell = new_markdown_cell(source)
    cell.id = cell_id
    cell.metadata[GENERATED_KEY] = GENERATED
    return cell


def _merge(generated: list[NotebookNode], existing: NotebookNode) -> list[NotebookNode]:
    """The generated cells, with every other cell of `existing` back where it was.

    A kept cell is anchored to the generated cell above it, so it returns to the same
    index whenever the same sections are generated - which is what makes "a regeneration
    leaves the figure cell byte-identical" (#47) reachable. A cell above the first
    generated cell stays above it; one under a section that no longer exists falls to the
    last surviving section above it, rather than being dropped.
    """
    ids = {cell.id for cell in generated}
    kept: dict[str | None, list[NotebookNode]] = {}
    anchor: str | None = None
    for cell in existing.cells:
        if is_generated(cell):
            if cell.get("id") in ids:
                anchor = cell["id"]
            continue
        kept.setdefault(anchor, []).append(copy.deepcopy(cell))
    out = list(kept.get(None, []))
    for cell in generated:
        out.append(cell)
        out += kept.get(cell.id, [])
    _settle_ids(out)
    return out


def _settle_ids(cells: list[NotebookNode]) -> None:
    """Give any kept cell that lacks an id of its own a derived one.

    nbformat.writes repairs a notebook as it serializes: it mints an id for a cell that
    has none, and silently renumbers one that duplicates another. Both mint a *random*
    value, so a notebook that reaches the writer needing repair is written differently
    every time - the one remaining way this builder's determinism can fail, and it fails
    at the byte level that #44 and #47 assert at, not at build_topic's.

    So the repair happens here, where it can be derived rather than drawn. A cell whose
    id is already its own is untouched, which is every cell of a notebook this builder
    wrote; the two that are not are a cell read back from a notebook older than cell ids
    (nbformat_minor 4) and a hand-authored cell that copied a generated cell's id. Both
    settle after one rebuild and are stable from then on.
    """
    taken = {cell["id"] for cell in cells if is_generated(cell)}
    for position, cell in enumerate(cells):
        if is_generated(cell):
            continue
        if cell.get("id") and cell["id"] not in taken:
            taken.add(cell["id"])
            continue
        # A minted id can itself be spoken for - a hand-authored cell is free to carry
        # any string, this shape included - so it is minted until it is free.
        candidate = f"{ID_PREFIX}kept-{position}"
        while candidate in taken:
            candidate += "x"
        cell["id"] = candidate
        taken.add(candidate)


def _assemble(sections: list[tuple[str, str]], existing: NotebookNode | None) -> NotebookNode:
    """The generated cells as a notebook, merged over `existing` where there is one.

    Notebook metadata is carried through, and the only metadata invented is the
    kernelspec a figure cell needs to be executed at all - so a notebook that has never
    held a figure still carries none. See KERNEL above.
    """
    cells = [_generated_cell(cell_id, source) for cell_id, source in sections]
    notebook = new_notebook()
    if existing is not None:
        notebook.metadata = copy.deepcopy(existing.metadata)
        cells = _merge(cells, existing)
    if any(is_figure(cell) for cell in cells):
        # dict(), so the module constant is never the object a notebook carries. No test
        # pins this and none can: NotebookNode converts a dict on assignment, so the
        # alias is already broken one line later whatever this does. It is here to say so.
        notebook.metadata[KERNELSPEC] = dict(KERNEL)
    notebook.cells = cells
    return notebook


def build_topic(topic: str, catalog: Catalog, existing: NotebookNode | None = None) -> NotebookNode:
    """One topic notebook, rendered from the records that carry the topic's tags.

    Pure: no disk, no clock, no randomness, so two builds of one catalog are the same
    bytes. `existing` is the notebook on disk, whose non-generated cells come through
    untouched; None builds from records alone.
    """
    if topic not in TOPICS:
        raise KeyError(f"unknown topic {topic!r}; CONTEXT.md's ten-questions table is the list")
    return _assemble(_sections(topic, catalog), existing)


def build_index(catalog: Catalog, existing: NotebookNode | None = None) -> NotebookNode:
    """The index notebook: group -> topic -> sub-topic counts, and the topic x region matrix.

    Pure, like build_topic, and merged over `existing` for the same reason: #44's issue
    gives this seam no `existing` parameter, and under that signature an entry point that
    regenerates everything would delete any cell of 00_index.ipynb it did not generate,
    which is exactly what build_topic's merge exists to prevent. Nothing observable turns
    on it today - the index has no such cell and CONTEXT.md specifies no figure for it -
    so the parameter is optional and `build_index(catalog)` is the signature the issue
    names. See the PR body.
    """
    return _assemble(_index_sections(catalog), existing)


def write_notebook(notebook: NotebookNode, path: Path) -> None:
    """Write the notebook to path, creating its folder.

    Not nbformat.write: that opens the file in text mode, so on Windows it would write
    CRLF into a repo whose .gitattributes commits every file with LF, and the same
    notebook would be different bytes on the two platforms CI runs.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = nbformat.writes(notebook)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8", newline="\n")

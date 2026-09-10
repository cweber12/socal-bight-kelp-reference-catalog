"""The committed notebooks, read back and checked against what CONTEXT.md requires.

CONTEXT.md, "Gates": `notebook-structure` asserts that "every topic notebook has exactly
the sections its sub-topic list requires, and the index lists every topic". This module is
that assertion; gate.py's row is the two lines that print it.

Seams:
    check_structure(root) -> (sections, problems)   the whole of the gate
    sections(notebook) -> list[str]                 pure; the headings a notebook holds

It reads `notebooks/`, never the builder's output. The two differ exactly when a notebook
has drifted from the records - a sub-topic added to `TOPICS` and not regenerated, a section
deleted by hand - and catching that is the whole of what this gate is for. So the expected
list is derived from `TOPICS` at the moment the gate runs, and the found list from the
committed bytes.

**Exactly**, which is CONTEXT.md's word: a missing section fails, and so does an extra one.

A gate reports; it does not fix. Nothing here writes, and there is no `--fix` flag (#43).

What it does not assert, so that a reader does not take more from a green row than it
says: outputs (#45) and figure provenance (#46).

It also does not assert that a notebook is **current with the records**, and no gate does.
A notebook whose sections are right and whose counts have gone stale passes here - and
passes #48 too, which re-executes a notebook and compares `execution_count`, `outputs` and
cell source. A generated cell is markdown, and re-executing a notebook never rebuilds a
markdown cell from the records, so a stale count line reproduces itself exactly. What keeps
the eleven current is process, not a gate: CONTEXT.md, "Notebooks" - "a source is not 'in'
until the notebooks that show it are refreshed in the same PR".

nbformat is a dev dependency, so - like build.py - this module is deliberately not imported
by `kelpcatalog/__init__.py`: `import kelpcatalog` must work in a runtime install.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from functools import partial
from pathlib import Path

import nbformat
from nbformat import NotebookNode

from .build import GENERAL, NOT_HELD, REVIEWED, is_generated
from .generate import NOTEBOOKS_DIR
from .plan import INDEX_PATH, NOTEBOOK_PATHS
from .schema import TOPICS, Problem

# CONTEXT.md, "Notebooks": a topic notebook's sections are its `#` title and one `##` per
# sub-topic and fixed section. A deeper heading is furniture *inside* a section - a region
# group in a topic notebook, a topic's entry in the index - and not a section itself.
SECTION_DEPTH = 2
INDEX_TOPIC_DEPTH = 3

# An ATX heading, with the optional closing run of hashes CommonMark allows. The heading
# is rebuilt from the match rather than kept as written, so that `##   heatwaves  ` and
# `## heatwaves` are one section and a message prints the tidy form.
HEADING_RE = re.compile(r"^(#{1,6}) +(\S.*?) *#*$")
# The index heads a topic with a link to its notebook; the topic is the link's text.
LINK_RE = re.compile(r"^\[([^\]]+)\]\([^)]*\)$")

MISSING_NOTEBOOK = "the notebook is missing; `python -m kelpcatalog.generate` writes it"
NOTEBOOK_FIELD = "notebook"


def _headings(notebook: NotebookNode) -> Iterator[tuple[int, str, str]]:
    """(depth, text, heading) for every heading of every generated markdown cell.

    Generated cells only: a figure cell carries no `kelpcatalog: generated` marker and
    never will (#47), so a heading a reader wrote over a figure is not a section, and its
    absence is not a section gone missing. Markdown cells only: `#` opens a comment in
    code, so a generated code cell's first line is not a heading.
    """
    for cell in notebook.cells:
        if cell.get("cell_type") != "markdown" or not is_generated(cell):
            continue
        for line in str(cell.get("source") or "").splitlines():
            found = HEADING_RE.match(line)
            if found:
                yield len(found[1]), found[2], f"{found[1]} {found[2]}"


def sections(notebook: NotebookNode) -> list[str]:
    """The section headings a notebook holds, in the order it holds them."""
    return [heading for depth, _, heading in _headings(notebook) if depth <= SECTION_DEPTH]


def expected_sections(topic: str) -> list[str]:
    """The sections a topic notebook must hold, in order.

    Derived, not transcribed: `TOPICS` is CONTEXT.md's sub-topic list and the three fixed
    English strings live in build.py. A fourth copy here would be a fourth thing to keep in
    step, and would let this gate pass a notebook that no longer matched the builder.
    """
    return [
        f"# {topic}",
        *(f"## {sub}" for sub in TOPICS[topic]),
        f"## {GENERAL}",
        f"## {NOT_HELD}",
        f"## {REVIEWED}",
    ]


def listed_topics(notebook: NotebookNode) -> set[str]:
    """The topics the index lists: the text of each `###` heading, a link unwrapped."""
    out = set()
    for depth, text, _ in _headings(notebook):
        if depth == INDEX_TOPIC_DEPTH:
            link = LINK_RE.match(text)
            out.add(link[1] if link else text)
    return out


def _topic_problems(path: str, notebook: NotebookNode, topic: str) -> list[Problem]:
    """Every way a topic notebook's sections differ from the ones `TOPICS` requires."""
    expected = expected_sections(topic)
    found = sections(notebook)
    if found == expected:
        return []
    out = [Problem(path, s, "section is missing") for s in expected if s not in found]
    # dict.fromkeys rather than a set: the order a reader meets the sections in is the
    # order they are reported in, and a set's is the hash seed's.
    for section in dict.fromkeys(found):
        if section not in expected:
            out.append(Problem(path, section, f"not a section of {topic}"))
        elif found.count(section) > 1:
            out.append(Problem(path, section, "section appears twice"))
    if out:
        return out
    # Same sections, same number of each, different order: the two lists line up, so the
    # first index they disagree at names the section that moved.
    at = next(i for i, section in enumerate(found) if section != expected[i])
    return [Problem(path, found[at], f"section is out of order; {expected[at]} comes here")]


def _index_problems(path: str, notebook: NotebookNode) -> list[Problem]:
    """CONTEXT.md asks the index for every topic. A topic with no sources is listed with
    its zeros - the empty rows are the ingestion worklist - so nothing exempts one."""
    listed = listed_topics(notebook)
    return [
        Problem(path, topic, "the index does not list this topic")
        for topic in TOPICS
        if topic not in listed
    ]


def _the_eleven() -> Iterator[tuple[str, Callable[[str, NotebookNode], list[Problem]]]]:
    """Each notebook's path under the repo root, with what is asked of it."""
    yield f"{NOTEBOOKS_DIR}/{INDEX_PATH}", _index_problems
    for topic in TOPICS:
        yield f"{NOTEBOOKS_DIR}/{NOTEBOOK_PATHS[topic]}", partial(_topic_problems, topic=topic)


def _read(path: Path, rel: str) -> tuple[NotebookNode | None, list[Problem]]:
    """The notebook at path, or why it could not be read.

    A gate returns (passed, message); one that raised would take gate.py down on exactly
    the hand-edited notebook it exists to catch, so a file that is not a notebook is a
    problem to report rather than an exception to raise.
    """
    if not path.is_file():
        return None, [Problem(rel, NOTEBOOK_FIELD, MISSING_NOTEBOOK)]
    try:
        return nbformat.read(path, as_version=4), []
    # Broad on purpose: the file is arbitrary bytes, and whatever a reader raises over it
    # is the one fact this gate has to report.
    except Exception as e:
        return None, [Problem(rel, NOTEBOOK_FIELD, f"is not a notebook this gate can read: {e}")]


def check_structure(root: Path) -> tuple[dict[str, list[str]], list[Problem]]:
    """The sections each committed notebook holds, and every way they are wrong.

    Counts are the caller's to print, never to assert: a gate never fails because the
    catalog grew (CONTEXT.md, "Gates").
    """
    root = Path(root)
    found: dict[str, list[str]] = {}
    problems: list[Problem] = []
    for rel, check in _the_eleven():
        notebook, unreadable = _read(root / rel, rel)
        problems += unreadable
        if notebook is None:
            continue
        found[rel] = sections(notebook)
        problems += check(rel, notebook)
    return found, problems

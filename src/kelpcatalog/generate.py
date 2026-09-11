"""One command, eleven notebooks: the whole of `notebooks/` rebuilt from the records.

    .venv/Scripts/python -m kelpcatalog.generate      from the repo root

This is the command `add-source` points at (#49) and the command a reviewer runs to check
that a committed notebook is current: regenerating a clean tree changes no bytes, so a
notebook that has fallen behind its records shows up as a diff.

Seams:
    generate(root, into) -> list[Path]     every notebook written, in the plan's order
    main() -> int                          the command, standing in the repo root

The one thing this must not do is call the builders without `existing`. A build from
records alone holds no figure cell (CONTEXT.md: "figure cells are never generated and
never touched"), so writing one over a committed notebook would delete the figure in
silence, and nothing would say so. Both loops below therefore read the file back first.
Both write through `build.write_notebook` rather than `nbformat.write`, which opens the
file in text mode and would put CRLF into a repo whose .gitattributes is `* text=auto
eol=lf`.

Paths come from `plan.INDEX_PATH` and `plan.NOTEBOOK_PATHS`, never a second copy of the
layout; the directory they sit under is the one CONTEXT.md's `notebooks/` tree names.
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbformat import NotebookNode

from .build import build_index, build_topic, write_notebook
from .plan import INDEX_PATH, NOTEBOOK_PATHS
from .schema import TOPICS, check_catalog

NOTEBOOKS_DIR = "notebooks"
CATALOG_DIR = "catalog"


def _existing(path: Path) -> NotebookNode | None:
    """The notebook on disk, or None the first time it is written."""
    return nbformat.read(path, as_version=4) if path.exists() else None


def generate(root: Path, into: Path | None = None) -> list[Path]:
    """Rebuild every notebook from `root`'s catalog. Returns what it wrote.

    `into` is the directory the eleven land in, `root/notebooks/` by default; a test
    passes its own so that two runs can be diffed without touching the repo.
    """
    root = Path(root)
    target = Path(into) if into is not None else root / NOTEBOOKS_DIR
    catalog, problems = check_catalog(root)
    if problems:
        raise ValueError(
            f"the catalog under {root} does not validate, so there is nothing to render:\n"
            + "\n".join(str(p) for p in problems)
        )

    written: list[Path] = []
    index = target / INDEX_PATH
    write_notebook(build_index(catalog, existing=_existing(index)), index)
    written.append(index)
    for topic in TOPICS:
        path = target / NOTEBOOK_PATHS[topic]
        write_notebook(build_topic(topic, catalog, existing=_existing(path)), path)
        written.append(path)
    return written


def main() -> int:
    """Regenerate the notebooks of the repo this is run from, and name what was written."""
    root = Path.cwd()
    if not (root / CATALOG_DIR).is_dir():
        print(f"no {CATALOG_DIR}/ under {root}: run this from the repo root", file=sys.stderr)
        return 1
    written = generate(root)
    for path in written:
        print(path.relative_to(root).as_posix())
    print(f"\n{len(written)} notebooks written to {NOTEBOOKS_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

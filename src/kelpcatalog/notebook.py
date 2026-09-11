"""What a figure cell calls: the caption under the plot, and the way to the bytes.

CONTEXT.md, "The rule": "a notebook may load a catalogued file by id, apply an equation
as a cited reference prints it, and plot; every mark on the figure traces to a record or
a printed equation, and a `provenance(...)` caption under the figure says which."

Seams:
    provenance(*, sources, references, equations) -> Provenance   the caption
    load(source_id, root=None) -> Mapping[str, Path]              the catalogued files

This is the one module in the package a *notebook* imports, which is why it depends on
nothing but the standard library and `.schema`. `nbformat` and `matplotlib` are both dev
dependencies and this module imports neither, so a figure cell that wants to plot imports
matplotlib itself; `provenance` renders markdown and knows nothing about figures.

**`provenance` resolves nothing.** It takes ids and renders them; whether an id names a
record is the `figure-provenance` gate's question, asked of the committed cell's source
text without executing it (`figure_provenance.py`). The split is that way round because a
gate that ran the notebook could not run in CI, and because a typo that raised inside the
cell would be reported as a broken figure rather than as a broken citation. The cost is
stated plainly: a figure cell with a mistyped id still renders a caption when it is run,
and it is the gate, not the run, that catches it.

**The caption names ids; it does not link them.** A link to `catalog/sources/<id>.md`
would have to be relative to the notebook the cell sits in, and that path would then be
baked into the caption text a committed cell carries - which is bytes `notebook-fresh`
(#48) compares, derived from where the kernel happened to be running. `_repo_root` below
does find the notebook's directory from `Path.cwd()`, so this is a choice not to use it
rather than an inability: the id is what the record is filed under, so a reader has the
name they need to find it, and the caption stays the same on every machine.

**`load()` is an interim, and CONTEXT.md already names its replacement.** A source record
carries `fetch_script`, not an artefact path, and the only id-to-bytes mapping on disk is
`data/raw/<id>/manifest_*.json` - a convention of the scripts under `src/fetch/`, written
into a git-ignored directory. CONTEXT.md does not endorse that convention. What it does
say is that `data/` "is git-ignored and reproducible from `src/fetch/` plus the lock", and
that `data-lock.json` holds "every fetched file's url, sha256 and bytes". So the catalog's
own answer to "load a catalogued file by id" is the lock, and the lock arrives in
milestone 6.5, which replaces this function's body with a lock lookup. One function, one
place to change, and no record field involved.

A caller should therefore not depend on the path layout: use the mapping's keys, not
`data/raw/...` spelled out in a figure cell. The keys are file names rather than list
positions because no record *field* states an order a caller could read - `sio_shore_
stations`'s `access` does list its five URLs north to south, and `calcofi`'s its two, but
those are prose steps and CLAUDE.md forbids parsing a prose file - so an index would be
the directory listing's order dressed up as a fact. Two of the three sources held today
are multi-file (`calcofi` holds a cast file and a bottle file, which are different data),
which is the other half of why a single `Path` cannot express the seam.

Know what the key costs before leaning on it: for `calcofi` it is
`siocalcofiHydroCast_d677_9801_7f83.csv`, whose suffix is ERDDAP's hash of the query and
is stated in no record - `src/fetch/calcofi.py` warns that a server upgrade changes it.
There is no supported way to ask for "the cast table" today, and 6.5's lock is where one
could exist.

`load()` resolves through the manifests rather than by listing the directory. A manifest
is the record that a fetch wrote that file, so a payload *no manifest names* - dropped in
by hand, or left by a fetch that was interrupted before its manifest - is not handed to a
figure. That is the whole of what this buys, and it is narrower than "stale files cannot
reach a figure": two of the three fetch scripts never delete and the third prunes only on
a clean run, so an old payload *and its manifest* both survive a re-fetch under a new name
and `load` returns the pair with nothing to say which is current. Every manifest carries
`fetched_at` and this reads none of them - resolving that is the lock's job in 6.5, not a
rule invented here.

It reads only each manifest's *name*, never its contents: the local file name is the one
thing a manifest does not carry as a field, and the key sets differ between scripts
(`calcofi`'s carries `content_type`, `last_modified` and `etag`; `noaa_oni`'s does not).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from .schema import load_catalog

# The three keywords a figure cell names its ids by, and the call it ends with. The gate
# matches a cell's source against these, so they are defined once, here, beside the
# signature that takes them - test_notebook.py pins the two against each other.
PROVENANCE = "provenance"
SOURCES = "sources"
REFERENCES = "references"
EQUATIONS = "equations"

# An equation is identified by the reference that prints it and its id on that reference:
# `equations: list of {id, as_printed, where}` hangs off a reference record, so an id
# alone would name nothing. CONTEXT.md does not spell the compound form, so this is the
# module's choice; "/" follows the one compound tag CONTEXT.md does spell, `<topic>/<sub>`.
EQUATION_SEP = "/"

# The fetch scripts' convention, and the interim this module resolves through. See the
# module docstring: 6.5's lock replaces it.
DATA_DIR = "data"
RAW_DIR = "raw"
MANIFEST_PREFIX = "manifest_"
MANIFEST_SUFFIX = ".json"

# What a repo root is recognised by, when a figure cell calls load() with none.
CATALOG_DIR = "catalog"
SOURCES_KIND = "sources"

# Caption furniture: a label per group, a separator, and what an empty citation says.
CAPTION_LABEL = "**Provenance**"
CAPTION_JOIN = " · "
CAPTION_EMPTY = "nothing named"


@dataclass(frozen=True)
class Provenance:
    """The ids a figure cell traces its marks to, and the caption they render as.

    Frozen, and rendered through `_repr_markdown_`: an object carrying that method is
    what IPython's markdown formatter displays, so the caption reaches the notebook
    without this module importing IPython, which is not a dependency and would not be
    one at a fresh clone.

    Two things the audit of #67 raised, both measured in #47 against a running kernel
    (matplotlib 3.11.1, ipykernel 7.3.0, nbclient 0.11.0) and both as it predicted.

    The `execute_result` a kernel writes carries a `text/plain` beside the markdown, and
    it comes from `__repr__` - the dataclass's - not from the `__str__` below. The cell
    in 11_ocean_climate commits `Provenance(sources=('noaa_oni',), references=(),
    equations=())` there, so the dataclass repr is part of the bytes #48 compares.

    And **CONTEXT.md says the caption goes *under* the figure**, which the gate's "ends
    with `provenance(...)`" does not secure. With the inline backend and no explicit
    `plt.show()`, `matplotlib_inline` publishes the figure from a `post_execute` hook,
    *after* this result, and the cell commits as `[caption, figure]` - measured. The
    answer is `plt.show()` before the call, which publishes the figure where the cell
    stands and commits `[figure, caption]`; PRD finding 7's "no image at all" was
    `matplotlib.use("Agg")`, not `plt.show()`, and does not reach the inline backend.
    No gate holds that order - `figure-provenance` reads source, and `notebook-outputs`
    reads only that an output exists and is neither an error nor a stderr stream. What
    holds it for the committed cell is a test
    (`test_the_committed_figure_commits_its_caption_under_its_figure`);
    what would hold it for a cell whose source stopped producing it is #48, since
    dropping the `plt.show()` changes no committed byte until something re-executes.
    """

    sources: tuple[str, ...] = ()
    references: tuple[str, ...] = ()
    equations: tuple[str, ...] = ()

    def _repr_markdown_(self) -> str:
        parts = [
            f"{label}: " + CAPTION_JOIN.join(f"`{value}`" for value in values)
            for label, values in (
                (SOURCES, self.sources),
                (REFERENCES, self.references),
                (EQUATIONS, self.equations),
            )
            if values
        ]
        return f"{CAPTION_LABEL} — " + (CAPTION_JOIN.join(parts) if parts else CAPTION_EMPTY)

    def __str__(self) -> str:
        return self._repr_markdown_()


def provenance(
    *,
    sources: Iterable[str] = (),
    references: Iterable[str] = (),
    equations: Iterable[str] = (),
) -> Provenance:
    """The citation that goes under a plot: which records and printed equations it traces to.

    Keyword-only, so that the three names the gate reads out of a cell's source are the
    three names the call takes. A positional list would have an order stated only by this
    signature, which the gate would then have to transcribe.

    Resolves nothing - see the module docstring. An `equations` id is
    `<citekey>/<equation id>` (EQUATION_SEP), naming the reference that prints it.
    """
    return Provenance(tuple(sources), tuple(references), tuple(equations))


def _repo_root(root: Path | None) -> Path:
    """The root given, or the nearest directory at or above the working directory holding
    `catalog/`.

    A notebook runs with its own folder as the working directory - two levels under the
    root for a topic notebook - so a figure cell calls `load("noaa_oni")` with no root.
    """
    if root is not None:
        return Path(root)
    here = Path.cwd()
    for candidate in (here, *here.parents):
        if (candidate / CATALOG_DIR).is_dir():
            return candidate
    raise FileNotFoundError(
        f"no {CATALOG_DIR}/ at or above {here}: run a notebook from inside the repo, "
        f"or name the root with load(source_id, root=...)."
    )


def load(source_id: str, root: Path | None = None) -> Mapping[str, Path]:
    """The files a source's fetch wrote, keyed by file name.

    An interim that resolves through `data/raw/<id>/manifest_*.json` and that 6.5's
    `data-lock.json` replaces; a caller should not depend on the path layout. The module
    docstring carries the whole of that argument, and why the keys are names.

    Raises rather than returning empty: `data/` is git-ignored, so a fresh clone has none
    and there is nothing to plot. That is not a state a reader falls into - a notebook
    carrying a figure is committed with its outputs and reads on GitHub without running.
    """
    root = _repo_root(root)
    if source_id not in load_catalog(root)[0].ids(SOURCES_KIND):
        raise KeyError(f"{source_id!r} is not a source record; catalog/{SOURCES_KIND}/ is the list")

    data = root / DATA_DIR
    if not data.is_dir():
        raise FileNotFoundError(
            f"no {DATA_DIR}/ under {root}: it is git-ignored, so a fresh clone has none. "
            f"Run the source's fetch_script to make one."
        )
    here = data / RAW_DIR / source_id
    # Sorted by name, not by Path: comparing Path objects case-folds on Windows and does
    # not on POSIX, so a source holding names that differ in case would come back in one
    # order here and another in CI - and #48 compares committed bytes. Found by the audit
    # of PR #67.
    listing = here.glob(f"{MANIFEST_PREFIX}*{MANIFEST_SUFFIX}") if here.is_dir() else []
    manifests = sorted(listing, key=lambda manifest: manifest.name)
    if not manifests:
        raise FileNotFoundError(
            f"nothing fetched for {source_id!r}: no manifest under "
            f"{DATA_DIR}/{RAW_DIR}/{source_id}/. Run its fetch_script."
        )

    files: dict[str, Path] = {}
    for manifest in manifests:
        name = manifest.name[len(MANIFEST_PREFIX) : -len(MANIFEST_SUFFIX)]
        payload = here / name
        if not payload.is_file():
            raise FileNotFoundError(
                f"{name!r} is named by a manifest in {DATA_DIR}/{RAW_DIR}/{source_id}/ "
                f"but is not there. Re-run its fetch_script."
            )
        files[name] = payload
    return files

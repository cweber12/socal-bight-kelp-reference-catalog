# PRD — Topic notebooks (milestone 6.2)

Status: active
Created: 2026-09-09
Revised: 2026-09-09, after an audit of the first draft reversed its central decision.

## Problem

The catalog holds three records and no way to read them. `CONTEXT.md` already specifies the
notebook — one per topic, in a folder per group, plus an index; five sections in a fixed order;
generated cells marked in cell metadata; committed with outputs so they read on GitHub without
running — and schedules the four gates that hold that shape. None of it exists: there is no
`notebooks/` directory, no builder, and `src/kelpcatalog/` is still just `schema.py`.

## Solution

A builder that turns records into the notebook `CONTEXT.md` already describes, the index that lists
them, and the four gates that keep them honest. `CONTEXT.md`'s prose becomes data the builder
reads; the builder writes generated cells and never touches figure cells; the gates hold the shape,
the outputs, the freshness and the provenance. Two `CONTEXT.md` silences that stop a notebook from
rendering at all are closed first. The first figure lands last, so `figure-provenance` and
`notebook-fresh` are exercised by a real artifact rather than only by fixtures.

## What the spike found

A throwaway builder rendered `11_ocean_climate` from the three existing records (`calcofi`,
`sio_shore_stations`, `noaa_oni` — between them all five `ocean-climate` sub-topics, both region
tags in use, and the whole current catalog). It was not committed. Numbers below are the ones that
reproduce from the repo; where a measurement depended on the discarded builder's exact output, it
has been dropped rather than quoted.

1. **Rendering `coverage` verbatim makes the table unreadable, and the notebook mostly
   repetition.** `CONTEXT.md` specifies the sources table as
   `id · title · steward · status · tier · coverage · link`, and is silent on what fills the
   coverage column. The three records' `coverage` fields are 1067, 1596 and 243 characters of
   prose — correct prose, exactly what the rule demands of a record. A source renders once per
   sub-topic it is tagged with, so one `ocean-climate` notebook carries **6636 characters of
   coverage prose, of which 3730 is the same text repeated**. At three sources.
2. **`coverage_start` / `coverage_end` cannot be filled from these records as dates.** This is the
   finding that decides the milestone's ordering, below. `noaa_oni` states its span in seasons —
   "SEAS DJF YR 1950 to SEAS JJA YR 2026" — and a date needs a convention the source does not
   state. `sio_shore_stations` states **eight** spans (five stations, temperature and salinity
   separately where both exist) plus a collection-level "1916 to present", a year rather than a
   date; one start date is `min()` over eight quoted values, which is a computed number. `calcofi`
   states three candidate spans — the page's "1949 - present", ERDDAP's
   1949-02-28T22:42:00Z → 2021-05-13T20:37:00Z, and the held files' 1959-02-06T23:48:00Z →
   2021-05-04T21:02:00Z — with no rule for choosing. "The rule" excludes computed numbers and
   re-derivations, so none of the three yields a start date without inventing something.
3. **`global` has nowhere to sort and no name.** The ordering is "Bight-wide first, then counties
   north to south, then islands". `noaa_oni` is `regions: [global]`, and `global` is allowed
   without a region record, so it has neither a slot in that order nor a display name. The spike
   had to invent both to render the `upwelling-enso` section at all.
4. **`CONTEXT.md` answers "load a catalogued file by id" with the lock, which is 6.5.** A source
   carries `fetch_script`, not an artefact path, and the only id → bytes mapping on disk is
   `data/raw/<id>/manifest_*.json` in a git-ignored directory. That is a convention of the fetch
   scripts, not of the catalog: `CONTEXT.md` says `data/` "is reproducible from `src/fetch/` plus
   the lock", and the lock holds "every fetched file's url, sha256 and bytes". So this is not a
   silence — it is a dependency of 6.2's figure work on an artifact 6.5 delivers. A source can also
   hold several files (`sio_shore_stations` five, `calcofi` two), so the resolution is not
   single-valued.
5. **The notebook's ordering facts are prose only.** The question per topic, the group folder names
   and notebook numbers (`1_physical_environment` / `11`), and counties north to south are stated
   in `CONTEXT.md` and appear nowhere in `schema.py`, which carries `TOPICS` and `GROUPS` alone.
6. **A topic notebook has zero code cells until it has a figure.** Eight of the ten topics have no
   sources at all today, and none has a figure. See "Readings adopted".
7. **`notebook-fresh` can be a byte comparison, under conditions.** Two executions of the same
   figure notebook were byte-identical only with `record_timing=False` — `nbclient` otherwise
   stamps a wall-clock `metadata.execution` into every executed cell — and with the inline backend.
   The first attempt used `matplotlib.use("Agg")` with `plt.show()`: it produced **no image at
   all**, its sole output being a stderr stream carrying the kernel's PID, which differs every run.
   Cross-platform PNG bytes will differ regardless, which is why `CONTEXT.md` already scopes this
   gate "local"; `gate.py`'s `skip_if` is the seam for that.
8. **Cell ids must be derived, not generated.** `nbformat.v4.new_markdown_cell` and
   `new_code_cell` both assign a random id per call, and `nbformat.validate` warns that a missing
   id will become a hard error. A builder that lets `nbformat` choose produces a whole-file diff on
   every rebuild even when no record changed.
9. **Salinity has no section to land in.** `sio_shore_stations` holds `SALINITY_PSU`,
   `SURF_SAL_PSU` and `BOT_SAL_PSU` and quotes the collection on "salinity (SSS)"; `calcofi` holds
   `salinity` and `r_sal`. `ocean-climate`'s sub-topics are temperature · nutrients ·
   upwelling-enso · heatwaves · oxygen-ph, so both records show their temperature half and drop
   their salinity half. Under the rule that is a missing sub-topic, not a property of the sources.

**Nothing here contradicts `CONTEXT.md`.** Each finding is one of three things: a place `CONTEXT.md`
is silent (3, and what fills the coverage column in 1); a place it has scheduled the answer to a
later milestone (4); or a fact about the records or the tooling rather than about `CONTEXT.md` at
all (2, 5–9). The first draft of this PRD said instead that findings were places "the schema is
short of what it specifies" — which was an equivocation, since `CONTEXT.md`'s own "Record schemas"
tables *are* the schema and `schema.py` merely implements them. Read literally that sentence had
`CONTEXT.md` disagreeing with itself, which is not what the spike found.

## Decision: record schema v2 stays parked, before 6.4

The Parking lot (#5) carries *"Record schema v2, one slice, before 6.4 — these each re-touch every
record, so they land together or not at all"*. **It does not move.** The first draft of this PRD
moved it to before 6.2's builder, as issue #38; that decision is reversed and #38 is closed.

Three reasons, in the order that decides it:

- **It is not forced.** The draft's case rested on `coverage_start` / `coverage_end` being what the
  specified coverage column needs. Finding 2 shows they cannot be filled from any of the three
  records without a derivation "The rule" excludes. v2 as parked would not fix the coverage column;
  it would replace an unreadable column with a rule-compliance problem, and the parked entry needs
  a rule for what fills those fields before it can be sliced at all.
- **Deferring is cheap, and the draft overstated the cost.** The draft claimed a post-6.2 field
  change means "regenerate eleven notebooks, re-execute every figure, re-commit — including the PNG
  payloads". That is wrong on its own reading of `CONTEXT.md`: generated cells are markdown, and
  figure cells are "never generated and never touched". A record-field change therefore rewrites
  markdown text and nothing else — no figure is re-executed, no PNG byte changes, and
  `notebook-fresh` still passes. #44 makes the regeneration one command and #49 wires it into
  `add-source`, so it is a routine operation the milestone is explicitly building.
- **It does not fit one PR.** v2 restructures `variables` to `{name, description, unit}` across 142
  entries (calcofi 122, `sio_shore_stations` 16, `noaa_oni` 4), each description and unit quoted
  from the steward; adds four more verbatim fields on three records; changes `RULES` for three
  record kinds; rewrites `CONTEXT.md`'s schema tables; and updates the `add-source` skill. That is
  a re-entry pass — 6.4's named work — and `CLAUDE.md` says small PRs.

**The actual defect has a cheaper fix, and it is a rendering decision, not a schema one.**
`CONTEXT.md` names the coverage column and is silent on what fills it, so the builder chooses.
Issue #42 renders the coverage prose truncated, with the record one click away, where GitHub already
displays the full field as a table. Nothing is re-entered, no record is touched, and it is
reversible the day a span field exists that the rule admits.

**`data-lock.json` also stays in 6.5, and the draft's argument for that is withdrawn too.** The
parked entry's stated reason is that "the sha256 of a fetch lives only in a git-ignored manifest
and CI cannot tell `VERIFIED` from asserted". The draft answered a different argument — notebook
regeneration — and then recorded the result on the Parking lot as settled. That comment has been
deleted. What 6.2 needs from the lock is narrower than the parked entry and does not settle it:
one resolution step for figure cells, `load(source_id)` in #46, whose interim is a fetch-script
convention and whose real answer, per finding 4, is the lock.

## Readings adopted

`CONTEXT.md` admits more than one implementation in two places. The reading is stated here so a
reviewer can reject it before eleven notebooks are built on it.

**`notebook-outputs` — "committed notebooks carry outputs and no errors"** is read as *every code
cell carries outputs, and no output is an error*. A notebook with no code cells passes with nothing
to check. The supporting argument is `CONTEXT.md`'s own Gates section: "A gate never fails because
the catalog grew; counts are printed, not asserted." The strict reading — every *notebook* carries
outputs — fails a topic notebook for not yet having a figure, which is a gate asserting content.

**Generated cells are markdown cells, not code cells emitting tables as outputs.** The third
reading is real and would satisfy even the strict one, so it is foreclosed on the text rather than
by omission: `CONTEXT.md` says generated cells are "rewritten by the builder whenever records or
this file change". Under the code-cell reading a generated cell would hold a call like
`render_sources(...)`, and a record changing would change its output but never its source — nothing
to rewrite. Under the markdown reading the record content *is* the cell source, which is what
"rewritten whenever records change" describes. `notebook-fresh` re-executing "needs `data/` for
figures" agrees: figures are the only thing execution touches.

Two smaller questions are carried by the slice that meets them, so each lands as a reviewed diff:
`CONTEXT.md` does not say whether `NOT HELD` and `ON REQUEST` sources appear in the sub-topic
tables as well as their own section (#42 settles it — all three current sources are `FETCHED`, so
the spike never hit it), and it does not say whether a source with two or more region tags repeats
in every group or renders once (parked; no current source has two).

## Slices

Numbers are issues on milestone 6.2. **The rows are in work order, which is not issue-number
order:** #43 and #45 read the committed notebooks and cannot finish before #44 creates them.

| order | # | slice | seam | done when |
|---|---|---|---|---|
| 1 | [#39](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/39) | `ocean-climate/salinity` sub-topic | `TOPICS`; the sub-topic table and the topic's question in `CONTEXT.md`; two records | `topic_problem("ocean-climate/salinity")` is `None`; both records carrying salinity variables carry the tag |
| 2 | [#40](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/40) | where `global` sorts, and what it is called | the ordering sentence in `CONTEXT.md`, "Notebooks" | `CONTEXT.md` states the slot, the display name and why |
| 3 | [#41](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/41) | the notebook plan as data | `TOPIC_QUESTIONS`, `NOTEBOOK_PATHS`, `region_sort_key`, `region_heading` | the plan reproduces `CONTEXT.md`'s tables; a topic with no question fails a test |
| 4 | [#42](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/42) | the builder | `build_topic(topic, catalog, existing) -> NotebookNode`, pure; a thin writer; `nbformat` | two builds byte-identical; cell ids derived; a figure cell in `existing` survives untouched |
| 5 | [#44](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/44) | the index, and the first generation | `build_index(catalog)`; `notebooks/` | eleven notebooks committed; regenerating a clean tree changes no bytes |
| 6 | [#43](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/43) | gate `notebook-structure` | a `gate.py` row | a notebook missing a sub-topic section fails; an extra section fails |
| 7 | [#45](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/45) | gate `notebook-outputs` | a `gate.py` row | an error output fails; a code cell with no outputs fails; a stderr stream fails |
| 8 | [#46](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/46) | the figure runtime | `kelpcatalog.notebook`: `provenance(...)`, `load(source_id)`; gate `figure-provenance` | a figure cell with no `provenance(...)` fails; an unresolvable id fails; a multi-file source resolves |
| 9 | [#47](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/47) | the first figure | one figure cell in `11_ocean_climate`; `matplotlib` | ONI anomaly from `noaa_oni`; a regeneration leaves the cell byte-identical |
| 10 | [#48](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/48) | gate `notebook-fresh` | a `gate.py` row with `skip_if`; `nbclient`, `ipykernel` | an edited committed output fails locally; skipped in CI with a reason |
| 11 | [#49](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/49) | refreshing notebooks with a source | `add-source`, `CLAUDE.md` | the skill regenerates the notebooks a new source appears in, in the same PR |

Issues #39 and #40 close the two gaps that stop a notebook rendering at all, and both are `CONTEXT.md`
diffs. #41–#45 are the builder, the index and the two gates that need no figure. #46–#48 are
figures. #49 closes the loop `CONTEXT.md` already states: "a source is not 'in' until the notebooks
that show it are refreshed in the same PR".

**#47 rests on a known interim.** Per finding 4, `CONTEXT.md`'s answer to resolving a source id to
bytes is the lock, and the lock is 6.5. #46's `load()` uses the fetch scripts' `data/raw/<id>/`
convention until then. The alternative is to defer #47 to 6.5 and leave `figure-provenance` and
`notebook-fresh` exercised only by fixtures for a milestone — which is why the figure is here
instead. A reviewer who would rather not build on the convention should move #47 and #48's real-tree
assertion to 6.5; nothing else in the milestone changes.

## Non-goals

No record-schema change: v2 stays parked (see the decision above), and no slice adds a record
field. No regions below `scb` (6.3) — the region ordering ships with the counties it will sort, and
the county nodes arrive later. No `data-lock.json` and no lock gate (6.5). No citation export and
no index pages beyond `00_index.ipynb` (6.6). No new sources. No analysis: a figure cell loads a
catalogued file, applies an equation as a reference prints it, and plots — it computes nothing else.

## Done

Eleven notebooks committed with outputs, four new gate rows green, and a source entering through
`add-source` refreshes the notebooks that show it.

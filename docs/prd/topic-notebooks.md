# PRD — Topic notebooks (milestone 6.2)

Status: active
Created: 2026-09-09

## Problem

The catalog holds three records and no way to read them. `CONTEXT.md` already specifies the
notebook — one per topic, in a folder per group, plus an index; five sections in a fixed order;
generated cells marked in cell metadata; committed with outputs so they read on GitHub without
running — and schedules the four gates that hold that shape. None of it exists: there is no
`notebooks/` directory, no builder, and `src/kelpcatalog/` is still just `schema.py`.

Notebooks are also the point at which the catalog stops being cheap to change. They are generated
from records and committed with outputs, and `notebook-fresh` re-executes them, so a record field
that changes after the notebooks land forces every notebook to be regenerated, re-executed and
re-committed. Whatever the record schema is when the first notebook is committed is the schema the
notebooks are built against.

## What the spike found

A throwaway builder rendered `11_ocean_climate` from the three existing records
(`calcofi`, `sio_shore_stations`, `noaa_oni` — between them every ocean-climate sub-topic except
`heatwaves`-only, both region tags in use, and the whole current catalog). It was not committed.
What it hit, in the order it hit it:

1. **The `coverage` column cannot be filled from the `coverage` field.** `CONTEXT.md` specifies the
   sources table as `id · title · steward · status · tier · coverage · link`. The three records'
   `coverage` fields are 1067, 1596 and 243 characters of prose — correct prose, exactly what the
   rule demands of a record, and unreadable in a markdown table cell. A source repeats in one
   section per sub-topic it is tagged with, so `calcofi`'s 1067 characters render three times and
   `sio_shore_stations`' 1596 twice: **6636 of the notebook's 11335 bytes, 59%, are the same
   coverage prose repeated.** At three sources.
2. **No record field says where a fetched file lands.** `CONTEXT.md` says a figure cell "loads a
   catalogued file by id", but a source carries `fetch_script`, not an artefact path. The only
   id → bytes mapping on disk is `data/raw/<id>/manifest_*.json`, written by the fetch script into
   a git-ignored directory. The spike hard-coded the path because there was nothing to resolve.
3. **`global` has nowhere to sort and no name.** The ordering is "Bight-wide first, then counties
   north to south, then islands". `noaa_oni` is `regions: [global]`, and `global` is allowed
   without a region record, so it has neither a slot in that order nor a display name. The spike
   had to invent both to render the `upwelling-enso` section at all.
4. **The notebook's ordering facts are prose only.** The question per topic, the group folder names
   and notebook numbers (`1_physical_environment` / `11`), and counties north to south are stated
   in `CONTEXT.md` and appear nowhere in `schema.py`, which carries `TOPICS` and `GROUPS` alone.
5. **A topic notebook has zero code cells until it has a figure.** All ten do today. So
   `notebook-outputs` must read as *every code cell carries outputs and none is an error* —
   vacuously true for a figure-free notebook — not *the notebook carries outputs*. See "Readings
   adopted" below.
6. **`notebook-fresh` can be a byte comparison, under three conditions.** Two executions of the
   same figure notebook were byte-identical (57632 bytes each) only with `record_timing=False` —
   `nbclient` otherwise stamps a wall-clock `metadata.execution` into every executed cell — and
   with the inline backend. The first attempt used `matplotlib.use("Agg")` with `plt.show()`: it
   produced **no image at all**, and a stderr warning carrying the kernel's PID
   (`ipykernel_27100` vs `ipykernel_18128`), which differs every run. Cross-platform PNG bytes will
   differ regardless, which is why `CONTEXT.md` already scopes this gate "local"; `gate.py`'s
   `skip_if` is the seam for that.
7. **Cell ids must be derived, not generated.** `nbformat.v4.new_code_cell` assigns a random id per
   call, and `nbformat.validate` warns that a missing id will become a hard error. A builder that
   lets `nbformat` choose produces a whole-file diff on every rebuild even when no record changed.
8. **`sio_shore_stations` holds salinity that no section can show.** Its variables include
   `SALINITY_PSU`, `SURF_SAL_PSU` and `BOT_SAL_PSU`, and its `coverage` quotes the collection on
   "salinity (SSS)" — but `ocean-climate`'s sub-topics are temperature · nutrients ·
   upwelling-enso · heatwaves · oxygen-ph. The notebook shows the temperature half of the source
   and silently drops the salinity half. Under the rule, that is a missing sub-topic, not a
   property of the source.

Nothing the spike hit contradicts `CONTEXT.md`. Every finding is a place it is silent or a place
the schema is short of what it specifies.

## Decision: schema v2 lands before the first notebook is committed

The Parking lot (#5) carries *"Record schema v2, one slice, before 6.4 — these each re-touch every
record, so they land together or not at all: `variables` entries as {name, description, unit};
`citation` + `citation_stated_at` verbatim; `version`; `coverage_start` / `coverage_end` as dates;
`license_stated_at`; `retrieved` on beds and sites."* **It moves to before 6.2's builder, as the
first slice of this milestone.** The date changes; the design and the "together or not at all"
do not.

Why:

- **Finding 1 is not cosmetic.** `coverage_start` / `coverage_end` are precisely the field the
  specified `coverage` column needs. Without them the builder must either render an unreadable
  table or invent a truncation rule — and a truncation rule is a rendering decision that will be
  deleted the moment v2 lands, after every notebook has been built against it.
- **The cost of touching records is at its floor and rises monotonically.** Three records today.
  6.4 is *Re-entry*; by then there are more, and `data-lock.json` (6.5) is hashing them.
- **After 6.2 the cost is no longer just the records.** Notebooks are committed with outputs, and
  `notebook-fresh` re-executes them, so a field change lands as: regenerate eleven notebooks,
  re-execute every figure, re-commit — including the PNG payloads, which run ~40 KB apiece. Landing
  v2 before the notebooks exist costs one sweep of three records and nothing else.
- **Splitting v2 to take only `coverage_start` / `coverage_end` now is the worst option.** It buys
  a smaller slice today and pays for it with a second full sweep of every record before 6.4 —
  which is the exact cost the parked entry's "together or not at all" exists to avoid.

**`data-lock.json` does not move, and stays scheduled for 6.5.** The Parking lot pairs the two
entries, but the argument above does not transfer: the lock is a file, not a record field, so it
forces no regeneration of anything. Finding 2 is real, but what 6.2 needs from it is one function
to resolve a source id to local bytes — `load(source_id)` in the notebook runtime. 6.5 replaces
that function's body with a lock lookup and touches no notebook and no record.

## Readings adopted

Two sentences in `CONTEXT.md` admit more than one implementation. The PRD adopts a reading so the
slices can name a failing test; the reading is stated here so a human can reject it.

- **`notebook-outputs` — "committed notebooks carry outputs and no errors"** is read as *every code
  cell carries outputs, and no output is an error*, which a figure-free notebook satisfies with
  nothing to check. The alternative — every notebook must carry outputs — means no topic notebook
  can be committed until it has a figure, i.e. ten figures before the milestone closes. That is a
  much larger 6.2 and is not what the rest of the section describes, since markdown generated cells
  already "read on GitHub without running".
- **Generated cells are markdown cells.** `notebook-fresh` re-executing "needs `data/` for figures"
  only makes sense if figures are the sole thing execution touches.

Two more, each carried by the slice that needs it, so it lands as a reviewed `CONTEXT.md` diff
rather than an unwritten assumption:

- **`global` sorts last, after the islands, and is called "No regional bound"** (slice 3). It is
  not a wider region than the Bight; `CONTEXT.md` defines it as the absence of a regional bound,
  and it is the one region tag with no record, so it is not a node of the tree and should not be
  interleaved with nodes. A Bight catalog leads with Bight-wide sources. The alternative — sorting
  it first as the widest bound — is the reason this is a `CONTEXT.md` diff and not a builder
  constant.
- **`salinity` sits second, after `temperature`** (slice 2), where a reader looking for the other
  half of a shoreline hydrographic record will look for it.

One ambiguity is left to the builder slice, which must settle it in its PR: `CONTEXT.md` puts
`NOT HELD` and `ON REQUEST` sources in their own section 4, and does not say whether they also
appear in the sub-topic tables of section 2. All three current sources are `FETCHED`, so the spike
never hit it.

## Slices

| # | slice | seam | done when |
|---|---|---|---|
| [#38](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/38) | record schema v2 | `RULES` in `schema.py`; the record-schema tables in `CONTEXT.md`; three records; `add-source` | every record carries the v2 fields; gate green; the Parking-lot entry is deleted |
| [#39](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/39) | `ocean-climate/salinity` sub-topic | `TOPICS` in `schema.py`; the sub-topic table in `CONTEXT.md`; `sio_shore_stations` | `topic_problem("ocean-climate/salinity")` is `None`; the record carries the tag |
| [#40](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/40) | where `global` sorts, and what it is called | the ordering sentence in `CONTEXT.md`, "Notebooks" | `CONTEXT.md` states the slot and the display name; two Parking-lot entries deleted |
| [#41](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/41) | the notebook plan as data | `TOPIC_QUESTIONS`, `NOTEBOOK_PATHS`, `region_sort_key`, `region_heading` | the plan reproduces `CONTEXT.md`'s tables; a topic with no question fails a test |
| [#42](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/42) | the builder | `build_topic(topic, catalog) -> NotebookNode`, pure; a thin writer; `nbformat` | builds `11_ocean_climate` from a fixture catalog; two builds byte-identical; cell ids derived |
| [#43](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/43) | gate `notebook-structure` | a `gate.py` row | a fixture notebook missing a sub-topic section fails; an extra section fails |
| [#44](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/44) | the index, and the first generation | `build_index(catalog)`; `notebooks/` | eleven notebooks committed; regenerating a clean tree changes no bytes |
| [#45](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/45) | gate `notebook-outputs` | a `gate.py` row | an error output fails; a code cell with no outputs fails; a stderr stream fails |
| [#46](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/46) | the figure runtime | `kelpcatalog.notebook`: `provenance(...)`, `load(source_id)`; gate `figure-provenance` | a figure cell with no `provenance(...)` fails; an unresolvable id fails |
| [#47](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/47) | the first figure | one figure cell in `11_ocean_climate` | ONI anomaly from `noaa_oni`; a regeneration leaves the cell byte-identical |
| [#48](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/48) | gate `notebook-fresh` | a `gate.py` row with `skip_if`; `nbclient`, `ipykernel` | an edited committed output fails locally; skipped in CI with a reason |
| [#49](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/49) | refreshing notebooks with a source | `add-source`, `CLAUDE.md` | the skill regenerates the notebooks a new source appears in, in the same PR |

\#38–#40 touch records and `CONTEXT.md` and must land before the builder — that is the whole point
of the schema decision above. #41–#45 are the builder, the index and the two gates that need no
figure. #46–#48 are figures. #49 closes the loop `CONTEXT.md` already states: "a source is not 'in'
until the notebooks that show it are refreshed in the same PR".

## Non-goals

No regions below `scb` (6.3) — the region ordering ships with the counties it will sort, and the
county nodes arrive later. No `data-lock.json` and no lock gate (6.5). No citation export and no
index pages beyond `00_index.ipynb` (6.6). No new sources. No analysis: a figure cell loads a
catalogued file, applies an equation as a reference prints it, and plots — it computes nothing
else.

## Done

Eleven notebooks committed with outputs, four new gate rows green, and a source entering through
`add-source` refreshes the notebooks that show it. If a slice needs a record field that is not in
schema v2, the schema decision above was wrong — stop and say so rather than adding the field
after the notebooks exist.

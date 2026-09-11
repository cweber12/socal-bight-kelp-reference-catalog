# CONTEXT — what this catalog is, and the rules every record follows

This file is the authority. `src/kelpcatalog/schema.py` implements it; if the two disagree, this
file is right and the code is a bug.

## Purpose

A catalog of the authoritative sources — datasets, monitoring programs, reports and papers — for
kelp forest monitoring in the Southern California Bight, organized by **topic** and by **region**,
so that a researcher can find what exists for a question or a place, reach the original in one
click, and check any value against it.

The catalog supports analysis repos; it does not do analysis.

## The rule

> A record holds only what the source itself states, and what anyone repeating the fetch would
> reproduce. Nothing else.

What that admits and excludes:

| admitted | excluded |
|---|---|
| a source's title, steward, URL, DOI, licence text as published | any judgement of a source's quality |
| access steps that a stranger can follow today | narrative about how the record came to be |
| format, variables and units as the source lists them | summary statistics computed here |
| coverage as the source states it, with where it states it | fits, corrections or re-derivations of published relationships |
| retrieved date, sha256 and byte count of a fetched file | "first-look" observations, interpretations, verdicts |
| a fact anyone repeating the fetch would see ("returns 401 without a bearer token, 2026-09-04") | drafts, correspondence, to-do notes |
| an equation exactly as a paper prints it, with page or equation number | an equation adjusted, clipped or extended here |
| a one-line reason a reviewed item was excluded | paragraphs about why |

Figures follow the same rule: a notebook may load a catalogued file by id, apply an equation as a
cited reference prints it, and plot; every mark on the figure traces to a record or a printed
equation, and a `provenance(...)` caption under the figure says which.

## Record format

A record is one markdown file whose entire content is a YAML frontmatter block. The body below the
closing `---` must be empty. Markdown rather than YAML because GitHub renders frontmatter as a table,
so records browse without a site build. The record's type is the directory it lives in; its id is
its file name.

```text
catalog/
  sources/<id>.md          a dataset, program, report series or transcribed table
  references/<citekey>.md  a paper or report cited by a source or a figure
  excluded/<slug>.md       an item reviewed and not admitted, with its one-line reason
  regions/<id>.md          a node of the region tree
  beds/<n>.md              a CDFW Administrative Kelp Bed
  sites/<id>.md            a monitoring program's named station
  tables/<id>.csv          transcribed tables; each has a source record with tier TRANSCRIBED
  data-lock.json           every fetched file's url, sha256 and bytes (arrives with the lock gate)
```

`data/` is git-ignored and reproducible from `src/fetch/` plus the lock. Nothing is ever written
into `data/` by hand.

## Vocabularies

**status** — whether the route to the source is known to work.
`VERIFIED` (the route was exercised: bytes fetched on the `retrieved` date, or a printed page
transcribed, per `transcribed_from`) · `PATTERN` (route documented but not exercised) ·
`NOT PUBLIC` · `ON REQUEST`. Status and tier are not independent: only a fetch or a printed page in
hand can have exercised the route, so `VERIFIED` requires a `tier` of `FETCHED` or `TRANSCRIBED`;
equivalently, a `NOT HELD` record's status is `PATTERN`, `NOT PUBLIC` or `ON REQUEST`.

**tier** — how the local content, if any, came to exist.
`FETCHED` (bytes retrieved unmodified from the steward's host) · `TRANSCRIBED` (values typed from a
printed page, or extracted from a document by a named script, into `catalog/tables/`) · `NOT HELD`
(nothing local; the record describes the source and how to ask).

**topics** — see *Topics: the ten questions* below. A tag is `<topic>` or `<topic>/<sub-topic>`.

**regions** — the tree below. A source tags the most specific node that covers it; `global` is
allowed without a record for sources with no regional bound (ONI). `global` is therefore not a node
of the tree, and not a region wider than the Bight: it states the *absence* of a bound, not a bound
that happens to be large. It is also the one region tag with no record, so it has no `name` to
print; *Notebooks* below gives the heading a notebook prints instead, and where in the order it
falls.

## Topics: the ten questions

Three groups, ten topics, each topic a question. The three groups follow how the drivers are
sorted in NOAA Office of National Marine Sanctuaries, "Kelp forest impacts"
(sanctuaries.noaa.gov/visit/ecosystems/kelpimpacts.html); California Research Bureau, "Kelp
forests" brief, 2 April 2026 (library.ca.gov/crb/nexus/briefs/kelp-forests/); and SCCWRP, Bight '08
Rocky Reef (dataportal.sccwrp.org, page 28ae52ed…), all retrieved 2026-09-07. The questions are
what a notebook answers.

| group | topic | question |
|---|---|---|
| Physical environment | `ocean-climate` | What thermal, salinity, nutrient, oxygen and pH climate are the beds exposed to, and how is it trending? |
| | `canyon-dynamics` | How much cool, nutrient-rich water do canyon internal tides deliver, and when? |
| | `waves-storms-sediment` | When do swells and storms remove kelp, and what is the sand doing at the bed margins? |
| | `substrate` | Where is the rock, how complex is it, and what does that predict? |
| Kelp and community | `canopy` | How has surface canopy extent changed since 1911, bed by bed? |
| | `bed-state` | What are the kelp and its community doing on the reef, where, and since when? |
| | `grazers-predators-competitors` | What sets urchin and competitor pressure on the beds, and what holds it in check? |
| | `recruitment-connectivity` | How do spores, larvae and genes move between beds, and what does that mean for recovery? |
| Human uses and management | `water-quality-harvest` | What do discharges, runoff, power plants and kelp harvest do to the beds? |
| | `restoration-mitigation` | What has been tried to restore or offset kelp loss, and what did it do? |

**Sub-topics** are the sections of a topic's notebook. A tag `ocean-climate/heatwaves` places a
source in that section; a bare `ocean-climate` places it under *General*. A source may carry any
number of tags across any topics.

| topic | sub-topics |
|---|---|
| `ocean-climate` | `temperature` · `salinity` · `nutrients` · `upwelling-enso` · `heatwaves` · `oxygen-ph` |
| `canyon-dynamics` | `internal-tides` · `canyon-circulation` · `observations` |
| `waves-storms-sediment` | `swell-climate` · `storms` · `sediment-sand` · `beach-coupling` |
| `substrate` | `rock-mapping` · `relief-rugosity` · `artificial-substrate` |
| `canopy` | `aerial-surveys` · `satellite` · `historical-baselines` · `persistence` |
| `bed-state` | `diver-surveys` · `community` · `invasives` · `mpas` |
| `grazers-predators-competitors` | `urchins` · `predators` · `grazing-fishes` · `drift-algae` · `competitors` |
| `recruitment-connectivity` | `spore-dispersal` · `larval-transport` · `settlement` · `genetics` |
| `water-quality-harvest` | `discharges-outfalls` · `runoff-sedimentation` · `power-plants` · `kelp-harvest` · `fishing-pressure` |
| `restoration-mitigation` | `outplanting` · `urchin-removal` · `artificial-reefs` · `kelp-farms` |

**Topics do not decide what is admitted.** Admission is by scope — an authoritative source about
kelp in the Bight. If a source fits no topic or sub-topic, add one (a row here, an entry in
`schema.py`, a notebook section) in its own PR; never exclude the source for want of a tag.

## The region tree

Every node's `defined_by` names the source that draws the boundary. Levels:

1. `scb` — the Southern California Bight, taken as the Bight '18 survey area, "from Point
   Conception, CA in the north to the US-Mexico border in the south" (Gillett, Enright & Walker
   2022, SCCWRP Technical Report 1289, Introduction).
2. `scb.mainland` and `scb.islands` — the Bight program samples the Channel Islands as their own
   stratum; every mainland program states coverage by county.
3. Mainland counties: `scb.mainland.santa-barbara`, `.ventura`, `.los-angeles`, `.orange`,
   `.san-diego` (coverage as stated for the Region Nine and Central Region Kelp Survey Consortia on
   the kelp.sccwrp.org home page, retrieved 2026-09-07). Island groups: `scb.islands.northern`,
   `scb.islands.southern`, with one node per island beneath.
4. **Beds**, keyed by CDFW Administrative Kelp Bed number (87 statewide including the Channel
   Islands; CDFW 2021, Giant Kelp and Bull Kelp Enhanced Status Report, Management section,
   https://marinespecies.wildlife.ca.gov/kelp/true/, retrieved 2026-09-07). The boundaries are
   drawn by shapefiles under the directory `filelib.wildlife.ca.gov/Public/R7_MR/BIOLOGICAL/Kelp/`
   (per the same report, Monitoring section); the exact file is recorded on each bed's `defined_by`
   when beds arrive in 6.3. Program bed names are `aliases:`.
5. **Sites**, a program's named station, with lat/lon from the program and the bed it falls in.

Consortium is an attribute on a county node, not a level, and it is a **list**: the kelp.sccwrp.org
home page, retrieved 2026-09-07, states that RNKSC covers San Diego and southern Orange counties and
CRKSC covers northern Orange, Los Angeles and Ventura, so the boundary runs through Orange County,
which states both (`consortium: [RNKSC, CRKSC]`), and Santa Barbara County is listed by neither
consortium on that page (`consortium: []`); the field states what the page lists, not a claim about
the county. A county node says which consortia the county falls under and nothing finer: which
consortium surveys a given **bed** is a bed field, `surveyed_by`, arriving in milestone 6.3.

Depth is not a level of the tree. A source's depth range is part of its `coverage`, as the source
states it. For orientation: CDFW gives giant kelp habitat as "the low intertidal to depths of 25
meters … with maximum depths of 30 meters" (ESR 2021, Species-at-a-Glance, same URL), which sits
within Bight '18's Inner Shelf stratum, 7–30 m (TR 1289, Table 1).

## Record schemas

Required fields are marked `*`. "Where from" says what may supply the value.

### sources/<id>.md

| field | type | where from |
|---|---|---|
| `id`* | str, `^[a-z0-9][a-z0-9._-]*$`, equals file name | chosen on entry, never changed |
| `title`* | str | the source's own title |
| `steward`* | str | the organisation that publishes or holds it |
| `url`* | str or null | the landing page or direct file |
| `doi` | str or null | |
| `status`* | status vocabulary | |
| `tier`* | tier vocabulary | |
| `access`* | list of str | numbered steps a stranger can follow |
| `format` | str or null | as the source describes its files |
| `license`* | str | the licence text as published, verbatim; "not stated" if absent |
| `variables`* | list of str | as the source lists them; empty list if NOT HELD |
| `coverage` | str or null | as the source states it |
| `coverage_stated_at` | str or null | the page or file where it is stated |
| `retrieved`* | date or null | required non-null when FETCHED; null when NOT HELD |
| `fetch_script` | path | required when FETCHED; must exist in the repo |
| `file` | path | required when TRANSCRIBED; a file under `catalog/tables/` |
| `transcribed_from` | `{reference, table, page}` | required when TRANSCRIBED |
| `topics`* | list of topic tags (`<topic>` or `<topic>/<sub-topic>`), ≥ 1 | |
| `regions`* | list of region ids or `global`, ≥ 1 | |
| `beds` | list of bed ids | |
| `sites` | list of site ids | |
| `references` | list of citekeys | |
| `human_task` | str or null | an `H<n>` id when the source arrives only through a person |

### references/<citekey>.md

| field | type | where from |
|---|---|---|
| `citekey`* | `^[a-z][a-z0-9]*\d{4}[a-z]?$`, equals file name | first author's surname + year |
| `ref`* | str | the citation as printed |
| `doi` / `url` | str or null; at least one non-null | |
| `year`* | int | |
| `equations` | list of `{id, as_printed, where}` | only equations a figure applies; verbatim |
| `topics`* | list of topic tags, ≥ 1 | |

### excluded/<slug>.md

`slug`* (equals file name), `reviewed`* (date), `what`* (the item), `reason`* (one line),
`url`, `doi`, `topics` (optional; lets the notebook list what was reviewed and not admitted).

### regions/<id>.md

`id`* (equals file name), `name`*, `parent`* (region id, or null for `scb`), `defined_by`*
(the source that draws the boundary), `consortium` (list of `RNKSC` / `CRKSC`, non-empty only
when `parent` is `scb.mainland`; `[]` where neither consortium covers the county).

### beds/<n>.md

`id`* (the bed number as a string, equals file name), `cdfw_bed`* (int), `name`* (as in the
shapefile), `status`* (`Open` · `Closed` · `Leasable` · `Lease Only`), `region`* (a county or
island region id), `aliases` (program names for the same bed), `defined_by`* (the shapefile URL).

### sites/<id>.md

`id`* (`<program>.<site>`, equals file name), `program`*, `name`* (as the program names it),
`bed`* (bed id or null), `lat`*, `lon`* (from the program), `defined_by`* (the program's document).

## Notebooks

Notebooks are how the catalog is read and shared. A notebook never holds a fact: it renders
records. One notebook per topic, in a folder per group, plus an index:

```text
notebooks/
  00_index.ipynb                     group → topic → sub-topic counts; topic × region matrix
  1_physical_environment/            11_ocean_climate  12_canyon_dynamics
                                     13_waves_storms_sediment  14_substrate
  2_kelp_and_community/              21_canopy  22_bed_state
                                     23_grazers_predators_competitors  24_recruitment_connectivity
  3_human_uses_management/           31_water_quality_harvest  32_restoration_mitigation
```

Each topic notebook has the same shape, generated from the records:

1. the question, verbatim from the table above; a count of sources and references; and, when the
   topic has sources, a small region × sub-topic table, whose columns are the topic's sub-topics
   **and *General***, because *General* is a section beside them and a source carrying the bare
   tag must be counted where the notebook renders it — a matrix of sub-topics alone would print a
   row of zeros for a region whose sources the notebook does show. A topic with none gets no
   table: its rows are one per region holding a source, so it would render a header and a rule
   over nothing, under a line that already reads `0 sources · 0 references`;
2. one section per sub-topic, in the order listed above — a sources table (id · title · steward ·
   status · tier · coverage · link) grouped by region, in the region order below; the references
   tagged to the sub-topic; then any figures;
3. *General* — sources tagged with the bare topic;
4. *Not held* — `NOT HELD` and `ON REQUEST` sources for the topic, with their `human_task`;
5. *Reviewed and not included* — exclusions tagged with the topic.

**The region order.** Groups run in the tree's own order, traversed depth-first — a node, then all
its descendants, before the next sibling — with siblings in the order this file lists them. The
tree above is numbered by level, so the traversal, not that numbering, fixes the order:
Bight-wide (`scb`) first; then `scb.mainland` and its counties north to south —
`santa-barbara`, `ventura`, `los-angeles`, `orange`, `san-diego`; then `scb.islands`, its groups in
the order listed (`northern`, then `southern`), and the islands beneath each; and `global` last.
Siblings this file does not itself put in an order — the islands within a group — sort by id, so
the order is total over every value a `regions` field can hold: every region id the tree has or
gains, down to the islands beneath each group, and `global`. Beds and sites are levels 4 and 5 of
the tree but are not region ids — a source carries them in `beds` and `sites` — so this order
does not reach them. The order is a property of the region id alone, because it must hold for the
county and island nodes before their records exist in 6.3. A group's heading is its node's `name`;
`global` has no record and is headed **No regional bound**.

`global` sorts last rather than first, and the three reasons are recorded here so that the next
reader need not re-derive them: `global` is the *absence* of a regional bound rather than a bound
wider than the Bight, so "widest first" does not reach it; it is the one region tag with no record,
so it is not a node of the tree and is not interleaved with nodes; and a Bight catalog leads with
its Bight-wide sources. Sorting it first, as the widest bound, is the alternative, and is rejected
on those three grounds.

Generated cells are marked in cell metadata (`kelpcatalog: generated`) and rewritten by the
builder whenever records or this file change; figure cells are never generated and never touched.
A figure cell loads a catalogued file by id, applies an equation as a cited reference prints it,
plots, and ends with `provenance(sources=[...], references=[...], equations=[...])`, which renders
the citation under the plot. Notebooks are committed with outputs so they read on GitHub without
running; a source is not "in" until the notebooks that show it are refreshed in the same PR.

There is no notebook per region. The by-region view is the grouping inside each topic notebook
and the matrix in the index.

## Gates

`gate.py` runs every gate and exits non-zero if one fails. A gate never fails because the catalog
grew; counts are printed, not asserted.

| gate | asserts | arrives |
|---|---|---|
| `unit` | the schema seams, ≥ 90 % coverage | scaffold |
| `catalog-schema` | every record parses, validates, and links only to records that exist, and a record directory holds nothing but records (`.gitkeep` aside) | scaffold |
| `notebook-structure` | every topic notebook has exactly the sections its sub-topic list requires, and the index lists every topic | milestone 6.2 |
| `notebook-outputs` | committed notebooks carry outputs and no errors | milestone 6.2 |
| `notebook-fresh` | re-executing a notebook reproduces its committed outputs (local; needs `data/` for figures) | milestone 6.2 |
| `figure-provenance` | every figure cell carries a `provenance(...)` whose ids resolve | milestone 6.2 |
| `lint` | `ruff check` and `ruff format --check` are clean over the repo's Python — `.py` files, notebook code cells, and Python fenced in Markdown — less what `pyproject.toml` excludes, which is `catalog` and the test fixtures | milestone 6.2 |
| `lock-consistency` / `lock-verify` | `data-lock.json` is well-formed; local `data/` matches it | milestone 6.5 |

## What is not a record

Analysis, notebook cells that compute anything beyond a printed equation, narrative changelogs,
correspondence, to-do notes, and anything about a source that the source does not itself say.
Analysis lives in a separate repo that reads this one.

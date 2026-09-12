# PRD — Regions and authorities (milestone 6.3)

Status: active
Created: 2026-09-12

## Problem

Milestone 6.2 closed with eleven notebooks and four sources. 6.3 could not be started as it stood:
there was no PRD, neither of its two issues carried a label, and the milestone was named "Regions,
beds, sites" while neither issue created a region, a bed or a site.

Planning it surfaced a larger problem. **`CONTEXT.md` names the wrong artifact as the authority for
kelp bed boundaries**, and three required fields of the `beds` schema cannot be filled from any
source that exists. Those facts are load-bearing: #18's whole purpose is to make `CONTEXT.md`
citable, and every bed record in the catalog's future carries them.

## What the checks found

Each of these is reproducible from a URL; none of it rests on a previous session's reasoning.

1. **The directory `CONTEXT.md` names holds canopy surveys, not boundaries.** `CONTEXT.md`'s region
   tree, level 4, says bed boundaries "are drawn by shapefiles under the directory
   `filelib.wildlife.ca.gov/Public/R7_MR/BIOLOGICAL/Kelp/`". That directory answered HTTP 200 on
   2026-09-12 with sixteen files, every one a dated canopy survey (`BIO_CA_Kelp1989` through
   `BIO_CA_Kelp2016`, plus `BIO_SCSR_Kelp2011` and `2012`). Their attribute tables carry `KelpBed`,
   `Shape_Leng` and `Shape_Area` — and `Class_Name` from 2016 — with no bed name, no status and no
   county. The 1989 layer holds 79 beds and the 2016 layer 78, and the two sets differ in both
   directions (union 85): a canopy survey maps only the beds that carried canopy that year, so **no
   roster of administrative beds can be read out of any of them**.

2. **The real authorities are a regulation and a different layer, and the canopy metadata names
   both.** `BIO_CA_Kelp1989.shp.xml` states: "File reindexed to match CDFW kelp administrative kelp
   bed boundaries modified by changes to California Code of Regulations, Title 14, Section 165,
   effective April 1, 2014", and that the dataset "was intersected with an updated kelp bed
   administrative layer" — a separate thing. That layer is **Administrative Kelp Beds - R7 - CDFW
   [ds3135]**: exactly 87 features, fields `KelpBed / Status / Lessee / TermEnds`, CC-BY, served
   from a FeatureServer and downloadable as shapefile, CSV, GeoJSON or file geodatabase. The
   boundaries themselves are drawn by **CCR Title 14 §165.5(k)**, which §165 cross-references and
   which prints, for each bed, its number, designation, area and boundary description with
   coordinates.

3. **Three required `beds` fields cannot be filled as specified.**
   - `name`* is specified "as in the shapefile". **Neither** shapefile has a name field, and the
     regulation names no bed — it labels them "Administrative kelp bed 8".
   - `status`* is specified as `Open · Closed · Leasable · Lease Only`. Three sources give three
     vocabularies and `CONTEXT.md` matches none of them exactly. ds3135: `OPEN` 33, `LEASABLE` 32,
     `CLOSED` 18, `LEASED` 1, `CLOSED (TEMPORARILY)` 3. CCR §165.5(k): `Open` 33, `Leasable` 31,
     `Leaseable` 2, `Closed` 18, `Lease only` 3. MBC's 2016 report: "closed, leasable, leased (from
     the state), or open". `Lease Only` occurs zero times in the regulation's text. The two
     `Leaseable` beds are **26 and 27 — both inside the Bight**, so the regulation's own
     inconsistent spelling is not a distant edge case.
   - `region`* is specified as "a county or island region id". It is stated for the 18 island beds
     and for **no mainland bed**. `kelp.sccwrp.org` states coverage as a span ("all coastal kelp
     beds from the Ventura River to the USA/Mexico Border"); the regulation states coordinates; the
     MBC report groups its *own* beds by county.

4. **The islands have an authority after all, and it is not the one that was being hunted.** The
   6.2 deep read of TR 1289 established that it cannot supply `defined_by` for any island node and
   cites no document that could, and named CDFW's bed shapefiles as a lead. Following that lead:
   **CCR §165.5(k) prints the island name on every island bed** — San Clemente 101–104, Santa
   Catalina 105, Santa Barbara 106, San Nicolas 107–108, Anacapa 109, Santa Cruz 110–112, Santa
   Rosa 113–116, San Miguel 117–118. All eight islands, named by a legal instrument with defined
   boundaries. But the regulation groups them as one flat "Channel Island administrative kelp beds"
   — **there is no northern/southern split in the authority**, so that level of `CONTEXT.md`'s
   promise still has none, and now has a cheaper alternative than finding one.

5. **The Bight subset is stated, not derived.** Bed 32 ends at Pt. Conception and bed 33 begins
   there. The catalog's northern bound is itself a bed boundary in the regulation, so the Bight
   holds **beds 1–32 (30 beds; 11 and 12 do not exist) plus the 18 island beds = 48**, not 87. The
   87 figure in `CONTEXT.md` is correct as a statewide count, and is confirmed by both ds3135 and
   the regulation.

6. **Program beds are a finer object than administrative beds, so `aliases` is false as defined.**
   `CONTEXT.md` says "Program bed names are `aliases:`". MBC's *Status of the Kelp Beds in 2016*
   states: "Most kelp beds recognized by the RNKSC and CRKSC are within California Department of
   Fish and Wildlife's (CDFW's) administrative kelp bed lease areas **that may include more than
   one giant kelp bed**", and "the CDFW recognizes just 10 administrative kelp bed lease areas. In
   this same area, MBC has identified 26 kelp beds". Twenty-six objects inside ten is not an
   aliasing relation.

7. **#38 is not sliceable as written.** Its "Done when" says `coverage_start` / `coverage_end` "come
   from the span each record's `coverage` already quotes". `calcofi` quotes three candidate spans,
   `sio_shore_stations` eight plus a collection-level range, and `noaa_oni` states seasons rather
   than dates. The Parking-lot entry that says so is correct, and the issue's own acceptance
   criterion begs the question it needs answered.

## Decisions

Taken in session, each against the evidence above rather than in the abstract.

1. **The island level is flattened.** Eight island nodes directly under `scb.islands`, each
   `defined_by` CCR §165.5(k) — the same authority that defines the beds they contain.
   `scb.islands.northern` and `scb.islands.southern` are struck. `CONTEXT.md` already says siblings
   it does not order sort by id, and `plan.py`'s `SIBLING_ORDER` already falls back to that, so the
   change is to delete one entry rather than to add a rule.

2. **A bed's county is derived, and recorded as a transcribed table.** A named script joins pinned
   ds3135 geometry against a pinned county boundary layer into `catalog/tables/`, with a
   `TRANSCRIBED` source record naming both inputs — the tier `CONTEXT.md` already defines as
   "extracted from a document by a named script". This is admitted by "The rule" on the same clause
   that already admits `calcofi`'s row counts and first/last data rows: deterministic, reproducible
   by anyone repeating the fetch, and neither a summary statistic nor a re-derivation of a published
   relationship.

3. **`beds.region` becomes a list.** Two beds' stated extents contain a county line — bed 8 ("the
   middle of the city of San Onofre to San Juan Creek", crossing San Mateo Point) and bed 17 ("Pt.
   Dume to Pt. Mugu", crossing County Line Beach). `consortium` is already a list for exactly this
   reason — "the boundary runs through Orange County" — and states what the source lists rather
   than resolving it. A straddling bed states both counties.

4. **CCR §165.5(k) is a bed's authority; ds3135 supplies geometry.** `defined_by` names the
   regulation and the subsection; `status` is the regulation's designation verbatim, including the
   printed `Leaseable` on beds 26 and 27 — which `BED_STATUS` in `schema.py` does not admit, so
   slice 10 changes that vocabulary in both `CONTEXT.md` and the code. ds3135 enters as its own
   source, cited by the derived region table. Each field traces to the source that states it.

5. **`defined_by` becomes `{source, where}`**, mirroring `transcribed_from`.
   `catalog/regions/scb.md` currently holds a ~300-character prose citation with a URL nothing
   checks, which is what #18 says no record should be.

6. **`beds.name` becomes `beds.extent`**, filled verbatim from CCR §165.5(k) — "Hope Ranch Creek to
   Goleta Pt.". A field called `name` holding an extent would make `beds.extent` and `sites.name`
   look like one concept when they are two. `CLAUDE.md` makes a rename its own slice; here it costs
   one schema line, twelve identical fixtures, one test helper and one `CONTEXT.md` row, because no
   bed record exists and `build.py` and `plan.py` never mention beds.

7. **`aliases` is dropped**, and "program bed as its own concept" is parked. No source checked
   states which administrative bed a program bed falls in.

8. **#38 is split and stays in 6.4.** Done in session: #38 keeps the cheap, independent fields
   (`citation`, `citation_stated_at`, `license_stated_at`, `version`) and is `ready-for-agent`; #89
   carries `coverage_start` / `coverage_end` and is `ready-for-human`, because it must first state a
   rule for choosing among quoted spans; #90 carries the 142-entry `variables` restructure. Nothing
   lands in 6.3 — 6.4 is the re-entry pass, and re-touching nine records instead of four costs
   little. #38's title no longer claims "before the first notebook"; notebooks shipped in 6.2.

### Two decisions this milestone still does not make

Both were flagged as due before #42 in the 6.2 PRD, and both stay parked — now with a reason rather
than an omission.

- **Where a context paper lives.** All five documents this milestone enters place cleanly as
  `sources/`, as TR 685 did before them. `references/` being empty is the design working, not a gap.
- **Whether references state findings.** Untouched; no reference record is created here.

## Solution

Land the corrections, the authorities, the region tree and every schema change **while there are
zero bed records and one region record**. Beds, the derived region table and sites follow in 6.3b.
This is #38's own argument applied to the `beds` schema: do the surgery when it costs one record,
not forty-eight.

## Slices

Numbers are issues on milestone 6.3. The rows are in work order. Dependencies run forward only:
`defined_by` cannot become a source reference until the source it names exists, and the region
records cannot be written until `defined_by`'s shape and the island level are settled.

| order | # | slice | seam | done when |
|---|---|---|---|---|
| 1 | [#77](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/77) | correct the bed-boundary facts | `CONTEXT.md` region tree level 4; the `beds` schema table | the directory claim names ds3135 and CCR §165.5(k); `Lease Only` and "as in the shapefile" are gone; no record changes |
| 2 | [#78](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/78) | add `ccr_t14_165_5` | `add-source` | the regulation is a source; its designations and island assignments are quoted as printed |
| 3 | [#79](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/79) | add `cdfw_ds3135` | `add-source` | 87 features, four attributes and the CC-BY terms are recorded; the FeatureServer route is exercised |
| 4 | [#80](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/80) | add `sccwrp_tr1289` | `add-source` | the Bight '18 survey area and Inner Shelf stratum are quoted; the locator is "Methods, Study Design", not "Introduction" |
| 5 | [#81](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/81) | add `cdfw_kelp_esr` | `add-source` | the 87-bed count and the depth range are quoted; the page is an SPA, so the route records how its text is reached |
| 6 | [#82](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/82) | add `sccwrp_kelp_aerial` | `add-source` | the consortium coverage sentences are quoted verbatim from the home page |
| 7 | [#83](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/83) | `defined_by` becomes `{source, where}` | `RULES` for `regions`/`beds`/`sites`; the schema tables; `catalog/regions/scb.md` | a `defined_by` naming no record fails; `scb.md` cites `sccwrp_tr1289` |
| 8 | [#84](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/84) | `beds.name` becomes `beds.extent` | `RULES["beds"]`; twelve fixtures; `a_bed()`; one `CONTEXT.md` row | a bed carrying `name` fails; one carrying `extent` validates |
| 9 | [#85](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/85) | drop `beds.aliases` | `RULES["beds"]`; the schema table; the fixtures | a bed carrying `aliases` fails as an unknown field |
| 10 | [#92](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/92) | the bed status vocabulary | `BED_STATUS` and `_vocab_problems` in `schema.py`; the `beds` schema row | a bed carrying `Lease Only` fails; one carrying `Leaseable` validates |
| 11 | [#16](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/16) | `beds.region` is a list of county or island nodes | the cross-record link pass in `schema.py` | a bed on `scb` or `scb.mainland` fails; one naming two counties validates; one naming an island validates |
| 12 | [#86](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/86) | flatten the island level | `CONTEXT.md` region tree and region order; `SIBLING_ORDER` in `plan.py` | the eight islands sort by id under `scb.islands`; `region_sort_key` stays total |
| 13 | [#87](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/87) | the mainland region nodes | `catalog/regions/` | `scb.mainland` and five counties, with the consortium lists `CONTEXT.md` already specifies |
| 14 | [#88](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/88) | the island region nodes | `catalog/regions/` | `scb.islands` and eight islands, each `defined_by` CCR §165.5(k) |
| 15 | [#18](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/18) | `CONTEXT.md` cites record ids | `CONTEXT.md`; #18 | every factual claim names a record that exists; verified by grepping the ids and checking each under `catalog/` |

Slice 1 is a correction of wrong facts and lands first so that nothing is built on them. Slices 2–6
are the five authorities, each its own `add-source` run. Slices 7–12 are the schema and ordering
changes, all of them cheapest now while no bed record exists. Slices 13–14 write the region tree.
Slice 15 closes #18.

**#16 is rewritten, not closed as filed.** As written it asserts a bed's `region` is a single county
or island node; slice 11 carries its intent with `region` as a list, and its non-goal — "not the
`surveyed_by` field, that is its own slice in this milestone" — moves to 6.3b with the beds.

## Non-goals

No bed records, no derived region table and no join script — 6.3b. No sites. No `surveyed_by`: it is
promised in `CONTEXT.md` prose and appears in neither the beds schema table nor `schema.py`, and no
source checked states it per bed, so it is a 6.3b decision with the beds it describes. No `sources`
schema change: #38 stays split across 6.4. No new topics or sub-topics. No gate that checks
`CONTEXT.md`'s citations resolve — #18 says explicitly that is a later slice, and this milestone
only makes it possible.

No northern/southern island grouping. If a source later needs it, it arrives with that source and an
authority that draws it; TR 685's use of the terms is an NMDS result, which "The rule" excludes.

## Done

`CONTEXT.md` states no fact about kelp beds that its own sources contradict, every factual claim in
it names a record, the region tree exists down to the counties and the eight islands, and the `beds`
schema is ready for records that do not exist yet.

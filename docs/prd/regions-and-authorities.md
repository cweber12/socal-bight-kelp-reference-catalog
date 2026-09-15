# PRD — Regions and authorities (milestone 6.3)

Status: active
Created: 2026-09-12
Revised: 2026-09-13, after an audit of the first draft reversed one of its findings and showed that
the decision it was proudest of could not be written against the schema it was proposing.
Revised: 2026-09-15, to record the freeze of 2026-09-14 in the Slices table it applies to, and the
split of #83 into a regions half (#104) and a frozen beds-and-sites half.

## Problem

Milestone 6.2 closed with eleven notebooks and four sources. 6.3 could not be started as it stood:
there was no PRD, neither of its two issues carried a label, and the milestone was named "Regions,
beds, sites" while neither issue created a region, a bed or a site.

The deeper problem is that **the catalog cannot answer a question about a place.** `regions/` holds
one record, `scb`, so every source must be tagged `scb` or `global` whatever it is actually about.
"What exists for San Diego?" has no expressible answer. The region tree is what makes retrieval by
place possible, and it is this milestone's real product.

Planning it also found that **`CONTEXT.md` names the wrong artifact as the authority for kelp bed
boundaries**, and that two of the `beds` schema's required fields cannot be filled from any source.

## What the checks found

Each is reproducible from a URL. Where the first draft of this PRD got one wrong, the correction is
stated in place rather than quietly removed.

1. **The directory `CONTEXT.md` names holds canopy surveys, not boundaries.** `CONTEXT.md`'s region
   tree, level 4, says bed boundaries "are drawn by shapefiles under the directory
   `filelib.wildlife.ca.gov/Public/R7_MR/BIOLOGICAL/Kelp/`". That directory answered HTTP 200 on
   2026-09-12 with sixteen files, every one a dated canopy survey. Their attribute tables carry
   `KelpBed`, `Shape_Leng`, `Shape_Area` — and `Class_Name` from 2016 — with no bed name, no status
   and no county. The 1989 layer holds 79 beds and the 2016 layer 78, and the sets differ in both
   directions (union 85): a canopy survey maps only the beds that carried canopy that year, so **no
   roster of administrative beds can be read out of any of them**.

   **The source confirms the correction.** The CDFW Enhanced Status Report, Monitoring §4.2.2: "The
   Department collected fishery-independent data on kelp canopy area … using aerial surveys in 1989,
   1999, and annually from 2002-2016 … **Shapefiles of these surveys** are available for download at
   filelib.wildlife.ca.gov - /Public/R7_MR/BIOLOGICAL/Kelp/". The directory is cited for *survey*
   shapefiles. `CONTEXT.md`'s "The boundaries are drawn by shapefiles under the directory … (per the
   same report, Monitoring section)" misreads that sentence.

2. **The boundaries are drawn by a regulation, and the ESR says so in one hop.** ESR Management
   §3.1: "Maps for all 87 Administrative Kelp Beds can be found at
   https://wildlife.ca.gov/Conservation/Marine/Kelp/Commercial-Harvest. The Beds are not based on
   individual kelp patches but rather geographic areas that are **delineated by latitude and
   longitude coordinates** and extend from the mean high tide to the state waters boundary line",
   with "(§165.5, Title 14, CCR)" two sentences earlier. **CCR Title 14 §165.5(k)** prints, for each
   of 87 beds, its number, designation, area and boundary description with coordinates.

   The GIS layer that carries those boundaries is **Administrative Kelp Beds - R7 - CDFW [ds3135]**:
   exactly 87 features, fields `KelpBed / Status / Lessee / TermEnds`, CC-BY. Note what the canopy
   metadata does and does not say: it names "Title 14 California Code of Regulations, **Section
   165.5**" precisely, but names the other layer only as "an updated kelp bed administrative layer"
   with an internal path `MarineGDB.gdb\MANAGEMENT\MAN_CA_KelpAdmin_ProposedChanges2013`. The string
   `ds3135` occurs **zero** times in it. Identifying that layer as ds3135 is an inference, and this
   PRD's first draft restated the inference as something the metadata said — the same defect it
   exists to correct. The ESR citation above replaces the inference chain.

3. **Two required `beds` fields cannot be filled as specified; a third was a false alarm.**
   - `name`* is specified "as in the shapefile". **Neither** shapefile has a name field, and the
     regulation names no bed — it labels them "Administrative kelp bed 8" and then states an extent.
   - `region`* is specified as "a county or island region id". It is stated for the 18 island beds
     and for **no mainland bed**. `kelp.sccwrp.org` states coverage as a span; the regulation states
     coordinates; the MBC report groups its *own* beds by county; and the ESR's county mentions are
     all in a restoration-projects table. No source states an administrative bed's county.
   - **`status`* is correct, and the first draft was wrong about it.** That draft said `Lease Only`
     "occurs zero times" and that `CONTEXT.md` "matches none of them exactly". Both are false,
     because it checked three sources and there is a fourth. The CDFW ESR, Management §3.1: "Beds
     are designated as Open (available to harvest by all and leases cannot be issued), Closed (…),
     Leasable (…), or **Lease Only** (Closed until leased)". Across ESR pages 0/3/4: `Lease Only`
     **9** occurrences, `Leaseable` **0**. That is exactly `CONTEXT.md`'s
     `Open · Closed · Leasable · Lease Only`, in the same order, transcribed from the source
     `CONTEXT.md` already cites for the 87 beds. **`CONTEXT.md` is right and nothing needs
     correcting.** What remains is a genuine question, below.

4. **Three authorities print three vocabularies for the same field.** ESR §3.1: `Open`, `Closed`,
   `Leasable`, `Lease Only`. CCR §165.5(k): `Open` 33, `Leasable` 31, `Leaseable` 2 (beds 26 and 27,
   both in the Bight), `Closed` 18, `Lease only` 3. ds3135: `OPEN` 33, `LEASABLE` 32, `CLOSED` 18,
   `LEASED` 1, `CLOSED (TEMPORARILY)` 3. They agree on what the designations *mean* and differ on
   how they spell them. Which one a bed record quotes is a decision, not a correction.

5. **The islands have an authority, and it is not the one that was being hunted.** The 6.2 deep read
   of TR 1289 established that it cannot supply `defined_by` for any island node and cites no
   document that could, and named CDFW's bed shapefiles as a lead. Following that lead: **CCR
   §165.5(k) prints the island name on every island bed** — San Clemente 101–104, Santa Catalina
   105, Santa Barbara 106, San Nicolas 107–108, Anacapa 109, Santa Cruz 110–112, Santa Rosa
   113–116, San Miguel 117–118. All eight islands, named by a legal instrument with defined
   boundaries. But the regulation groups them as one flat "Channel Island administrative kelp beds"
   — **there is no northern/southern split in the authority.**

6. **The Bight subset is stated, not derived.** Bed 32's stated extent ends at Pt. Conception and bed
   33's begins there, so the Bight holds **beds 1–32 (30 beds; 11 and 12 do not exist) plus the 18
   island beds = 48**, not 87. The 87 figure in `CONTEXT.md` is correct as a statewide count.

7. **Exactly two Bight beds straddle a county line, and that count is complete.** Bed 8 ("the middle
   of the city of San Onofre to San Juan Creek") contains the San Diego/Orange line at San Mateo
   Point; bed 17 ("Pt. Dume to Pt. Mugu") contains the Los Angeles/Ventura line at County Line
   Beach. The other two Bight county lines do not straddle: the Orange/Los Angeles line falls in the
   gap where beds 11 and 12 do not exist, and Rincon Pt. — the Ventura/Santa Barbara line — is
   exactly the break between beds 19 and 20.

8. **Program beds are a finer object than administrative beds, so `aliases` is false as defined.**
   `CONTEXT.md` says "Program bed names are `aliases:`". MBC's *Status of the Kelp Beds in 2016*:
   administrative beds "may include more than one giant kelp bed", and "the CDFW recognizes just 10
   administrative kelp bed lease areas. In this same area, MBC has identified 26 kelp beds".
   Twenty-six objects inside ten is not an aliasing relation.

9. **#38 is not sliceable as written.** Its "Done when" says `coverage_start` / `coverage_end` "come
   from the span each record's `coverage` already quotes". `calcofi` quotes three candidate spans,
   `sio_shore_stations` eight plus a collection-level range, and `noaa_oni` states seasons rather
   than dates. The Parking-lot entry that says so is correct.

## Decisions

### 1. The island level is flattened

Eight island nodes directly under `scb.islands`, each `defined_by` CCR §165.5(k).
`scb.islands.northern` and `scb.islands.southern` are struck. `CONTEXT.md` already says siblings it
does not order sort by id, and `plan.py`'s `SIBLING_ORDER` already falls back to that, so the change
is to delete one entry rather than to add a rule. Removing a *listed* sibling set also moves the
tree away from the undefined third case parked on #5 (a set listed *in part*), not toward it.

### 2. "The rule" excludes analysis, not all computation — and the derived index says so out loud

A bed's county is derived, by a named script joining pinned ds3135 geometry against a pinned county
boundary layer. **The first draft justified this by analogy to `calcofi`'s row counts, and that
analogy does not hold**: a row count is a property of one fetched file, while a join states what
neither input states, and its answer depends on a predicate, a CRS and a tolerance chosen here. The
audit was right to reject it on those grounds.

It is admitted anyway, for a reason the first draft did not give and the audit could not know. **"The
rule" was written against analysis** — fits, trends, summary statistics, interpretations — and a
bed→county mapping is none of those. It is *retrieval machinery*: it asserts nothing about kelp, it
says where to look. The 6.2 PRD already drew exactly this line for the planned on-demand notebook
generator: **"the session chooses the filter; the builder produces the content."** A join key is
filter, not content.

So the permission is made explicit rather than smuggled through an analogy:

- **"The rule" is amended** to say it excludes analysis — anything that states a finding — rather
  than all computation, and that a deterministic index over pinned catalogued inputs is admitted.
- **A `DERIVED` tier is added**, defined as: computed here, from pinned catalogued inputs, by a
  committed script, recording predicate, CRS and tolerance; **never a finding, only a join key.**
  `TRANSCRIBED` is *not* stretched to cover it — that tier means "extracted from a document by a
  named script", one document, and its `transcribed_from` requires a `references/` record, which
  would not resolve. Note the knock-on: `CONTEXT.md`'s "Record format" says a CSV under
  `catalog/tables/` "has a source record with tier TRANSCRIBED", and **#17 gates exactly that**, so
  both are amended to admit any tier that writes a file there. The rule is about provenance, not
  about which tier supplies it. Stretching it would also admit per-bed canopy area summed from `Shape_Area`,
  which is a summary statistic the rule excludes by name.

The 18 island beds take their region from §165.5(k), **stated**. Only the 30 mainland beds are
derived.

### 3. `beds.region` is a list

Two Bight beds' stated extents contain a county line (finding 7), and that count is complete.
`consortium` is already a list for exactly this reason — "the boundary runs through Orange County" —
and states what the source lists rather than resolving it.

### 4. CCR §165.5(k) is a bed's authority; ds3135 supplies geometry

`defined_by` names the regulation and the subsection. ds3135 enters as its own source, cited by the
derived region table. Each field traces to the source that states it.

### 5. `status` quotes one authority, and the slice says which

Finding 4 leaves a real choice, and it is a choice rather than a fix because `CONTEXT.md`'s current
four values are a correct transcription of the ESR. Decision 4 makes the regulation a bed's
authority, which argues for the regulation's spellings; the ESR argues for leaving the vocabulary
untouched. #92 carries it, with both readings written out and the schema and `CONTEXT.md` landing
together.

### 6. `defined_by` becomes `{source, where}`

Mirroring `transcribed_from`. `catalog/regions/scb.md` currently holds a ~300-character prose
citation with a URL nothing checks, which is what #18 says no record should be.

### 7. `beds.name` becomes `beds.extent`

Filled verbatim from CCR §165.5(k) — "Hope Ranch Creek to Goleta Pt.". A field called `name` holding
an extent would make `beds.extent` and `sites.name` look like one concept when they are two.
`CLAUDE.md` makes a rename its own slice; here it costs one schema line, eleven identical fixtures
plus `invalid_bed`, one test helper and one `CONTEXT.md` row, because no bed record exists and
`build.py` and `plan.py` never mention beds. **The field's definition must admit two forms**: beds
105 and 106 print no "This bed extends from X to Y" but "This area is bounded by the mean high tide
line and the three nautical mile offshore boundary surrounding Santa Catalina Island."

### 8. `aliases` is dropped

And "program bed as its own concept" is parked. No source checked states which administrative bed a
program bed falls in.

### 9. Every beds-field correction lands `CONTEXT.md` and code together

The first draft put all five `CONTEXT.md` bed corrections in one docs-only slice ahead of the code
slices. That opens a window on protected `main` where `CONTEXT.md` and `schema.py` disagree — a
state `CONTEXT.md` itself defines as "the code is a bug" — and **no gate sees it**, because no test
reads `CONTEXT.md`. So slice 1 narrows to the one correction that touches no field (the boundary
authority), and each field's slice carries its own `CONTEXT.md` row.

### 10. #38 is split and stays in 6.4

Issue #38 keeps the cheap, independent fields and is `ready-for-agent`; #89 carries `coverage_start` /
`coverage_end` and is `ready-for-human`, because it must first state a rule for choosing among quoted
spans; #90 carries the `variables` restructure (155 entries live, not the 142 the first draft
quoted). `retrieved` on beds and sites was the sixth parked item and fell through that split — it is
picked up here, where it costs zero records.

### Two decisions this milestone still does not make

- **Where a context paper lives.** All five documents this milestone enters place cleanly as
  `sources/`. `references/` being empty is the design working, not a gap.
- **Whether references state findings.** Untouched; no reference record is created here.

## Solution

Land the corrections, the authorities, the region tree and every schema change **while there are
zero bed records and one region record**. Beds, the derived region table and sites follow in 6.3b,
which is scheduled rather than assumed.

## Slices

Numbers are issues on milestone 6.3. The rows are in work order. **Forward dependencies exist and
are named per row**; where an issue can land ahead of what it points at, its own "Depends on" says
so.

**Freeze, 2026-09-14.** Slices 7–14 were moved from `ready-for-agent` to `needs-triage` after the
audits of this PRD's first draft showed that its external facts held and its decisions did not.
Slices 9–13 are frozen on the bed vocabulary: "bed" is at least four objects — the administrative
kelp bed of §165.5(k), one survey year's canopy, a continuous kelp forest, and a program bed such as
"Point Loma" — and the plan is to enter the five authorities first and write the vocabulary from what
they state. **The exit trigger is on #84**: after #81 merges, one session reads what the five records
state about spatial units and rewrites slices 9–13 against that before any is labelled ready again.
Slices 7, 8 and 14 are not frozen on the vocabulary; they wait on order, since nothing needs them
before #107 and the bed records exist. Decision 2 was reaffirmed by the owner on 2026-09-15: the
bed-to-county key is retrieval machinery held here so that a session generating a county-scoped
notebook filters through a pinned, gated record rather than computing the join itself. Slice 6a is
the region half of #83, split out the same day because it does not depend on what a bed is and
because slices 16–17 would otherwise write fifteen records into a field slice 9 later rewrites.

| order | # | slice | seam | done when |
|---|---|---|---|---|
| 1 | [#77](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/77) | correct the bed-boundary authority | `CONTEXT.md` region tree level 4 only | the directory is described as canopy surveys; §165.5(k) and ds3135 are named; no schema field changes |
| 2 | [#78](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/78) | add `ccr_t14_165_5` | `add-source` | designations and island assignments quoted unclipped |
| 3 | [#79](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/79) | add `cdfw_ds3135` | `add-source` | 87 features, four attributes, CC-BY terms; FeatureServer route exercised |
| 4 | [#80](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/80) | add `sccwrp_tr1289` | `add-source` | survey area and Inner Shelf stratum quoted |
| 5 | [#81](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/81) | add `cdfw_kelp_esr` | `add-source` | the JSON API route reaches the report text; the TLS caveat is recorded |
| 6 | [#82](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/82) | add `sccwrp_kelp_aerial` | `add-source` | consortium coverage sentences verbatim |
| 6a | [#104](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/104) | `regions.defined_by` becomes `{source, where}` | `RULES["regions"]`; the link pass; the `regions` row; `catalog/regions/scb.md` | a bare-string `defined_by` on a region fails; `scb.md` cites `sccwrp_tr1289`; a bed's bare string still validates |
| 7 | [#93](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/93) | "The rule" excludes analysis, not computation | `CONTEXT.md`, "The rule" and its table | the admitted column names a deterministic index; the excluded column still names findings |
| 8 | [#94](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/94) | a `DERIVED` tier | `TIER` and `_tier_problems` in `schema.py`; **five** `CONTEXT.md` lines, including the `tables/` provenance rule | a `DERIVED` record without a script is a problem; `transcribed_from` is not required of it; #17 admits the tier |
| 9 | [#83](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/83) | `defined_by` becomes `{source, where}` on beds and sites (regions: slice 6a); *frozen* | `RULES` for `beds`/`sites`; the twelve bed fixtures | a bare-string `defined_by` on a bed or site fails; the PR says whether a bed's authority is the regulation, a layer, or both |
| 10 | [#84](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/84) | `beds.name` becomes `beds.extent` | `RULES["beds"]`; fixtures; `a_bed()`; the `beds` row | a bed carrying `name` fails; beds 105/106's form validates |
| 11 | [#85](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/85) | drop `beds.aliases` | `RULES["beds"]`; the `beds` row; eleven fixtures | a bed carrying `aliases` fails as unknown |
| 12 | [#92](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/92) | which authority `status` quotes | `BED_STATUS`; `_vocab_problems`; the `beds` row | the chosen vocabulary is in both files, and the PR says which and why |
| 13 | [#16](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/16) | `beds.region` is a list | the cross-record link pass; the `beds` row | `[scb.mainland]` fails; two counties validate; an island validates |
| 14 | [#95](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/95) | `retrieved` on beds and sites | `RULES["beds"]`, `RULES["sites"]`; two schema rows | `retrieved` follows the same `date?` rule it follows on a source |
| 15 | [#86](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/86) | flatten the island level | `SIBLING_ORDER`; the tree *and* the region-order paragraph; `region_sort_key`'s docstring | the eight sort by id; **no test or fixture names `scb.islands.northern` or `.southern`** |
| 16 | [#87](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/87) | the mainland region nodes | `catalog/regions/` | `scb.mainland` and five counties with their consortium lists |
| 16a | [#106](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/106) | re-enter `ccr_t14_165_5` as `FETCHED` | `add-source`, update path; `src/fetch/ccr_t14_165_5.py`; two notebooks | `status: VERIFIED`, `tier: FETCHED`, manifest held; the authority nine region records cite is held before they cite it |
| 17 | [#88](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/88) | the island region nodes | `catalog/regions/` | `scb.islands` and eight islands, each citing §165.5(k) |
| 18 | [#18](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/18) | `CONTEXT.md` cites record ids | `CONTEXT.md` | every factual claim names a record that exists |

Slice 1 corrects the one wrong fact that touches no field. Slices 2–6 are the five authorities, and
6a gives the region records the field shape they are written in. Slices 7–8 make the derived index
legitimate before anything relies on it. Slices 9–14 are the schema, each landing `CONTEXT.md` and
code together. Slices 15–17 build the region tree, with 16a holding the islands' authority before
slice 17 cites it. Slice 18
closes #18.

**#16 is rewritten, not closed as filed.** As written it asserted a bed's `region` is a *single*
county or island node; slice 13 carries its intent with `region` as a list. Its non-goal — "not the
`surveyed_by` field, that is its own slice in this milestone" — moves to 6.3b with the beds.

## Milestone 6.3b

Scheduled here so decision 2 is carried by a slice rather than by an intention, which is what the
audit found it was. Filed 2026-09-13:

| # | slice |
|---|---|
| [#107](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/107) | the California county boundary layer #96 joins against, as its own source — filed 2026-09-15; the layer must state its offshore extent, since ds3135's polygons run to the state-waters line |
| [#96](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/96) | the derived bed-region table and its join script — **blocked on #93, #94 and #107** |
| [#97](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/97) | the 18 island bed records — needs no join; §165.5(k) states the island |
| [#98](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/98) | the 30 mainland bed records — depends on #96 |
| [#99](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/99) | `surveyed_by`, `ready-for-human`: no source states it per bed |

Sites follow once a program's own documents are entered.

## Non-goals

No bed records, no derived region table and no join script — 6.3b, and filed there. No sites. No
`surveyed_by`. No `sources` schema change: #38 stays split across 6.4. No new topics or sub-topics.
No gate that checks `CONTEXT.md`'s citations resolve — #18 says that is a later slice.

No northern/southern island grouping. If a source later needs it, it arrives with that source and an
authority that draws it; TR 685's use of the terms is an NMDS result, which "The rule" excludes.

## Done

`CONTEXT.md` states no fact about kelp beds that its own sources contradict, every factual claim in
it names a record, the region tree exists down to the counties and the eight islands, and the `beds`
schema is ready for records that do not exist yet.

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
`VERIFIED` (the route was exercised, and `access` states what was received and when) · `PATTERN`
(route documented but not exercised) · `NOT PUBLIC` · `ON REQUEST`.

A route is exercised three ways. Its bytes were taken. Or a printed page was in hand and its values
typed, per `transcribed_from`. Or — only where the entity is disproportionate to hold, so that the
record keeps nothing and says so with the entity's size — enough of the entity itself answered to
show that it opens: `sbc_lter_landsat_canopy` records its first 64 bytes arriving beside its byte
count, its checksum and its access policy. The third way is the exception: an entity a record could
hold is fetched, not probed. A landing page answering is not the source answering, and a document
describing the source is not the source.

Status and tier are independent, with one exception. Holding content means the route was
exercised, so `FETCHED` and `TRANSCRIBED` exclude `PATTERN` — but they do not compel `VERIFIED`,
because `NOT PUBLIC` and `ON REQUEST` state what a stranger faces whatever is held here. Holding
nothing excludes nothing, because a route can be exercised without its bytes being kept, so a
`NOT HELD` record carries whichever of the four its own `access` steps support; `PATTERN` there
means nobody here has tried the route, not that nothing was kept.

**tier** — how the local content, if any, came to exist.
`FETCHED` (bytes retrieved unmodified from one of the three routes below) · `TRANSCRIBED` (values
typed from a printed page, or extracted from a document by a named script, into `catalog/tables/`)
· `NOT HELD` (nothing local; the record describes the source and how to ask).

`FETCHED`'s route is one of three, and nothing else. A host the steward runs, or that a body
constituting it runs: `calcofi`'s bytes come from an ERDDAP on "a host of the NOAA Southwest
Fisheries Science Center", which the steward's own data usage policy lists among its participating
agencies. A route the steward names as where the source is to be had: `sio_shore_stations`' Data
Access page names the UC San Diego Library Digital Collections, and `ccr_t14_165_5`'s steward links
the Barclays Official California Code of Regulations as the route to the text. Or a service that
serves that same object under the identifier one of those two issued it, a replica or a proxy
included: `sbc_lter_landsat_canopy` records DataONE serving the PASTA object under its PASTA
identifier, with a `DataONE-Proxy` header naming it — that record holds nothing, so the limb is
stated from a route it documents rather than from bytes it keeps. Anyone else's copy of the same
content is not a route, however faithful.

Subsetting is a question about a single file, and only about a single file. Which of the files a
publisher offers a record holds is not subsetting at all, and needs no licence here: a record holds
what its `coverage` and `access` say it holds, and says which of the offered files those are
(`sio_shore_stations` holds five of ten station objects, `sccwrp_kelp_status_2016` the report and
not its appendices, `sccwrp_kelp_aerial` two pages and not the PDFs behind them).

Within one file, a subset is `FETCHED` when the publisher's own service selected it by the data's
own variables and served the result whole, so that what is held is every byte of what that service
returned: `calcofi` asks ERDDAP for one station by `sta_id`. A slice of a file's bytes is not,
whoever asked for it — a Range request is transport rather than a query, and what it yields is a
fragment of a file rather than a file. Nor is a subset this repo computed from a file it fetched.

**topics** — see *Topics: the ten questions* below. A tag is `<topic>` or `<topic>/<sub-topic>`.

**regions** — the tree below. A source tags each node its stated coverage names as its own extent,
not each place it mentions: a source about an island tags the island node, not the county; a source
stating county-wide coverage that includes islands tags the county and the islands it names, a
county's islands belonging to the island nodes by convention (level 3 below); a source stating
Bight-wide coverage tags `scb` and not the islands or counties inside it that its coverage names
(`sccwrp_tr1289`); a source whose stated bound is wider than the Bight, statewide, nationwide or a
species range alike, tags the nodes inside the Bight it names as its own extent, and `scb`
otherwise, a node named only as a part, group or row of that wider extent being a mention (the bed
groups of `ccr_t14_165_5`, the county rows of `census_tiger_county_2025`); and a source within the
Bight whose stated coverage names no node (a station list, a coordinate box) tags the smallest node
that contains it. A source carrying two or more region tags renders under each of them in a topic
notebook's sources tables, and each matrix counts it once per region it carries: in the index matrix
a column per region, in a topic's matrix a row per region (`build.py`, `_sources_by_region`,
`_matrix`, `_index_matrix`). `global` is allowed without a record for sources with no regional bound
(ONI). `global` is therefore not a node of the tree, and not a region wider than the Bight: it
states the *absence* of a bound, not a bound that happens to be large. It is also the one region tag
with no record, so it has no `name` to print; *Notebooks* below gives the heading a notebook prints
instead, and where in the order it falls.

## Topics: the ten questions

Three groups, ten topics, each topic a question. The three groups follow how the drivers are
sorted in NOAA Office of National Marine Sanctuaries, "Kelp forest impacts"
(sanctuaries.noaa.gov/visit/ecosystems/kelpimpacts.html); California Research Bureau, "Kelp
forests" brief, 2 April 2026 (library.ca.gov/crb/nexus/briefs/kelp-forests/); and the Bight '08
Rocky Reef landing page, the first access step of `sccwrp_b08_rocky_reef`, which gives the route
to the page and does not state the sorting; all three retrieved 2026-09-07. The questions are
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

Every region record's `defined_by` (levels 1-3, `regions/<id>.md`) is `{source, where}`: the
`sources/` record that draws the boundary and a locator within it (a section, a subsection, a
page, or for a data file an attribute value). Beds and sites (levels 4 and 5) carry the string
their own rows describe. Levels:

1. `scb` — the Southern California Bight, taken as the Bight '18 survey area, "from Point
   Conception, CA in the north to the US-Mexico border in the south" (`sccwrp_tr1289`, Chapter II,
   Methods, Study Design, printed page 3 (PDF page 20)).
2. `scb.mainland` and `scb.islands` — CCR Title 14 §165.5(k) lists its beds in four groups, and
   `ccr_t14_165_5` quotes all four headings; the two that reach the Bight define these nodes.
   `scb.mainland` is defined at "(1) Mainland administrative kelp beds U.S./Mexico Border to Pt.
   Arguello (Total 19.07 square miles)" and `scb.islands` at "(2) Channel Island administrative
   kelp beds (Total 20.68 square miles)". Group (1) runs north of level 1's Point Conception
   bound to Pt. Arguello: it adds bed 33, which "extends from Pt. Conception to Espada Bluff"
   (subsection (k)(1), paragraph (EE)), and bed 34, which "extends from Espada Bluff to Pt.
   Arguello" (paragraph (FF)). This file keeps the Point Conception bound and records the
   difference rather than resolving it; #96 scopes the mainland beds to 1–32 on that reading.
   Every mainland program states coverage by county.
3. Mainland counties: `scb.mainland.santa-barbara`, `.ventura`, `.los-angeles`, `.orange`,
   `.san-diego` (the Region Nine and Central Region Kelp Survey Consortia's coverage as
   `sccwrp_kelp_status_2016` states it: "Giant kelp beds have been mapped quarterly off Ventura, Los
   Angeles, Orange, and San Diego counties for both the Central Region (CRKSC) and Region Nine Kelp
   Survey Consortiums (RNKSC).", Executive Summary, printed page i (PDF page 8); the first
   consortium paragraph below gives the extents by county). A mainland county node's `defined_by` is
   `census_tiger_county_2025` at the county's `GEOID` in that file's attribute table, the county's
   geometry as the file draws it: Santa Barbara 06083, Ventura 06111, Los Angeles 06037, Orange
   06059 and San Diego 06073, as the record's `coverage` states them from the held `.dbf`; Santa
   Barbara County has the same form as the other four. The catalog assigns a county's islands and
   the water around them to the island nodes, by convention and drawing no line. Islands: eight
   nodes directly under `scb.islands` — `.anacapa`, `.san-clemente`, `.san-miguel`, `.san-nicolas`,
   `.santa-barbara`, `.santa-catalina`, `.santa-cruz`, `.santa-rosa`. There is no group level
   between them and `scb.islands`: CCR Title 14 §165.5(k)(2) names all eight, printing the island on
   every island bed (each island record's `defined_by.where` states the beds and the printed name),
   and gathers them under one heading, "Channel Island administrative kelp beds (Total 20.68 square
   miles)" (`ccr_t14_165_5`, subsection (k)(2)). A finer grouping arrives with the source that draws
   it. Note `scb.islands.santa-barbara` (the island) and `scb.mainland.santa-barbara` (the county)
   are distinct nodes; their ids differ by branch.
4. **Beds**, keyed by CDFW Administrative Kelp Bed number (87 statewide including the Channel
   Islands, as `cdfw_kelp_esr` states it: "87 officially delineated Administrative Kelp Beds that
   span the entire California coastline including the Channel Islands", section "0.15."
   Management, page 0 (Species-at-a-Glance)). The beds are defined by **CCR Title 14 §165.5(k)**,
   in its own words: "Administrative kelp beds are defined as follows: kelp bed number,
   designation, area …, and boundary descriptions", and "All geographic coordinates listed use the
   North American Datum 1983 (NAD83)" (`ccr_t14_165_5`, subsection (k)). The ESR corroborates that
   the coordinates live in the regulation: the 2014 amendments "updated the Administrative Kelp
   Bed boundaries from compass headings to latitude and longitude coordinates" (`cdfw_kelp_esr`,
   section "3.1.1.2." Past and Current Stakeholder Involvement, page 3 (Management)). The
   shapefiles under `filelib.wildlife.ca.gov/Public/R7_MR/BIOLOGICAL/Kelp/` are the Department's
   **canopy surveys** — its Monitoring section offers them as "Shapefiles of these surveys", the
   aerial surveys of 1989, 1999 and annually 2002–2016 (`cdfw_kelp_esr`, section "4.2.2."
   Fishery-independent Data Collection, page 4 (Monitoring and Essential Fishery Information)).
   Program bed names are `aliases:`.
5. **Sites**, a program's named station, with lat/lon from the program and the bed it falls in.

Consortium is an attribute on a county node, not a level, and it is a **list**. The authority is
`sccwrp_kelp_status_2016`, the 2016 "Status of the Kelp Beds" report, which states each
consortium's extent by county and by landmark: "The CRKSC program area extends from Ventura Harbor
(also referred to as Ventura Marina) in Ventura County south to Abalone Point in northern Laguna
Beach in Orange County" (Introduction, Description of the Central Region Kelp Beds, printed page 4
(PDF page 17)), and "In the Region Nine kelp survey area, between Abalone Point in Laguna Beach
(Orange County) and the U.S./Mexico Border to the south" (Introduction, Description of the Region
Nine Kelp Beds, printed page 7 (PDF page 20)); Los Angeles County, which lies between those
landmarks, it names in "the Central Region (off north and central Los Angeles County, beds from
Sunset Malibu, and off Orange County)" (Results, Status of the 50 Kelp Beds along the Central
Region and Region Nine through 2016, Central Region Kelp Surveys, printed page 32 (PDF page 45)).
So Ventura and Los Angeles state `[CRKSC]`, San Diego states `[RNKSC]`, and the boundary runs
through Orange County, which states both (`consortium: [RNKSC, CRKSC]`). Santa Barbara County is
named by neither the report, whose Executive Summary maps "off Ventura, Los Angeles, Orange, and
San Diego counties" (Executive Summary, printed page i (PDF page 8)), nor the kelp.sccwrp.org home
page (`sccwrp_kelp_aerial`), so it states `consortium: []`; the field states what the report names,
not a claim about the county. Every locator into the report gives section, printed page and PDF
page, as the citations in this file do, because the report's printed page labels differ from its
PDF page numbers and the labels iii, iv and v each appear twice.

Where the report and the home page differ, this file adopts the report and records the difference
rather than resolving it. The report's northern end is "Ventura Harbor" (Introduction, Description
of the Central Region Kelp Beds, printed page 4 (PDF page 17)) where the home page has "all coastal
kelp beds from the Ventura River to the USA/Mexico Border". The report says "The CRKSC was formed
in 2003" and "the long-established RNKSC that formed in 1983" (Executive Summary, printed page i
(PDF page 8)) where the home page says "The program began about 30 years
ago (1982-1983) when the Region Nine Kelp Survey Consortium (RNKSC) was formed" and "The extent of
these surveys was extended to northern Orange County, Los Angeles County and Ventura County in
2002 when the Central Region Kelp Survey Consortium (CRKSC) was formed". The home page attaches
counties to RNKSC through the regulations it was "formed to address", "for San Diego and southern
Orange Counties", and to CRKSC through "when"; it does not state which counties either consortium
covers, and this file no longer cites it for that. Within the report, the Introduction says "The
CRKSC covers kelp beds from Ventura Harbor to Newport Beach (Figure 1), and the RNKSC covers
Newport Beach to the Baja California border (Figure 2). The upcoast extent of the RNKSC is Abalone
Point (Laguna Beach)." (Introduction, printed page 1 (PDF page 14)), and the Results explain: "the
boundary between the Central Region and Region Nine is Abalone Point in Laguna Beach. However, the
Region Nine surveys have historically included the beds from Newport Harbor to Abalone Point
(described above)." (Results, Status of the 50 Kelp Beds along the Central Region and Region Nine
through 2016, Region Nine Kelp Surveys, printed page 46 (PDF page 59)). Abalone Point is "in Orange
County" (Introduction, Description of the Central Region Kelp Beds, printed page 4 (PDF page 17)),
and the Region Nine beds whose values Figure 20 presents are "(beds offshore Orange County, and
offshore San Diego County, minus Point Loma and La Jolla)" (Results, Region Nine Kelp Surveys,
printed page 46 (PDF page 59)), so the county lists above are the same under either landmark.

A county node says which consortia the county falls under and nothing finer: which consortium
surveys a given **bed** is a bed field, `surveyed_by`, arriving in milestone 6.3b (#99).

Depth is not a level of the tree. A source's depth range is part of its `coverage`, as the source
states it. For orientation: CDFW gives giant kelp habitat as "the low intertidal to depths of 25
meters … with maximum depths of 30 meters" (`cdfw_kelp_esr`, section "0.3." Habitat, page 0
(Species-at-a-Glance)), which sits within Bight '18's Inner Shelf stratum, 7–30 m
(`sccwrp_tr1289`, Table 1, printed page 4 (PDF page 21)).

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
(`{source, where}`: a source id that exists, and where in that source the boundary is drawn — a
section, a subsection, a page, or for a data file an attribute value), `consortium` (list of
`RNKSC` / `CRKSC`, non-empty only when `parent` is `scb.mainland`; `[]` where neither consortium
covers the county).

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
tree above is numbered by level, so the traversal, not that numbering, fixes the order: Bight-wide
(`scb`) first; then `scb.mainland` and its counties north to south — `santa-barbara`, `ventura`,
`los-angeles`, `orange`, `san-diego`; then `scb.islands` and its eight islands; and `global` last.
Siblings this file names but does not order — the islands — sort by id, so the order is total
over every value a `regions` field can hold: every region id the tree has or gains, down to the
islands under `scb.islands`, and `global`. Beds and sites are levels 4 and 5 of the
tree but are not region ids — a source carries them in `beds` and `sites` — so this order does not
reach them. The order is a property of the region id alone, because it must hold for the county
and island nodes before their records exist in 6.3. A group's heading is its node's `name`;
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

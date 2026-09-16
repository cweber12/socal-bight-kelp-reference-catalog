# PRD — Monitoring sources (milestone 6.3c)

Status: queued; opens when milestone 6.3's Slices table has no open `ready-for-agent` row
Created: 2026-09-15

## Problem

The catalog holds seven sources, and three of them are authorities for the region tree rather than
observations of kelp. Three of the ten topic questions have no source at all —
`canyon-dynamics`, `recruitment-connectivity` and `restoration-mitigation` — and four more
(`canopy`, `bed-state`, `substrate`, `grazers-predators-competitors`) hold exactly one, the 2008
Bight regional survey report. A researcher opening `21_canopy` finds that one snapshot and nothing
that runs to today.

A candidate manifest of 22 items, prepared outside the repo on 2026-09-15 by an agent that had read
`README.md` and `CONTEXT.md` and nothing else, was reviewed against the catalog and the tracker in
the same session. Twenty of the 22 are papers. The papers are the route to the datasets; the
datasets are the records. This milestone enters those datasets. The manifest itself is not
committed: `CLAUDE.md` forbids a parser for any external manifest, and records are entered, not
migrated.

## What the review settled

Each is a reading of an existing rule, applied to the manifest's proposals, and stated here so a
slice does not re-derive it.

1. **Driver data is admitted.** `CONTEXT.md` admits "an authoritative source about kelp in the
   Bight", and four of its ten questions are about the environment the beds are exposed to. Three of
   the seven records held on 2026-09-15 — `noaa_oni`, `calcofi`, `sio_shore_stations` — observe no
   kelp. The practice is that a source answering one of the ten questions is in scope. The manifest
   asked for that to be written into the admission sentence; that is a Parking-lot line, not a gate
   on this milestone.
2. **A public dataset enters as `FETCHED` on first entry.** The manifest proposed every candidate as
   `PATTERN / NOT HELD` "now" with an upgrade later. `add-source` step 2 says a route that downloads
   today is `VERIFIED / FETCHED`, and #106 exists because one record went in as a placeholder.
   No slice here creates a placeholder.
3. **Papers are leads, not records.** `CONTEXT.md` defines `references/` as "a paper or report cited
   by a source or a figure", and where a context paper lives is parked (Parking lot, 2026-09-09).
   The manifest's fifteen proposed reference records are not filed. The one exception a field
   needs — `transcribed_from.reference` for a transcribed table — arrives with that table's slice.
4. **Region tags are `scb` until the nodes exist.** The link check fails on a region with no record.
   #87 and #88 create the counties and islands; a slice here that lands before them tags `scb` and
   says in its PR which node it would tag, so the re-tag is a lookup and not a re-read. Two sources
   state a bound wider than the Bight (the Landsat canopy series and PISCO); how they tag is #105,
   and a slice that reaches it before #105 is decided stops and says so.
5. **A source that fits no sub-topic waits for the sub-topic, in its own PR.** `CONTEXT.md`: "never
   exclude the source for want of a tag". Three sub-topics the manifest could not place are Parking-
   lot lines: circulation (HF radar, inner-shelf currents), carbonate chemistry (DIC, alkalinity,
   isotopes) and productivity (chlorophyll). The rows that need them are `needs-triage` until the
   row exists in `CONTEXT.md` and `schema.py`.
6. **Records are named by steward, not by host.** Dryad, EDI and BCO-DMO are repositories. The
   catalog's ids name the steward (`noaa_oni`, `cdfw_ds3135`), with underscores. What "the
   steward's host" admits when the bytes come from a repository is the parked CalCOFI question
   (Parking lot, 2026-09-09) and is answered per record in its `access` steps, as `calcofi` does.
7. **`ON REQUEST` records wait on an H-id registry.** `human_task: H<n>` has no registry in the
   repo (Parking lot, 2026-09-08). The three study-data candidates are not filed.
8. **Two items are exclusions; three are not.** A taxonomic review and a California Current study
   were reviewed and are not admitted, and get `excluded/` records with one-line reasons. A redirect
   URL and two superseded preprints are the same items as their canonical versions and are not
   records of any kind.

## Solution

One record per dataset, entered through `add-source`, `FETCHED`, in an order that fills the empty
questions first and lets each program's later datasets copy the fetch shape of its first. Programs
that expose several datasets get one record per dataset with its own route, as `sio_shore_stations`
holds five files under one record only because one DOI covers them.

## Slices

Issues are filed on milestone `6.3c Monitoring sources` after this PRD merges, and their numbers
are added to this table then. The rows are in work order. Every row is a record issue in the shape
`docs/agents/issue-tracker.md` gives them: `add-source` is the seam, there is no mechanical failing
test, and the notebooks the record's topics move land in the same PR.

| order | # | source | steward | topics | region today | note |
|---|---|---|---|---|---|---|
| 1 | — | Channel Islands National Park Kelp Forest Monitoring | National Park Service | `bed-state/diver-surveys`, `bed-state/community`, `grazers-predators-competitors/urchins` | `scb` (islands after #88) | the longest-running diver survey in the Bight; find the program's own data endpoint, not a paper's subset |
| 2 | — | SBC LTER Landsat kelp canopy, quarterly since 1984 | Santa Barbara Coastal LTER | `canopy/satellite`, `canopy/persistence` | #105 decides | statewide NetCDF; state coverage as the package states it |
| 3 | — | SBC LTER reef bottom temperature | Santa Barbara Coastal LTER | `ocean-climate/temperature`, `ocean-climate/heatwaves` | `scb` (Santa Barbara after #87) | one record per EDI package, the current version; the version a paper used is that paper's business |
| 4 | — | SBC LTER annual kelp forest biomass | Santa Barbara Coastal LTER | `bed-state/diver-surveys`, `bed-state/community` | `scb` (Santa Barbara after #87) | |
| 5 | — | SBC LTER kelp removal: sessile cover | Santa Barbara Coastal LTER | `bed-state/community` | `scb` (Santa Barbara after #87) | an experiment's monitoring; say so in `coverage` as the package states it |
| 6 | — | SBC LTER kelp removal: invertebrate and algal density | Santa Barbara Coastal LTER | `bed-state/community` | `scb` (Santa Barbara after #87) | |
| 7 | — | PISCO kelp forest monitoring | PISCO | `bed-state/diver-surveys`, `bed-state/community`, `grazers-predators-competitors/predators` | #105 decides | spans California and Oregon |
| 8 | — | Giant kelp microsatellite genotypes, 2008 and 2018–19 (Klingbeil et al.) | the depositing authors; Dryad is the host | `recruitment-connectivity/genetics` | `scb` | the topic's first source |
| 9 | — | Monthly cross-shore biogeochemical transects, La Jolla | BCO-DMO dataset 839175 | `ocean-climate/nutrients`, `ocean-climate/oxygen-ph`, `ocean-climate/temperature`, `ocean-climate/salinity` | `scb` (San Diego after #87) | |
| 10 | — | NDBC buoy observations, Bight stations | NOAA National Data Buoy Center | `waves-storms-sediment/swell-climate`, `waves-storms-sediment/storms` | `scb` | station-scoped; which stations is the slice's first question, answered from NDBC's own station list |
| 11 | — | Catalina Marine Society thermograph array | Catalina Marine Society | `ocean-climate/temperature` | `scb` (mainland and Catalina after #87/#88) | the portal must be exercised; the licence is whatever the portal states |
| 12 | — | Catalina Marine Society Catalina chemistry and current collections | Catalina Marine Society | `ocean-climate/temperature`, `ocean-climate/salinity`, `ocean-climate/oxygen-ph` | `scb` (Catalina after #88) | likely more than one record once the portal's collections are seen; chlorophyll waits on the productivity sub-topic |
| 13 | — | Channel Islands fish excretion dataset (Shrestha et al.) | the depositing authors; Dryad is the host | `bed-state/community`, `bed-state/mpas` | `scb` (islands after #88) | derived from PISCO surveys; enters after row 7 and cites it |
| 14 | — | CORDC HFRNet surface currents, Bight subset | Scripps CORDC | *waits on a circulation sub-topic* | `scb` | `needs-triage` until the sub-topic row lands |
| 15 | — | Inner-shelf flow archive, San Diego (Okun et al.) | the depositing authors; Dryad is the host | *waits on a circulation sub-topic* | `scb` | `needs-triage`; one study's instrument archive, after row 14 |
| 16 | — | Surface-water DIC isotope time series, Table 1 (Hauksson et al.) | transcribed from the paper | *waits on a carbonate-chemistry sub-topic* | `scb` | `needs-triage`; `TRANSCRIBED`, and the first slice that legitimately creates a reference record |
| 17 | — | CDFW California marine habitat GIS | California Department of Fish and Wildlife | `substrate/rock-mapping` | `scb` | `needs-triage` until the exact layer and its Bight coverage are identified |
| 18 | — | NASA Ocean Color chlorophyll | NASA Ocean Biology Processing Group | *waits on a productivity sub-topic* | `global` | `needs-triage`; a global product with no regional bound, as ONI is |
| 19 | — | exclude: Stebbins & Wetzer 2023, Bight isopod review | — | — | — | `excluded/` record, one-line reason |
| 20 | — | exclude: Cheresh et al. 2023, California Current corrosive events | — | — | — | `excluded/` record, one-line reason |

Rows 1–13 are `ready-for-agent` on filing. Rows 14–18 are `needs-triage` and each names what it
waits on. Rows 19–20 are entry.

## Found while reviewing, not filed

- The CDFW aerial canopy survey shapefiles for 1989, 1999 and 2002–2016, described in
  `CONTEXT.md`'s region tree, are not a record and are not queued anywhere. They belong beside row 2
  and #82 as `canopy/aerial-surveys`. Filed as a Parking-lot line rather than a row, because the
  manifest did not name them and this milestone's rows are the manifest's.
- CalCOFI appears in the manifest as a lead. It is held as `calcofi`, one station. Whether the record
  widens is a 6.4 re-entry question.
- Hoel et al. 2025's study data, kelp canopy against nutrient sources, is the one `ON REQUEST`
  candidate worth returning to once H-ids have a registry.

## Non-goals

No reference records except the one row 16 needs. No `ON REQUEST` records. No sub-topic rows: each
is a Parking-lot line and its own PR, decided by the owner. No region node, bed or site. No change to
the admission sentence in `CONTEXT.md`. No lock. No record for a preprint, a redirect URL, or either
ProQuest item, whose titles could not be established without guessing. Nothing here jumps milestone
6.3's queue: this milestone opens when that table has no open `ready-for-agent` row.

## Done

Every `ready-for-agent` row merged as a `FETCHED` record with its notebooks; every `needs-triage` row
either merged after its sub-topic landed or still open with the dependency named; the two exclusions
in `excluded/`; and no topic notebook renders its question over an empty *sources* count except
`canyon-dynamics` and `restoration-mitigation`, which this manifest did not reach.

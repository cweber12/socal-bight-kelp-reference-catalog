# PRD — Monitoring sources (milestone 6.3c)

Status: not started — opens when every `ready-for-agent` row of milestone 6.3's table has merged
(its frozen rows 9–14 excepted, whether or not the exit trigger on #84 has fired); milestone 6.3b
follows this one, since no row here needs a bed record and the region nodes 6.3 delivers let each
row tag its county or island on entry rather than in a re-tag pass
Created: 2026-09-15
Revised: 2026-09-15, after the audit of PR #110 found the table carried no routes, one reading
contradicted `CONTEXT.md`'s definition of `steward`, another contradicted the bare topic tag, and
four Parking-lot lines the text described as filed were not. Revised again the same day after the
second audit: ids added, `steward` aligned with the seven held records, and the exclusion reason
made the one reading 1 does not contradict. Revised 2026-09-16, after the second manifest review:
row 17 added, NOAA Fisheries Rocky Reefs HAPC GIS, the one item of that review with a route that
verified on the day; rows 17–20 became 18–21.

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
migrated. The routes it named are carried in the table below, **as leads**: every one is a claim
the manifest made and nobody in this repo has opened, and `add-source` steps 1 and 2 are where each
is checked.

## What the review settled

Each is a reading of an existing rule, applied to the manifest's proposals, and stated here so a
slice does not re-derive it.

1. **Driver data is admitted.** `CONTEXT.md` admits "an authoritative source about kelp in the
   Bight", and four of its ten questions are about the environment the beds are exposed to. Three of
   the seven records held on 2026-09-15 — `noaa_oni`, `calcofi`, `sio_shore_stations` — observe no
   kelp. The practice is that a source answering one of the ten questions is in scope. The manifest
   asked for that to be written into the admission sentence; that is a Parking-lot line (filed
   2026-09-15), not a gate on this milestone.
2. **A public dataset enters as `FETCHED` on first entry.** The manifest proposed every candidate as
   `PATTERN / NOT HELD` "now" with an upgrade later. `add-source` step 2 says a route that downloads
   today is `VERIFIED / FETCHED`, and #106 exists because one record entered without its bytes
   while its own `access` steps showed the route had been exercised. No slice here enters a source
   whose route downloads as anything but `FETCHED`; a portal that does not serve bytes gets the
   status step 2's table gives it.
3. **Papers are leads, not records.** `CONTEXT.md` defines `references/` as "a paper or report cited
   by a source or a figure", and where a context paper lives is parked (Parking lot, 2026-09-09).
   The manifest's fifteen proposed reference records are not filed; they are listed on the Parking
   lot (filed 2026-09-15) as evidence for that decision. The one exception a field needs —
   `transcribed_from.reference` for a transcribed table — arrives with that table's slice (row 16).
4. **Region tags are `scb` until the nodes exist.** `schema.py`'s link pass rejects a region id with
   no record. #87 and #88 create the counties and islands; a slice here that lands before them tags
   `scb` and says in its PR which node it would tag, so the re-tag is a lookup and not a re-read.
   Two rows (2 and 7) are described by the manifest as spanning beyond the Bight; they tag `scb`,
   state coverage as the package states it, and are the records #105 may retag if it chooses the
   containment reading. `ccr_t14_165_5` and `cdfw_ds3135`, both statewide and tagged `scb`, are
   the precedent.
5. **A source that fits no sub-topic takes the bare topic tag.** `CONTEXT.md`: a bare tag "places
   it under *General*", and `noaa_oni`'s bare `waves-storms-sediment` is the precedent. No row here
   waits on a sub-topic. The manifest's three suggested sub-topics — circulation, carbonate
   chemistry, productivity — are one Parking-lot line (filed 2026-09-15) as ideas, not blockers.
   Surface currents are an input to the `recruitment-connectivity` question, so `larval-transport`
   is the cataloguer's index for rows 14 and 15 on the same footing as `noaa_oni`'s waves tag;
   carbonate chemistry is what `oxygen-ph` already holds for `calcofi` (`dic1`, `ta1`, `ph1`), so it
   holds row 16; chlorophyll takes bare `ocean-climate` for row 19.
6. **`steward` is the producer, as the landing page names it; the host goes in `access`.**
   `CONTEXT.md` defines `steward` as "the organisation that publishes or holds it", and the seven
   held records read that as the program or agency that produced and publishes the data:
   `sio_shore_stations` is a UC San Diego Library deposit whose steward is the Shore Stations
   Program, and `calcofi`'s bytes come from a NOAA host while its steward is CalCOFI. So an EDI
   package's steward is Santa Barbara Coastal LTER and a Dryad deposit's is the depositing program
   or institution the page names, with the repository in `access` and `url`. Ids name the source,
   as the seven held do (`calcofi`, `sio_shore_stations`, `cdfw_ds3135`), with underscores; the
   `id` column below is the proposed id, chosen on entry and never changed.
7. **`ON REQUEST` records wait on an H-id registry.** `human_task: H<n>` has no registry in the
   repo (Parking lot, 2026-09-08). The three study-data candidates are not filed.
8. **Two items are exclusions; three are not.** An `excluded/` record is "an item reviewed and not
   admitted". Two items were reviewed as candidate sources and are not admitted because each is a
   paper with no dataset behind it that the paper or its host publishes — a taxonomic review of
   isopods, and a carbonate-system study of the California Current. That is the separation from
   the fifteen papers of reading 3, which were never reviewed as sources: each of those leads to a
   dataset, and the dataset is the row. A redirect URL and two superseded preprints are the same
   items as their canonical versions and are not records of any kind.

## Solution

One record per dataset as its steward publishes it, entered through `add-source`, in an order that
fills the empty questions first and lets each program's later datasets copy the fetch shape of its
first. A collection with one landing page is one record whose `access` steps name each file, as
`sio_shore_stations` names five station files under the collection's page; distinct packages with
distinct landing pages and DOIs are distinct records, as the four SBC LTER rows are.

## Slices

Issues are filed on milestone `6.3c Monitoring sources` after this PRD merges, and their numbers
are added to this table then; `docs/agents/issue-tracker.md`'s milestone list gains the name in the
same change. The rows are in work order. Rows 1–19 are record issues in the shape
`docs/agents/issue-tracker.md` gives them: `add-source` is the seam, there is no mechanical failing
test, and the notebooks the record's topics move land in the same PR. Rows 20–21 are one issue.

The **route** column is the manifest's lead, unopened. A slice opens it at `add-source` step 2 and
enters what the page states, not what this table says. The **id** column is the proposed id.

| order | # | id | source | route (lead) | topics | region today | note |
|---|---|---|---|---|---|---|---|
| 1 | — | `cinp_kfm` | Channel Islands National Park Kelp Forest Monitoring | none given; find the program's own data endpoint (NPS) | `bed-state/diver-surveys`, `bed-state/community`, `grazers-predators-competitors/urchins` | `scb` (islands after #88) | the manifest calls it the longest-running diver survey in the Bight; enter the program's own statement of its span |
| 2 | — | `sbc_lter_landsat_canopy` | SBC LTER Landsat kelp canopy, quarterly since 1984 | EDI package `knb-lter-sbc.74`, https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.74.13 | `canopy/satellite`, `canopy/persistence` | `scb`; #105 may retag | the manifest says statewide NetCDF; state coverage as the package states it |
| 3 | — | `sbc_lter_bottom_temperature` | SBC LTER reef bottom temperature | doi:10.6073/pasta/e565d409b63f20c768133c653ccdb2d7 | `ocean-climate/temperature`, `ocean-climate/heatwaves` | `scb` (Santa Barbara after #87) | one record per EDI package; the DOI the manifest gives is revision-pinned, and the record enters the package's current revision and states which |
| 4 | — | `sbc_lter_kelp_biomass` | SBC LTER annual kelp forest biomass | doi:10.6073/pasta/cb45bf15430ba570828444b13dd8521f | `bed-state/diver-surveys`, `bed-state/community` | `scb` (Santa Barbara after #87) | revision-pinned DOI, as row 3 |
| 5 | — | `sbc_lter_kelp_removal_cover` | SBC LTER kelp removal: sessile cover | doi:10.6073/pasta/1151c1dcf5110432b6d35f7dc00bb834 | `bed-state/community` | `scb` (Santa Barbara after #87) | an experiment's monitoring; `coverage` says so as the package states it; revision-pinned DOI, as row 3 |
| 6 | — | `sbc_lter_kelp_removal_density` | SBC LTER kelp removal: invertebrate and algal density | doi:10.6073/pasta/decb1dcc7b35d2ef401b2dd7d79ea257 | `bed-state/community` | `scb` (Santa Barbara after #87) | revision-pinned DOI, as row 3 |
| 7 | — | `pisco_kelp_forest` | PISCO kelp forest monitoring | data paper doi:10.1002/ecy.3630; the data host is what the paper names | `bed-state/diver-surveys`, `bed-state/community`, `grazers-predators-competitors/predators` | `scb`; #105 may retag | the manifest says California and Oregon; state coverage as the host states it |
| 8 | — | `klingbeil_kelp_genotypes` | Giant kelp microsatellite genotypes, 2008 and 2018–19 | doi:10.5061/dryad.nzs7h44v9 | `recruitment-connectivity/genetics` | `scb` | the topic's first source |
| 9 | — | `bcodmo_839175` | Monthly cross-shore biogeochemical transects, La Jolla | doi:10.26008/1912/bco-dmo.839175.1 | `ocean-climate/nutrients`, `ocean-climate/oxygen-ph`, `ocean-climate/temperature`, `ocean-climate/salinity` | `scb` (San Diego after #87) | id follows `cdfw_ds3135`: host and dataset number, since the page names no shorter producer |
| 10 | — | `ndbc_bight_buoys` | NDBC buoy observations, Bight stations | none given; NDBC's own station list | `waves-storms-sediment/swell-climate`, `waves-storms-sediment/storms` | `scb` | station-scoped; which stations is the slice's first question, answered from the station list, as `sio_shore_stations` narrowed to Bight stations |
| 11 | — | `cms_thermograph_array` | Catalina Marine Society thermograph array | https://www.catalinamarinesociety.org/data-portal.html | `ocean-climate/temperature` | `scb` (mainland and Catalina after #87/#88) | the portal must be exercised; tier is what step 2's table gives the route; licence as the portal states it |
| 12 | — | `cms_catalina_collections` | Catalina Marine Society Catalina chemistry and current collections | same portal | `ocean-climate/temperature`, `ocean-climate/salinity`, `ocean-climate/oxygen-ph`, bare `ocean-climate` for chlorophyll | `scb` (Catalina after #88) | likely more than one record once the portal's collections are seen; the id is then per collection |
| 13 | — | `shrestha_fish_excretion` | Channel Islands fish excretion dataset (Shrestha et al.) | doi:10.5061/dryad.k6djh9wgj | `bed-state/community`, `bed-state/mpas` | `scb` (islands after #88) | the manifest says it derives from PISCO surveys; enters after row 7, and its `coverage` quotes what the deposit states about its source data |
| 14 | — | `cordc_hfrnet` | CORDC HFRNet surface currents, Bight subset | https://hfrnet-tds.ucsd.edu/thredds/catalog.html | `recruitment-connectivity/larval-transport` | `scb` | format is what the THREDDS metadata states; the host did not answer from one machine on 2026-09-15, so step 2 may stop |
| 15 | — | `okun_inner_shelf_flow` | Inner-shelf flow archive, San Diego (Okun et al.) | doi:10.5061/dryad.x3ffbg7tk | `recruitment-connectivity/larval-transport` | `scb` (San Diego after #87) | one study's instrument archive; after row 14 |
| 16 | — | `hauksson2023_table1` | Surface-water DIC isotope time series, Table 1 (Hauksson et al.) | doi:10.1017/RDC.2023.73 | `ocean-climate/oxygen-ph` | `scb` (Orange after #87, if Methods states Newport Beach) | `TRANSCRIBED`; the first slice that legitimately creates a reference record, for `transcribed_from` |
| 17 | — | `noaa_rocky_reefs_hapc` | NOAA Fisheries Rocky Reefs HAPC GIS, West Coast USA | doi:10.25921/2p36-q188, NCEI accession 0313075 | `substrate/rock-mapping` | `scb` | a West Coast product; `coverage` states the bounding box as NCEI prints it; steward is the producer the landing page names (NWFSC) and NCEI the host, per reading 6; the DOI resolved 2026-09-16 to v.2025-06, GeoPackage, CC0; from the 2026-09-16 manifest review, ahead of row 18 because its route needs no triage |
| 18 | — | `cdfw_marine_habitat_gis` | CDFW California marine habitat GIS | none given; identify the layer | `substrate/rock-mapping` | `scb` | `needs-triage` until the exact layer and its Bight coverage are identified — a fact question, not a vocabulary one; the id follows the layer's own number once known |
| 19 | — | `nasa_modis_aqua_chl` | NASA Ocean Color chlorophyll, MODIS Aqua L3 | doi:10.5067/AQUA/MODIS/L3B/CHL/2018 | bare `ocean-climate` | `global` | a global product; `global` if it states no regional bound, as `noaa_oni` does |
| 20 | — | `stebbins-wetzer-2023` | exclude: Stebbins & Wetzer 2023, Bight isopod review | title as the manifest gives it; find the DOI | — | — | `excluded/` record; reason: a review paper with no dataset behind it |
| 21 | — | `cheresh-2023` | exclude: Cheresh et al. 2023, California Current corrosive events | title as the manifest gives it; find the DOI | — | — | `excluded/` record; reason: a study paper with no dataset behind it that its host publishes |

Rows 1–17 and 19 are `ready-for-agent` on filing. Row 18 is `needs-triage` until the layer is
identified. Rows 20–21 are one `ready-for-agent` issue.

## Found while reviewing, not filed as rows

- The CDFW aerial canopy survey shapefiles for 1989, 1999 and 2002–2016, described in
  `CONTEXT.md`'s region tree, are not a record and are not queued anywhere. They belong beside row 2
  and #82 as `canopy/aerial-surveys`. A Parking-lot line (filed 2026-09-15), not a row, because the
  manifest did not name them and this milestone's rows are the manifest's.
- CalCOFI appears in the manifest as a lead. It is held as `calcofi`, one station. Whether the record
  widens is a 6.4 re-entry question.
- Hoel et al. 2025's study data, kelp canopy against nutrient sources, is the one `ON REQUEST`
  candidate worth returning to once H-ids have a registry.

## Non-goals

No reference records except the one row 16 needs. No `ON REQUEST` records. No sub-topic rows. No
region node, bed or site. No change to the admission sentence in `CONTEXT.md`. No lock, and no
decision on pulling the lock forward. No record for a preprint, a redirect URL, or either ProQuest
item, whose titles could not be established without guessing. Nothing here jumps milestone 6.3's
queue.

## Done

Every `ready-for-agent` row merged as a record with the tier its route supports, with its notebooks;
row 18 either merged after its layer was identified or still open with the question named; the two
exclusions in `excluded/`; and no topic notebook renders its question over an empty *sources* count
except `canyon-dynamics` and `restoration-mitigation`, which this manifest did not reach.

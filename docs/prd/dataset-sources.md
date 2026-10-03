# PRD — Dataset sources (milestone 6.4d)

Status: active, opened by the owner on 2026-10-02 by the PR for #297, which revised this line
(#263, Non-goals, left opening the milestone to the owner). The declaring sentence above the Slices
table stands (`CLAUDE.md`, "Auto-merge in a declared PRD run"); PR #290 merged unattended under it
on 2026-10-01, and the run's state since is on the #261 ledger thread. Which rows are open and
which labels they carry is read from GitHub, not from this file.
Created: 2026-10-01

## Problem

Milestone 6.3c closed on 2026-09-28 (PR #256), and it was the milestone for datasets: its Problem
section says "The papers are the route to the datasets; the datasets are the records." Closing it
left dataset record issues with no table to sit in. #263 names the three that were open on
2026-09-28 — #144, #148 and #261 — and two more were filed ahead of this table since, #267 on
2026-09-28 and #285 on 2026-10-01, each saying it was filed ahead of the table so that the table's
row would name it. Milestone 6.4d was created on 2026-09-28 to hold them, and the owner expects to
add more sources of this kind (#263, "Why this milestone exists").

A dataset's content is its `variables`, "the named columns or fields of the source's data files"
(`CONTEXT.md`, the sources table). That is what separates this track from 6.4b (#213, #214) and
6.4c (#258), whose rows enter documents and wait on the `measures` and `findings` fields: no row
here waits on #208 (#263, "A consequence worth stating in the PRD", and each of #261, #267 and #285
says the same of itself).

What the three filed rows add, re-counted on `main` at `fb15aac` on 2026-10-01 over the 28 records
in `catalog/sources/`: `recruitment-connectivity/settlement` tags 0 of the 28, and #261 proposes it;
`ocean-climate/temperature` tags 8 of the 28 (`bcodmo_839175`, `calcofi`,
`cms_burcham_updike_mooring`, `cms_thermograph_array`, `sbc_lter_bottom_temperature`,
`sccwrp_kelp_status_2016`, `sccwrp_tr1289`, `sio_shore_stations`); #267 states that none of those
eight is a mooring inside a San Diego County kelp bed (2026-09-28), and #285 that no record on
`main` is a mooring at the San Diego outfalls (2026-10-01).

## What the review settled

Each is a reading of an existing rule or a recorded ruling, applied to this milestone's rows, and
stated here so a slice does not re-derive it. Recommended by the review of 2026-10-01 and
commissioned by the owner from it. The readings of `docs/prd/monitoring-sources.md`, "What the
review settled", 1–8, govern every row of this table as they governed 6.3c's (reading 4 below);
this file points at them and restates none.

1. **#144 and #148 are candidates, not rows.** Both left 6.3c without a record on 2026-09-28
   (`docs/prd/monitoring-sources.md`, the paragraph under its Slices table; #144
   issuecomment-5864435556; #148 issuecomment-5864436112), and both sit on this milestone
   `needs-triage` on 2026-10-01. #144's host answered none of the probes recorded against it:
   2026-09-15 from one machine (the 6.3c row's note), 2026-09-27 from the cloud checkout (#141
   issuecomment-5852435312, the owner's ruling), and 2026-09-27 and 2026-09-28 from the owner's
   machine (#144 issuecomment-5864435556; #141 issuecomment-5862877754). The owner's ruling of
   2026-09-27 is that it is re-dispatched only once its host answers or the owner rules on a route.
   #148's title says "once identified", and its body says what makes it ready: a comment there
   naming the layer, its landing page and what that page states about coverage. Each is named
   below the table with that condition. #263's Non-goals forbid this PR re-triaging either, and it
   changes neither label.
2. **A dataset's paper gets no `references/` record.** `CONTEXT.md` glosses `references/` as "a
   paper or report cited by a source or a figure" (*Record format*, the `catalog/` tree), and
   6.3c's reading 3 is that papers are leads, not records. The four dataset-behind-paper records
   the review of 2026-10-01 named — `shrestha_fish_excretion`, `okun_inner_shelf_flow`,
   `bcodmo_839175` and `pisco_kelp_forest` — each name the paper in an `access` step, as the
   landing page, the API or the paper's own data availability statement puts it, and each carries
   `references: []`: the paper is a fact of the route, and no field of the four names a
   `references/` record. Counted on `main` at `fb15aac`: all 28 records in `catalog/sources/` carry
   `references: []`, and the two records in `catalog/references/` are reached by
   `transcribed_from.reference` (`hauksson2023`, from `hauksson2023_table1`) and by ten site
   records (`klingbeil2022`). The paper behind #261, doi:10.1002/eap.70181, is a candidate on
   #214's track (#214 issuecomment-5878054337, 2026-09-28), where "a paper and its dataset are two
   records" (#214, as #263 quotes it). No row here creates a `catalog/references/` record, and
   #263's Non-goals forbid this PR creating one.
3. **A byte-unstable repository deposit enters `VERIFIED / FETCHED`, verified per member.**
   `add-source` step 2's first row gives a route whose file downloads `VERIFIED / FETCHED`, and
   Dryad's version download does download. Three records on `main` at `fb15aac` hold a Dryad
   version zip — `klingbeil_kelp_genotypes` (PR #170), `shrestha_fish_excretion` (PR #243) and
   `okun_inner_shelf_flow` (PR #244) — and each states in its last `access` step that the zip is
   assembled on request, the sizes of the zips it was served and that their SHA-256s differ, and
   that its fetch script keeps the file only when every member has the size and the SHA-256 the
   deposit's files listing states. `check_container` — the file begins with the zip local file
   header, carries no bytes before its first member and no archive comment — came from the audit
   of PR #243, F5 (#141 issuecomment-5851915734); `src/fetch/shrestha_fish_excretion.py` and
   `src/fetch/okun_inner_shelf_flow.py` carry it, and `src/fetch/klingbeil_kelp_genotypes.py`,
   written before that audit, does not (counted 2026-10-01). #261's row follows the `access` steps
   and scripts of `shrestha_fish_excretion` and `okun_inner_shelf_flow`. What the lock gate will
   verify for such a record is parked, not decided here: #5 issuecomment-5788964109 (2026-09-22),
   "two `verify` modes, `bytes` and `members`". No `CONTEXT.md` change (#263, Non-goals).
4. **6.3c's readings 1–8 carry over, and six rulings from its controller ledger with them.**
   Readings 1–8 of `docs/prd/monitoring-sources.md`, "What the review settled", govern each row
   here as written there, reading 2's proportionality clause included and unchanged; a row's PR
   cites that file by reading number. Reading 1 is dated to the review that made it, and the
   admission sentence it quotes has since been replaced (#202, PR #266), so the sentence a row
   applies is `CONTEXT.md`'s today. Six rulings from the 6.3c run, ledgered on #141, reach a row
   here where its premise recurs, each with the scope its comment gives it, which a row reads from
   the comment and not from this list: (a) `variables` is every column name the held files state,
   Reading A, for a source that publishes no metadata document — owner, 2026-09-25,
   issuecomment-5839124033; the audit of PR #243 says it does not reach a source whose deposit
   ships a README (issuecomment-5851915734, F1); (b) a label that carries its unit is the whole
   label as `name` with `unit: null` — owner, 2026-09-27, ruled for #142 at
   issuecomment-5851281379, with #5 issuecomment-5841215379 open as the general question; (c) a
   README's spelling of a column over a header line's — audit of PR #243, F1,
   issuecomment-5851915734, landed at issuecomment-5851954076; (d) `steward` on a Dryad deposit
   whose page names no depositor: the research facility the page names — owner, 2026-09-27, PR
   #243 F2, issuecomment-5851915734 — and, when it names neither a depositor nor a facility, the
   first author's affiliation — owner, 2026-09-27, on #145, issuecomment-5852470425; (e) a README
   that names no fields gives `variables: []`, and nothing is read out of binaries — the same
   ruling; (f) `regions` is the smallest node containing the sites the README names, a title's "in
   the Southern California Bight" not read as Bight-wide coverage — the same ruling, which the
   ledger carries forward at issuecomment-5852533661 as "named sites inside one county tag that
   county".
5. **#267 is one record, `bcodmo_3638`, holding dataset 3638's file.** Ground: #267's own
   measurement that 3639's four rows equal the `Latitude`, `Longitude`, `Start_Date` and
   `End_Date` tuples 3638's columns carry for the four moorings, the one difference being the
   spelling of `Site_Description` (#267, "Two questions the PR has to settle", 1), and its comment
   of 2026-09-29 (issuecomment-5888801758): each of the four deployment pages links exactly 3638
   and 3639, and 3638's Description says one data file per mooring where its file listing says one
   file — a self-disagreement the record's `coverage` quotes both ways and resolves neither, the
   owner's decision of 2026-09-24 (#5 issuecomment-5822998934), whose rule issue, #204, is open
   and `ready-for-agent` on 2026-10-01. The record names 3639 in `access` as where the positions
   are also published, and creates no `sites/` record (#267, Non-goals). **This departs from** the
   Solution of `docs/prd/monitoring-sources.md`, "distinct packages with distinct landing pages and
   DOIs are distinct records", which the 6.3c run applied on #142 (#141 issuecomment-5851252050,
   2026-09-27): 3639 has its own landing page, so that sentence read alone makes it a record, and
   the departure rests on #267's measurement that its four rows are, except the spelling of one
   string, values 3638's columns state for the same four moorings. The test this reading and
   reading 6 share is content: a dataset whose rows another dataset's columns already state is
   named in that record's `access`, and datasets whose files state different parameters are
   distinct records. Neither page prints a `DOI:` label for the dataset (#267). The SeapHOx
   project's five other datasets are candidates on #5 (issuecomment-5888939902, 2026-09-29), not
   rows.
6. **#285 is one record per DCAT dataset, temperature first, holding all eight files.** The three
   siblings — DCAT identifiers `monitoring_ocean_rtoms_salinity`,
   `monitoring_ocean_rtoms_ocean_chemistry` and `monitoring_ocean_rtoms_water_quality` — each have
   their own identifier, landing page and eight files, and those files state different parameters
   (#5 issuecomment-5933645289, 2026-10-01, names them; #285 question 1), so under the content test
   reading 5 states they are distinct records. They are rows 4–6 below, `to file` in the form
   `docs/prd/re-entry.md`'s Slices intro gives, and the owner files them only after row 3 merges
   (filed 2026-10-03 UTC as #303, #304 and #305).
   Row 3 holds all eight CSVs (#285 question 2): 137.46 MB by the page's stated sizes (#285),
   against a largest held file of 582,980,514 bytes (`sbc_lter_bottom_temperature`, as its `access`
   states and as held under `data/raw/` on 2026-10-01) and the one entity 6.3c's reading 2 met as
   disproportionate, 2,430,814,959 bytes re-released quarterly. `license` takes the shape
   `bcodmo_839175` uses for a linked page: the label as the page prints it and the linked page's
   terms quoted, `license_stated_at` naming both. The RTOMS page prints the label "License" and a
   link whose text is "View License", to opendefinition.org, and no licence text (#285 question 3,
   which names `bcodmo_839175` and `ndbc_bight_buoys` as the two precedents for a page that links
   rather than prints); what the linked page states is the row's to read. No `sites/` record (#285
   question 4 and Non-goals): the source states no position, and the positions #285 found
   numerically are in SIO's `js/map.js`, a script.
7. **How a new candidate arrives.** The Slices intro below states it once; this reading records
   the ground. #5 issuecomment-5890391263 (2026-09-29, from the audit of PR #270) parked that no
   PRD states how its track takes a new candidate. #148's body asks the same three things of a
   comment, as its own readiness condition — ready "when a comment here names the layer, its
   landing page and what that page states about coverage" — and `CLAUDE.md`, "How work is
   tracked", keeps filing with the owner. #263 closes when the PR that creates this file merges and
   stays the inbox closed; candidates parked on #5 before this file existed stay there. This
   resolves that parked line for this track and for no other.

## Solution

One record per dataset as its steward publishes it, entered through `add-source`, as
`docs/prd/monitoring-sources.md`'s Solution says, with the one departure reading 5 records. The
order is by distance to a settled precedent: #261 first, because both Dryad records its route
copies have merged (PRs #243 and #244); #267 second, because `bcodmo_839175` is the precedent for
its host, its licence and its citations; #285 third, because no tracked file on `main` names its
host (#285, measured 2026-09-30) or its licence link (measured 2026-10-01 at `fb15aac`, over the
tracked files outside this one); then the three RTOMS siblings, each copying row 3's shape.

## Slices

Issues #261, #267 and #285 were filed ahead of this table, on 2026-09-28, 2026-09-28 and
2026-10-01, and their numbers are in the `#` column; the three RTOMS siblings carried `to file`, the
convention `docs/prd/re-entry.md`'s Slices intro gives for a row whose issue does not exist yet,
until filed 2026-10-03 UTC as #303, #304 and #305.
The rows are in work order. Every row whose `#` cell names an issue is a record issue in the shape
`docs/agents/issue-tracker.md` gives them: `add-source` is the seam, there is no mechanical failing
test, and the notebooks the record's topics move land in the same PR. Each of #261, #267 and #285
says it waits on this PR, and #267 says so under a heading `## Scheduling` rather than
`## Blocked by`; when this PR merges, the labels are the owner's to move (`CLAUDE.md`, "How work
is tracked").

A row whose seam is `add-source` is auto-merge eligible; every other row is not (`CLAUDE.md`,
"Auto-merge in a declared PRD run").

A new candidate for this track arrives as a comment on #263, open or closed, naming the dataset,
its landing page and what that page states about coverage; the owner files the row (reading 7).

The **route** column is the issue's lead, measured on the date the issue states; a slice opens it
at `add-source` step 2 and enters what the page states that day, not what this table says. The
**topics** and **region today** columns are the issues' own proposals, which the row reads off the
source; nothing here settles them. The **id** column is the proposed id, which step 3 confirms.

| order | # | id | source | route (lead) | topics | region today | note |
|---|---|---|---|---|---|---|---|
| 1 | [#261](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/261) | `parnell_kelp_demography` | Giant kelp cohort demography off San Diego, four decades (Parnell et al.) | Dryad doi:10.5061/dryad.fttdz096d; the version download, as `shrestha_fish_excretion` and `okun_inner_shelf_flow` take it | `bed-state/diver-surveys`, `bed-state/community`, `recruitment-connectivity/settlement`; `grazers-predators-competitors/urchins` and `ocean-climate/heatwaves` only if the dataset's own columns or coverage state them | `scb.mainland.san-diego` | readings 2 and 3 answer the two questions its body leaves to this file; the data behind doi:10.1002/eap.70181, which is #214's candidate; `recruitment-connectivity/settlement` would be the catalog's first record under that sub-topic |
| 2 | [#267](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/267) | `bcodmo_3638` | SeapHOx La Jolla kelp forest moorings, "from 2010-2011" as the title says, BCO-DMO dataset 3638 | https://www.bco-dmo.org/dataset/3638; the one file the page lists, `MOORING_DATA.csv`, byte-stable across two clients on 2026-09-28 | `ocean-climate/temperature`, `ocean-climate/oxygen-ph`, `ocean-climate/salinity` | `scb.mainland.san-diego` | reading 5: one record, 3639 named in `access`; `bcodmo_839175` is the shape for `license`, `license_stated_at` and `citations`; neither page prints a DOI, so `doi` is null unless the page states one; its body has no `## Blocked by` section and says under `## Scheduling` that it wants this table first |
| 3 | [#285](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/285) | `sandiego_rtoms_water_temperature` | RTOMS water temperature, City of San Diego Ocean Monitoring Program, DCAT `monitoring_ocean_rtoms_water_temperature` | https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-water-temperature/; eight CSVs on `seshat.datasd.org`, the two 2023 files byte-identical across two fetches on 2026-09-30 | `ocean-climate/temperature`; `water-quality-harvest/discharges-outfalls` only if the record's own reading supports it | `scb.mainland.san-diego` | reading 6 answers its questions 1–3 and its question 4 rules itself out; holds all eight files; `variables` from the dictionary CSV the DCAT entry names; `site_key` one entry per file on `project` |
| 4 | [#303](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/303) | `sandiego_rtoms_salinity` | RTOMS salinity, DCAT `monitoring_ocean_rtoms_salinity` | https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-salinity/, identified to its DCAT entry only (#5 issuecomment-5933645289) | `ocean-climate/salinity`, the #5 entry's lead | as row 3 | reading 6; filed 2026-10-03 UTC after row 3 merged (PR #302), copying row 3's shape; the id follows #285's proposed form and step 3 confirms it |
| 5 | [#304](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/304) | `sandiego_rtoms_ocean_chemistry` | RTOMS ocean chemistry, DCAT `monitoring_ocean_rtoms_ocean_chemistry` | https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-ocean-chemistry/, identified to its DCAT entry only | `ocean-climate/oxygen-ph`, `ocean-climate/nutrients`, the #5 entry's leads | as row 3 | as row 4 |
| 6 | [#305](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/305) | `sandiego_rtoms_water_quality` | RTOMS water quality, DCAT `monitoring_ocean_rtoms_water_quality` | https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-water-quality/, identified to its DCAT entry only | none proposed: the #5 entry names the parameters and no tag; read off the source | as row 3 | as row 4 |
| 7 | [#293](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/293) | `cugn_sp030_20260701` | Spray glider sp030, CUGN Line 90, deployment `sp030-20260701T1719` of 2026-07-01, on the NOAA IOOS National Glider Data Assembly Center ERDDAP | https://gliders.ioos.us/erddap/tabledap/sp030-20260701T1719.html; the unconstrained tabledap CSV, held whole and dated, where `calcofi` holds one station's subset of its ERDDAP tables; `VERIFIED` / `FETCHED` under the second limb, the GDAC being the route the steward's own page `https://spraydata.ucsd.edu/data-access` names for Level 2 data (the record's third `access` step) | `ocean-climate/temperature`, `ocean-climate/salinity`, `ocean-climate/oxygen-ph` | `scb` | merged as PR #294 on 2026-10-02 (`b90cf7f`) before this row existed, so its cells are read from the record on `main`, not proposed: topics and region are its `topics` and `regions`; steward `Instrument Development Group, Scripps Institution of Oceanography`; the other 110 CUGN datasets on the DAC, `binnedCUGN90` on the steward's ERDDAP, and the chlorophyll and current columns that fit no sub-topic are parked at #5 issuecomment-5944478720 |
| 8 | [#295](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/295) | `opc_mlpa_kelp_forest` | Monitoring and Evaluation of Kelp Forest Ecosystems in the MLPA Marine Protected Area Network (Carr et al.), revision `.12` on the California Ocean Protection Council's DataONE member node | https://opc.dataone.org/view/doi:10.25494/P6/MLPA_kelpforest.12; seven entities fetched by the identifiers the node's system metadata states, each kept when its SHA-256 and size equal them, as `pisco_kelp_forest` is fetched; `VERIFIED` / `FETCHED` under the second limb, the route the creators' EML names through `cn.dataone.org/cn/v2/resolve/` (the record's fifth `access` step; PR #296, "Audit rulings", F1) | `bed-state/diver-surveys`, `bed-state/community`, `bed-state/mpas`, `grazers-predators-competitors/urchins`, `substrate/relief-rugosity` | `scb` | merged as PR #296 on 2026-10-02 (`206c351`) before this row existed, so its cells are read from the record on `main`, not proposed; `steward` is `UCSC`, the producer, with the host repository in `access` — `docs/prd/monitoring-sources.md` reading 6, carried here by reading 4, on which the audit of PR #296 blocked (PR #296, "Audit rulings", F1); the next DataONE row copies that; one record beside `pisco_kelp_forest`, not a mention in its `access` |

Rows 7 and 8 are appended out of the work order because they had no work left when they were
written: each merged before its row existed, and neither was dispatched from this table, since
the run's ledger thread on #261 names neither #293 nor #295 (0 of its 11 comments on 2026-10-02)
and neither issue was in any table when its PR merged. On `main` at `206c351`
(2026-10-02) the table's merged rows are 1, 7 and 8, and `catalog/sources/` holds 31 records:
`ocean-climate/temperature` tags 9 of the 31 (the eight the Problem section names at `fb15aac`
and `cugn_sp030_20260701`) and `recruitment-connectivity/settlement` tags 1
(`parnell_kelp_demography`). The Problem section's counts stand as measured at `fb15aac`.

Each of #261, #267 and #285 was `needs-triage` on 2026-10-01, waiting on this PR; the merged
table is what their issues say they wait for.

**#144 and #148 are candidates, not rows** (reading 1), and both are `needs-triage` on this
milestone on 2026-10-01. #144, `cordc_hfrnet`, becomes a row when its host answers a probe or the
owner rules on a route, the owner's ruling at #141 issuecomment-5852435312; its lead and its
proposed tags are 6.3c's row 14 and are not carried forward here as fresh. #148, the CDFW marine
habitat GIS layer, becomes a row when a comment on it names the layer, its landing page and what
that page states about coverage, which its own body says and which is the form this track takes a
new candidate in. Neither is re-triaged by this PR.

## Non-goals

No record entered by the PR that creates this file, no fetch script, no reference record, no
notebook regenerated (#263). No re-triage of #144 or #148 by that PR. No second PRD file and no
second Slices table for this milestone. No `CONTEXT.md` change; if reading 3 ever needs a rule, that
is its own PR. No edit to #213's, #214's or #258's tracks or rows, and no change to any existing
record. No `sites/` record for any row (each of #261, #267 and #285 says so of itself). The SeapHOx
project's five other datasets and the City's seven other Ocean Monitoring Program datasets are
candidates on #5, not rows (readings 5 and 6). That PR did not open the milestone or make it
active; the PR for #297 did, on 2026-10-02, by revising the status line.

## Done

Every row whose issue is `ready-for-agent` merged as a record with the tier its route supports,
with its notebooks; the three `to file` rows filed and merged, or still `to file` with the condition
in reading 6 unmet; and #144 and #148 either rows in a revision of this table or still candidates
with their conditions named under the table.

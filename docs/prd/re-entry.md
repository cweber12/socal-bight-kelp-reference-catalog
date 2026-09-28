# PRD — Re-entry (milestone 6.4)

Status: not active, and this file does not open 6.4; the owner does. Milestone 6.3c closed on
2026-09-28 and no PRD's status line reads `active` today. The owner's gate for opening 6.4
is #5 issuecomment-5823169852: open it when 6.3c closes and #198 and #208 have merged; on 2026-09-28
the first of those three has happened and the other two have not. That comment gives three reasons
for holding 6.4 shut, and they have not aged alike: the `coverage` reorder collides with the open
6.3c rows that enter a source record, **spent** — 6.3c closed with none open; rows M1–M15 want two
fields that do not exist yet, so opening now costs a second touch per record, **live**, and it is
why the gate's other two conditions are #198 and #208; and nothing ready to run needs it open,
whose own clause was "beside an active 6.3c" and so no longer reads as written. Of this milestone's
rows that comment names the six rule rows of Part three, #198, #179, #208 and this file's own
revision (#210) as needing no open milestone; it names rows of other milestones too, and this file
adds nothing to that list. The rows that wait for 6.4 to open are the migration rows (M1–M15) and
the two closers. Which reading of "one milestone is active at a time" the practice of merging a row
of an inactive milestone answers is still an open question on the Parking lot (settled point 6),
and this file takes no reading of it.
Created: 2026-09-23
Revised: 2026-09-28, for the grill of 2026-09-24 (#210): settled point 2 reversed, `coverage` added
to every migration row's fills, the schema queue reordered, the Problem paragraph and three counts
re-measured, and a rule queue added as Part three.

## Problem

The source records that predate this milestone were entered before the fields a view needs existed.
Measured on `main` at `7a74c4f` on 2026-09-28, `catalog/sources/` holds 28 records — 23 `FETCHED`,
4 `NOT HELD` (`cinp_kfm`, `nasa_modis_aqua_chl`, `noaa_rocky_reefs_hapc`,
`sbc_lter_landsat_canopy`) and 1 `TRANSCRIBED` (`hauksson2023_table1`). Nineteen of the 28 are the
records this milestone re-enters; the other nine were entered after 2026-09-23 in the shape the
schema queue is building toward, and Part two gives them no row.

Of the 28: `variables` holds 369 bare-string entries across 15 records — the fifteen Part two
migrates — and 224 map-form entries across 6 records, while 7 records carry `variables: []`.
`license_stated_at` (PR #171) is present on 9 records and absent from 19; `site_key` (PR #189) and
`citations` (PR #191) are each non-empty on 5 and present-but-empty on 4 more, a state
`CONTEXT.md`'s sources table distinguishes from absence. The nine records entered since
2026-09-23 are exactly the nine that carry `license_stated_at`, so the 19
lacking it are exactly the 15 migration rows plus the 4 records of Part two's closing paragraph,
which is what row C2 counts. `catalog/sites/` holds 21 site records, listed in the `sites` field of
5 source records: `klingbeil_kelp_genotypes` (10, PR #187) and the four `sbc_lter_*` records (11,
11, 5 and 5, drawn from the same 11). None of the five states a `site_key`, which is the field that
says how the source's own data names them.

The grill of 2026-09-21/22 sliced the `variables` change three ways — expand (#90), migrate (one
`catalog:` PR per record), contract (#182) — and left the migration with no order and no table
(#183). Eight issues, six of them open, sat on the milestone on 2026-09-23 with nothing to order
them by. This file is that table.

## What the review settled

Each point names where it was decided; none restates the rule it points at.

1. **`variables` means the named columns or fields of the source's data files.** #90, Decision.
   A document's phrases are not `variables`; they move verbatim to `measures` (row S3), and a
   non-tabular source has `variables: []`.
2. **Four of a migration row's five fills move no notebook; the fifth moves one per topic the
   record carries, where it changes what the sources table renders.** #90's failing test asserts
   that `build.py` renders no `variables`, and on 2026-09-28 no module under `src/kelpcatalog/`
   except `schema.py` names `variables`, `license_stated_at`, `site_key` or `citations` as a
   field — the one other grep hit, `citations` in `figure_provenance.py`, is the English word in a
   docstring — so those four move nothing under `notebooks/`.
   `coverage` is the exception and it is new here: `build.py` carries `coverage` in
   `SOURCE_COLUMNS` and renders it truncated to `COVERAGE_CHARS`, so the reorder every migration
   row now carries (#203) changes the rendered cell. Measured on 2026-09-28 on two records, by
   reordering the first words of `coverage` and running the generator. `klingbeil_kelp_genotypes`,
   tagged with one sub-topic of one topic, moved one notebook:
   `2_kelp_and_community/24_recruitment_connectivity.ipynb`. `sccwrp_tr1289`, tagged with four
   sub-topics across three topics, moved three: `1_physical_environment/11_ocean_climate.ipynb`,
   `1_physical_environment/13_waves_storms_sediment.ipynb` and
   `3_human_uses_management/31_water_quality_harvest.ipynb`. So the count is one notebook per
   **topic**, not per tag. Neither moved `00_index`: its generated cells are counts and a matrix
   today, and its third section is unbuilt (#160), neither of whose candidate column sets carries
   `coverage`. The same measurement with a `license_stated_at` fill moved no notebook at all.
   **Both experiments changed the first characters of the field, so they measure the mechanism and
   not how often it fires**: `build.py` truncates the cell to `COVERAGE_CHARS`, so a reorder that
   leaves those characters alone moves nothing, and the Slices intro counts how many of the fifteen
   records the reorder is expected to reach. Every migration PR reports which notebooks it moved,
   and one that moves a notebook this does not predict reports the diff in its body rather than
   absorbing it (#183, Goal).
3. **`sccwrp_b08_rocky_reef`'s 13 phrases become column headers or `measures` depending on what
   its held files carry.** Whoever migrates it opens `data/raw/sccwrp_b08_rocky_reef/` (on
   2026-09-28 still `685_B08RockyReef.pdf` and its manifest, two files) and says which in the PR
   (#183, Goal).
4. **The fills ride the migration, one touch per record — on #183's word, which #180
   disagrees with.** #183 (Goal) has each migration row carry the record's `license_stated_at`,
   `site_key`, `citations` and `coverage_spans` fills, "one touch per record, not four". #38's
   amendment of 2026-09-22 agrees for `license_stated_at`: "per record as re-entry". #180
   (Non-goals) places `citations` fills "per record, in the `catalog:` PR of whichever view
   renders it first", and #179 (The rule) has a finding quoted "because a view needs it", "never
   harvested in bulk" — a trigger no row here waits for. This file follows #183 and quotes both;
   the owner chose #183's bundling at the review of PR #192 on 2026-09-23 (the Parking-lot line,
   #5 issuecomment-5805925788, records the choice under it). `site_key` is filled where the
   sources table's `site_key` row admits it (`CONTEXT.md`). The fifth fill is the `coverage`
   reorder of #203 and not `coverage_spans` (#89): `coverage_spans` is 6.6's, its schema row S4
   waits on #178 (6.6), so no migration row carries it and its fill on every record migrated here
   is a second touch — row P1, also 6.6's. Rows say which fields they carried when they merge.
5. **`measures` and findings-on-sources are filed.** Both were the owner's to file and both were
   filed on 2026-09-24 (#5 issuecomment-5823169852): `measures` is #198 and findings-on-sources is
   #208, the row this file had carried as an unfiled S2. The shape #183 gives `measures` is
   `list[str]`, a document's phrases as printed, with the failing test that a non-string entry is
   a problem; findings on sources points at the rule #179 writes for references rather than
   restating it (#179, The rule, last sentence). #179 moved from milestone 6.6 to 6.4 on
   2026-09-24, on the owner's standing instruction and for the reason that comment gives — so that
   it is not split from the row that points at it — and it carries row S5 here.
6. **"One milestone is active at a time" is followed here by precedent, not by a recorded
   reading.** The Parking-lot line (#5 issuecomment-5686055147, 2026-09-15) asks which reading the
   sentence means, and nothing under `docs/` or on #5 answers it; the status line names the gate
   that governs this milestone and does the same and no more.

## Solution

Three queues and two closers. The schema queue lands one `CONTEXT.md` sources-table row per PR,
serial, with a cold re-read of the row between PRs (#90, #180 and #89 each say so); one of its five
rows is 6.6's. The rule queue lands one `CONTEXT.md` rule per PR on the same terms. The migration
queue re-enters one record per `catalog:` PR, filling every field of that record the table names,
in the order a first view needs them. #182 then contracts the `variables` type, and #38 makes
`license_stated_at` required. #17 runs whenever someone picks it up.

## Slices

Rows are in work order within each part; the order letter is an identifier and not the position.
Rows with no issue carry "to file" in the `#` column, as `docs/prd/monitoring-sources.md` carried
"—" until PR #151 filed its issues; this PR files none. Two schema rows, #175 (`site_key`, PR #189)
and #180 (`citations`, PR #191), merged before this file existed and have no row.

The migration order below is the one written when the first view was undecided: by what any first
view needs — a record with sites, citations and expanded `variables` first, then the records whose
files key rows by site, then the rest, then the four document records, three of which wait on row
S3 (M12 waits on it only if settled point 3 falls to `measures`). **The first view has since been
named**: `bed-state` in Santa Barbara County, the owner's decision of 2026-09-24
(#5 issuecomment-5822998934), which restores the choice the triage comment on #183 (2026-09-23)
had recorded and this file had recorded as overridden. The rows below have not been re-derived
against it, and whether they should be is a question for whoever files M1, not one this revision
answers.

That ordering principle also needs the reorder to bite. Measured on 2026-09-24
(#5 issuecomment-5822999312): as the builder stands a view renders identically whether or not any
migration row has merged, because the builder names none of the four fields — the one exception is
row M6's `site_key`, which #177 reads for `pisco_kelp_forest`'s held site table. `coverage` is the
fill that changes what a reader sees, so it is what makes "what a first view needs" an order rather
than a preference.

**Every migration row now carries the `coverage` reorder, and a row moves notebooks when its
reorder changes the first `COVERAGE_CHARS` characters `build.py` renders — not otherwise**
(settled point 2). Which rows those are is not known in advance: measured 2026-09-28, 9 of the 15
open `coverage` with an attribution clause and 6 open with the content itself
(`noaa_oni`, `census_tiger_county_2025`, `cdfw_ds3135`, `sccwrp_b08_rocky_reef`,
`sccwrp_kelp_status_2016`, `sccwrp_tr1289`), so a row of the second group may move none. Each row
reports what it moved, as settled point 2 requires. A row that does move collides in `notebooks/`
with any other open PR that adds or edits a source record reaching the same topic notebooks. That
collision is the first of the three reasons the grill of 2026-09-24 gave for holding 6.4 shut: on
that day it was the 10 open 6.3c rows that entered a source record
(#5 issuecomment-5823169852). 6.3c closed on 2026-09-28 with none open, so that reason is spent. The
live case beside this file is issue #209, which retags `sccwrp_tr1289` — the record row M15
migrates — and is its own `catalog:` PR for exactly this reason.

Every migration row carries `license_stated_at`, because no record it covers has it, and moves the
where-I-looked text out of its `license` value (#38, Done when); it carries `citations` on
settled point 4, as the sources table's `citations` row admits them. No migration row carries
`coverage_spans`: its schema row is 6.6's, so the fill is the second pass, row P1, also 6.6's.

### Part one: the schema queue

Row S4 is #89, which the owner assigned to milestone 6.6 at the review of PR #192 (2026-09-23)
because it waits on a 6.6 issue, and which sits on 6.6 today. It keeps its place in the queue's
order and is listed here so the queue reads whole, and it does not gate this milestone's close.

Rows S3 (#198) and S2 (#208) are the two the owner's gate names as the condition for opening 6.4,
and both land before row M1 runs, so that a migration row fills every field the record has to state
in one touch. S5 (#179) is in the queue because S2 waits on it, not because the gate names it.

| order | # | slice | seam | note |
|---|---|---|---|---|
| S1 | [#90](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/90) | expand: a `variables` entry may be `{name, description, unit, file?}` | `RULES["sources"]`, `_type_ok`, the `variables` row, `add-source` step 3 | **done** — merged as PR #193; the `variables` row admits `{name, description, unit, file?}` and existing string-shaped records still validate |
| S3 | [#198](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/198) | `measures`: `list[str]`, a document's phrases as printed | `RULES["sources"]`, `_type_ok`, a new sources-table row, the `variables` row for the one sentence #198's Seam names, `add-source` step 3 | unblocked; failing test: a non-string entry is a problem (#183, Goal); rows M13–M15 wait on it, and M12 if settled point 3 falls to `measures` |
| S5 | [#179](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/179) | findings on references | the `references/` rule S2 points at | moved from milestone 6.6 to 6.4 on 2026-09-24 so it is not split from S2 (#5 issuecomment-5823169852); S2 waits on it |
| S2 | [#208](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/208) | findings on sources | `RULES["sources"]`, `_type_ok`, a sources-table row that points at #179's rule | after S5 has written the rule it points at; failing test as #179's, on the sources table; `needs-triage` |
| S4 | [#89](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/89) | `coverage_spans`, one entry per span the source states | `RULES["sources"]`, `_type_ok`, the sources table, `add-source` step 3 | `ready-for-human` until [#178](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/178) (6.6) merges, so it lands after this milestone's migration rows; the fills are row P1; a 6.6 row |

### Part two: the migration rows

One `catalog:` PR per row, filed as a record issue in the shape `docs/agents/issue-tracker.md`
("Record issues") gives one that enters a source, with the seam narrowed to the record, its fetch
script where a `site_key` entry names a stored file, and `add-source` step 3 as what drafts the
fields; as there, no failing test can be named — the gate checks the shape (S1's tests) and the
audit checks each entry against the source. The **held** column counts the files under
`data/raw/<id>/` on 2026-09-28 excluding manifests, because #90 makes `file` required on an entry
when the record holds more than one data file. How a column that more than one held file carries
takes `file`, and whether a stored archive is one file or what it contains, were parked for S1 and
**S1's landing settled both**: the `variables` row of `CONTEXT.md`'s sources table now answers each
in its own words, and the parked lines are closed (#5 issuecomment-5822999312, closing
issuecomment-5805925619 and issuecomment-5806181504). Read that row rather than this paragraph; it
is the authority and nothing compares a copy to it. The records that raise it are `calcofi`, which
states five columns in both its files; `sio_shore_stations`, which states that no single file
carries all of its variables; and `pisco_kelp_forest`, whose 76 names are the union of seven
tables' attributeNames, no table carrying all of them, 17 occurring in more than one, and `size`
stating "number" in one table and "centimeter" in another. The four rows holding archives — M1, M7,
M10 and M11 — take their `file` values from that row's archive clause, which is also why the
**held** column counts each archive as one. The **fills** column names
every field the record has to state in that PR; `coverage` on every row is the reorder of #203
(settled points 2 and 4), which is what makes the row move notebooks.

| order | # | id | `variables` today | held | fills | note |
|---|---|---|---|---|---|---|
| M1 | [#199](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/199) | `klingbeil_kelp_genotypes` | 6 strings → maps | 1 (zip) | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables`, `coverage` | `needs-triage`, because a migration row waits for 6.4 to open; one of five records whose `sites` is non-empty, and the only one outside the `sbc_lter_*` group (ten site records, PR #187); columns the source never names and its undefined `999` stay out of `variables` (#90, Decision; #5 issuecomment-5761453102) |
| M2 | to file | `sbc_lter_bottom_temperature` | 5 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables`, `coverage` | the four `sbc_lter_*` rows share one EML vocabulary and draw their sites from the same eleven site records (11, 11, 5 and 5), and run in the order the 6.3c table entered them; M2 and M3 were not checked for the code-list disagreement #90's comments record on M4 and M5 |
| M3 | to file | `sbc_lter_kelp_biomass` | 25 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables`, `coverage` | as M2 |
| M4 | to file | `sbc_lter_kelp_removal_cover` | 22 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables`, `coverage` | two separate disagreements. The EML's `SITE` and `TREATMENT` code lists contradict the held file (#90, comment of 2026-09-20), which is a `variables` matter and S1 says what the record states. Separately, the `coverage` fill gains **the two EML `methods` sentences row M5 carries** and this record does not, under R3 (#204), quoting both and resolving neither — the owner's decision of 2026-09-24, #5 issuecomment-5822998934 |
| M5 | to file | `sbc_lter_kelp_removal_density` | 24 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables`, `coverage` | the EML's `TREATMENT` code list contradicts the held file (#90, second comment); as M4 |
| M6 | to file | `pisco_kelp_forest` | 76 strings → maps | 8 (7 CSV, 1 PDF) | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables`, `coverage` | the 76 are the union of seven tables' attributeNames, as the record states; the site table is a held file |
| M7 | to file | `sio_shore_stations` | 16 strings → maps | 5 (zip) | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables`, `coverage` | one archive per station; `{file}` alone is the `site_key` form for a file that is one site's (`CONTEXT.md`, `site_key`) |
| M8 | to file | `calcofi` | 122 strings → maps | 2 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables`, `coverage` | whether a per-cast position is "the coordinates of its sites" is parked (#5 issuecomment-5801732071); the fill says which reading it took; whether the record widens past one station is a separate question (`docs/prd/monitoring-sources.md`, Found while reviewing) |
| M9 | to file | `noaa_oni` | 4 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `citations`, `variables`, `coverage` | `global`; no site to key |
| M10 | to file | `census_tiger_county_2025` | 18 strings → maps | 1 (zip) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `variables`, `coverage` | no site to key |
| M11 | to file | `cdfw_ds3135` | 7 strings → maps | 1 (zip) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `variables`, `coverage` | no site to key |
| M12 | to file | `sccwrp_b08_rocky_reef` | 13 strings → column headers or `measures` | 1 (PDF) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `variables` or `measures`, `coverage` | settled point 3: the migrating PR says which; placed after S3 because `measures` is the case that blocks |
| M13 | to file | `cdfw_kelp_esr` | 8 strings → `measures` | 7 (JSON, one per report page) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `measures`, `coverage` | a document record; `variables` becomes `[]`; after S3 |
| M14 | to file | `sccwrp_kelp_status_2016` | 14 strings → `measures` | 1 (PDF) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `measures`, `coverage` | as M13 |
| M15 | to file | `sccwrp_tr1289` | 9 strings → `measures` | 1 (PDF) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `measures`, `coverage` | as M13; the `water-quality-harvest` retag of this record is #209's own `catalog:` PR and not part of this row, because a retag moves notebooks (#5 issuecomment-5823169852) |

Four of the nineteen records this milestone covers get no migration row. `ccr_t14_165_5` is
`FETCHED` with `variables: []` and nothing to expand. `sccwrp_kelp_aerial` is `FETCHED` with
`variables: []`, and the owner settled on 2026-09-24 that its five appendix titles are neither its
`variables` nor its `measures`, so it keeps `variables: []` and gets no row on that ground
(#5 issuecomment-5822998934, which closes issuecomment-5700763690). `cinp_kfm` and
`sbc_lter_landsat_canopy` are `NOT HELD`, whose `variables` is the empty list by the sources
table. #182 does not wait on them. What the four still have to state — `license_stated_at`, with the
where-I-looked text moved out of `license`, and `citations` where the source prints one — is #38's
fill work and lands in row C2.

The nine records entered since 2026-09-23 — `bcodmo_839175`, `cms_burcham_updike_mooring`,
`cms_thermograph_array`, `hauksson2023_table1`, `nasa_modis_aqua_chl`, `ndbc_bight_buoys`,
`noaa_rocky_reefs_hapc`, `okun_inner_shelf_flow` and `shrestha_fish_excretion` — get no row either,
and this is a measurement rather than a decision: on 2026-09-28 all nine carry `license_stated_at`,
none carries a bare-string `variables` entry — six state `variables` in map form and three state
`variables: []` — and five carry `site_key` and five carry `citations`. Whether any of the nine
needs a row is a question for whoever notices one that does; on this measurement none does.

### Part three: the rule queue

The grill of 2026-09-24 filed six `CONTEXT.md` rule PRs on this milestone and the queues above had
no home for them (#5 issuecomment-5823169852). One rule per PR, serial, with a cold re-read
between — `CLAUDE.md`, "Changing a rule in `CONTEXT.md`", says how and this file does not restate
it. The order is the grill's.

| order | # | slice |
|---|---|---|
| R1 | [#202](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/202) | the admission sentence states three tests |
| R2 | [#203](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/203) | `coverage` states span and extent first, attribution after |
| R3 | [#204](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/204) | where a source states a thing two ways, `coverage` quotes both |
| R4 | [#205](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/205) | a site's `key` and `defined_by` may name two documents |
| R5 | [#206](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/206) | the `references/` gloss names sites |
| R6 | [#207](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/207) | `excluded/` holds an item that passed the scope test |

R2 is the rule every migration row's `coverage` fill applies, so it lands before row M1; R3 is the
rule row M4's fill applies.

### Part four: the closers, and the row outside the queue

| order | # | slice | blocked on | note |
|---|---|---|---|---|
| C1 | [#182](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/182) | contract: a bare-string `variables` entry is a problem | M1–M15 | closes when a count of bare-string `variables` entries on `main` reads zero; 369 on 2026-09-28, the same 369 across the same 15 records as on 2026-09-23; `needs-triage` |
| C2 | [#38](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/38) | `license_stated_at` on the four records with no migration row, the where-I-looked text out of every `license` value, then required | M1–M15, for the required flag | closes when a count of records lacking `license_stated_at` on `main` reads zero, no `license` value carries where it was read, and the field is required (#38, Done when); 19 lacking on 2026-09-28, which is the 15 migration rows plus those four |
| P1 | to file | `coverage_spans` fills, one `catalog:` PR per record whose `coverage` quotes a span | S4 | a 6.6 row: the second touch of every record migrated here that quotes a span; one issue per record in Part two's shape, filed when S4 merges, which is when the records that quote a span are counted |
| X1 | [#17](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/17) | every CSV under `catalog/tables/` has a `TRANSCRIBED` source record | nothing | outside the serial queue; may run at any time; on 2026-09-28 `catalog/tables/` holds one CSV, `hauksson2023_table1.csv`, whose `TRANSCRIBED` source record exists |

Issue #172 (`version`) is closed `wontfix` and has no row (its closing comment, 2026-09-23).

## Non-goals

No `CONTEXT.md` change. No issue filed or edited: the migration rows are filed when 6.4 opens. No
record edit and no notebook regenerated. 6.4 does not become active by this file. No `version`
field (#38, amendment; #172). No builder change: how a view renders `measures`, findings or
`coverage_spans` is 6.6's. This file decides no row's schedule beyond what the owner's gate
at #5 issuecomment-5823169852 and the grill's decisions of 2026-09-24 already entail: the two
ordering sentences under Part three are derived from #203's Non-goals and from #204, not decided
here.

## Done

Rows S1, S3, S5 and S2 merged as `CONTEXT.md` rows; rows R1–R6 merged as one rule per PR; rows
M1–M15 merged as `catalog:` PRs, each saying which fields it carried, which notebooks it moved
and, for M12, which of the two forms its held file supported; C1 merged with a count of
bare-string `variables` entries on `main` at zero; C2 merged with `license_stated_at` required, no
record lacking it and no `license` value carrying where it was read; X1 merged. S4 and P1 are
6.6's and do not gate this milestone's close.

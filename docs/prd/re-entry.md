# PRD — Re-entry (milestone 6.4)

Status: not active — 6.3c is (`docs/prd/monitoring-sources.md`, its status line), and this file
does not open 6.4; the owner does. Two kinds of row may run beside 6.3c: a schema row once it is
unblocked — S1 today, S3 once filed; S2 and S4 are 6.6's — because a schema row changes no
record and so moves no notebook; and #17, which touches the link pass and not the sources table
(its triage comment of 2026-09-23). The precedent is PR #191, which closed
an issue of this milestone, #180, on 2026-09-23 while 6.3c was active; PR #186 (#174) and PR #189
(#175) did the same for 6.3b the same day. Which reading of "one milestone is active at a time"
that practice answers is still an open question on the Parking lot (settled point 6). The
migration rows (M1–M15) and the two closers wait for 6.4 to open.
Created: 2026-09-23

## Problem

All 19 source records were entered before the fields a view needs existed. Measured on `main` at
`825bf61` on 2026-09-23, `catalog/sources/` holds 19 records, 17 `FETCHED` and 2 `NOT HELD`
(`cinp_kfm`, `sbc_lter_landsat_canopy`). Their `variables` lists hold 369 entries, each a bare
string, across 15 records; the other 4 records carry `variables: []`. Not one of the 19 carries
`license_stated_at` (PR #171), `site_key` (PR #189) or `citations` (PR #191), the three optional
fields the sources table gained on 2026-09-23; `coverage_spans` (#89) is not a field yet. The
one source with site records, `klingbeil_kelp_genotypes` (ten under `catalog/sites/`, PR #187),
keys them in `sites` and nowhere else.

The grill of 2026-09-21/22 sliced the `variables` change three ways — expand (#90), migrate (one
`catalog:` PR per record), contract (#182) — and left the migration with no order and no table
(#183). Eight issues, six of them open, sat on the milestone on 2026-09-23 with nothing to order
them by. This file is that table.

## What the review settled

Each point names where it was decided; none restates the rule it points at.

1. **`variables` means the named columns or fields of the source's data files.** #90, Decision.
   A document's phrases are not `variables`; they move verbatim to `measures` (row S3), and a
   non-tabular source has `variables: []`.
2. **A migration PR moves no notebook.** #90's failing test asserts that `build.py` renders no
   `variables`; measured 2026-09-23, no module under `src/kelpcatalog/` except `schema.py` names
   `variables`. So a `catalog:` PR that changes only the fields this table names moves nothing
   under `notebooks/`. A migration PR that does move a notebook reports the diff in its body
   rather than absorbing it (#183, Goal).
3. **`sccwrp_b08_rocky_reef`'s 13 phrases become column headers or `measures` depending on what
   its held files carry.** Whoever migrates it opens `data/raw/sccwrp_b08_rocky_reef/` (on
   2026-09-23: `685_B08RockyReef.pdf` and its manifest, two files) and says which in the PR (#183,
   Goal).
4. **The fills ride the migration, one touch per record — on #183's word, which #180
   disagrees with.** #183 (Goal) has each migration row carry the record's `license_stated_at`,
   `site_key`, `citations` and `coverage_spans` fills, "one touch per record, not four". #38's
   amendment of 2026-09-22 agrees for `license_stated_at`: "per record as re-entry". #180
   (Non-goals) places `citations` fills "per record, in the `catalog:` PR of whichever view
   renders it first", and #179 (The rule) has a finding quoted "because a view needs it", "never
   harvested in bulk" — a trigger no row here waits for. This file follows #183 and quotes both;
   the owner chose #183's bundling at the review of PR #192 on 2026-09-23 (the Parking-lot line,
   #5 issuecomment-5805925788, records the choice under it). `site_key` is filled where the
   sources table's `site_key` row admits it (`CONTEXT.md`). `coverage_spans` is 6.6's: its schema
   row S4 (#89) waits on #178 (6.6), so no migration row carries it and its fill on every record
   migrated here is a second touch — row P1, also 6.6's. Rows say which fields they carried when
   they merge.
5. **`measures` and findings-on-sources have no issue yet.** The shape #183 gives `measures` is
   `list[str]`, a document's phrases as printed, with the failing test that a non-string entry is
   a problem; findings on sources points at the rule #179 writes for references rather than
   restating it (#179, The rule, last sentence). Both are the owner's to file; the table says "to
   file".
6. **"One milestone is active at a time" is followed here by precedent, not by a recorded
   reading.** The Parking-lot line (#5 issuecomment-5686055147, 2026-09-15) asks which reading the
   sentence means, and nothing under `docs/` or on #5 answers it; the status line names the PRs
   that merged a schema row of an inactive milestone, and this file does the same and no more.

## Solution

Two queues and two closers. The schema queue lands one `CONTEXT.md` sources-table row per PR,
serial, with a cold re-read of the row between PRs (#90, #180 and #89 each say so); two of its
four rows are 6.6's. The migration queue re-enters one record per `catalog:` PR, filling every
field of that record the table names, in the order a first view needs them. #182 then contracts
the `variables` type, and #38 makes `license_stated_at` required. #17 runs whenever someone picks
it up.

## Slices

Rows are in work order within each part. Rows with no issue carry "to file" in the `#` column, as
`docs/prd/monitoring-sources.md` carried "—" until PR #151 filed its issues; this PR files none.
Two schema rows, #175 (`site_key`, PR #189) and #180 (`citations`, PR #191), merged before this
file existed and have no row.

The migration order is provisional: the owner's input for this PR left the first view undecided,
overriding the choice the triage comment on #183 (2026-09-23) records ("bed-state in Santa
Barbara County", with its own order), so the rows are ordered by what any first view needs — a
record with sites, citations and expanded `variables` first, then the records whose files key
rows by site, then the rest, then the four document records, three of which wait on row S3 (M12
waits on it only if settled point 3 falls to `measures`) — and the owner reorders when the first
view is named. A migration PR moves no
notebook, and one that does move a notebook reports it rather than absorbing it (settled point
2). Every migration row carries `license_stated_at`, because no record has it, and moves the
where-I-looked text out of its `license` value (#38, Done when); it carries `citations` on
settled point 4, as the sources table's `citations` row admits them. No migration row carries
`coverage_spans`: its schema row is 6.6's, so the fill is the second pass, row P1, also 6.6's.

### Part one: the schema queue

S2 and S4 belong to milestone 6.6 (the owner's decision at the review of PR #192, 2026-09-23),
because each waits on a 6.6 issue; they keep their place in the queue's order and are listed here
so the queue reads whole, and neither gates this milestone's close. #89 sits on milestone 6.4
today and moves to 6.6 when the owner moves it.

| order | # | slice | seam | note |
|---|---|---|---|---|
| S1 | [#90](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/90) | expand: a `variables` entry may be `{name, description, unit, file?}` | `RULES["sources"]`, `_type_ok`, the `variables` row, `add-source` step 3 | existing string-shaped records still validate; two `sbc_lter_*` cases where the EML's code lists contradict the held file are on the issue's comments |
| S2 | to file | findings on sources | `RULES["sources"]`, `_type_ok`, a sources-table row that points at #179's rule | after [#179](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/179) (6.6) has written the rule it points at; failing test as #179's, on the sources table; a 6.6 row |
| S3 | to file | `measures`: `list[str]`, a document's phrases as printed | `RULES["sources"]`, `_type_ok`, a new sources-table row, `add-source` step 3 | failing test: a non-string entry is a problem (#183, Goal); rows M13–M15 wait on it, and M12 if settled point 3 falls to `measures` |
| S4 | [#89](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/89) | `coverage_spans`, one entry per span the source states | `RULES["sources"]`, `_type_ok`, the sources table, `add-source` step 3 | `ready-for-human` until [#178](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/178) (6.6) merges, so it lands after this milestone's migration rows; the fills are row P1; a 6.6 row |

### Part two: the migration rows

One `catalog:` PR per row, filed as a record issue in the shape `docs/agents/issue-tracker.md`
("Record issues") gives one that enters a source, with the seam narrowed to the record, its fetch
script where a `site_key` entry names a stored file, and `add-source` step 3 as what drafts the
fields; as there, no failing test can be named — the gate checks the shape (S1's tests) and the
audit checks each entry against the source. The **held** column counts the files under
`data/raw/<id>/` on 2026-09-23 excluding manifests, because #90 makes `file` required on an entry
when the record holds more than one data file. The `variables` cells say nothing about `file`:
whether a zip counts as one file or as what it contains, and how a column that more than one held
file carries takes `file` — `calcofi` states five columns in both its files, `sio_shore_stations`
that no single archive carries all of its variables, and `pisco_kelp_forest` that its 76 names
are the union of seven tables' attributeNames, no table carrying all of them, 17 occurring in
more than one, and `size` stating "number" in one table and "centimeter" in another, which one
`unit` per entry cannot hold — are S1's to settle before M1 is filed (parked, #5
issuecomment-5805925619, corrected for pisco in the line under it). The **fills** column names
every field the record has to state in that PR.

| order | # | id | `variables` today | held | fills | note |
|---|---|---|---|---|---|---|
| M1 | to file | `klingbeil_kelp_genotypes` | 6 strings → maps | 1 (zip) | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables` | the only record whose `sites` is non-empty (ten site records, PR #187); columns the source never names and its undefined `999` stay out of `variables` (#90, Decision; #5 issuecomment-5761453102) |
| M2 | to file | `sbc_lter_bottom_temperature` | 5 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables` | the four `sbc_lter_*` rows share one EML vocabulary and run in the order the 6.3c table entered them; M2 and M3 were not checked for the code-list disagreement #90's comments record on M4 and M5 |
| M3 | to file | `sbc_lter_kelp_biomass` | 25 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables` | as M2 |
| M4 | to file | `sbc_lter_kelp_removal_cover` | 22 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables` | the EML's `SITE` and `TREATMENT` code lists contradict the held file (#90, comment of 2026-09-20); S1 says what the record states |
| M5 | to file | `sbc_lter_kelp_removal_density` | 24 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables` | the EML's `TREATMENT` code list contradicts the held file (#90, second comment); as M4 |
| M6 | to file | `pisco_kelp_forest` | 76 strings → maps | 8 (7 CSV, 1 PDF) | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables` | the 76 are the union of seven tables' attributeNames, as the record states; the site table is a held file |
| M7 | to file | `sio_shore_stations` | 16 strings → maps | 5 (zip) | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables` | one archive per station; `{file}` alone is the `site_key` form for a file that is one site's (`CONTEXT.md`, `site_key`) |
| M8 | to file | `calcofi` | 122 strings → maps | 2 | `license_stated_at`, `license` (the cleanup, #38), `site_key`, `citations`, `variables` | whether a per-cast position is "the coordinates of its sites" is parked (#5 issuecomment-5801732071); the fill says which reading it took; whether the record widens past one station is a separate question (`docs/prd/monitoring-sources.md`, Found while reviewing) |
| M9 | to file | `noaa_oni` | 4 strings → maps | 1 | `license_stated_at`, `license` (the cleanup, #38), `citations`, `variables` | `global`; no site to key |
| M10 | to file | `census_tiger_county_2025` | 18 strings → maps | 1 (zip) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `variables` | no site to key |
| M11 | to file | `cdfw_ds3135` | 7 strings → maps | 1 (zip) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `variables` | no site to key |
| M12 | to file | `sccwrp_b08_rocky_reef` | 13 strings → column headers or `measures` | 1 (PDF) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `variables` or `measures` | settled point 3: the migrating PR says which; placed after S3 because `measures` is the case that blocks |
| M13 | to file | `cdfw_kelp_esr` | 8 strings → `measures` | 7 (JSON, one per report page) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `measures` | a document record; `variables` becomes `[]`; after S3 |
| M14 | to file | `sccwrp_kelp_status_2016` | 14 strings → `measures` | 1 (PDF) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `measures` | as M13 |
| M15 | to file | `sccwrp_tr1289` | 9 strings → `measures` | 1 (PDF) | `license_stated_at`, `license` (the cleanup, #38), `citations`, `measures` | as M13 |

Four records get no migration row. `ccr_t14_165_5` is `FETCHED` with `variables: []` and nothing
to expand. `sccwrp_kelp_aerial` is `FETCHED` with `variables: []`, and whether its appendix
titles are its `variables` is open on the Parking lot (#5 issuecomment-5700763690, owner's call);
it gets a row if the owner says yes. `cinp_kfm` and `sbc_lter_landsat_canopy` are `NOT HELD`,
whose `variables` is the empty list by the sources table. #182 does not wait on them. What the
four still have to state — `license_stated_at`, with the where-I-looked text moved out of
`license`, and `citations` where the source prints one — is #38's fill work and lands in row C2.

### Part three: the closers, and the row outside the queue

| order | # | slice | blocked on | note |
|---|---|---|---|---|
| C1 | [#182](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/182) | contract: a bare-string `variables` entry is a problem | M1–M15 | closes when a count of bare-string `variables` entries on `main` reads zero; 369 on 2026-09-23 |
| C2 | [#38](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/38) | `license_stated_at` on the four records with no migration row, the where-I-looked text out of every `license` value, then required | M1–M15, for the required flag | closes when a count of records lacking `license_stated_at` on `main` reads zero, no `license` value carries where it was read, and the field is required (#38, Done when); 19 lacking on 2026-09-23 |
| P1 | to file | `coverage_spans` fills, one `catalog:` PR per record whose `coverage` quotes a span | S4 | a 6.6 row: the second touch of every record migrated here that quotes a span; one issue per record in Part two's shape, filed when S4 merges, which is when the records that quote a span are counted |
| X1 | [#17](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/17) | every CSV under `catalog/tables/` has a source record | nothing | outside the serial queue; may run at any time; `catalog/tables/` is empty on `main` today |

Issue #172 (`version`) is closed `wontfix` and has no row (its closing comment, 2026-09-23).

## Non-goals

No `CONTEXT.md` change. No issue filed or edited: S2 and S3 are the owner's to file, and the
migration rows are filed when 6.4 opens. No record edit and no notebook regenerated. 6.4 does not
become active by this file. No `version` field (#38, amendment; #172). No builder change: how a
view renders `measures`, findings or `coverage_spans` is 6.6's. Nothing here jumps 6.3c's queue
except the rows the status line names.

## Done

Rows S1 and S3 merged as sources-table rows; rows M1–M15 merged as `catalog:` PRs, each saying
which fields it carried and, for M12, which of the two forms its held file supported; C1 merged
with a count of bare-string `variables` entries on `main` at zero; C2 merged with
`license_stated_at` required, no record lacking it and no `license` value carrying where it was
read; X1 merged. S2, S4 and P1 are 6.6's and do not gate this milestone's close.

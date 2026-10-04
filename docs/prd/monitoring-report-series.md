# PRD — Monitoring report series (milestone 6.4c)

Status: not active. The PR for #258 created this file and did not open the milestone (#258,
Non-goals); opening it is the owner's. Which rows are open and which labels they carry is read from
GitHub, not from this file.
Created: 2026-10-04

## Problem

Milestone 6.4c was created on 2026-09-28 as an open intake for monitoring-program report series:
the owner expects to add to it (#258, "Why a new milestone rather than a track on an existing
one"). Its candidates arrived as leads from source reviews rather than from a held index, which is
what separates it from 6.4b, whose two tracks (#213, #214) are closed enumerations, and from 6.4d,
which enters datasets. #261, a dataset, left this milestone for 6.4d on 2026-09-28, so this
milestone holds reports only (#258 issuecomment-5878207037).

Four record issues were filed on this milestone ahead of this table, each saying it waits on #258:
#259 and #260, two installments of the City of San Diego's kelp forest monitoring reports by
Scripps Institution of Oceanography authors; #262, the City's monthly receiving-water reports for
its two ocean outfalls; and #283, the Channel Islands National Park Kelp Forest Monitoring
Program's annual reports, 1990–2015. All four are documents, so a record's content is its phrases
in `measures` and its `variables` is `[]` (`CONTEXT.md`, the `variables` and `measures` rows of
*sources/<id>.md*). On `main` at `b2a5306`, 0 of the 37 records in `catalog/sources/` carry a
non-empty `measures` or a non-empty `findings`.

Each of the four turns on the same question, which #258 names first and #213 asks for 6.4b: one
record per report, or one for the series. #213 names the precedents both ways and has not been
answered; #258 says that if this milestone runs first it settles the question and says so.
Reading 1 below does.

## What the review settled

Each is a reading of an existing rule or a ruling of the owner's, applied to this milestone's rows
and stated here so a slice does not re-derive it.

1. **One record per installment when the installments are distinct documents; one record per
   series when they are one template differing only in the period reported.** The owner's ruling
   of 2026-10-04, in the session that wrote this file. The test is what the fields would hold.
   Where installments differ only in the period they report, a record per installment would repeat
   one record with the period changed, and the series is one record. Where they differ in title,
   authors or what they report beyond the period, the record's `title` ("the source's own title"),
   `citations` and `coverage` differ in substance from one installment to the next, and each is a
   record: the `citations` row excludes a citation "for a part of that (a station, a file, an
   appendix)", so a series record could carry no installment's own citation. The precedent on
   `main` for an installment of a series as its own record is `sccwrp_kelp_status_2016`, the 2016
   installment of the "Status of the Kelp Beds" reports, whose series landing pages are a second
   record, `sccwrp_kelp_aerial`. The precedent for one record over several files under one landing
   page is 6.3c's Solution: "A collection with one landing page is one record whose `access` steps
   name each file" (`docs/prd/monitoring-sources.md`). This reading sorts the four filed issues as
   follows:
   - **The kelp forest reports are seven records.** The City's page lists seven installments under
     "Available Reports", with link texts that name three spans as "Biennial Report", two as "Final
     Report" and two as "Annual Report", over spans that overlap (#258 issuecomment-5878382525;
     re-measured 2026-10-04, rows 1–7). #259 and #260, the two installments measured, have
     different titles and authors.
   - **The monthly reports are a template.** Measured 2026-10-04 on two PLOO installments,
     `ploo_mwqr_jun_2026.pdf` and `ploo_mwqr_jul_2026.pdf`: with every number and month name
     masked, the text `review-source`'s `pdftext_literal.py` takes out of each scores 0.953 under
     Python's `difflib.SequenceMatcher` ratio. Two months of one outfall are the whole sample.
     They are two records, one per outfall, not one: each monthly report states one month's
     results for one outfall's stations, and the page groups them under its own headings:
     on 2026-10-04 its `h2` headings were "2026 Monthly Receiving Waters Monitoring Reports for the
     PLOO", the same for the SBOO, "PLOO Monthly Receiving Waters Monitoring Report Archives" and
     "SBOO Monthly Receiving Waters Monitoring Report Archives". The two families state results for
     different station sets (#262, "Why a kelp catalog wants it"), so they are distinct records by
     the content test 6.4d's reading 5 states for datasets. #262 is the PLOO record (row 8); the
     SBOO record is `to file` (row 9).
   - **The Channel Islands reports are 26 records**, one per year: each year is its own DataStore
     reference with its own `DisplayCitation`, two of them with their own DOIs (#283, "The series"
     and "Decisions this record cannot avoid"). #283 is the 1990 report
     (row 10); the other 25 are `to file` (rows 11–35).

   #213 is not edited here (#258, Non-goals). Its series question is the same one, and its rows
   will read this reading where the premise recurs.
2. **`steward` is the organisation that publishes the report; an author who is not that
   organisation goes in `access`.** `CONTEXT.md` defines `steward` as "the organisation that
   publishes or holds it". For the kelp forest reports, that is the City of San Diego and not
   Scripps Institution of Oceanography: the reports are listed on the City's page titled "San Diego
   Coastal Kelp Forest Ecosystem Monitoring", under its Public Utilities ocean monitoring section,
   and the 2023–2025 report states that it was "Submitted to City of San Diego Public Utilities
   Department" (#260). The precedent is `sccwrp_kelp_status_2016`, whose steward is the Southern
   California Coastal Water Research Project while its `access` states that the report was
   "Prepared by" MBC Applied Environmental Sciences. `docs/prd/monitoring-sources.md` reading 6
   separates a producer from a host that only holds a deposit; the City is not a host only here,
   because it publishes the series on its own program page. The four `sandiego_rtoms_*` records
   spell the steward `Public Utilities, City of San Diego`; a row spells it as that, unless its
   landing page names a different unit. The steward's own host is the route, so `FETCHED`'s first
   limb applies (`CONTEXT.md`, *Vocabularies*, **tier**). For #262 the City writes as well as
   publishes, so the question does not arise. For #283, the steward is the publisher as the
   DataStore reference names it; `cinp_kfm` spells the program's steward `Channel Islands National
   Park`.
3. **No `access` rule is needed for a file that no landing page links.** #258 asked for one. Its
   correction, issuecomment-5878382525, found the page, and on 2026-10-04 it answered HTTP 200 in
   149,754 bytes at
   `https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports/kelp-monitoring-report-archives`,
   linking all seven installments. Each row's `access` walks a reader from that page.
4. **No row waits on #198 or #208; `findings` is `[]` at entry.** #198 merged as PR #265 on
   2026-09-29 and #208 as PR #319 on 2026-10-04. The `findings` row of *sources/<id>.md* points
   at the `findings` row of *references/<citekey>.md*, whose last sentence reads: "An entry is
   quoted because a view needs it, in the `catalog:` PR of that view, and never harvested in bulk,
   so the field grows with use." So a row here enters `findings: []`, puts the report's phrases in
   `measures`, and does not plan to fill `findings` (PR #319 audit F1, posted on #258 as
   issuecomment-5983528887). A row that planned otherwise would need a `CONTEXT.md` change in its
   own PR first. Whether a dataset source can carry `findings` is parked at #5
   issuecomment-5983528322 and is not this milestone's question.
5. **6.3c's readings 2, 4, 5 and 6 carry over.** `docs/prd/monitoring-sources.md`, "What the
   review settled": reading 2 (a route that downloads enters `FETCHED`, with its proportionality
   clause), reading 4 (region tags follow the tagging sentence), reading 5 (a bare topic tag for a
   source that fits no sub-topic) and reading 6 (`steward`, as reading 2 above applies it). A row's
   PR cites them by number. Readings 1, 3, 7 and 8 decide the admission of datasets, papers,
   `ON REQUEST` sources and exclusions, and no row here turns on any of them.
6. **The methods paper is not a row.** The 2023–2025 report cites "Parnell et al. 2026" for the
   program's full methods; it is doi:10.1002/eap.70181 (#260 issuecomment-5878053618), a candidate
   on #214's track, and its dataset is `parnell_kelp_demography` on 6.4d. A row creates a
   `references/` record for it only if a field of that row needs one, as the Non-goals of #259 and
   #260 say.
7. **Extraction is a cost each kelp forest row carries.** The 2019–2024 and 2023–2025 PDFs use
   subset fonts whose text comes out only through each font's `/ToUnicode` CMap (#258, "A cost to
   name"); `.claude/skills/review-source/pdftext_cmap.py` decodes them. A row's `citations`
   `stated_at` names those steps where the text came out only by a tool, as the `citations` row
   requires. The five unmeasured installments may or may not share the cost; the row finds out.
8. **How a new candidate arrives.** As a comment on #258, open or closed, naming the series or
   installment, its landing page and what that page states about coverage; the owner files the row
   (`CLAUDE.md`, "How work is tracked"). The ground is the one 6.4d's reading 7 records for its own
   track. The comment says which half of reading 1 the candidate falls under.

## Solution

One record per installment or per series as reading 1 sorts it, entered through `add-source`. The
order is by distance to a settled precedent: the kelp forest reports first, because
`sccwrp_kelp_status_2016` is an installment of a series entered as its own record, beginning with
the two installments that have been fetched and measured (#260, #259) and then the other five in
the order the City's page lists them; then the two monthly-report records, PLOO first and SBOO
copying its shape, because each holds a run of monthly files and row 8 sets that shape; then the
Channel Islands reports, 1990 first because its file is the one #283 fetched, then by year.

## Slices

Issues #259, #260, #262 and #283 were filed ahead of this table, and their numbers are in the `#`
column; every other row is `to file`, the convention `docs/prd/re-entry.md`'s Slices intro gives
for a row whose issue does not exist yet. The rows are in work order. Each row is a record issue in
the shape `docs/agents/issue-tracker.md` gives them: `add-source` is the seam, there is no
mechanical failing test, and the notebooks the record's topics move land in the same PR. When the
PR that creates this file merges, the labels on #259, #260, #262 and #283 are the owner's to move,
and filing the `to file` rows is the owner's (`CLAUDE.md`, "How work is tracked").

A row whose seam is `add-source` is auto-merge eligible; every other row is not (`CLAUDE.md`,
"Auto-merge in a declared PRD run").

A new candidate for this track arrives as reading 8 states.

The **route** column is the lead, measured on the date given; a slice opens it at `add-source`
step 2 and enters what the page states that day, not what this table says. The **topics** and
**region today** columns are the issues' own proposals, which the row reads off the document;
nothing here settles them. The **id** column is the proposed id, which step 3 confirms. The kelp
forest ids are keyed to the span the City's link text gives each installment rather than to a
publication year, because two of the seven file names do not match their link text ("Biennial
Report: 2020-2021" is `KelpForest2022_FinalDraft.pdf`, "Annual Report: 2016-2017" is
`kelpforestfinalreport_2018.pdf`); that replaces the `sandiego_kelp_forest_2024` and
`sandiego_kelp_forest_2026` #259 and #260 proposed. A record's `title` is the title its document
prints, not the link text.

| order | # | id | source | route (lead) | topics | region today | note |
|---|---|---|---|---|---|---|---|
| 1 | [#260](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/260) | `sandiego_kelp_forest_2023_2025` | Kelp forest monitoring, "Biennial Report: 2023-2025" (Ladah et al., SIO), as the City's page labels it | the City's kelp forest page; `https://www.sandiego.gov/sites/default/files/2026-07/city-of-san-diego-kelp-forest-monitoring-biennial-report-final-version-2023-2025.pdf`, 9,616,297 bytes on 2026-09-28 (#260) | `bed-state/diver-surveys`, `bed-state/community`, `grazers-predators-competitors/urchins`, `ocean-climate/temperature` | `scb.mainland.san-diego` | readings 1–4 and 7; #260 counts `outfall` once in the text and advises against `water-quality-harvest/discharges-outfalls`; the PDF's info Title differs from its cover (#260) |
| 2 | [#259](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/259) | `sandiego_kelp_forest_2019_2024` | Kelp forest monitoring, "Final Report: 2019-2024" (Parnell, SIO) | the City's kelp forest page; `https://www.sandiego.gov/sites/default/files/2024-10/kelpforest2024_final.pdf`, 5,128,132 bytes on 2026-09-28 (#259) | `bed-state/diver-surveys`, `bed-state/community`, `grazers-predators-competitors/urchins`, `water-quality-harvest/discharges-outfalls`, `ocean-climate/temperature`, `ocean-climate/heatwaves` | `scb.mainland.san-diego` | as row 1; #259 quotes the sentence that supports the outfall tag |
| 3 | to file | `sandiego_kelp_forest_2020_2021` | Kelp forest monitoring, "Biennial Report: 2020-2021" | the City's kelp forest page; `https://www.sandiego.gov/sites/default/files/2024-02/KelpForest2022_FinalDraft.pdf` | read off the document; rows 1 and 2 are leads | `scb.mainland.san-diego`, if the document names no place outside the county | as row 1; the file name says 2022 and "FinalDraft" |
| 4 | to file | `sandiego_kelp_forest_2014_2019` | Kelp forest monitoring, "Final Report: 2014-2019" | the City's kelp forest page; `https://www.sandiego.gov/sites/default/files/kelpforest_finalreport_2014-2019.pdf` | as row 3 | as row 3 | as row 1 |
| 5 | to file | `sandiego_kelp_forest_2018_2019` | Kelp forest monitoring, "Biennial Report: 2018-2019" | the City's kelp forest page; the link is relative, `/sites/default/files/kelpforestfinalreport_2018-2019.pdf` | as row 3 | as row 3 | as row 1 |
| 6 | to file | `sandiego_kelp_forest_2016_2017` | Kelp forest monitoring, "Annual Report: 2016-2017" | the City's kelp forest page; relative link `/sites/default/files/kelpforestfinalreport_2018.pdf` | as row 3 | as row 3 | as row 1; the file name says 2018 |
| 7 | to file | `sandiego_kelp_forest_2015_2016` | Kelp forest monitoring, "Annual Report: 2015-2016" | the City's kelp forest page; relative link `/sites/default/files/kelpforestfinalreport_2016.pdf` | as row 3 | as row 3 | as row 1 |
| 8 | [#262](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/262) | `sandiego_mwqr_ploo` | Monthly receiving waters monitoring reports, Point Loma Ocean Outfall | `https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports/monthly-report-archives`, HTTP 200 in 190,386 bytes on 2026-10-04; the `ploo_mwqr_*` file names, 125 distinct, plus the legacy names the row assigns to this outfall | `water-quality-harvest/discharges-outfalls`, `ocean-climate/temperature`, `ocean-climate/nutrients` | `scb.mainland.san-diego` | reading 1 makes #262 the PLOO record, where its body asks for the series; which installments it holds is the subsetting paragraph's question, which #262 names; of the page's 269 distinct PDF hrefs on 2026-10-04, 198 began `http://www.sandiego.gov`, 10 `https://` and 61 were relative, where #262 counted 7 served over `http://`; #262 proposed `sandiego_mwqr` |
| 9 | to file | `sandiego_mwqr_sboo` | Monthly receiving waters monitoring reports, South Bay Ocean Outfall | the same page; the `sbwrp_mwqr_*` file names, 137 distinct, plus the legacy names the row assigns to this outfall | as row 8 | `scb.mainland.san-diego`, with #262's note on the three stations south of the border, which states and decides nothing about the boundary | as row 8; file after row 8 merges, copying its shape |
| 10 | [#283](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/283) | `cinp_kfm_report_1990` | Channel Islands National Park Kelp Forest Monitoring, 1990 annual report | NPS DataStore saved search 1508, its 1990 reference; holding 485218, `chis_kelp90.pdf`, 306,257 bytes on 2026-09-30 (#283) | `bed-state/diver-surveys`, `bed-state/community`, `bed-state/mpas`, `grazers-predators-competitors/urchins`; `ocean-climate/temperature` from the year the loggers appear | `scb.islands.anacapa`, `scb.islands.san-miguel`, `scb.islands.santa-barbara`, `scb.islands.santa-cruz`, `scb.islands.santa-rosa` | reading 1 makes #283 the 1990 record, where its body asks for the series; #283 proposed `cinp_kfm_annual_reports`; `steward` per reading 2 |
| 11 | to file | `cinp_kfm_report_1991` | as row 10, 1991 | saved search 1508, the 1991 reference | as row 10 | as row 10 | as row 10; file after row 10 merges, copying its shape |
| 12 | to file | `cinp_kfm_report_1992` | as row 10, 1992 | saved search 1508, the 1992 reference | as row 10 | as row 10 | as row 11 |
| 13 | to file | `cinp_kfm_report_1993` | as row 10, 1993 | saved search 1508, the 1993 reference | as row 10 | as row 10 | as row 11 |
| 14 | to file | `cinp_kfm_report_1994` | as row 10, 1994 | saved search 1508, the 1994 reference | as row 10 | as row 10 | as row 11 |
| 15 | to file | `cinp_kfm_report_1995` | as row 10, 1995 | saved search 1508, the 1995 reference | as row 10 | as row 10 | as row 11 |
| 16 | to file | `cinp_kfm_report_1996` | as row 10, 1996 | saved search 1508, the 1996 reference | as row 10 | as row 10 | as row 11 |
| 17 | to file | `cinp_kfm_report_1997` | as row 10, 1997 | saved search 1508, the 1997 reference | as row 10 | as row 10 | as row 11 |
| 18 | to file | `cinp_kfm_report_1998` | as row 10, 1998 | saved search 1508, the 1998 reference | as row 10 | as row 10 | as row 11 |
| 19 | to file | `cinp_kfm_report_1999` | as row 10, 1999 | saved search 1508, the 1999 reference | as row 10 | as row 10 | as row 11 |
| 20 | to file | `cinp_kfm_report_2000` | as row 10, 2000 | saved search 1508, the 2000 reference | as row 10 | as row 10 | as row 11 |
| 21 | to file | `cinp_kfm_report_2001` | as row 10, 2001 | saved search 1508, the 2001 reference | as row 10 | as row 10 | as row 11 |
| 22 | to file | `cinp_kfm_report_2002` | as row 10, 2002 | saved search 1508, the 2002 reference | as row 10 | as row 10 | as row 11 |
| 23 | to file | `cinp_kfm_report_2003` | as row 10, 2003 | saved search 1508, the 2003 reference | as row 10 | as row 10 | as row 11 |
| 24 | to file | `cinp_kfm_report_2004` | as row 10, 2004 | saved search 1508, the 2004 reference | as row 10 | as row 10 | as row 11 |
| 25 | to file | `cinp_kfm_report_2005` | as row 10, 2005 | saved search 1508, the 2005 reference | as row 10 | as row 10 | as row 11 |
| 26 | to file | `cinp_kfm_report_2006` | as row 10, 2006 | saved search 1508, the 2006 reference | as row 10 | as row 10 | as row 11; #283 says its citation prints its series line twice, entered as printed |
| 27 | to file | `cinp_kfm_report_2007` | as row 10, 2007 | saved search 1508, the 2007 reference | as row 10 | as row 10 | as row 11 |
| 28 | to file | `cinp_kfm_report_2008` | as row 10, 2008 | saved search 1508, the 2008 reference | as row 10 | as row 10 | as row 11 |
| 29 | to file | `cinp_kfm_report_2009` | as row 10, 2009 | saved search 1508, the 2009 reference | as row 10 | as row 10 | as row 11; #283 says its citation prints "NPS/ARCN/NRDS—2013/581", entered as printed |
| 30 | to file | `cinp_kfm_report_2010` | as row 10, 2010 | saved search 1508, the 2010 reference | as row 10 | as row 10 | as row 11 |
| 31 | to file | `cinp_kfm_report_2011` | as row 10, 2011 | saved search 1508, the 2011 reference | as row 10 | as row 10 | as row 11 |
| 32 | to file | `cinp_kfm_report_2012` | as row 10, 2012 | saved search 1508, the 2012 reference | as row 10 | as row 10 | as row 11 |
| 33 | to file | `cinp_kfm_report_2013` | as row 10, 2013 | saved search 1508, the 2013 reference, which #283 says holds two PDFs, a print copy and a Section 508 copy | as row 10 | as row 10 | as row 11; one record, and which copy it holds is the subsetting paragraph's question |
| 34 | to file | `cinp_kfm_report_2014` | as row 10, 2014 | saved search 1508, the 2014 reference, doi:10.36967/2293855; `Content-Length: 125003151` (#283) | as row 10 | as row 10 | as row 11; whether to hold it is 6.3c reading 2's proportionality clause, against the 137.46 MB `sandiego_rtoms_water_temperature` holds (`docs/prd/dataset-sources.md` reading 6) |
| 35 | to file | `cinp_kfm_report_2015` | as row 10, 2015 | saved search 1508, the 2015 reference, doi:10.36967/nrr-2288646; 128,949,906 bytes by its holding record (#283) | as row 10 | as row 10 | as row 34 |

The years in rows 11–35 are #283's count of 2026-09-30, one reference per year from 1990 to
2015. Row 10 re-counts the saved search at entry, and the rows after it are revised if the count
has changed.

**One candidate is named and not a row.** The South Bay monthly report points at "the City of San
Diego's most recent Biennial Receiving Waters Monitoring and Assessment Report for the Point Loma
and South Bay Ocean Outfalls" (#262; #258 issuecomment-5878053986). Nobody has fetched
it, so it is a candidate, and it arrives as reading 8 states.

**One link on the kelp forest page is not a candidate**: "Union Tribune: San Diego’s kelp forests
under threat", a newspaper article (#258 issuecomment-5878382525), recorded so that
nobody reviews it again.

## Non-goals

No record entered by the PR that creates this file, no fetch script, no reference record, no
notebook regenerated (#258). No issue filed by that PR; the `to file` rows are the owner's to file.
No second PRD file and no second Slices table for this milestone. No `CONTEXT.md` change; reading 1
reads the `title` and `citations` rows as they stand, and if it ever needs a rule, that is its own
PR. No edit to #213's or #214's tracks or rows, and no change to any existing record. No `sites/`
record for any row (#260, #262 and #283 each say so of themselves). That PR does not open the
milestone or make it active.

## Done

Every row whose issue is `ready-for-agent` merged as a record with the tier its route supports,
with its notebooks; each `to file` row filed and merged, or still `to file`.

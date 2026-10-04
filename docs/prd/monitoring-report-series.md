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
Reading 1 records the owner's answer for this milestone's rows.

## What the review settled

Each is a reading of an existing rule or a ruling of the owner's, applied to this milestone's rows
and stated here so a slice does not re-derive it.

1. **Series or installment: the owner's ruling of 2026-10-04**, recorded with the option text the
   owner chose at #258 issuecomment-5985079368: "One record per installment when installments are
   distinct documents (their own title page, authors, span) … One record per series when
   installments are one template differing only in reporting period." The option named its
   outcomes, which the owner chose with it: "Kelp: 7 rows (5 to file). #283: 26 rows. #262: one
   record per outfall family, PLOO and SBWRP (2 rows)." Each sort below rests on that ruling; the
   evidence beside it is what was measured, and a sort is not re-derived by a row.
   - **The kelp forest reports are seven records.** The City's page lists seven installments under
     "Available Reports", with link texts that name three spans as "Biennial Report", two as "Final
     Report" and two as "Annual Report", over spans that overlap (#258 issuecomment-5878382525;
     re-measured 2026-10-04, rows 1–7). #259 and #260 have different titles and authors. Three of
     the other five, 2016–2017, 2018–2019 and 2020–2021, print "Appendix A" on their first page
     (measured 2026-10-04), and the 2016–2017 one is listed as "Appendix A: Status and Trends of
     San Diego Kelp Forests, 2016–2017" in the contents of the City's 2016–2017 Biennial Receiving
     Waters Monitoring Report (audit of PR #320, F1). On the owner's second ruling at the same
     comment, each of the three is a record of the standalone PDF the kelp page links, its row
     says it prints "Appendix A" and which parent report it belongs to, and a parent report's
     record, if one is filed, says in
     `coverage` that it holds the report and not that appendix, as `sccwrp_kelp_status_2016`
     holds "the report and not its appendices" (`CONTEXT.md`, the subsetting paragraph).
   - **The monthly reports are two records, one per outfall.** The page groups them under its own
     headings: on 2026-10-04 its `h2` headings were "2026 Monthly Receiving Waters Monitoring
     Reports for the PLOO", the same for the SBOO, "PLOO Monthly Receiving Waters Monitoring
     Report Archives" and "SBOO Monthly Receiving Waters Monitoring Report Archives". The template
     evidence is two installments of one outfall, `ploo_mwqr_jun_2026.pdf` and
     `ploo_mwqr_jul_2026.pdf`: with digits, decimal points and English month names masked, the
     text `review-source`'s `pdftext_literal.py` takes out of each, about 6.4k characters of PDFs
     of 74 to 80 pages, scores 0.95 under Python's `difflib.SequenceMatcher` ratio. The audit of
     PR #320 (F6) measured the full text at 0.731 for the same pair and 0.385 for April 2015
     against July 2026, whose title and issuing unit differ. So the template claim holds for the
     2026 installments sampled and not, as measured, across the run; which installments each
     record holds is the subsetting paragraph's question, and the row states it in `coverage` and
     `access`. #262 is the PLOO record (row 8); the SBOO record is `to file` (row 9).
   - **The Channel Islands reports are 26 records**, one per year, the outcome the owner chose.
     Each year is its own DataStore reference with its own `DisplayCitation`, two of them with
     their own DOIs (#283, "The series" and "Decisions this record cannot avoid"); the audit of PR
     #320 (F2(b)) found the 1995–2004 citations differ in little but the year, so the 26 rest on
     the ruling's named outcome. #283 is the 1990 report (row 10); the other 25 are `to file`
     (rows 11–35).

   **Three departures this records.** 6.3c's Solution says "A collection with one landing page is
   one record whose `access` steps name each file" (`docs/prd/monitoring-sources.md`); read alone,
   that makes the seven kelp forest installments one record, and this milestone departs from it on
   the owner's ruling, as 6.4d's reading 5 records its own departure from the clause after it in
   the same sentence. The same clause makes the PLOO and SBOO families one record, since both sit
   under the one `monthly-report-archives` page, and the split departs from it. And the split is
   not the content test 6.4d's reading 5 states, which separates datasets whose files state
   different parameters: the two families report the same parameters at different stations, a case
   `sio_shore_stations` holds as one record. The split is the ruling's named outcome.
   `sccwrp_kelp_status_2016` is a precedent for an installment of a series entered as its own
   record, and for nothing finer. #213 is not edited here (#258, Non-goals); its rows may read this
   ruling as a precedent, and its question stays its own.
2. **`steward` is the producer**, 6.3c's reading 6 (`docs/prd/monitoring-sources.md`), applied to
   each series; this reading states no rule about authors in general.
   - **Kelp forest and monthly reports, rows 1–9: `Public Utilities, City of San Diego`**, as the
     four `sandiego_rtoms_*` records spell the department behind the same Ocean Monitoring
     Program. Not Scripps Institution of Oceanography: the kelp forest page states "Researchers at
     the Scripps Institution of Oceanography (SIO) have partnered with the City of San Diego Ocean
     Monitoring Program to conduct regular surveys of the kelp forests off San Diego County."
     (2026-10-04); the 2023–2025 report states that it was "Submitted to City of San Diego Public
     Utilities Department" (#260), the 2018–2019 report prints "Contract No. H146233", and the
     2016–2017 report is an appendix of the City's own biennial report (reading 1). The monthly
     index page names no producer, and the PLOO April 2015, June 2026 and July 2026 installments
     each print "Public Utilities Department" (audit of PR #320, R2-F3). For rows 1–7 this departs
     from 6.3c reading 6's "as the landing page names it", since the sentence quoted names the
     program as "City of San Diego Ocean Monitoring Program"; the department's string is taken so
     that one department has one spelling across the catalog. Each row states in `access` how its
     page and its installments name the program and the issuing unit, and rows 1–7 state SIO's
     authorship there. `sccwrp_kelp_status_2016` is not a precedent here: its steward is the
     Southern California Coastal Water Research Project, its host, while its `access` states it
     was "Prepared for" two consortia and "Prepared by" MBC Applied Environmental Sciences (audit
     of PR #320, F4).
   - **Channel Islands reports: `Channel Islands National Park`, for all 26.** The owner's third
     ruling at #258 issuecomment-5985079368, as `cinp_kfm` spells the same program. The landing
     page `https://www.nps.gov/im/medn/kelp-forest-communities.htm` is the NPS Mediterranean
     Coast Inventory & Monitoring Network's, as `cinp_kfm`'s `access` names it, not the park's;
     it states "The Kelp Forest Monitoring Program was established by Channel Islands National
     Park in 1982" (2026-10-04), and its "Monitoring Reports" link opens saved search 1508 (#283).
     The publisher each year's `DisplayCitation` names varies: the Cooperative National Park
     Resource Studies Unit at UC Davis for 1990–91, Channel Islands National Park for 1992–94,
     National Park Service for 2005–15, and for 1995–2004 no publisher, only the place "Ventura,
     California" (audit of PR #320, F3 and R2-F10). Each record states in `access` what its own
     citation prints, a place where that is all it prints.
   - **Which `FETCHED` limb a route is, this reading leaves open.** The kelp forest and monthly
     PDFs are on the City's host, and the Channel Islands PDFs are on irma.nps.gov, reached from
     the network's page; in each the host or page is run by a body the steward is a part of.
     Whether that is "A host the steward runs, or that a body constituting it runs", the first
     limb, or "A route the steward names as where the source is to be had", the second, or
     neither, is not settled here (`CONTEXT.md`, *Vocabularies*, **tier**). Row 1's PR states the
     limb for rows 1–9 and row 10's for rows 10–35, each with its ground, at `add-source` step 2;
     the rows that copy them are entered after.
3. **No `access` rule is needed for a file that no landing page links.** #258 asked for one. Its
   correction, issuecomment-5878382525, found the page, and on 2026-10-04 it answered HTTP 200 in
   149,754 bytes at
   `https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports/kelp-monitoring-report-archives`,
   linking all seven installments. Each kelp forest row's `access` walks a reader from that page.
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
7. **Extraction differs from one kelp forest installment to the next.** The 2019–2024 and
   2023–2025 PDFs use subset fonts whose text comes out only through each font's `/ToUnicode` CMap
   (#258, "A cost to name"); `.claude/skills/review-source/pdftext_cmap.py` decodes them. The audit
   of PR #320 (F7) found that `pdftext_literal.py` reads the 2020–2021 and 2016–2017 PDFs, and that
   the 2015–2016 PDF has no text layer, 0 `/Font` and 1,669 image XObjects, so neither tool
   returns text from it; row 7 says what that means for its quoted fields before it enters any.
   Measured 2026-10-04: on the 2018–2019 PDF (row 5) `pdftext_literal.py` returns 0 characters and
   `pdftext_cmap.py` 71,180 over 41 pages, with ligatures left as U+FB01 and U+FB00; on the
   2014–2019 PDF (row 4) `pdftext_literal.py` returns 3,739,430 characters, not checked for being
   text, and `pdftext_cmap.py` 471; pypdf 6.19.0's `extract_text` returns 70,706 and 61,366
   characters from the two, in that order, with prose readable on the sixth page of each, the one
   page sampled. A row's `citations` `stated_at` names the steps where the text came out only by a
   tool, as the `citations` row requires.
8. **How a new candidate arrives.** As a comment on #258, open or closed, naming the series or
   installment, its landing page and what that page states about coverage; the owner files the row
   (`CLAUDE.md`, "How work is tracked"). The ground is the one 6.4d's reading 7 records for its own
   track, and this resolves #5 issuecomment-5890391263 for this track and for no other. The
   comment says which half of reading 1's ruling the candidate falls under.

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
prints, not the link text. Rows 8 and 9 hold runs of installments whose printed titles differ; each
takes the title one installment prints, the row's PR names that installment, and its `access`
quotes the index page's heading for the family.

| order | # | id | source | route (lead) | topics | region today | note |
|---|---|---|---|---|---|---|---|
| 1 | [#260](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/260) | `sandiego_kelp_forest_2023_2025` | Kelp forest monitoring, "Biennial Report: 2023-2025" (Ladah et al., SIO), as the City's page labels it | the City's kelp forest page; `https://www.sandiego.gov/sites/default/files/2026-07/city-of-san-diego-kelp-forest-monitoring-biennial-report-final-version-2023-2025.pdf`, 9,616,297 bytes on 2026-09-28 (#260) | `bed-state/diver-surveys`, `bed-state/community`, `grazers-predators-competitors/urchins`, `ocean-climate/temperature` | `scb.mainland.san-diego` | readings 1–4 and 7; #260 counts `outfall` once in the text and advises against `water-quality-harvest/discharges-outfalls`; the PDF's info Title differs from its cover (#260) |
| 2 | [#259](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/259) | `sandiego_kelp_forest_2019_2024` | Kelp forest monitoring, "Final Report: 2019-2024" (Parnell, SIO) | the City's kelp forest page; `https://www.sandiego.gov/sites/default/files/2024-10/kelpforest2024_final.pdf`, 5,128,132 bytes on 2026-09-28 (#259) | `bed-state/diver-surveys`, `bed-state/community`, `grazers-predators-competitors/urchins`, `water-quality-harvest/discharges-outfalls`, `ocean-climate/temperature`, `ocean-climate/heatwaves` | `scb.mainland.san-diego` | as row 1; #259 quotes the sentence that supports the outfall tag |
| 3 | to file | `sandiego_kelp_forest_2020_2021` | Kelp forest monitoring, "Biennial Report: 2020-2021" | the City's kelp forest page; `https://www.sandiego.gov/sites/default/files/2024-02/KelpForest2022_FinalDraft.pdf` | read off the document; rows 1 and 2 are leads | `scb.mainland.san-diego`, if the document names no place outside the county | as row 1; the file name says 2022 and "FinalDraft"; its first page prints "Appendix A" (reading 1), and its parent is the "2020-2021 Report" the City's annual report archives page links, `compressed_2020-2021_biennial_receiving_waters_monitoring_report.pdf`, 38,157,298 bytes on 2026-10-04, whose contents list "Appendix A: Evaluation of Anthropogenic Impacts on the San Diego Coastal Kelp Forest" (PDF page 9) |
| 4 | to file | `sandiego_kelp_forest_2014_2019` | Kelp forest monitoring, "Final Report: 2014-2019" | the City's kelp forest page; `https://www.sandiego.gov/sites/default/files/kelpforest_finalreport_2014-2019.pdf` | as row 3 | as row 3 | as row 1 |
| 5 | to file | `sandiego_kelp_forest_2018_2019` | Kelp forest monitoring, "Biennial Report: 2018-2019" | the City's kelp forest page; the link is relative, `/sites/default/files/kelpforestfinalreport_2018-2019.pdf` | as row 3 | as row 3 | as row 1; its first page prints "Appendix A" and "Contract No. H146233" (reading 1), and its parent is the "2018-2019 Report" the City's annual report archives page links, `2018_2019_biennial_report_new.pdf`, 44,231,934 bytes on 2026-10-04, whose contents list "Appendix A: Evaluation of Anthropogenic Impacts on the San Diego Coastal Kelp Forest" (PDF page 8) |
| 6 | to file | `sandiego_kelp_forest_2016_2017` | Kelp forest monitoring, "Annual Report: 2016-2017" | the City's kelp forest page; relative link `/sites/default/files/kelpforestfinalreport_2018.pdf` | as row 3 | as row 3 | as row 1; the file name says 2018; "Appendix A" of the City's 2016–2017 Biennial Receiving Waters Monitoring Report, an installment of the series named as a candidate under the table (reading 1) |
| 7 | to file | `sandiego_kelp_forest_2015_2016` | Kelp forest monitoring, "Annual Report: 2015-2016" | the City's kelp forest page; relative link `/sites/default/files/kelpforestfinalreport_2016.pdf` | as row 3 | as row 3 | as row 1; the PDF has no text layer (reading 7) |
| 8 | [#262](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/262) | `sandiego_mwqr_ploo` | Monthly receiving waters monitoring reports, Point Loma Ocean Outfall | `https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports/monthly-report-archives`, HTTP 200 in 190,386 bytes on 2026-10-04; the `ploo_mwqr_*` file names, 125 distinct, plus the legacy names the row assigns to this outfall | `water-quality-harvest/discharges-outfalls`, `ocean-climate/temperature`, `ocean-climate/nutrients` | `scb.mainland.san-diego` | reading 1 makes #262 the PLOO record, where its body asks for the series; which installments it holds is the subsetting paragraph's question, which #262 names; of the page's 269 distinct PDF hrefs on 2026-10-04, 198 began `http://www.sandiego.gov`, 10 `https://` and 61 were relative, a different set from the 7 legacy-named files #262 counted as served over `http://`; #262 proposed `sandiego_mwqr` |
| 9 | to file | `sandiego_mwqr_sboo` | Monthly receiving waters monitoring reports, South Bay Ocean Outfall | the same page; the `sbwrp_mwqr_*` file names, 137 distinct, plus the legacy names the row assigns to this outfall | as row 8 | `scb.mainland.san-diego`, with #262's note on the three stations south of the border, which states and decides nothing about the boundary | as row 8; file after row 8 merges, copying its shape |
| 10 | [#283](https://github.com/cweber12/socal-bight-kelp-reference-catalog/issues/283) | `cinp_kfm_report_1990` | Channel Islands National Park Kelp Forest Monitoring, 1990 annual report | NPS DataStore saved search 1508, its 1990 reference; holding 485218, `chis_kelp90.pdf`, 306,257 bytes on 2026-09-30 (#283) | `bed-state/diver-surveys`, `bed-state/community`, `bed-state/mpas`, `grazers-predators-competitors/urchins`; `ocean-climate/temperature` from the year the loggers appear | `scb.islands.anacapa`, `scb.islands.san-miguel`, `scb.islands.santa-barbara`, `scb.islands.santa-cruz`, `scb.islands.santa-rosa` | reading 1 makes #283 the 1990 record, where its body asks for the series; #283 proposed `cinp_kfm_annual_reports`; `steward` `Channel Islands National Park` for this row and rows 11–35, each year's printed publisher in `access` (reading 2) |
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
| 34 | to file | `cinp_kfm_report_2014` | as row 10, 2014 | saved search 1508, the 2014 reference, doi:10.36967/2293855; `Content-Length: 125003151` (#283) | as row 10 | as row 10 | as row 11; whether to hold it is 6.3c reading 2's proportionality clause, against the eight CSVs `sandiego_rtoms_water_temperature` holds, 137.46 MB by the page's stated sizes (`docs/prd/dataset-sources.md` reading 6) |
| 35 | to file | `cinp_kfm_report_2015` | as row 10, 2015 | saved search 1508, the 2015 reference, doi:10.36967/nrr-2288646; 128,949,906 bytes by its holding record (#283) | as row 10 | as row 10 | as row 34 |

The years in rows 11–35 are #283's count of 2026-09-30, one reference per year from 1990 to
2015. Row 10 re-counts the saved search at entry, and the rows after it are revised if the count
has changed.

**One candidate is named and not a row.** The South Bay monthly report points at "the City of San
Diego's most recent Biennial Receiving Waters Monitoring and Assessment Report for the Point Loma
and South Bay Ocean Outfalls" (#262; #258 issuecomment-5878053986). It is a series of its own,
and it overlaps this table: its 2016–2017, 2018–2019 and 2020–2021 installments carry rows 6, 5
and 3 as their Appendix A (rows 3, 5 and 6). No review has judged the series as a candidate; it
arrives as reading 8 states, and a record of an installment says what reading 1 says a parent
report's record says.

**One link on the kelp forest page is not a candidate**: "Union Tribune: San Diego’s kelp forests
under threat", a newspaper article (#258 issuecomment-5878382525), recorded so that
nobody reviews it again.

## Non-goals

No record entered by the PR that creates this file, no fetch script, no reference record, no
notebook regenerated (#258). No issue filed by that PR; the `to file` rows are the owner's to file.
No second PRD file and no second Slices table for this milestone. No `CONTEXT.md` change; reading 1
records a ruling for this milestone's rows, and if it ever needs a rule, that is its own PR. No
edit to #213's or #214's tracks or rows, and no change to any existing record. No `sites/` record
for any row (#260, #262 and #283 each say so of themselves). That PR does not open the
milestone or make it active.

## Done

Every row whose issue is `ready-for-agent` merged as a record with the tier its route supports,
with its notebooks; each `to file` row filed and merged, or still `to file`.

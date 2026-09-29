---
name: review-source
description: Use when a link, DOI or citation arrives and nobody has decided whether it belongs in the SoCal Bight kelp reference catalog, or where. Invoked as /review-source <url-or-doi>. Normalises the input, de-duplicates against the tree and the tracker, identifies the thing from machine metadata, probes its route, judges scope then region then topics, returns one of four verdicts with a destination derived from the tracker, and drafts what the verdict needs. Files nothing; sits before add-source, which assumes the decision is made.
---

# review-source

Decide **whether** one candidate belongs in the catalog and **where**, and stop. `add-source`
(`.claude/skills/add-source/SKILL.md`) enters a source; it assumes someone has already decided the
source is one. This skill is that someone. It writes nothing a gate reads: its output is a review
note under `Claude outputs/` (git-ignored), a drafted Parking-lot line, and, for a candidate that
should be entered, a drafted issue body. It opens no branch, because it touches no tracked file.

`CONTEXT.md` is the authority for what is admitted and how it is tagged. This file points at its
sections and restates none of them: a second copy of a rule drifts, and no gate compares the two
(`CLAUDE.md`, "Changing a rule in `CONTEXT.md`"). Where a step below says "read" a section, read
it at that step, not from memory.

Do the eight steps **0–7 in order**. Stop at the first that cannot be answered and say which, what
it found, and what is written so far. The steps generalise a review of thirteen candidates on
2026-09-27/28 (`Claude outputs/source-review-2026-09-28.md`, git-ignored, on the owner's machine),
and *What this skill has not seen* at the end says what that sample did not contain.

## 0. Read first

Read, in `CONTEXT.md`: *Purpose*; *The rule* and its table of what is admitted and excluded;
*Vocabularies*, the **status** and **tier** entries, and the **regions** entry, which holds the
region-tagging sentence; *Topics: the ten questions*, both tables, and its closing paragraph, which
holds the admission sentence; *Record schemas*, the `sources/<id>.md` table, the
`excluded/<slug>.md` section and the last paragraph of `human-tasks/<id>.md`, which says what a
candidate nobody has entered is; and *What is not a record*.

Then `docs/agents/issue-tracker.md` whole: it gives the forms for reading the tracker, and
"Ideas are not issues" is where step 6 sends two of the four verdicts, and where step 7's one-line
drafts go.

Write down today's date. Every count and status code this skill records is stated as of it.

## 1. Normalise the input

Reduce what arrived to the identifier the steward or publisher issued, and record both forms.

- A DOI arrives wrapped: `https://doi.org/`, `dx.doi.org/`, a publisher's `/doi/abs/`, `/doi/pdf/`,
  `/doi/full/`. Keep the bare DOI (`10.` followed by the registrant and suffix) and the wrapper.
- A search engine or reader wraps the URL: `google.com/url?q=`,
  `scholar.google.com/scholar_url?url=`, a reader-mode or proxy prefix. Unwrap it.
- Tracking parameters go: `utm_*`, `fbclid`, `casa_token`, `sessionid` and their like. A query
  string that selects content stays: an ERDDAP query, an ArcGIS layer id, a `?item=` on an order
  page are the identifier, not tracking.
- A shortener resolves: fetch it, record the final URL, and review that. In the thirteen, a
  `bit.ly` link hid an ArcGIS Experience application whose web maps named the layers of interest.
- A citation with no link becomes a DOI search on Crossref (step 3) before anything else.

Write down: the input as it arrived, the normalised form, and, for a DOI, the bare DOI. Step 2
searches for the normalised forms; step 7 records both.

## 2. De-duplicate

Four places — the working tree, the earlier review notes, the Parking lot, the open issues — and
the counts go in the review note with the command that produced each. Search for the bare DOI,
the host and path, the host's name, one distinctive title word, and the steward's name, each as
its own term. Where the steward is an affiliation the page prints rather than the host, that name
is a step-3 output: run it once step 3 has given it, and record it under this step's counts (on
2026-09-29 the host's name and the title words ran first, and three investigators' and two
institutions' names after).

**The working tree.** Run the two searches `add-source` step 1 gives, and widen the path list to
the whole tree: a candidate can already be a lead in a PRD.

**The earlier review notes.** `git grep` skips `Claude outputs/`, which is git-ignored, and that
directory is where a candidate already reviewed and not filed anywhere is written down. Read each
file there in Python and count the terms, as for the two dumps below. A clone without the
directory has nothing to read here; say so in the note rather than skipping the line.

**The Parking lot and the open issues.** Dump both whole to the session scratchpad and count in
Python — never with a shell pipeline (*Hazards* below). The pinned Parking-lot issue's number is
in `docs/agents/issue-tracker.md`, "Ideas are not issues".

```sh
gh issue view <parking-lot number> --json comments -q '.comments[].body' \
  > <scratchpad>/parking-lot.txt
gh issue list --state open --limit 200 --json number,title,body,comments \
  > <scratchpad>/open-issues.json
```

Count each search term in each file with `str.count` over the whole text, and print the term and
its count on one line. A count of zero for a term is a finding only when the file's byte count
printed beside it is what the dump wrote: a stale file at a different path gave a count wrong by a
factor of three in the thirteen (*Hazards*). Read every hit: a term with a non-zero count is a line
to open, not a number to report.

**STOP if a hit is this candidate.** Name the file or comment and the matching line. A record
means the answer is `add-source`'s update path, not this skill; a parked line means the review
already happened, and the question is what has changed since; an open issue means it is filed, and
the review note says so. In the thirteen the one hit came from the open issues — a lead already
recorded on two of them — and none from the tree or the Parking lot, so the first two stops have
never fired; see *What this skill has not seen*.

## 3. Identify

Establish what the thing is — title, authors or steward, date, licence as published, type, stated
geography, and what it holds — from **machine metadata before the rendered page**. In the
thirteen, the human page was the least reliable route: a 403, a 202 with a zero-byte body, a
paywalled stub and a 303 to an identity provider. Try the rungs in this order and stop at the
first that answers with metadata; record which one did and what the ones above it returned. Of
the two datasets whose machine metadata this skill's sample obtained, one had it in its page
(BCO-DMO 709181, 2026-09-29) and one in a repository API (the Dryad deposit of 2026-09-28, whose
page rung 6 says 403s). So for a dataset whose page serves structured data, rung 2 is tried early
and does not end the ladder: run rung 1 as well and record what each returned. If step 2 found a
record on the same host, read its `access` steps before probing: they are a dated observation of
that host's route for one source, the probe run today is the fact, and where the two differ the
note says so. `bcodmo_839175`'s fourth `access` step records its file's S3 `ETag` and its MD5 as
the same 32 characters; 709181's ETag is a multipart one (2026-09-29). The record's values were
its file's, and the generalisation was a start prompt's.

1. **Crossref**, for a DOI: `https://api.crossref.org/works/<doi>` to the honest User-Agent. Full
   metadata, abstract and licence URLs. It answered when the publisher's own page sent a 303 to an
   identity provider and when another answered 403.
2. **The page's structured data**, for a dataset whose page serves it: the schema.org `Dataset`
   JSON-LD in the landing HTML, an ISO 19115 or EML document the page links, a service's `.das`.
   For BCO-DMO 709181 on 2026-09-29 the JSON-LD, the Next.js payload behind it, `/iso` and
   `/description` carried the licence text, the data file's stated MD5 and byte count, fifteen
   variables with descriptions and units, both citation forms and the supplemental files' MD5s.
   Crossref (rung 1) had answered first, with less — and with what only it carried: the funder,
   two award numbers, the registration dates and the Crossref member, which the run's scope test
   1 rested on. One dataset's ordering, on one host.
3. **OAI-PMH**, for a repository item. eScholarship's form is
   `https://escholarship.org/oai?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:escholarship.org:ark:/13030/qt<id>`,
   colon-delimited; the slash form errors `idDoesNotExist`. It served full Dublin Core to the
   honest User-Agent while the item page answered 403 and, to a browser, 202 with no body.
4. **The publisher's XML**, where one is offered: Pensoft's `/article/<id>/download/xml/` gave
   clean JATS where the landing page was a shell.
5. **PMC**, when the publisher is walled: `https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/` served
   the full text where ACS and Wiley each answered 403. Its `/pdf/` path is not the PDF (step 4).
   PMC serves under a PMCID rather than an identifier the publisher issued, so whether it is one
   of `FETCHED`'s routes (`CONTEXT.md`, *Vocabularies*, tier) is **undecided**; the review note
   says so rather than settling it, and a candidate reachable only through PMC is a *park* or an
   *add* whose issue body carries the question, not an *add* that assumes an answer.
6. **A repository's API.** Dryad's `https://datadryad.org/api/v2/datasets/doi%3A<doi>` returned
   licence, version, size and a download href to the honest User-Agent; the page links 403 by
   `robots.txt`.
7. **OpenAlex**, for open-access locations. It answered 429 on two of two attempts in the
   thirteen; best effort, and its version labels are to be confirmed before they are quoted.
8. **The PDF's own info dictionary and XMP.** For an image-only PDF with no extractable text, this
   gave the title and producer; the extractors below give the rest of a PDF.
9. **The rendered page**, last for a document, and read with step 4's probe rather than a browser,
   so that what it served is a record and not an impression. A dataset's page was read at rung 2
   for its structured data; what its rendered text prints — labels, roles, the licence label —
   is read here through the same probe.

**A PDF in hand** is read with the two extractors bundled beside this file, which take the PDF path
and write `<path>.txt` beside it. Try the literal one first:

```sh
.venv/Scripts/python .claude/skills/review-source/pdftext_literal.py <path.pdf>
.venv/Scripts/python .claude/skills/review-source/pdftext_cmap.py <path.pdf>
```

`pdftext_literal.py` reads content streams carrying literal strings and returned 11 pages from a
Springer PDF. `pdftext_cmap.py` decodes glyph-index strings through each font's `/ToUnicode` CMap
and is for the PDF on which the literal one printed `PAGES 0`: it returned 62 pages from a City of
San Diego report whose fonts are subset. A PDF that is image only returns nothing from either, and
that is the finding. Count terms in the `.txt` in Python, and write extracted text to a file
rather than the console (*Hazards*).

**One link can carry several candidates.** A paper, the dataset its data-availability statement
names, and the code repository beside it are three things with three routes and three verdicts. A
project report that states activities and names the data pages it reports on is the route to a
dataset, not the source. Separate them here and rank them, in two cases. What the input itself
is — those three — gets its own line through steps 4–7; on 2026-09-28 the paper and the Dryad
deposit behind it were separated that way, reaching #261 and a comment on #214
(`Claude outputs/source-review-2026-09-28.md`, §11). What the input merely links — another
dataset on the same project or deployment page — is not a candidate this run judges, so step 6
does not reach it: the set is not carried through steps 4–7, and the note records it as
identified only. The run may identify the one nearest the input's question to its machine
metadata, by whichever rung answers, and says which and why: on 2026-09-29 the deployment page of
BCO-DMO 709181 linked 8 datasets and its project page 11, the 8 among the 11 and the input among
both, so ten linked datasets, all ten drafted into one Parking-lot line naming each by id and
title, and one of the ten (707078, the same sites and span) identified to its JSON-LD first.
Where an issue for the input already exists, that line is a comment on its thread instead — step
6's *not a source* destination — as #267's comment of 2026-09-29 did for a project's five other
datasets. An index page whose links are the installments of one series is the input's own content
and not a linked set: the 2026-09-28 note's §12 read seven reports as one series record (#262).
The line between the two cases is the relation to the input, not a count.

## 4. Evidence the route

Probe the URL that would be the source's `access` step with the bundled probe, which fetches it
twice and prints the fixed record:

```sh
.venv/Scripts/python .claude/skills/review-source/probe.py <url> [--save <scratchpad>/<name>]
```

The record, per fetch: the URL asked for · final URL after redirects · status · bytes ·
`Content-Type` · first 8 bytes, hex and ASCII · `Content-Disposition` · `Last-Modified` ·
`ETag` · sha256. Then `same_final_url` and `same_sha256` across the two fetches. Paste the whole
JSON into the review note; do not summarise it to a status code.

**Read the bytes, not the status.** A 2xx status was wrong about content four times in the
thirteen: PMC's `/pdf/` path served 1,816 bytes beginning `<htm`; a university search page echoed
the query 986 times whichever query was sent; a repository item page answered 202 with 0 bytes; a
ProQuest preview carried no abstract. The probe shows each of those in `content_type` and
`first_8_ascii`, and a `.pdf` URL whose first bytes are not `%PDF-` did not serve a PDF, whatever
the status. A route also changes day to day: a Springer PDF URL that served 2,822,182 bytes on
2026-09-28 served a 3,038-byte "Client Challenge" page on 2026-09-29 to two User-Agents. Date
every probe.

**Two fetches tell apart two cases that one fetch cannot.** A final URL carrying a per-request
token while the bytes stay identical — `same_final_url` false, `same_sha256` true — is a stable
file behind an unstable address. An archive whose bytes vary per request — `same_sha256` false —
is a file whose members must be verified rather than the archive: Dryad's version download is
one. Record which.

**The User-Agent is part of the finding.** The default names this skill, as the fetch scripts
under `src/fetch/` name their source (23 of 23 on `main`, 2026-09-29). When a route answers
differently to a different string, run the probe once per string with `--ua` and record both:
eScholarship's three routes answered differently to two strings, and the table of which answered
what is the reusable result.

What the probe shows is what an `access` step would state, and which row of `add-source` step 2's
table the facts support. Do not decide the row here; write the facts into the issue draft (step
7) and let entry decide. The **status** entry of `CONTEXT.md`, *Vocabularies*, says what a
landing page's answer does not establish, so probe the file URL where one exists, and the page as
well.

## 5. Judge: scope, then region, then topics

In that order, because the order is what keeps the third from deciding the first.

**Scope.** The admission sentence, `CONTEXT.md`, *Topics: the ten questions*, closing paragraph,
names the tests a source passes together. For each test write one line: the evidence from step 3
or 4, and pass or fail. Evidence for the first test is who issued the thing and in what capacity
— a steward's own monitoring report, a journal of record, an agency's data service — and against
it, in the thirteen, a consumer-facing website and a newspaper article. Evidence for the third is
which of the ten questions the thing answers, and the sentence in it that answers that question;
against it, in the thirteen, a textbook whose metadata page named no Bight place and no kelp, a
project's activity log and a case study of a data pipeline, each answering none.

**Region.** The tagging sentence, `CONTEXT.md`, *Vocabularies*, regions, gives the cases. The
evidence is the stated geography from step 3 and the extracted text: count the place names in
Python and quote each sentence that states an extent — a source can state more than one, and the
note quotes each rather than choosing; what `coverage` does with two statements at entry is
decided and not yet written into `CONTEXT.md` (#204, open on 2026-09-29, milestone 6.4). Write
the tag the sentences' case gives and which case, saying whether each stated extent gives the same
one (BCO-DMO 709181 stated two on 2026-09-29 — a box in three documents and an ERDDAP
`actual_range` — and its file's rows, a measurement rather than a statement, lay outside the box;
box, range and rows all fell in one county), or that the stated bound lies outside the tree and
the source has no regional bound either. In the thirteen a study collected in one
named city was read under the smallest-containing-node case, a three-state index under the
wider-than-Bight case with its tags left open for entry, and a report sampling stations on both
sides of the international border was noted for the boundary question it raises.

**Topics.** The two tables in *Topics: the ten questions*. List the tags the thing would carry
and, for each, the sentence in the source that supports it: a tag supported by one hit in a
bibliography title is the pattern an open issue exists to correct on one existing record. **A fit
to no topic changes nothing above.** The section's closing paragraph says what happens then; the
verdict stays what scope made it, and the review note names the missing tag as the gap. Where a
tag is ambiguous between two sub-topics, the bare topic is the rule-compliant answer and the note
says why.

## 6. Verdict and destination

One of four, written with the step-5 line that decided it.

| verdict | what it means | destination |
|---|---|---|
| **add** | passes scope; a record can be drafted from what steps 3–4 established. Where the track it lands on is blocked, the note names the blocker — the *add but blocked* of the line that proposed this skill, folded into the derivation | derived below |
| **park** | passes scope on what it is about, and entering it today would be premature: no open copy and the open page states too little to fill a record; it would be the first of a kind the repo has no shape for yet; or a rule question decides its tier | the Parking lot, one line naming what would change the verdict |
| **decline** | fails the scope test, or passed it and fails on its own merits | the Parking lot, one line, so nobody re-reviews it; see below for `excluded/` |
| **not a source** | not a candidate for a record, but evidence about something the tracker or a record already carries — a citation for a parked question, a document that is the route to a dataset | the thread or record it is evidence about; the draft is a comment |

**Which declines get an entry in `catalog/excluded/`** is decided by `CONTEXT.md`, *Record
schemas*, `excluded/<slug>.md`, and by the decision #207 was filed to put there, while that issue
is open. Read both before drafting one; two of the thirteen were nearly routed there against that
decision. The thirteen held no decline that got one; the one record in `catalog/excluded/` on
`main` on 2026-09-29 is the precedent.

**The destination for an *add* is derived from the tracker, never listed here.** Destinations
moved three times in the two days of the thirteen, so a milestone written into this file is stale
within a week. Derive it every time:

1. List the milestones with the form under "Milestones themselves" in
   `docs/agents/issue-tracker.md`, and keep the open ones.
2. For each open milestone, find its PRD: a file under `docs/prd/`, whose `Status:` line (it
   begins on line 3 and wraps) the note records; or, where no file exists yet, the open
   `docs(prd):` issue or issues on that milestone (`gh issue list --milestone "<name>"`). A
   milestone with neither is not a destination. Read the prose of each track: what kind of source
   it admits, and what it says it does not reach.
3. Decide the candidate's kind from what its record would hold — the `variables` and `measures`
   rows of the `sources/<id>.md` table in `CONTEXT.md`, *Record schemas*, say what a dataset and a
   document each carry — and match it to the track that admits that kind. Where two tracks admit
   the kind, their own prose separates them; the note quotes the sentence that did.
4. How a track takes a new candidate — a row of its table, for which step 7 drafts an issue body,
   or a comment on its PRD issue, for which step 7 drafts the comment — is not something to read
   off the PRD: the four PRD issues open on 2026-09-29 each describe rows, and the review's
   candidates for one of them arrived as a comment because its rows were blocked. Read how the
   last candidate arrived on that track, draft that form, and say in the note that the form was
   inferred.
5. If no open milestone admits the kind, the destination is the Parking lot and the note says a
   milestone is wanted. Creating one is the owner's (`CLAUDE.md`, "How work is tracked").

Write the derivation into the note: the milestones listed, the status line read, the track
matched and why. A destination with no derivation beside it is a guess.

## 7. Record and stop

Append to `Claude outputs/source-review-<YYYY-MM-DD>.md` one section for the candidate: the
citation as the metadata gives it; the input and its normalised form; the step-2 counts with
their commands and the file byte counts; the identity rung that answered and what the rungs above
it returned; the step-4 JSON whole, dated; the three step-5 lines; the verdict and the derivation
of its destination; and the drafts below. Numbers are stated with the date they were measured and
nothing is carried over from an earlier note.

Then draft, into that note or a file beside it:

- **The Parking-lot line**, one line, in the form "Ideas are not issues" gives, for every verdict
  but *add* — and for an *add* too where a question came up that the issue body should not carry,
  or where step 3 set aside what the input merely links: that line is one of these.
- **The issue body**, for an *add* whose track takes rows, in the shape "Record issues" in
  `docs/agents/issue-tracker.md` gives: seam, the failing test it cannot name, acceptance,
  non-goals. Its body carries the step-4 facts, the step-5 lines, and any open question — PMC as a
  route, a licence not stated, a boundary the region tree does not draw — as a question, not as a
  choice made for the row.
- **The comment**, for an *add* whose track takes comments and for a *not a source*.

**File nothing.** No `gh issue create`, no `gh issue comment`, no record, no branch, no commit.
What a candidate nobody has entered is, and where it lives, is the last paragraph of
`human-tasks/<id>.md` in `CONTEXT.md`, *Record schemas*; putting it there is the owner's
(`CLAUDE.md`, "How work is tracked"). Print the verdict, the destination with its derivation, and
every draft in full, then **stop**.

## What this skill has not seen

Thirteen candidates, reviewed on two days, and the sample is lopsided. Each line below is a step
whose text above was written without an example of the case it names.

- **De-duplication hit once, in the open issues, and never in the tree or the Parking lot.** Step
  2's stops for a record and for a parked line are untested.
- **No `ON REQUEST` case, and no `human_task` entry.** A thesis available only by order was parked
  rather than entered, in part because the registry an `H<n>` id would live in is itself parked.
- **No source that needed a new topic or sub-topic.** Step 5's "fit to no topic" line has not run.
- **No linked paper.** Of the links the two notes set aside, zero were a paper of the same project
  as the input: the sets were datasets on a project or deployment page and the installments of one
  report series, and the 709181 page prints "No Related Publications" (2026-09-29). Step 3's
  two cases have no example of one.
- **Two datasets walked end to end**, through Dryad's API (2026-09-28) and a BCO-DMO page
  (2026-09-29, `Claude outputs/source-review-2026-09-29.md`). No EDI/DataONE candidate, and the
  one ArcGIS FeatureServer named was not walked; an ERDDAP answered a `.das` and two `distinct()`
  queries on 2026-09-29 — the first 400, `Unrecognized variable="lat"`, because it renames the
  CSV's columns; the second 200 — and was not walked as the route: these are the routes where
  `variables`, `site_key` and subsetting bite.
- **No decline that passed the scope test**, so the `excluded/` branch of step 6 rests on one
  record entered outside this skill.
- **Three of the thirteen named a dataset** — a FeatureServer, a Dryad deposit, two mooring data
  pages — and one was walked; the rest were documents. The identity ladder is ranked by how
  document routes performed; one dataset, on 2026-09-29, ordered differently, and rung 2 is that
  one instance.

## Hazards on the owner's machine

- **Bash `/tmp` is `%LOCALAPPDATA%\Temp`, not `c:\tmp`.** A stale file at `c:\tmp` gave a count
  wrong by a factor of three. Write and read by the same absolute path in the session scratchpad.
- **`grep` can return an empty string that reads as zero, and can abort** (exit 134) on a
  151 KB file. Count in Python, from a file, and print the byte count beside the counts.
- **The console codepage is cp1252.** Printing extracted text with `—`, `–` or a thin space
  raises `UnicodeEncodeError` mid-script. Write to a file, or encode `ascii` with `replace`.
- **Multi-line content goes to a file with an editor tool** (`CLAUDE.md`, "Branches, commits,
  PRs"). Backticks inside a `python -c "…"` string are evaluated by bash first.
- **`.venv/Scripts/python`, not bare `python`**, for the extractors, the probe and the counts.

## Non-goals

No record, no reference record, no exclusion record: entering is `add-source`'s, and an
`excluded/` entry arrives in its own PR. No issue, comment, label or milestone. No Parking-lot
sweep: the dump in step 2 is read for this candidate's terms and nothing else. No change to
`CONTEXT.md`, to `add-source`, to `gate.py` or to `pyproject.toml`. No subagent: this needs
measurement, not independence, so it runs inline. No decision on the `review-source` →
`add-source` handoff beyond the drafts step 7 makes. More than one candidate is more than one run
of steps 1–7, in one note.

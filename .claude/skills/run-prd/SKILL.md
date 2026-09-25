---
name: run-prd
description: Use when driving one milestone's PRD as a run in the SoCal Bight kelp reference catalog. Invoked as /run-prd docs/prd/<slug>.md. Derives that PRD's work order from its tables of rows, recovers each row's state from GitHub, and writes the order to the ledger. It reads only — it dispatches nothing, branches nothing and merges nothing.
disable-model-invocation: true
---

# run-prd

Derive **one** PRD's work order and write it down where compaction cannot reach it. A controller's
first job is to know the order. Here that order is the PRD's **Slices** table, and which row is next
follows from it: `CLAUDE.md`, "How work is tracked", and `docs/agents/issue-tracker.md`,
"Conventions".

This is the controller's read-only half. It dispatches nothing — no agent, no branch, no worktree,
no PR, no merge. Dispatching a record row is #228, review and merge are #229, a code row is #230.

Do the four steps **1–4 in order**. **Stop at the first one that cannot be answered from the repo
and the tracker**: say which step, what it found, and what you have derived so far, then wait. Never
make a step pass by picking between two readings of a rule — a stop here is cheap and a wrong order
is not.

## 0. Take the argument

`/run-prd docs/prd/<slug>.md`, one file. **STOP** if the argument names no file under `docs/prd/`.
Do not guess which PRD was meant, and do not run against more than one.

## 1. Read the PRD once, whole

Read the file rather than searching it. A search returns a row and loses the intro that governs it,
and the intro is where this repo keeps the freezes, the declarations and the exceptions.

- **The `Status:` line.** It begins on line 3 in all five files under `docs/prd/` today and wraps
  over several lines. **Report it; do not rule on it.** A file whose status says "not active" can
  still hold a track that runs beside the active milestone, and the track's own prose is what says
  so — `docs/prd/regions-and-authorities.md`, "Sites track": "**This track runs beside milestone
  6.3c, which is active**".
- **Problem**, and the readings an intro says a slice does not re-derive.
- **The prose around every table, above it and below it.** Not the intro alone: the sentences that
  say where the work order departs from the `order` column sit *below*
  `regions-and-authorities.md`'s `## Slices` table, not in its intro. Between them that prose
  carries a freeze and its exit trigger ("**Freeze, 2026-09-14**"), the declaration (`CLAUDE.md`,
  "Auto-merge in a declared PRD run"), which rows share one issue, which rows a track's exceptions
  cover, and the `to file` convention (`re-entry.md`, its Slices intro).
- **Every table of rows in the file.** Measured 2026-09-25: the five files hold nine such tables
  between them. Two sit outside their file's `## Slices` section, under `## Milestone 6.3b`; three
  more sit under sub-headings inside it. A file's tables are not one table.

## 2. Read a table the way a reader does

**Take no cell by its position, and none by its header name either.** The nine tables as measured on
2026-09-25:

| file under `docs/prd/` | table | columns, in order | count |
|---|---|---|---|
| `monitoring-sources.md` | `## Slices` | order, #, id, source, route (lead), topics, region today, note | 8 |
| `regions-and-authorities.md` | `## Slices` | order, #, slice, seam, done when | 5 |
| `regions-and-authorities.md` | Beds track | #, slice | 2 |
| `regions-and-authorities.md` | Sites track | order, #, slice | 3 |
| `re-entry.md` | Part one: the schema queue | order, #, slice, seam, note | 5 |
| `re-entry.md` | Part two: the migration rows | order, #, id, `variables` today, held, fills, note | 7 |
| `re-entry.md` | Part three: the closers | order, #, slice, blocked on, note | 5 |
| `scaffold.md` | `## Slices` | #, slice, seam, done when | 4 |
| `topic-notebooks.md` | `## Slices` | order, #, slice, seam, done when | 5 |

Seven things a reader gets right and a column reader does not. Each carries the row it was measured
on, so a claim here can be contradicted by opening that row.

- **`#` is the only column all nine share, and it does not always name an issue.** In `scaffold.md`
  it holds `1`–`6`, order numbers, and no row in that file names an issue at all. In the Beds track
  it holds issue links. One header, two meanings.
- **A `#` cell can say `to file`** — the row is planned and its issue does not exist yet, a
  convention `re-entry.md`'s Slices intro states in its own words. Measured 2026-09-25, that file
  has **eighteen** such rows: S2 and S3 in Part one, all fifteen of Part two's M1–M15, and P1 in
  Part three. So a whole table can name no issue. Such a row is not in the order and is reported
  instead.
- **`order` is not always there.** Seven of the nine tables carry it; the Beds track and
  `scaffold.md` do not.
- **The order is the rows' document order, and the `order` cell is a label.** Sorting by that cell
  gives a different order from the file. `regions-and-authorities.md`'s `## Slices` runs `15`,
  `16b`, `16c`, `16d`, `16e`, `16`, `16a`, `17`, `18`, `18a` down the page, and the prose *below*
  that table says why — "Between 16b and 16 sit 16c, 16d and 16e, in that order", and "18a follows
  16e, not in any order". `re-entry.md`'s three tables label their rows `S1`–`S4`, `M1`–`M15`, and
  `C1`, `C2`, `P1`, `X1`.
- **A row can say its place is not its document position.** `re-entry.md`'s third table is
  `### Part three: the closers, and the row outside the queue`, and the row that clause names, X1,
  has a slice cell reading "outside the serial queue; may run at any time". Report what the row says
  about its own place rather than dropping it or moving it.
- **An issue cell can name several issues, and two rows can share one issue.** The Sites track's row
  4 names #195, #196 and #197. `monitoring-sources.md`'s rows 20 and 21 both name #150. So the
  derived order is a list of issues: row 4 contributes three entries, and #150 one entry that says
  it carries two rows.
- **A `#N` anywhere but the `#` column is not that row's issue.** The Beds track's `#96` row says
  "blocked on #93, #94 and #122" in its slice cell; Part one's S2 says "after [#179](…)" in its
  note. Take the row's issue from the `#` cell's own markdown link, `[#131](…/issues/131)`, which is
  the form every issue cell in these tables uses.

Then the two things the table cannot tell you, because a hand maintains them:

- **Inline state goes stale.** Measured 2026-09-25: the Sites track's row 4 ends
  "`ready-for-agent`", and #195, one of its three issues, had closed that day. Rows 1–3 of the same
  table end "**merged**, PR #186 / #189 / #187".
- **A row's label may not be in the table at all.** `monitoring-sources.md` states its labels in the
  prose below the table — "Rows 1–17 and 19 were filed `ready-for-agent`" — which is where they were
  at filing, not where they are now.

So the row tells you the work and its place in the order. Step 3 tells you its state.

## 3. Recover every row's state from GitHub, never from the table and never from memory

The `gh issue` forms are `docs/agents/issue-tracker.md`, "Commands"; the `gh pr` and `git` forms
below are not there. One listing covers every row of every table:

```sh
gh issue list --state all --limit 300 --json number,title,state,labels,milestone \
  --jq '.[] | "\(.number)\t\(.state)\t\([.labels[].name]|join("+"))\t\(.milestone.title // "-")"'
```

`--state all`, not `--state open`: an open listing cannot tell a closed issue from one that does not
exist, and the stop below turns on that difference. `milestone` is what the last section needs.

- **`CLOSED`** — the row is done, whatever the row says.
- **`OPEN` and `ready-for-agent`** — in the order.
- **`OPEN` and anything else** — not in the order; report it with the label it carries.

Then, for each row in the order, two more reads:

```sh
gh pr list --state open --json number,title,body,headRefName    # a body's "Closes #N" ties it to a row
gh issue view <N> --json title,body,comments --jq '.title, .body, .comments[].body'
```

An open PR whose body closes a row's issue means that row is in progress. The last controller
comment on the issue says where its loop stands — that is the ledger, step 4.

**STOP if a row names an issue the `--state all` listing does not return.** It does not exist: the
table is ahead of the tracker or a number in it is wrong, and which is not this skill's to decide.

## 4. Write the order to the ledger, then report

**The ledger is the issue thread.** Compaction erases the controller's memory; the thread does not.
Write the comment to a file and pass it with `--body-file` (`CLAUDE.md`, "Branches, commits, PRs";
`docs/agents/issue-tracker.md`, "Commands"):

```sh
gh issue comment <the first entry's issue> --body-file <path>
```

**One thread per run, named in its own first comment, and it does not move.** The thread is the
issue of the order's first entry *as first derived*, and the comment says so in a line a resume can
read: `ledger thread: #<N>`. #228's per-row transitions continue that same thread. Write the order
before doing anything else with it, so the order is fixed and auditable rather than re-derived
silently on every resume.

The thread has to be named because it would otherwise move. Once #228 merges the first entry, that
issue closes and the next resume's first entry is a different issue with an empty thread, so a run
of nine rows would leave nine unlinked threads and each resume would read the wrong one. A resume
therefore finds the thread by reading the order's issues for the most recent `ledger thread:`
comment — including the closed ones, which is the other reason step 3 lists `--state all` — and
keeps using it even after it has closed.

**An empty order has no thread.** Where no row of the file is both open and `ready-for-agent`, post
nothing and report that instead, with the rows that were ruled out and why. `docs/prd/scaffold.md`
and `docs/prd/topic-notebooks.md` are both `Status: done` and reach this, so it is not a corner.

**STOP before posting if more than one of the file's tables has an open `ready-for-agent` row.**
Nothing in this repo orders between two tables in one file, and that gap is parked twice: #5
issuecomment-5823293391 ("two tables on one milestone is two orders with nothing ordering between
them") and #5 issuecomment-5834515570, which counts this file's tables. Ask which track to run; do
not interleave them and do not pick one. Measured 2026-09-25, neither file with a live track trips
this — `monitoring-sources.md` has one table, and of `regions-and-authorities.md`'s three only the
Sites track has an open `ready-for-agent` row.

The comment carries one line per entry, in order: the table the row came from, the row's `order`
cell, the issue, the label GitHub gives it, whether an open PR already closes it, whatever the row
states about its own blockers or its place in the queue, and the row's own inline state wherever
that disagrees with GitHub. The blockers go in because a first entry can be the one the table calls
blocked: `re-entry.md`'s order today is #38 then #17, and #38's `blocked on` cell reads
"M1–M15, for the required flag" — fifteen rows whose `#` cells all say `to file` — while #17's
reads "nothing". What a blocked first entry means for dispatch is #228's, not this half's; naming
it is this half's.

Above those lines goes the commit the PRD was last changed in, so a mid-run edit to a table is
visible rather than silent:

```sh
git log -1 --format=%H -- docs/prd/<slug>.md
```

Then report: the order as posted, the comment's URL, and the two lists below. The report ends the
run — this half does not go on to work the first entry.

## What the order leaves out, and says so out loud

- **Every row whose issue is closed or carries another label**, each with its label, so the report
  shows the whole table rather than only its live part. A row whose `#` cell says `to file` belongs
  here too.
- **An open `ready-for-agent` issue on the milestone that no row names.** It is invisible to this
  order, and closing that gap is parked — #5 issuecomment-5638837943, which measured #68 as "on
  milestone 6.2, labelled `ready-for-agent`, and in neither ordering". List any such issue under
  "not in the order" and point at that entry. Do not order it, and do not edit the table to add it.

  **Take the milestones from the issues the `#` cells name, never from the prose.** A track's prose
  names the milestone it runs *beside*, not the one its rows are on: the Sites track's own sentence
  names 6.3c, while its rows' issues are on `6.3b Beds and sites`. Keying on the prose there looks
  for strangers on 6.3c — every one of which `monitoring-sources.md` has already ordered — and never
  looks at 6.3b, which is where the one real stranger is. Measured 2026-09-25: #201, open,
  `ready-for-agent`, on 6.3b, named by no row in any of the five files.

## Non-goals

No dispatch and nothing written to the checkout: no agent, no branch, no worktree, no PR, no merge
(#228, #229, #230). No change to any PRD or to any table in one — the controller adapts to the repo,
not the reverse (#222, Non-goals). No new label: run state lives in the ledger, and the label
vocabulary is `docs/agents/triage-labels.md`'s. No work order from `gh issue list --search`. No
change to `CONTEXT.md`. And no code that parses a table: step 2 is a reading, not a parse.

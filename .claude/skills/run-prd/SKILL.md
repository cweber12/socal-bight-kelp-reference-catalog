---
name: run-prd
description: Use when driving one milestone's PRD as a run in the SoCal Bight kelp reference catalog. Invoked as /run-prd docs/prd/<slug>.md. Derives that PRD's work order from its tables of rows, recovers each row's state from GitHub, writes the order to the ledger, then dispatches its first entry when that entry is a record row and carries it to an open PR with CI green. It stops before review: it audits nothing and merges nothing.
disable-model-invocation: true
---

# run-prd

Derive **one** PRD's work order, write it down where compaction cannot reach it, and work its first
entry. A controller's first job is to know the order. Here that order is the PRD's **Slices** table,
and which row is next follows from it: `CLAUDE.md`, "How work is tracked", and
`docs/agents/issue-tracker.md`, "Conventions".

Steps 1–4 derive the order and write it down. Steps 5–9 carry its first entry from a branch to an
open PR with CI green, and stop there: review and merge are #229, and a row whose seam is not
`add-source` is #230 — step 5 stops on one.

Do the nine steps **1–9 in order**. **Stop at the first one that cannot be answered from the repo
and the tracker**: say which step, what it found, and what you have derived so far, then wait. Never
make a step pass by picking between two readings of a rule — a stop here is cheap and a wrong order
is not.

## 0. Take the argument

`/run-prd docs/prd/<slug>.md`, one file. **STOP** if the argument names no file under `docs/prd/`.
Do not guess which PRD was meant, and do not run against more than one.

## 1. Read the PRD once, whole

Read the file rather than searching it. A search returns a row and loses the prose that governs it,
and that prose is where this repo keeps the freezes, the declarations and the exceptions.

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
| `re-entry.md` | Part three: the closers, and the row outside the queue | order, #, slice, blocked on, note | 5 |
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
  derived order is a list of issues rather than of rows: a cell naming three contributes up to three
  entries, one per issue step 3 leaves in, and #150 contributes one entry that says it carries two
  rows. Row 4 contributes two today, not three, because #195 has closed — which is what the
  staleness bullet below records.
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
gh issue comment <the ledger thread> --body-file <path>
```

**One thread per run, named in its own first comment, and it does not move.** The thread is the
issue of the order's first entry *as first derived*, and the comment says so in a line a resume can
read: `ledger thread: #<N>`. The per-row transitions of steps 5–9 continue that same thread. Write
the order before doing anything else with it, so the order is fixed and auditable rather than
re-derived silently on every resume.

The thread has to be named because it would otherwise move. Once the first entry merges — which is
#229's, not this skill's — that issue closes and the next resume's first entry is a different issue
with an empty thread, so a run of nine rows would leave nine unlinked threads and each resume would
read the wrong one. A resume therefore finds the thread by reading the order's issues for the most
recent `ledger thread:` comment — including the closed ones, which is the other reason step 3 lists
`--state all` — and keeps using it even after it has closed.

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
reads "nothing". What a blocked first entry means for dispatch is step 5's; naming it is this
step's.

Above those lines goes the commit the PRD was last changed in, so a mid-run edit to a table is
visible rather than silent:

```sh
git log -1 --format=%H -- docs/prd/<slug>.md
```

Then report: the order as posted, the comment's URL, and the two lists in the section below. Then
step 5, with the order's first entry.

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

## 5. Take the first entry, and check that it is a record row

The order's first entry is what steps 5–9 work — not the first `ready-for-agent` row of the table,
because step 3 already left out everything that is not open and `ready-for-agent` and step 4 wrote
the result down.

**The predicate: the row's seam is `add-source`.** The same predicate decides auto-merge
eligibility, and `CLAUDE.md`, "Auto-merge in a declared PRD run", is where it is written down — as
the sentence a PRD's preamble carries above the rows it governs. Read it there: the consequence
differs (eligibility there, dispatch here) and the test does not, so a second account of the test
would be a copy that can drift. `docs/prd/monitoring-sources.md` carries the sentence itself,
between its Slices intro and its table.

**Read the seam from the issue, not from the table.** `monitoring-sources.md`'s `## Slices` has no
seam column at all — step 2's table of the nine — so the table cannot answer, while the issue's
`## Seam` section can, in the shape `docs/agents/issue-tracker.md`, "Record issues", gives it.
**Take the seam from that section's first sentence.** A later sentence in the same section may name
`add-source` while the seam is something else: #150's `## Seam` names
`catalog/excluded/stebbins-wetzer-2023.md` and `catalog/excluded/cheresh-2023.md`, then says
"`add-source` walks sources, not exclusions; its step 1 … and step 6 … apply as written". A grep for
the string selects that row; a reader does not.

Measured 2026-09-25 over the nine entries of `monitoring-sources.md`'s order: eight are record rows
— #141, #142, #143, #144, #145, #147 and #149 open "`add-source`, add path", and #146 opens
"`add-source`, transcribed path" — and #150, the ninth, is not one.

**STOP if the first entry is not a record row.** A code row is #230 and nothing here works one. Say
which entry, quote the seam you read, and wait.

**STOP if the row or its issue states a blocker that is not closed.** Two places state one and both
are read: the row's own cell where its table has that column (`re-entry.md`'s Part three has
`blocked on`), and the issue's `## Blocked by` section. Where a blocker names an issue the tracker
settles it, and step 3's listing already holds the state — #143's row says "enters after row 7",
which is row 7's issue #137, `CLOSED`, so it is satisfied. Where it names no issue nothing settles
it: `re-entry.md`'s #38 is blocked on "M1–M15, for the required flag", fifteen rows whose `#` cells
all say `to file`, so that file's order stops here at its first entry. #141's `## Blocked by` reads
"None; can start immediately."

**A note is not a blocker.** #144's row says "the host did not answer from one machine on
2026-09-15, so step 2 may stop" — a fact about the route, which `add-source` step 2 is where it
lands, not this step.

**One row per run**, and the reason is mechanical rather than a limit on ambition: two source-record
rows collide in `notebooks/00_index.ipynb`, which counts sources and references, so the second
cannot branch from a `main` the first has not merged into. Measured 2026-09-25: of the 22
`catalog: add` commits on `main` after `notebooks/00_index.ipynb` existed (`5438219`, #61,
2026-09-10), **20 moved it**; the two that did not — `24111f6` (#117, region nodes) and `668cb22`
(#215, site records) — add no source record. Merging is #229's, so a run ends after one row until it
lands.

## 6. Branch a worktree, and leave the checkout you are standing in alone

The controller goes on reading the tracker and the PRD while the row is built, and `add-source`
step 0 branches before it writes anything. Both want the same `HEAD`, so the row gets its own
checkout.

```sh
git worktree list                                    # first, always
git fetch origin
git worktree add -b catalog/add-<id> .claude/worktrees/catalog-add-<id> origin/main
```

- **`git worktree list` first, and read it against the path this row needs.** A directory under
  `.claude/worktrees/` that the listing does not name is not a worktree. **STOP when it is that
  path**: `git worktree add` will not write into a non-empty directory, and neither reusing a stray
  checkout nor removing one is the controller's call — removing it is the owner's. A stray at any
  other path is **reported and is not a stop**; it belongs to no row of this run. Measured on the
  first live run of these steps, 2026-09-25: `.claude/worktrees/docs-prd-noaa-hapc-row` existed,
  empty, while `git worktree list` returned only the main checkout, and the path this row needed was
  `.claude/worktrees/catalog-add-cms_thermograph_array`, so the run reported the stray and went on.
  #5 carries its removal.
- **`origin/main` after a fetch**, never the local `main`: `main` is protected and the row's PR
  merges into its tip, so a branch cut from a stale local `main` opens a PR whose diff is not the
  row's.
- **The branch name is `add-source` step 0's**, `catalog/add-<id>`, with `<id>` the row's proposed
  id — which that skill's step 3 may still change, and if it does the branch keeps the name it was
  cut with. The directory name flattens the slash and nothing reads it.
- **`.claude/worktrees/` is git-ignored** (`.gitignore`, "Agent worktrees"), so the nested checkout
  stays out of the controller's `git status` and out of the file set `ruff` walks.

Five mechanical facts about running this repo's commands from a worktree, each read from the file
named rather than from habit:

- **The interpreter is the controller's checkout's.** `.venv/` is git-ignored, so a worktree has
  none and every command takes an absolute path to that one.
- **`gate.py` gates the worktree.** `ROOT = Path(__file__).parent` (`gate.py:24`), so the
  worktree's own copy roots at the worktree.
- **`python -m kelpcatalog.generate` renders the tree it is run from.** `main()` takes
  `root = Path.cwd()` (`src/kelpcatalog/generate.py:74`), so from the worktree root it reads that
  tree's `catalog/` and writes that tree's `notebooks/`.
- **The code it runs is not the worktree's.** `pip install -e` wrote an absolute path to the
  controller's checkout's `src/` into the venv, so `kelpcatalog` imports from there whatever tree
  you stand in. `audit-pr` measured it (`.claude/skills/audit-pr/SKILL.md`, step 3) and the file is
  readable: `.venv/Lib/site-packages/__editable__.kelpcatalog-0.1.0.pth` holds that one path.
  Harmless for a
  record row, whose seam names no file under `src/kelpcatalog/` — `docs/agents/issue-tracker.md`,
  "Record issues", lists the record, a fetch script or a table, a reference record and the
  notebooks. Not harmless for a row that changes the generator, and step 5 stops before one gets
  here.
- **The row's own fetch un-skips `notebook-fresh`, and the cell it then runs wants another source's
  bytes.** That row skips only while `data/` is absent — `skip_reason` returns its reason unless
  `(root / DATA_DIR).is_dir()` (`src/kelpcatalog/fresh.py:343`) — and a fresh worktree has no
  `data/` at all. So the moment a `FETCHED` row's script writes `data/raw/<id>/`, the row stops
  skipping and executes the committed figure cells, and today that is one cell loading one source:
  `notebooks/1_physical_environment/11_ocean_climate.ipynb`'s `load("noaa_oni")`, the only `load(`
  in the eleven notebooks. The worktree therefore also needs `data/raw/noaa_oni/`, which its own
  committed script writes — `<interpreter> src/fetch/noaa_oni.py` from the worktree root. Running a
  committed fetch script is not writing into `data/` by hand and stages nothing, `data/` being
  git-ignored and per-tree. Measured on #141, whose topic is `ocean-climate`, so the notebook it
  moves is the notebook that carries the figure; the general form is every source a committed figure
  cell loads.

## 7. Dispatch the row

```
Agent(subagent_type="general-purpose", prompt=<the six things below>, description="Record row #<N>")
```

**`general-purpose` pointed at the brief** — not a new agent type, and never the brief pasted into
the prompt. The brief is `.claude/skills/run-prd/record-row.md`, the dispatch names its path, and
the agent reads it from disk. `audit-pr` gives the reason for pointing rather than pasting: "Two
copies drift, and the copy you paste is the one you were about to edit in your own favour"
(`.claude/skills/audit-pr/SKILL.md`, step 3). The path is the **controller's checkout's**, because
the row's branch was cut from `origin/main` and carries only what `main` carries.

The prompt carries six things:

1. the brief's absolute path, and to read it in full, first, and follow it
2. the issue number, with the `gh issue view` form to read it (`docs/agents/issue-tracker.md`,
   "Read")
3. the worktree's absolute path and the branch it is already on
4. the interpreter's absolute path
5. the PRD file and the row's `order` cell, so the agent reads the readings the row does not
   re-derive
6. the four report words, named and not explained — the brief explains them

**It carries no field values.** The controller has not opened the source, and a controller that
drafts `status`, `coverage` or `regions` has made the row's judgements for it while holding none of
the evidence. The PRD's route column is a lead and `add-source` step 2 opens it
(`docs/prd/monitoring-sources.md`, the paragraph above its table).

**One row per dispatch and never two at once**, for step 5's collision.

## 8. Read the report, and rule on it

Four outcomes. Verify each from the worktree rather than from the report — a report is a claim, and
`git` and the gate settle it:

```sh
git -C .claude/worktrees/catalog-add-<id> status --short
<interpreter> gate.py                                      # run from the worktree root
```

- **`DONE`** — the eight steps passed and step 8 printed. Check that `git status --short` shows the
  row's seam and nothing else, that the gate you ran yourself is green, and that the notebooks which
  moved are the ones the record's topics name (`add-source` step 7 states that set and says the add
  path's is exact). Then step 9.
- **`DONE_WITH_CONCERNS`** — the same, plus something wanting a reader's ruling rather than another
  step. Rule on each concern, carry it into the PR body in the agent's own words, and ledger it.
  Then step 9.
- **`NEEDS_CONTEXT`** — a question the repo does not settle, with the readings it found. **Answer
  nothing.** The row was dispatched to make the row's judgements, and a controller answering the one
  the agent could not has widened the schema by proxy while holding less of the evidence. Ledger the
  question and the readings, put them to the owner with what each would cost, and stop.

  **When the owner rules, resume the same agent with the ruling**, and ledger the ruling first so
  the record's PR body can cite a ruling rather than a preference. Two things belong in that resume
  besides the ruling: what the controller checked and could not reproduce, so the agent's own
  measurement is the one in play rather than silently contested; and anything the controller found
  *already settled in the repo*, which is not part of the ruling and is what stops a second question
  on ground a record or a Parking-lot entry already covers. The resume is not a retry of an
  unchanged dispatch — the input changed, and what changed is the ruling.
- **`BLOCKED`** — an `add-source` STOP fired: a dead route, a duplicate record, a topic that does
  not exist, a gate contradicting `CONTEXT.md`. Ledger which step stopped and what it found, and
  stop the run.

**Never retry unchanged.** A STOP is a fact about the source, and the same brief over the same
source returns the same fact. Where the report is unusable — no step-8 output, files outside the
seam, a report word the message below it contradicts — that is a finding about the brief or the
prompt rather than about the row: fix it on the controller's own branch, say in the ledger that you
did, and dispatch the corrected one. Three things are not retries of an unchanged dispatch: a resume
(step 9), a CI failure diagnosed from its own log (step 9), and a dispatch after the brief changed.

## 9. Resume for the commit and the PR, gate on CI, then stop

**Resume the agent that did the work** — `SendMessage`, not a fresh agent and not the controller
committing on its behalf. Its context holds the record, the manifest, the gate output and the
notebooks that moved, and the commit body has to state them; a controller writing that body from the
report writes a second copy of facts it did not observe. This is the opposite of `audit-pr`'s "send
it nothing until it reports", for the opposite reason: there the silence buys the auditor's
independence, here the row has already reported and the review the resume acts on is the
controller's own.

Name the forms in the resume so the agent does not re-derive them (`CLAUDE.md`, "Branches, commits,
PRs"):

- commit subject `catalog: add <id>`, `catalog` being the type for record changes, the body saying
  why, passed with `-F` from a file
- `git push -u origin catalog/add-<id>`, where `-u` is load-bearing: step 6's
  `git worktree add -b … origin/main` leaves the new branch *tracking `origin/main`*, which it says
  as it runs, and `-u` repoints it at the row's own remote branch
- `gh pr create --base main --head catalog/add-<id> --title "catalog: add <id>" --body-file <path>`,
  the body carrying `Closes #<N>` and the `gate.py` output (`CLAUDE.md`, "Running things": paste it
  into the PR)

Then the CI gate, which is the controller's and not the agent's:

```sh
gh pr checks <PR> --watch
```

**All three checks green.** `.github/workflows/ci.yml` runs `gate (ubuntu-latest)`,
`gate (windows-latest)` and `lint` on every pull request — `CLAUDE.md`, "Running things", names the
same three as "`gate.py` (Ubuntu and Windows), `ruff check` and `ruff format --check`", the last two
being the `lint` job's steps. A red check is diagnosed, not retried: read that job's own output and
resume the agent with it. **STOP if the fix is not in the row's own seam** — a record row that needs
`src/kelpcatalog/`, `gate.py` or `CONTEXT.md` changed to go green is a bug or a rule question, and
`CLAUDE.md`'s in-flight rules route it.

**Then stop.** The PR is open and green and it is not ready: `CLAUDE.md`, "Branches, commits, PRs",
says a PR is ready when it has been audited, and both the audit and the merge are #229 — until that
lands the owner runs `/audit-pr <PR>` by hand, as today. Report the PR, the worktree it was built in
and that you left it there for #229, and the ledger comments.

## The ledger, per row

Four writes per row, each its own comment, because a resume arriving between two of them has to be
able to tell them apart:

1. **dispatched** — the issue, the branch, the worktree path, the `origin/main` commit it was cut
   from, and the brief's path
2. **reported** — the report word, and for anything but `DONE` what it said. A row that reported
   `NEEDS_CONTEXT` and was then ruled on adds a fifth write between this one and the next, the
   ruling, because the resume it authorises is the thing a later reader will want the authority for
3. **PR opened** — the number and the files it touches
4. **CI settled** — the three checks green and that the run stopped for review, or red and what it
   was

Four is a judgement about what a resume needs rather than a measurement. On
`monitoring-sources.md` it would come to 32 over the whole file — its order has nine entries and
eight of them are record rows, and step 5 stops the run at the ninth — spread over as many runs as
#229 takes merges to allow. Each is
`gh issue comment <thread> --body-file <path>` (`docs/agents/issue-tracker.md`, "Commands"), and
`<thread>` is the one step 4 named in its own first comment — **not the row's own issue**, which is
the same only for the first entry.

## Non-goals

No audit and no merge (#229): the PR step 9 opens is not ready, and nothing here runs `/audit-pr` or
`gh pr merge`. No code row (#230) — step 5 stops on one. No parallel dispatch, for step 5's
collision, and #222's non-goals already exclude fan-out. No second row in one run. No change to
`.claude/skills/add-source/SKILL.md`, whose step-8 stop is what step 8 here reads. No change to any
PRD or to any table in one — the controller adapts to the repo, not the reverse (#222, Non-goals).
No new label: run state lives in the ledger, and the label vocabulary is
`docs/agents/triage-labels.md`'s. No work order from `gh issue list --search`. No writing into
`data/`. No change to `CONTEXT.md`. And no code that parses a table: step 2 is a reading, not a
parse.

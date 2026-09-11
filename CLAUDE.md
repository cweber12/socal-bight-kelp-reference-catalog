# CLAUDE.md

A catalog of authoritative sources for kelp forest monitoring in the Southern California Bight,
organized by topic and region. It supports analysis repos; it does not do analysis. **Read
`CONTEXT.md` before touching `catalog/`** — the rule, schemas, vocabularies and region tree live
there, and if code and `CONTEXT.md` disagree, `CONTEXT.md` wins.

## The rule, in one line

A record holds only what the source itself states and what anyone repeating the fetch would
reproduce. No commentary, no computed numbers, no narrative. Facts in fields; prose body empty.
Topics and sub-topics are tags from `CONTEXT.md`, never a filter: a source that fits none means
add a topic in its own PR, not exclude the source. Notebooks render records; they hold no facts.

## Running things

```sh
python -m venv .venv && .venv/Scripts/pip install -e ".[dev]"    # Windows; use .venv/bin on Unix
.venv/Scripts/python gate.py   # every gate; run before every PR, paste the output into the PR
.venv/Scripts/python -m kelpcatalog.generate   # rebuild all eleven notebooks from the records
```

CI runs `gate.py` (Ubuntu and Windows), `ruff check` and `ruff format --check` on every PR. `main`
is protected.

## How work is tracked

One milestone is active at a time. A PRD for each milestone lives at `docs/prd/<slug>.md`, and its
**Slices** table is the work order. `gh issue list` is not: it sorts newest-first, so its top row
is the last slice in the milestone. The next thing to do is the first open `ready-for-agent` issue
in that table. An issue is ready when it names the seam, the failing test and the non-goals and
fits one PR; if you cannot state the failing test, stop and ask. Ideas go in the pinned Parking-lot
issue as one-line comments, never as new issues; the only issues an agent opens on its own are
found-in-flight bugs under rule 3.

## In-flight bugs

When you find a bug while implementing an issue, apply the first rule that fits and say which in the
PR body:

1. In files this PR already touches and fixable with a test in minutes → fix it in its own `fix:`
   commit on this branch; list it under "Also fixed".
2. Blocks the current slice → fix it first in its own commit. If not small, stop: open the issue,
   mark the slice blocked, report back.
3. Neither → open an issue labelled `bug` + `found-in-flight` + `needs-triage` with file, line, a
   repro if cheap, and a link to this PR. Continue.

## Branches, commits, PRs

- One issue, one branch (`<type>/<slug>`), one PR, squash-merged. Small PRs; if the branch's
  commits are each worth keeping, the PR is too big — split it.
- Commit and PR-title format: `<type>(<scope>): <imperative subject ≤ 72 chars>`, body says why,
  `Closes #N`. Types: `feat fix docs test ci chore refactor`, and `catalog` for record changes
  (`catalog: add noaa_oni`). Add `Co-Authored-By:` for yourself.
- A PR is ready when it has been audited, unless the owner says to skip. The `audit-pr` skill
  commissions the audit in a context that never watched the PR being written, and relays what it
  found; which findings to act on is the owner's call, not the author's.
- Never write into `data/`. Never add a record by hand when the `add-source` skill exists — use it.
- Never write a parser for any external manifest or prose file. Records are entered, not migrated.

## Scope guards

Split work only when it earns its keep. A rename is its own slice. Do not add fields, gates,
directories or dependencies an open issue does not ask for; put the idea in the Parking lot.

## Agent skills

### Issue tracker

GitHub Issues and milestones in this repo, via `gh`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical role strings unchanged, plus `bug` and `found-in-flight`.
See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` at the root is the authority; no `docs/adr/` yet.
See `docs/agents/domain.md`.

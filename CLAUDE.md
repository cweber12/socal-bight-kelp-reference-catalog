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
python gate.py            # every gate; run before every PR, paste the output into the PR
```

CI runs `gate.py` (Ubuntu and Windows), `ruff check` and `ruff format --check` on every PR. `main`
is protected.

## How work is tracked

One milestone is active at a time; the next thing to do is the top open `ready-for-agent` issue in
it. A PRD for each milestone lives at `docs/prd/<slug>.md`.

## Branches, commits, PRs

- Small PRs; if the branch's commits are each worth keeping, the PR is too big — split it.
- A bug found while implementing an issue: apply the first rule that fits in
  `docs/agents/issue-tracker.md`, and say which in the PR body.
- Commit and PR-title format: `<type>(<scope>): <imperative subject ≤ 72 chars>`, body says why,
  `Closes #N`. Types: `feat fix docs test ci chore refactor`, and `catalog` for record changes
  (`catalog: add noaa_oni`). Add `Co-Authored-By:` for yourself.
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

# Issue tracker: GitHub

Issues, milestones and the Parking lot live in GitHub Issues at
`cweber12/socal-bight-kelp-reference-catalog`. Use the `gh` CLI for every operation; it infers the
repo from `git remote -v` when run inside a clone.

## Commands

- **Create**: `gh issue create --title "..." --body "..."` (heredoc for multi-line bodies)
- **Read**: `gh issue view <number> --comments`
- **List**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] |
  {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`, with `--label`
  and `--milestone` filters
- **Comment**: `gh issue comment <number> --body "..."`
- **Label**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Milestone**: `gh issue edit <number> --milestone "6.2 Topic notebooks"`
- **Close**: `gh issue close <number> --comment "..."`
- **Milestones themselves**: `gh api repos/{owner}/{repo}/milestones` — `gh` has no `milestone`
  subcommand.

## Conventions

- One milestone is active at a time; they are named `<number> <name>`: `6.1 Scaffold`,
  `6.2 Topic notebooks`, `6.3 Regions, beds, sites`, `6.4 Re-entry`, `6.5 Lock and fetch`,
  `6.6 Indexes and citation`, `6.7 Bight expansion`. A PRD for each lives at
  `docs/prd/<slug>.md`.
- **The next thing to do** is the top open `ready-for-agent` issue in the active milestone.
- An issue is ready when it names the seam (function signature, gate row or file format), the
  failing test, the non-goals, and fits one PR. If you cannot state the failing test, stop and ask.
- One issue → one branch (`<type>/<slug>`) → one PR, squash-merged, `Closes #N` in the body.

## Record issues

An issue whose work is entering one source into `catalog/sources/` takes a fixed shape. Like any
issue whose work is entry or prose rather than code, it cannot name a failing test, so the
readiness bar's "stop and ask" does not apply — the answer is written here. The `add-source` skill
is what works it.

- **Seam** — the record, its fetch script, and the notebooks the source appears in:
  `catalog/sources/<id>.md`, `src/fetch/<id>.py` when the tier is `FETCHED`, and the notebooks
  `add-source` step 7 regenerates. `CONTEXT.md`, "Notebooks": *a source is not "in" until the
  notebooks that show it are refreshed in the same PR.*
- **Failing test** — none mechanical. Gates print counts and never assert them (`CONTEXT.md`,
  "Gates"), so there is no test to write. Say that; do not invent one.
- **Acceptance** — `gate.py` green, the record reviewed field by field against the source, and the
  notebooks regenerated and committed in the same PR.
- **Non-goals** — no other source, no schema change.
- **Done when** — merged.

## Ideas are not issues

Ideas go in the pinned **Parking lot** issue (#5) as one-line comments, never as new issues:

    gh issue comment 5 --body "- <one line>"

Weekly, each comment becomes an issue with acceptance criteria, becomes a PRD bullet, or is
deleted. Nothing stays longer than two weeks.

## In-flight bugs

When you find a bug while implementing an issue, apply the first rule that fits and say which in
the PR body:

1. In files this PR already touches and fixable with a test in minutes → fix it in its own `fix:`
   commit on this branch; list it under "Also fixed".
2. Blocks the current slice → fix it first in its own commit. If not small, stop: open the issue,
   mark the slice blocked, report back.
3. Neither → open an issue labelled `bug` + `found-in-flight` + `needs-triage` with file, line, a
   repro if cheap, and a link to this PR. Continue.

## When a skill says "publish to the issue tracker"

Create a GitHub issue. Label it `needs-triage` unless it already clears the readiness bar above.

## When a skill says "fetch the relevant ticket"

`gh issue view <number> --comments`.

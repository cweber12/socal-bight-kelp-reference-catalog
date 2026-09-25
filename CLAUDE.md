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

A design or grill session that settles more than one `CONTEXT.md` rule ends in decisions and
issues, not in text: the issues carry the seam, the failing test where there is one, and the
non-goals, and the text is drafted against them by whoever picks them up. The owner files them, or
asks for them by name — the sentence above still holds, and an agent opening them on its own is
the thing it forbids. On 2026-09-19 a grill's decisions went straight to four PRs, none of which
closed an issue or had one filed for it.

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
- Multi-line content is written to a file with an editor tool, never built with a heredoc; the
  command then reads the file — `--body-file` for a `gh` issue or PR body or comment, `-F` for a
  commit message, a path for a script. Measured here: a heredoc piped to `python -` decodes with the
  console codepage and mangles `·`, `…` and `—`, and an escape written in a heredoc lands as a raw
  byte — `\x03` became byte 003, which `cat` and `git diff` both render as nothing.
- A PR is ready when it has been audited, unless the owner says to skip. The `audit-pr` skill
  commissions the audit in a context that never watched the PR being written, and relays what it
  found. The agent that commissioned the audit then rules on every finding, including one the
  auditor's blocking call names, and records why wherever it routes that finding — not only in the
  session that ruled. It does not wait for the owner to accept the ruling.
- Never write into `data/`. Never add a record by hand when the `add-source` skill exists — use it.
- A record and the notebooks that show it land in one PR: after the gate, run
  `.venv/Scripts/python -m kelpcatalog.generate` and commit every notebook it moves
  (`CONTEXT.md`, "Notebooks").
- Never write a parser for any external manifest or prose file. Records are entered, not migrated.

## Auto-merge in a declared PRD run

Merging is the owner's, except inside a run of a PRD whose preamble carries the declaration below.
There a PR may merge unattended when **both** halves hold: the row is declared eligible **and** its
diff satisfies the allowlist. A declaration is made before the work and the diff is the only fact
available after it, so neither half stands in for the other. Outside such a run nothing here
applies.

- **The declaration is by seam**, one sentence in the preamble above the rows it governs — *a row
  whose seam is `add-source` is auto-merge eligible; every other row is not* — pointing here
  rather than transcribing the patterns. A PRD that does not carry the sentence declares nothing,
  and a row it does not declare is ineligible.
- **The allowlist is five patterns**: `catalog/sources/*.md`, `catalog/sites/*.md`,
  `catalog/references/*.md`, `notebooks/**`, and `src/fetch/<id>.py` whose basename matches a
  source record id added in the same diff. That fifth pattern is derived from the diff rather than
  a bare wildcard because the id match is what ties a fetch script to the record it fetches.
  `notebooks/**` is a bare wildcard and holds executable code of its own — a figure cell, which
  `CONTEXT.md`, "Notebooks", says is never generated and never touched — so what stands behind it
  is that file's "Gates" rows: `lint` over notebook code cells, `figure-provenance`,
  `notebook-structure`, `notebook-outputs`, and `notebook-fresh` where that row's own scope lets
  it run. Every other path is outside. `catalog/regions/` is out because every commit in this
  repo's history that added a region record changed code beside it — three, `b12b4e7`, `24111f6`
  and `0b40a82`; `catalog/beds/`, `catalog/excluded/` and `catalog/tables/` are out because a
  directory's first record establishes a shape rather than repeating one, and none of the three
  has one yet.
- **A multi-record row is eligible** when the diff's record ids are the ones the row names.
- **The audit runs per row.** Auto-merge neither batches it across rows nor stands in for one, and
  who may say to skip it is unchanged ("Branches, commits, PRs"). Paths are what the allowlist
  checks and content is what the audit checks, and a clipped quotation or a widened universal in a
  record's `access` steps lives entirely inside the allowlist.
- **Three conditions stop an unattended merge, and each stops it differently.** A diff outside the
  allowlist hands the PR to the owner. CI red on either OS blocks eligibility until it is green.
  An audit finding whose premise the agent judges shared by the rows not yet built halts the run.
  That judgement is additional to the ruling "Branches, commits, PRs" requires, and it is a
  judgement rather than a consequence of the finding's severity — in a repetitive run every row is
  built from the same premise, so one row's finding is evidence about the rows not yet built. The
  recorded justification names the premise either way, which is what makes a wrong call visible in
  the report below.
- **Report after five consecutive auto-merges**, naming the union of fields entered across the
  batch. An auditor reads one PR, so an error the run makes on every row can pass each audit and
  be visible only as a pattern; the report shows the pattern rather than merely pausing. Five is a
  judgment about how much unseen work is tolerable, not a measurement.

## Scope guards

Split work only when it earns its keep. A rename is its own slice. Do not add fields, gates,
directories or dependencies an open issue does not ask for; put the idea in the Parking lot.

## Changing a rule in `CONTEXT.md`

`gate.py` does read `CONTEXT.md` — `lint` walks it for fenced Python — but **no row checks a rule
in it**: a mutation sweep on 2026-09-19 flipped "one of three" to "one of four" in the `FETCHED`
routes, and it survived a full `gate.py`. Review is the only check on a rule, so an audit is where
a mistake surfaces instead of a failing test. Each practice below comes from a defect that reached
one.

- **One rule per PR.** #154 and #158 carried three rules each, and every audit they got blocked
  them — five rounds between the two.
- **Point at a rule rather than restating it.** A second copy of a *rule* drifts from the first
  and no gate compares them. A rationale is different: the authority records several on purpose,
  including the three reasons `global` sorts last. #158's drafts restated `CONTEXT.md` sentences
  instead of naming them and contradicted them; what settled it was "its status is whatever
  *Vocabularies* allows a record of that tier".
- **Re-read the section cold before a second edit to a file this session already changed.** #158
  collided with `CONTEXT.md` text the same session had written, in all three of its audit rounds.
- **Grep every restatement outside the file.** Grep the repo outside `CONTEXT.md` and
  `Claude outputs/` for the sentence's distinctive phrases, not the whole sentence; nothing
  compares a transcription to `CONTEXT.md`. The audit of PR #154 found its first draft leaving
  `.claude/skills/add-source/SKILL.md` stating the rule that PR removed — the file a record entry
  actually reads.
- **Before writing "every", "any", "no" or "only", name the set and count it from the repo.** The
  audits of 2026-09-19 blocked on this in a record's `access` steps (#153) and in `CONTEXT.md`
  rules (#154, #158).

## Agent skills

### Issue tracker

GitHub Issues and milestones in this repo, via `gh`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical role strings unchanged, plus `bug` and `found-in-flight`.
See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` at the root is the authority; no `docs/adr/` yet.
See `docs/agents/domain.md`.

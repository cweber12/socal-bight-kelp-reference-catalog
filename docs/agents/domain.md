# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the
codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root. This repo is single-context; there is no `CONTEXT-MAP.md`.
- **`docs/adr/`** — does not exist yet. If it appears, read the ADRs touching the area you are
  about to work in.

If a file listed here doesn't exist, **proceed silently**. Don't flag its absence; don't suggest
creating it upfront. The producer skill (`/grill-with-docs`) creates them lazily when terms or
decisions actually get resolved.

## `CONTEXT.md` is the authority

`CONTEXT.md` states the rule, the record schemas, the vocabularies and the region tree;
`src/kelpcatalog/schema.py` implements it. **If the code and `CONTEXT.md` disagree, `CONTEXT.md` is
right and the code is a bug** — change the code, not the document, unless a human decides otherwise.

## File structure

    /
    ├── CONTEXT.md          the authority: the rule, schemas, vocabularies, region tree, notebooks, gates
    ├── CLAUDE.md           how to work: tracker, branches, commits, scope guards
    ├── catalog/            the records themselves, one markdown file each
    │   ├── sources/        a dataset, program, report series or transcribed table
    │   ├── references/     a paper or report cited by a source or a figure
    │   ├── excluded/       an item reviewed and not admitted, with its one-line reason
    │   ├── regions/        a node of the region tree
    │   ├── beds/           a CDFW Administrative Kelp Bed
    │   ├── sites/          a monitoring program's named station
    │   └── tables/         transcribed and derived tables as CSV
    ├── notebooks/          generated from the records: 00_index plus one per topic in a folder per group
    ├── docs/
    │   ├── agents/         this file and its siblings
    │   └── prd/<slug>.md   one PRD per milestone
    ├── .claude/
    │   ├── skills/         add-source (walks one record in), audit-pr (commissions the audit),
    │   │                   run-prd (derives a PRD's work order, then dispatches its first
    │   │                   record row through record-row.md and opens its PR)
    │   ├── agents/         pr-auditor, the audit method
    │   ├── hooks/          advise.py and advise.sh, the two advisory PostToolUse checks
    │   ├── settings.json   declares those two hooks on Edit and Write
    │   └── worktrees/      git-ignored; where an agent's worktree checkouts go
    ├── gate.py             the one command that runs every gate
    ├── src/fetch/<id>.py   one script per FETCHED source; writes data/raw/<id>/ and its manifests
    ├── src/kelpcatalog/
    │   ├── schema.py       implements CONTEXT.md's records, vocabularies and links
    │   ├── plan.py         CONTEXT.md's notebook facts as data: questions, paths, region order
    │   ├── build.py, generate.py     records in, notebooks out
    │   ├── notebook.py     what a figure cell imports: provenance(...) and load(source_id)
    │   └── structure.py, outputs.py, fresh.py, figure_provenance.py   the four notebook gates
    ├── data/               git-ignored; reproducible from src/fetch/
    └── tests/              the unit gate's tests, with fixtures

## Use the vocabulary as written

When your output names a domain concept — an issue title, a refactor proposal, a hypothesis, a test
name — use the term as `CONTEXT.md` defines it. The controlled vocabularies are `status`, `tier`,
the ten `topics` with their sub-topics, the region tree, a bed's `status` (`Open` · `Closed` ·
`Leasable` · `Lease Only`) and a county node's `consortium` (`RNKSC` · `CRKSC`). These are closed
sets: a value outside them is a schema error, not a synonym.

If the concept you need isn't there, that's a signal — either you're inventing language the project
doesn't use (reconsider), or there's a real gap. A missing topic is added in its own PR; a source is
never excluded for want of a tag.

## Flag conflicts

If your output contradicts `CONTEXT.md` (or, once they exist, an ADR), surface it explicitly rather
than silently overriding:

> _Contradicts `CONTEXT.md` "Record format" (the body below the frontmatter must be empty) — but
> worth reopening because…_

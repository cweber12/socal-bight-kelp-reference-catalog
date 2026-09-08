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
    ├── CONTEXT.md          the authority: the rule, schemas, vocabularies, region tree
    ├── CLAUDE.md           how to work: tracker, branches, commits, scope guards
    ├── docs/
    │   ├── agents/         this file and its siblings
    │   └── prd/<slug>.md   one PRD per milestone
    └── src/kelpcatalog/    schema.py implements CONTEXT.md

## Use the vocabulary as written

When your output names a domain concept — an issue title, a refactor proposal, a hypothesis, a test
name — use the term as `CONTEXT.md` defines it. The controlled vocabularies are `status`, `tier`,
the ten `topics` with their sub-topics, and the region tree. These are closed sets: a value outside
them is a schema error, not a synonym.

If the concept you need isn't there, that's a signal — either you're inventing language the project
doesn't use (reconsider), or there's a real gap. A missing topic is added in its own PR; a source is
never excluded for want of a tag.

## Flag conflicts

If your output contradicts `CONTEXT.md` (or, once they exist, an ADR), surface it explicitly rather
than silently overriding:

> _Contradicts `CONTEXT.md` "Record format" (the body below the frontmatter must be empty) — but
> worth reopening because…_

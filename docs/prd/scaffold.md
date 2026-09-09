# PRD — Scaffold (milestone 6.1)

Status: active
Created: 2026-09-07

## Problem

There is no repo yet. Before a single source can be catalogued, the rules, the schema that enforces
them, a gate that runs the schema, CI that runs the gate, and the workflow that turns an issue into
a reviewed record all have to exist. If they are built after the content, the content is entered
inconsistently and re-done.

## Solution

The smallest set of files that lets one source enter through the intended workflow and be checked
by a machine. `CONTEXT.md` is the authority; `schema.py` implements it; `gate.py` runs it; CI runs
`gate.py`; the `add-source` skill walks an agent through one record; the first source proves the
loop.

## Slices

| # | slice | seam | done when |
|---|---|---|---|
| 1 | `CONTEXT.md`, `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`, `LICENSE` | — | reviewed and merged; `CLAUDE.md` fits one screen |
| 2 | schema, tests, gate, CI | `parse_record`, `validate`, `load_catalog`, `check_catalog`; gate rows `unit`, `catalog-schema` | CI green on Ubuntu and Windows with an empty catalog; branch protection on |
| 3 | tracker setup | labels, milestones, board, Parking lot, `docs/agents/` | `docs/agents/issue-tracker.md` says `gh` |
| 4 | `add-source` skill v0 | `.claude/skills/add-source/SKILL.md` | de-dupes against sources, references, excluded; checks the route; writes the record; runs `gate.py` |
| 5 | first source: `noaa_oni` | one record, one fetch script | merged via PR through the skill |
| 6 | second and third: `sio_shore_stations`, `calcofi` | two records, two scripts | merged; the skill's rough edges from slice 5 fixed first |

## Non-goals

No lock file, no fetch entry point, no notebooks, no index pages, no regions below `scb`, no parser
for any file from the reference repo. Each of those has its own milestone.

## Done

Three sources in `catalog/sources/`, entered through the skill, gate green in CI. If this milestone
runs past a week, the scaffold is too big; cut, do not extend.

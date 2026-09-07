# Contributing

## Adding a source

1. Check it is not already in `catalog/sources/`, `catalog/references/` or `catalog/excluded/`.
2. Open the source's own page and confirm the route works today.
3. Create `catalog/sources/<id>.md` with the fields in `CONTEXT.md` — every value from the source
   itself, the licence text verbatim, no prose body.
4. Run `python gate.py`. Fix every problem it names.
5. Open a PR titled `catalog: add <id>`; paste the gate output into the body.

Inside a Claude Code session the `add-source` skill does steps 1–4.

## Adding a reference, exclusion, region, bed or site

Same shape; the schemas are in `CONTEXT.md`. A reference needs a DOI or URL. An exclusion needs a
one-line reason. A region, bed or site needs `defined_by` — the source that draws its boundary.

## Anything else

Open an issue first, or add the idea to the pinned Parking-lot issue. Code changes come with a
failing test first, one PR per issue, squash-merged. Commit messages: `<type>(<scope>): <subject>`,
body says why, `Closes #N`.

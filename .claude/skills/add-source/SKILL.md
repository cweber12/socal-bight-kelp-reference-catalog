---
name: add-source
description: Use when adding one source — a dataset, monitoring program, report series or transcribed table — to catalog/sources/ in the SoCal Bight kelp reference catalog. Invoked as /add-source <id-or-url>. Walks the source in: de-duplicate, confirm the route, draft the record, fetch, run the gate, stop for review.
---

# add-source

Walk **one** source into `catalog/sources/`. `CONTEXT.md` is the authority for every field, every
vocabulary and the rule the record obeys: *a record holds only what the source itself states, and
what anyone repeating the fetch would reproduce.* Facts in fields; the body below the closing `---`
is empty.

Do the seven steps **in order**. **Stop at the first one that fails**: say which step, what it
found, and what you have written so far, then wait. Never skip ahead, and never make a step pass by
widening the schema or by writing a value the source does not state.

## 0. Read first

`CONTEXT.md` — "The rule", "Vocabularies", "Record schemas" (the `sources` table), "The region
tree". Do not work from memory of them; the vocabularies are closed sets.

## 1. De-duplicate

Search all three directories for the id, the URL, the DOI and distinctive words of the title — the
same source is often already in under a different id, or already reviewed and turned down:

```sh
grep -ril -e "<id>" -e "<url>" -e "<doi>" -e "<title words>" \
  catalog/sources catalog/references catalog/excluded
```

**STOP if anything matches.** Name the file and the matching line and ask whether to update that
record instead. Do not add a second record for one source.

## 2. Confirm the route works today

Open the landing page (or the direct file URL). Write down today's date — that is `retrieved`, and
it is also the date any "…, retrieved YYYY-MM-DD" fact in the record is stated as of.

What you find decides `status`, and it is a fact either way:

| what happens | `status` | `tier` |
|---|---|---|
| the file downloads / the page opens and you take the bytes | `VERIFIED` | `FETCHED` |
| you have the printed page in hand and type its values | `VERIFIED` | `TRANSCRIBED` |
| the route is documented but you did not exercise it | `PATTERN` | `NOT HELD` |
| it needs a login or an account you do not have | `NOT PUBLIC` | `NOT HELD` |
| it arrives only by asking a person | `ON REQUEST` | `NOT HELD` |

`VERIFIED` requires a `tier` of `FETCHED` or `TRANSCRIBED` — nothing else has exercised the route.

**STOP if the URL is dead or resolves to something other than the source.** There is no route to
record, and guessing one is a fact the source does not state.

## 3. Draft `catalog/sources/<id>.md`

Every field in `CONTEXT.md`'s sources schema, in the order that table lists them; required fields
are marked `*` there. The whole file is one YAML frontmatter block and the body is empty.

- Every value comes from the page or the file itself. No commentary, no computed numbers, no
  judgement of quality, no note about how the record came to be.
- `license`: the licence text **verbatim** as published; `"not stated"` when the source states none.
- `variables`: as the source lists them; `[]` when `tier` is `NOT HELD`.
- `coverage` as the source states it, and `coverage_stated_at` where it states it.
- `retrieved`: today's date from step 2 when `FETCHED`; `null` when `NOT HELD`.
- `topics`: tags from `CONTEXT.md` only. **A source that fits no topic is never excluded for it** —
  stop and say so, and adding the topic is its own PR.
- `regions`: the most specific node that covers it, or `global` for a source with no regional bound.
- Unknown optional value → `null`; unused list → `[]`. Never invent a field.

## 4. If `tier` is `FETCHED`: write and run `src/fetch/<id>.py`

The script downloads the file(s) into `data/raw/<id>/` and writes, per file,
`data/raw/<id>/manifest_<stem>.json` with `url`, `fetched_at`, `sha256`, `bytes`, `http_status`.
Standard library only (`urllib`, `hashlib`, `json`) — do not add a dependency.

Run it. Set `retrieved` from that run, and set `fetch_script: src/fetch/<id>.py`.

`data/` is git-ignored and reproducible from the script. **Never write into `data/` by hand and
never `git add` it** — the script is the record of the fetch.

**STOP if the download fails.** Do not hand-fill a manifest, and do not leave `status: VERIFIED`
behind a fetch that did not happen.

## 5. If the source cites a paper a figure will apply: draft `catalog/references/<citekey>.md`

`citekey` is first author's surname + year and equals the file name. Only equations a figure will
actually apply go in `equations`, each `{id, as_printed, where}` — the equation **exactly as the
paper prints it**, with its page or equation number. Never adjusted, clipped or extended here. A
reference needs a `doi` or a `url`.

## 6. Run the gate

```sh
.venv/Scripts/python gate.py     # .venv/bin/python on macOS/Linux
```

Fix every problem it names **in the record**. Never in `src/kelpcatalog/schema.py`, never by
relaxing a rule, never by deleting the field it complains about.

**STOP if the gate is wrong** — if it contradicts `CONTEXT.md`. `CONTEXT.md` wins and the code is a
bug: report it instead of working around it (`CLAUDE.md`, "In-flight bugs").

## 7. Show and stop

Print the record in full and the gate output verbatim, and **stop**. Do not commit, do not open a
PR, do not touch notebooks or index pages. Wait to be told.

## Non-goals

No lock file. No changes to `schema.py`. No index or notebook pages. No writing into `data/` by
hand. No parser for any external manifest or prose file — records are entered, not migrated. More
than one source is more than one run of this skill.

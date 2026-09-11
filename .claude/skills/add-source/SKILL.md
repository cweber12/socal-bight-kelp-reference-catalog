---
name: add-source
description: Use when adding one source — a dataset, monitoring program, report series or transcribed table — to catalog/sources/ in the SoCal Bight kelp reference catalog. Invoked as /add-source <id-or-url>. Walks the source in: de-duplicate, confirm the route, draft the record, fetch, run the gate, refresh the notebooks, stop for review.
---

# add-source

Walk **one** source into `catalog/sources/`. `CONTEXT.md` is the authority for every field, every
vocabulary and the rule the record obeys: *a record holds only what the source itself states, and
what anyone repeating the fetch would reproduce.* Facts in fields; the body below the closing `---`
is empty.

Step 0 is setup. Do the eight steps **1–8 in order**. **Stop at the first one that fails**: say
which step, what it found, and what you have written so far, then wait. Never skip ahead, and never
make a step pass by widening the schema or by writing a value the source does not state.

`noaa_oni` is the worked example throughout: `catalog/sources/noaa_oni.md` and
`src/fetch/noaa_oni.py` on `main` are what a finished run of this skill produces.

## 0. Read first, then branch

Read `CONTEXT.md` — "The rule", "Vocabularies", "Record schemas" (the `sources` table), "The region
tree". Do not work from memory of them; the vocabularies are closed sets.

Then branch, before writing any file:

```sh
git switch -c catalog/add-<id>
```

A branch is `<type>/<slug>` and `catalog` is the type for record changes (`CLAUDE.md`, "Branches,
commits, PRs"). Every file this skill writes belongs on that branch — the record, any reference
record, the fetch script, and the notebooks step 7 regenerates, nothing else. Creating the branch is
not committing to it; step 8 still stops short of a commit.

## 1. De-duplicate

The same source is often already in under a different id, or already reviewed and turned down.
Search all three record directories twice: once with `-w`, so an id or an acronym matches as a whole
word instead of inside a longer one, and once for the URL by host and path, so the scheme and any
query string cannot hide it.

```sh
git grep -ilw -e "<id>" -e "<acronym>" -e "<doi>" -e "<distinctive title word>" \
  -- catalog/sources catalog/references catalog/excluded
git grep -il -e "<host>/<path>" \
  -- catalog/sources catalog/references catalog/excluded
```

`-w` is what keeps the search honest: for `noaa_oni`, a bare `-e "oni"` matches every record with
the word *monitoring* in it, and a search that fires on every run gets ignored. The URL search takes
`www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt` — no `https://`, no `?query`.

Both searches are load-bearing, and neither covers for the other. `-w` counts underscore as a word
character, so searching `noaa_oni` does not match the id `noaa_oni_copy`: two records of one source
need not share an id, but they do share a URL, which is what the second search is for.

Read every match. **STOP if one is this source** — name the file and the matching line and ask
whether to update that record instead. Do not add a second record for one source.

## 2. Confirm the route works today

Open the landing page (or the direct file URL). Write down today's date: it is the date every
"…, retrieved YYYY-MM-DD" fact in the record is stated as of, and for a fetch it is `retrieved`,
which step 4 sets from the manifest.

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

The whole file is one YAML frontmatter block and the body is empty.

**Write every field in `CONTEXT.md`'s `sources` table, every time, in the order that table lists
them** — `null` for a scalar that does not apply, `[]` for a list you are not using. Absent and null
validate the same, but a record showing every row renders as a complete table on GitHub and diffs
against every other record. Required fields are marked `*` there. Never invent a field the table
does not list.

- Every value comes from the page or the file itself. No commentary, no computed numbers, no
  judgement of quality, no note about how the record came to be.
- `license`: the licence text verbatim as published. Look in this order and stop at the first that
  states terms: the file itself, its landing page, then a terms/licence/disclaimer page that landing
  page links from its own footer. Quote it, then say where you found it — inside the same value,
  since the schema has no second field for it. Never substitute a licence name you inferred:
  "public domain (US federal government work)" is a conclusion, not published text. `"not stated"`
  only when none of those states terms.
- `variables`: as the source lists them; `[]` when `tier` is `NOT HELD`.
- `coverage` as the source states it, and `coverage_stated_at` where it states it. When `coverage`
  draws on several places, name each in `coverage_stated_at` in the order its clause appears in
  `coverage`. A span read off a file's first and last rows is a fact of the copy you fetched: date
  it, and expect to restate it on re-fetch.
- `retrieved`: the date of the fetch in step 4 when `FETCHED`; `null` when `TRANSCRIBED` (the
  provenance is `transcribed_from`, not a fetch); `null` when `NOT HELD`.
- `topics`: tags from `CONTEXT.md` only. **A source that fits no topic is never excluded for it** —
  stop and say so, and adding the topic is its own PR.
- `regions`: the most specific node that covers it, or `global` for a source with no regional bound.

`catalog/sources/noaa_oni.md` shows all of this: every row present, `file: null` and
`transcribed_from: null` among them; a licence quoted from the NWS disclaimer two hops out, with the
footer it was reached through; and a `coverage_stated_at` naming the landing page, then the file, in
the order `coverage` uses them.

## 4. If `tier` is `FETCHED`: write and run `src/fetch/<id>.py`

Standard library only (`urllib`, `hashlib`, `json`) — do not add a dependency (`CLAUDE.md`: no
dependencies an issue did not ask for). Copy the shape of `src/fetch/noaa_oni.py`.

**The bytes.** Each file lands in `data/raw/<id>/` exactly as the server sent it — never unzipped,
converted or re-encoded on the way in. The manifest hashes those served bytes.

**The manifest.** One per file, named for the served file name whole, extension included:
`data/raw/<id>/manifest_<served file name>.json` — so `oni.ascii.txt` gives
`manifest_oni.ascii.txt.json`. A stem would be ambiguous for a multi-dot name and would collide for
two files differing only by extension. Each manifest holds:

| key | value |
|---|---|
| `url` | the URL fetched |
| `fetched_at` | local timestamp of the fetch |
| `sha256`, `bytes` | of the bytes as served |
| `http_status` | the response status |
| `content_type`, `last_modified`, `etag` | the like-named response headers; `null` when absent |

The headers are what a repeat fetch *records*, not what it reproduces — `Last-Modified` moves when
the steward updates the file, and CPC sends no `ETag` on the ONI file at all. Do not add
`content_length`: it duplicates `bytes`.

**Run it, then lint it** — CI runs `ruff` on every PR:

```sh
.venv/Scripts/python src/fetch/<id>.py     # .venv/bin/… on macOS/Linux
.venv/Scripts/ruff check src/fetch/<id>.py && .venv/Scripts/ruff format src/fetch/<id>.py
```

Set `fetch_script: src/fetch/<id>.py`, and set `retrieved` to the local date of the manifest's
`fetched_at`. When that differs from the date you wrote down in step 2 — a fetch that lands after
midnight, a run resumed the next day — re-confirm the page facts in step 6, and the record then
dates to the fetch day throughout. A "…, retrieved YYYY-MM-DD" clause states the day you read that
page, so never re-date one you did not re-read: a record may honestly carry two dates, but never a
date you did not observe.

`data/` is git-ignored and reproducible from the script. **Never write into `data/` by hand and
never `git add` it** — the script is the record of the fetch.

**STOP if the download fails.** Do not hand-fill a manifest, and do not leave `status: VERIFIED`
behind a fetch that did not happen.

## 5. If a field needs a reference: draft `catalog/references/<citekey>.md`

Add a reference only when a field needs it — `transcribed_from.reference` — or when a figure that
already exists applies it. Otherwise `references: []`. Judge that against the figures committed
today: step 7 regenerates markdown and writes no figure cell, so a figure that would cite the paper
arrives in its own change and brings whatever it cites with it.

`citekey` is first author's surname + year and equals the file name, and a reference needs a `doi`
or a `url`. Only equations an existing figure applies go in `equations`, each
`{id, as_printed, where}` — the equation **exactly as the paper prints it**, with its page or
equation number. Never adjusted, clipped or extended here.

## 6. Run the gate, then check the record against the source

```sh
.venv/Scripts/python gate.py     # .venv/bin/python on macOS/Linux
```

Fix every problem it names **in the record**. Never in `src/kelpcatalog/schema.py`, never by
relaxing a rule, never by deleting the field it complains about.

**STOP if the gate is wrong** — if it contradicts `CONTEXT.md`. `CONTEXT.md` wins and the code is a
bug: report it instead of working around it (`CLAUDE.md`, "In-flight bugs").

Then two checks no gate makes. Both feed step 8.

- **Byte-diff every quoted string against the source.** Take each quoted string in the record —
  title, licence, `coverage`, `format`, any phrase in quotation marks — back to the live page or
  file it came from and compare it character for character. A curly quote straightened, a hyphen
  dropped, a line break turned into a space: each is a value the source does not state. Correct
  the record to what the source states today; if the source itself has changed since you drafted
  the record, say so in the step-8 report.
- **Every URL the script fetches appears in `access`.** Verbatim, when `FILES` is a literal list.
  When `FILES` is built from a template or a query string, `access` names the pattern and gives one
  worked example URL.

## 7. Refresh the notebooks the source appears in

`CONTEXT.md`, "Notebooks": *a source is not "in" until the notebooks that show it are refreshed in
the same PR.* One command rebuilds every notebook from the records:

```sh
.venv/Scripts/python -m kelpcatalog.generate     # .venv/bin/python on macOS/Linux
```

**Name the notebooks before running it**, so the diff can contradict you.

**Adding a record** — the set is exact, and every notebook in it moves: one per *topic* in the
record's `topics`, one per topic on a reference record step 5 drafted (`topics` is required there
too, and a reference renders in its own topics, not the source's), and `00_index.ipynb`, which
counts sources and references and so moves for either. A tag is `<topic>` or `<topic>/<sub-topic>`
and only the topic half picks the notebook — `ocean-climate/salinity` puts the source in a section
of `11_ocean_climate.ipynb`, not in a notebook of its own. `plan.NOTEBOOK_PATHS` maps a topic to its
path and `plan.INDEX_PATH` is the index; they transcribe `CONTEXT.md`'s `notebooks/` tree, which is
the authority.

**Updating a record**, when step 1 sent you to one — name the union of its topics *before* and
*after* your edit, plus `00_index.ipynb`. A tag you removed or retagged still moves the notebook it
is leaving, so neither reading alone bounds the set. The union is a bound and not an equality:
inside it a notebook moves only when something it prints changed, so expect fewer to move than you
named — a `steward` edit moves both of this record's topic notebooks and not the index, and adding
one tag moves one topic notebook and the index.

Then read what moved. The command writes them all; git shows the ones whose rendering changed.

```sh
git status --short notebooks/
```

**STOP if anything moved that your set does not contain.** That means the `topics` are not what you
read them to be, or the tree was already behind its records and this run swept it in. Tell the two
apart by opening the moved notebook's diff and looking for the id you are working on: if it is
there, your set was wrong; if the diff is entirely other records, someone landed a record without
refreshing. Report which, rather than running the command again.

On the **add** path also **STOP if a notebook you named did not move** — the set is exact there. On
the **update** path that is ordinary, because the union is a bound.

**Regeneration never touches a figure.** The builder writes generated cells as markdown only, and a
figure cell is "never generated and never touched" (`CONTEXT.md`, "Notebooks"), so a record change
rewrites prose and moves no PNG byte, so a regeneration after a record change cannot turn
`notebook-fresh` red. That row gets
teeth when you open a notebook in Jupyter to change a figure — it compares `execution_count` as well
as outputs, so a cell saved with `execution_count: 2`, what running a cell twice gives, is reported
stale even when the picture is right. End such a session with **Restart and Run All**.

Stage the record, any reference record, the fetch script and every notebook that moved, then **run
`gate.py` again** — step 6's run described bytes these have replaced, and rows of it read notebooks.

## 8. Show and stop

Print, in full: the record and any reference record; the manifest of every file fetched; the gate
output verbatim; the
result of the two step-6 checks — which quoted strings you diffed and against what, and that every
URL the script fetches is in `access`; and the notebooks step 7 moved. Then **stop**. Do not commit
and do not open a PR. Wait to be told.

## Non-goals

No lock file. No changes to `schema.py`. No hand-edited notebook or index page — step 7 regenerates
both, and nothing else under `notebooks/` is this skill's to write. No writing into `data/` by
hand. No parser for any external manifest or prose file — records are entered, not migrated. More
than one source is more than one run of this skill.

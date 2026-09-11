# Southern California Bight kelp source catalog

A catalog of the authoritative sources — datasets, monitoring programs, reports and papers — behind
kelp forest monitoring from Point Conception to the US–Mexico border, including the Channel
Islands. Each source is one record: who holds it, how to reach it, what it contains, under what
licence, and when it was last retrieved. Records are tagged by **topic** (ten questions in three
groups, each with sub-topics) and by **region** (the Bight, its counties and islands, CDFW
Administrative Kelp Beds, and program sites), so a researcher can find what exists for a question
or a place and reach the original in one click.

One rule governs every record: it holds only what the source itself states, and what anyone
repeating the fetch would reproduce. No commentary, no numbers computed here. The rule, the record
schemas and the region tree are in [`CONTEXT.md`](CONTEXT.md). Figures, where they exist, plot
catalogued data with equations as the cited paper prints them, with the citation under the plot.

**Licences.** Code is MIT ([`LICENSE`](LICENSE)); everything else in the repository — catalog
records, documentation, `CONTEXT.md`, `README.md`, `CLAUDE.md`, `CONTRIBUTING.md` — is CC BY 4.0
([`LICENSE-CATALOG.md`](LICENSE-CATALOG.md)). Each source's own licence is on its record; no data
is relicensed.

## Using it

Records live under `catalog/` and render as tables on GitHub. Notebooks — one per question, in a
folder per group, generated from the records — start at
[`notebooks/00_index.ipynb`](notebooks/00_index.ipynb), which counts what each topic holds and
sets the topics against the regions in use. They are committed, so they read on GitHub without
running; `.venv/Scripts/python -m kelpcatalog.generate` rebuilds every one of them from the
records.

## Adding a source

See [`CONTRIBUTING.md`](CONTRIBUTING.md). In short: open an issue, run the `add-source` skill
(or follow the checklist by hand), run `.venv/Scripts/python gate.py`, open a PR.

## Running the gates

```sh
python -m venv .venv
.venv/Scripts/pip install -e ".[dev]"      # .venv/bin/pip on macOS/Linux
.venv/Scripts/python gate.py               # .venv/bin/python on macOS/Linux
```

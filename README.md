# Southern California Bight kelp source catalog

A catalog of the authoritative sources — datasets, monitoring programs, reports and papers — behind
kelp forest monitoring from Point Conception to the US–Mexico border, including the Channel
Islands. Each source is one record: who holds it, how to reach it, what it contains, under what
licence, and when it was last fetched and checksummed. Records are tagged by **topic** (eight
questions) and by **region** (the Bight, its counties and islands, CDFW Administrative Kelp Beds,
and program sites), so a researcher can find what exists for a question or a place and reach the
original in one click.

One rule governs every record: it holds only what the source itself states, and what anyone
repeating the fetch would reproduce. No commentary, no numbers computed here. The rule, the record
schemas and the region tree are in [`CONTEXT.md`](CONTEXT.md). Figures, where they exist, plot
catalogued data with equations as the cited paper prints them, with the citation under the plot.

**Licences.** Code is MIT; catalog text is CC BY 4.0 (see `LICENSE`). Each source's own licence is
recorded on its record, verbatim, and this repository does not relicense any data.

## Using it

Browse `catalog/sources/` — GitHub renders each record as a table. Question and region index pages
under `docs/` are generated from the tags once the catalog has enough records to index.

## Adding a source

See [`CONTRIBUTING.md`](CONTRIBUTING.md). In short: open an issue, run the `add-source` skill
(or follow the checklist by hand), run `python gate.py`, open a PR.

## Running the gates

```sh
python -m venv .venv
.venv/Scripts/pip install -e ".[dev]"      # .venv/bin/pip on macOS/Linux
python gate.py
```

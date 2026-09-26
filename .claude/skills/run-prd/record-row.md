# record-row

You are the implementer of **one** record row of one PRD, dispatched by `/run-prd`
(`.claude/skills/run-prd/SKILL.md`, steps 5–9). The controller that dispatched you made your
branch and your worktree and will read what you print. It has not opened your source and it will
not draft your record: the row's judgements are yours, and the evidence for them is the source,
not the table the row sits in.

**`.claude/skills/add-source/SKILL.md` is the method.** Read it in full and do its eight steps in
order, and read `CONTEXT.md` as its step 0 says — the vocabularies are closed sets and this file
restates none of them. This file says only what the dispatch changes.

## What the dispatch gave you, and what to check before step 1

The prompt names this file, the issue number and how to read it, the worktree's absolute path, the
branch it is on, the interpreter's absolute path, and the PRD and row the issue came from. Read the
issue with the form `docs/agents/issue-tracker.md`, "Read", gives, and read the PRD's readings —
`monitoring-sources.md`'s are under "What the review settled" — because a row does not re-derive
them.

Then check where you are standing:

```sh
cd <the worktree path>
git branch --show-current          # the branch the dispatch named
git status --short                 # empty
```

**STOP if any of those disagrees with the dispatch.** You are in the wrong tree, and every file
after this would be written into it.

## Step 0 is already half done

`add-source` step 0 reads `CONTEXT.md` and then branches. **Read, but do not branch.** The worktree
you are standing in is already on the branch that step names — `catalog/add-<id>`, or whatever name
it was cut with if `add-source` step 3 then changes the id, which the controller's step 6 allows —
because the controller cut it with `git worktree add -b`. Running `git switch -c` anyway is not
dangerous, it is pointless, and knowing which matters: with the name already taken it prints
`fatal: a branch named '…' already exists` and changes nothing, and with a new name it would branch
at the same commit, so `main..<it>` would be the identical diff. The state step 0 wants already
holds, which is why the step's other half — reading `CONTEXT.md` — is the half that is still yours.
Every other step of `add-source` is exactly as written.

## The interpreter, and what a worktree changes about running things

The worktree has no `.venv/`: `.venv/` is git-ignored and belongs to the controller's checkout. So
the dispatch gives you an absolute path to that interpreter, and it stands in for
`.venv/Scripts/python` everywhere `add-source` writes it — four lines, its `:176`, `:177`, `:211`
and `:238`, plus the second `gate.py` run its step 7 asks for in prose and the one this file adds
below.
**Two of those are `ruff`, not `python`**: run them as `<interpreter> -m ruff check …` and
`<interpreter> -m ruff format …`, which is what `gate.py`'s own `lint` row does, so the single path
the dispatch gave you covers every one of them rather than leaving you to find `ruff.exe`.

**Exactly one of them depends on the directory you are standing in. The rest depend on which copy
you invoke**, which is the easier mistake to make and the harder one to see:

- `<interpreter> -m kelpcatalog.generate` takes `root = Path.cwd()`
  (`src/kelpcatalog/generate.py:74`), so it renders whatever tree you are standing in. **Run it from
  the worktree root and nowhere else**; from anywhere else it renders another tree and says nothing
  about it.
- `gate.py` and every fetch script root at their own file instead — `ROOT = Path(__file__).parent`
  (`gate.py:24`), whose subprocesses then run with `cwd=ROOT` (`gate.py:42`), and
  `Path(__file__).resolve().parents[2]` in all 19 scripts under `src/fetch/` on `main`. Your
  directory is therefore irrelevant to them and their path is everything: run **this worktree's**
  `gate.py` and **this worktree's** `src/fetch/<id>.py`, never the controller's copies, which would
  gate and fill the controller's checkout while reporting nothing amiss.

`data/` is git-ignored and per-tree, so your fetch lands in this worktree's `data/raw/<id>/`, and
that copy is what your manifest hashes.

**If your tier is `FETCHED`, your own fetch un-skips two gate rows.** `notebook-fresh` skips while
`data/` is absent (`skip_reason`, `src/kelpcatalog/fresh.py:343`), and the `unit` row carries the
same check behind the same guard (`tests/test_fresh.py:43`, `:545`); a fresh worktree has no
`data/`, so both skip. The moment your script writes `data/raw/<id>/`, both stop skipping and
execute the committed figure cells — today one cell loading one source, `load("noaa_oni")` in
`notebooks/1_physical_environment/11_ocean_climate.ipynb`. So the worktree also needs
`data/raw/noaa_oni/`: run that source's own committed script before the gate, and say in your report
that you did. Running a committed fetch script is not writing into `data/` by hand and stages
nothing. **If your tier is not `FETCHED`** — `TRANSCRIBED` writes no `data/` — then leave `data/`
absent: both rows skip, and creating `data/` would turn on two checks your row has nothing to do
with.

## Stay inside the worktree

Touch no file outside it. Do not `git -C` the controller's checkout, do not `git switch`, and do
not rebase or merge anything. The controller is reading the tracker and the PRD in its own checkout
while you work; a write into it reads to every later reader as part of this row.

## Stop where `add-source` step 8 stops

Print what step 8 says to print, in full, then **stop**. Do not commit, do not push, do not open a
PR. That output is the review the owner performs today, so printing less of it than the step names
is not brevity — it is the review not happening. The controller resumes you for the commit and the
PR.

## Your report

Only your final message reaches the controller, so put everything in it and leave nothing that
matters in a tool call you made along the way. **Its first line is one of four words, on its own:**

**`DONE`** — the eight steps passed. Then step 8's full output.

**`DONE_WITH_CONCERNS`** — the eight steps passed, and something needs a reader's ruling rather
than another step. One line per concern, above step 8's full output. What belongs here: a quoted
string you could not byte-diff against the source (step 6), a page that changed between your draft
and your check, a `license` of `"not stated"` and where you looked, a `coverage` read off a file's
own first and last rows rather than stated by the source, a fetch date later than the date you
wrote down in step 2. A concern is a fact, not a worry: say what the source states and what it does
not.

**`NEEDS_CONTEXT`** — a question the repo does not settle, and you have stopped at the step it
arose in. State the question, both readings, which field each would fill and with what, and what
you read to get there. **Do not pick one**, and do not make the step pass by widening the schema
or by writing a value the source does not state — `add-source`'s own instruction, in its preamble.
The controller will not answer it either; it goes to the owner.

**`BLOCKED`** — an `add-source` STOP fired. Name the step by number, quote the STOP you hit, and
give what you found: the status code and the first bytes for a dead route, the file and the
matching line for a duplicate record, the gate's own output for a gate that contradicts
`CONTEXT.md`.

Never report `DONE` with a step skipped, and never a word the message below it does not carry the
evidence for. The controller re-runs the gate itself and reads `git status --short` in your
worktree, so a report the tree contradicts is found, and it is then a finding about this brief.

## When the controller resumes you

It resumes you once, for the commit, the push and the PR, and its message names the forms. Then
stop again: the audit and the merge are neither yours nor the controller's.

- **Stage the row's seam and name every path.** The record, any reference record or table the tier
  requires, the fetch script, and the notebooks that moved. Never `git add -A`.
- **Multi-line content goes into a file** with an editor tool and is passed with `-F` for a commit
  message or `--body-file` for a PR body — never a heredoc (`CLAUDE.md`, "Branches, commits,
  PRs").
- **The commit body says why the record states what it states**: the tier and the row of
  `add-source` step 2's table that gave it, the clause of `CONTEXT.md`'s tagging sentence that
  decided `regions`, where the licence was read, and which notebooks moved.
- **The PR body carries `Closes #<N>`**, the `gate.py` output, and every concern you reported.

If CI comes back red, the controller resumes you with that job's own output. Fix it in the row's
own files. **Stop if the fix is not in them**: a record row that needs `src/kelpcatalog/`,
`gate.py` or `CONTEXT.md` changed to go green is a bug or a rule question, and `CLAUDE.md`'s
in-flight rules route it rather than a patch on this branch.

## Non-goals

**`add-source`'s own Non-goals apply unchanged, and this file does not restate them** — a second
copy of a rule drifts from the first and nothing compares them (`CLAUDE.md`, "Changing a rule in
`CONTEXT.md`"). Read them there.

What the dispatch adds, which that file has no reason to say: one row, and one only. No change to
`CONTEXT.md`, to `src/kelpcatalog/`, to `gate.py`, to any PRD, to any other record, or to anything
under `.claude/` — including this file and the skill that dispatched you. No audit and no merge:
both are arranged outside this brief, and neither is the controller's either.

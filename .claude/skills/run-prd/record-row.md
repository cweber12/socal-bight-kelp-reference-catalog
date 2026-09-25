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
you are standing in is already on the branch that step names, `catalog/add-<id>`, because the
controller cut it with `git worktree add -b`. A second `git switch -c` would branch off your own
branch, and the PR would diff against the wrong base. Every other step of `add-source` is exactly
as written.

## The interpreter, and what a worktree changes about running things

The worktree has no `.venv/`: `.venv/` is git-ignored and belongs to the controller's checkout. So
the dispatch gives you an absolute path to that interpreter, and it goes everywhere `add-source`
writes `.venv/Scripts/python`. Three of its commands care where you run them from, and all three
want the worktree root:

- `<interpreter> gate.py` — `gate.py` roots at its own file (`ROOT = Path(__file__).parent`,
  `gate.py:24`), so the worktree's own copy gates the worktree.
- `<interpreter> -m kelpcatalog.generate` — it roots at the current directory
  (`root = Path.cwd()`, `src/kelpcatalog/generate.py:74`), so from the worktree root it reads this
  tree's `catalog/` and writes this tree's `notebooks/`. From anywhere else it renders another tree
  and says nothing about it.
- `<interpreter> src/fetch/<id>.py`, and the two `ruff` commands of `add-source` step 4.

`data/` is git-ignored and per-tree, so your fetch lands in this worktree's `data/raw/<id>/`, and
that copy is what your manifest hashes.

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

One row. No other source — a second is a second row and a second run of `add-source`. No change to
`CONTEXT.md`, to `src/kelpcatalog/`, to `gate.py`, to any PRD, to any other record, or to anything
under `.claude/`. No hand-edited notebook or index page: `add-source` step 7 regenerates both. No
writing into `data/` by hand and no `git add` of it. No new dependency. No parser for any external
manifest or prose file — records are entered, not migrated. No audit and no merge.

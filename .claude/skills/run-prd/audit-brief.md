# audit-brief

How the controller of `/run-prd` assembles the brief that `.claude/skills/audit-pr/SKILL.md`,
step 1, specifies, at `run-prd` step 10. The brief's six parts are that step's; this file adds no
part and restates none. It says where each part's content already is when the diff's author is an
implementer the controller dispatched (`run-prd`, step 7) and the brief's author is the controller.

Write it to `Claude outputs/prompt-audit-pr<N>-<id>.md`, as `audit-pr` step 1 says, then run
`audit-pr` step 2 over every sentence of it.

## Header

Everything here the run already holds, and none of it needs the record opened:

- the PR number, from the `PR opened` write, and its head from `gh pr view <N> --json headRefOid`
  read now — the auditor audits the head, and a resume may have moved it since the write
- the local checkout is the controller's, on whichever branch it stands on, clean; and the branch
  is also checked out at the worktree step 6 cut, clean and left in place. The auditor audits the
  branch in the controller's checkout (`audit-pr`, step 3, its last paragraph). The fetched bytes
  are in the worktree, under its `data/raw/<id>/`, because `data/` is git-ignored and per-tree and
  the controller's checkout holds none for this record; say so, and that a re-fetch runs the
  worktree's own `src/fetch/<id>.py`, which writes into that worktree's `data/` and leaves its
  `git status` clean
- the interpreter's absolute path, the one step 7 gave the implementer, since no worktree has a
  `.venv/`
- the diff command, `git diff main..<branch>`, and the files from `gh pr view <N> --json files`,
  split into the record, the fetch script, any table or reference record the tier required, and
  the notebooks `generate` moved
- the issue, with the read form `docs/agents/issue-tracker.md`, "Read", gives, and the PRD row:
  file, table, `order` cell
- **what downstream depends on it**: the rows left in the order, from step 4's comment, and the
  `to file` rows under them, named. Step 10's premise judgement is made against those rows, and
  the auditor ranks a finding by what it would cost there.

## The governing clause

The record's tier row in `CONTEXT.md`, which `add-source` step 2's table names for the route the
row took, and the tagging sentence that decided `regions`; and the PRD reading the row's `note`
cell cites, by number. Quote each from its file, not from the issue's or the row's paraphrase.

## The questions

Two or three, from where **this row** decided something the readings did not settle. The run has
them written down already:

- the implementer's `DONE_WITH_CONCERNS` lines, from the `reported` write — each names a place
  the record states something the source stated unevenly
- the open questions the row's issue poses in its own body
- every concern the controller ruled on at step 8. A ruling the controller made is a conclusion,
  and the auditor is to reach it or refute it on its own evidence; the question is phrased as what
  to check against what, never as the ruling

## Standing questions

`audit-pr` step 1 states both and the condition for each. A record row meets the second whenever
`access`, `format`, `coverage` or `license` quotes a page or a file; name which fields do.

## Claims to re-run

Every count and universal in the PR body and the commit message, flat. The implementer wrote
both, so the controller lists them rather than vouching for them. Add the controller's own
verifications from step 8 — the gate it ran, the `git status` it read, the notebook set it checked
against the record's topics — as claims, since the auditor can trust neither author.

## What you cannot get from the repo

Three kinds of fact, each cited by comment id so the auditor can open it, and each marked as
whose word it is, because `audit-pr` step 2 asks for the owner's word to be kept separate from the
repo's and a run adds a third voice:

- **the owner's** — rulings in the ledger thread written `ruled (owner, …)`, and the PRD's
  readings, by number. The auditor does not reopen these.
- **the controller's** — its rulings on the implementer's concerns and on earlier rows' findings,
  in the same thread, marked as the controller's so the auditor knows they are open to it. The
  6.3c run's audit of PR #253 reversed one such ruling, C3, at #141 issuecomment-5861820435, F2.
- **what is parked** — the Parking-lot entries the row touched, read from #5's comments and cited
  by id, so a parked choice is not re-filed as new.

Then **what is newly in scope**, which none of the three can say: the first record under a
sub-topic, on a host, of a tier, or in a shape no record on `main` has — read from the row's `note`
cell and the implementer's report, and counted from `catalog/` before it is written. If there is
none, the brief says so and lets the auditor judge that.

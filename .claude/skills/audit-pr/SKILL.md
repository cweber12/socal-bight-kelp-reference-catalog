---
name: audit-pr
description: Use when a PR you opened in this repo is ready for review, and whenever asked to audit or double-check one. Invoked as /audit-pr <number>. Commissions the pr-auditor agent in a fresh context: assembles the brief, dispatches it, relays what it found. The last step of every PR.
---

# audit-pr

Commission an independent audit of **one** open PR. You wrote the code, so you are the last one who
can tell whether it is right — the audit exists to be a reader who never watched you decide.

The auditor's method is its own (`.claude/agents/pr-auditor.md`). Yours is the brief, and a brief
that carries your conclusions produces an auditor that agrees with you. Do the four steps in order.

## When

After the PR is open and CI is green — the auditor re-runs `gate.py` and both `ruff` commands, and
reads the PR by number, so all of it must exist. `gate.py` runs no ruff, so "green" means all three.
Then commission the audit **before** you report the PR as ready. A PR that has not been audited is
not ready; say that plainly rather than reporting it as done and offering an audit.

Skip it only when the owner says to.

## 1. Assemble the brief

Write it to `Claude outputs/prompt-audit-pr<N>-<slug>.md`, four parts:

**Header.** PR number, repo, the local checkout path, branch, commits, open-and-unmerged state, and
the `git diff main..<branch>` command that shows it. How many files, split into what kind. Then the
one thing the header is for: **what downstream depends on this slice** — the issues that will read
what it commits, so the auditor can rank a finding by what it would cost there rather than by how
much there is to say about it.

**The questions.** Two or three. Not more — a fourth question buys less than the depth it costs on
the first. A question earns its place by being answerable wrongly: "does the index render only what
CONTEXT.md asks for, and is every count right?" is a question; "is the code good?" is not. Draw
them from where this slice had to decide something `CONTEXT.md` did not settle, and from the gap
between what the tests construct and what a user will do. Name what to check against what — the
catalog directly, not the PR's own tests.

**Claims to re-run.** Every assertion in your PR body, flat, as things to re-run rather than facts:
counts, byte-identity, "the gate is green", coverage figures. Put the one you are least sure of in
the list, unmarked. This section is why the auditor can trust nothing and still move fast.

**What you cannot get from the repo.** The load-bearing part. Facts from conversations the auditor
was not in, each with a citation it can open:

- decisions the owner made in conversation and does not want reopened, and what was approved
- what is already on the Parking lot — read the pinned issue's comments and list the entries this
  diff touches, so a parked item is not re-filed as new
- what is out of scope: open issues nearby, stale docs that read as live status
- readings adopted in a PRD, and where the PRD says so
- **what is newly in scope, which the four above cannot say.** Every other kind narrows the audit,
  and a section that only narrows is one an author can quietly shrink. Name what nobody has looked
  at yet: surface this PR creates, a question a previous review deferred until now, a decision that
  was approved for something narrower than what this PR does. The predecessor prompt's was "the
  index has never been read by anyone, because it has never existed — that render is new surface
  and is in scope." If you cannot find one, say so in the brief and let the auditor judge that.

Every bullet cites something the auditor can open — an issue number, a file path, a commit. A
bullet citing the PR body is circular and is worth nothing; a bullet citing nothing is worth less.

Without this section the audit returns known issues and settled arguments, and you will spend more
reading it than it saved.

## 2. Prune the brief of conclusions

Read it back with one test: **does this sentence tell the auditor what it will find?** Every
sentence that does is either deleted or rewritten as something to check. "The counts are right
because one function computes both" becomes "check what the index and the topic notebooks say about
the same topic, and whether they can ever disagree."

Keep the pointers, keep the claims, cut the conclusions.

## 3. Dispatch, and stay off the checkout

```
Agent(subagent_type="pr-auditor", prompt=<the brief, inline>, description="Audit PR #<N>")
```

Pass the brief's text, and name the file too so the auditor can re-read it.

Agent types load when a session starts, and the loud failure is the easy one: a session older than
`.claude/agents/pr-auditor.md` answers with `Agent type 'pr-auditor' not found`. The quiet one
matters more — a session that loaded an *earlier* version of the file dispatches an auditor running
that earlier method, and says nothing. So when this file or the method file has changed in the
session you are standing in, dispatch `general-purpose` and point at the method instead, which
reads it from disk:

> Read `.claude/agents/pr-auditor.md` in full, first, and follow it as your standing instructions
> for this task. Then the brief:

Never inline the method into the brief. Two copies drift, and the copy you paste is the one you
were about to edit in your own favour. **One exception, and only this one:** when the diff under
audit *is* the method — a PR touching `.claude/agents/pr-auditor.md` — an auditor dispatched as
`pr-auditor` would be running the text it is meant to read as an artifact. Dispatch
`general-purpose`, write the method into the brief, and say in the brief that this is why. Note it
as a deviation when you relay.

**A PR that closes no issue** still gets an audit; the brief says so in place of the issue number,
and the questions come from the diff and `CONTEXT.md` alone. Do not skip the audit for want of an
issue to read.

**Then send it nothing until it reports.** `SendMessage` can continue a running subagent, and an
author who "clarifies" a finding mid-run has talked their own auditor into agreement — the one
thing a fresh chat prevented that a subagent does not prevent by itself. One dispatch, one report.
If the brief was wrong, that is a finding about the brief: let the audit land, then fix the brief
and commission a new one.

Commission from a **clean tree**: `git status --short` empty, everything committed and pushed. The
auditor restores what it changes and verifies the restore against `git status`, so a tree that
starts dirty gives it no baseline to verify against — and your uncommitted work reads to it as part
of the PR.

Then leave the checkout alone until it reports: touch no file, run nothing that writes, start no
other branch. The reason is the clean tree above — the auditor restores what it changes and
verifies the restore against `git status`, so a tree moving underneath it produces findings about a
state that never existed, and it cannot tell your edit from its own. Tell the owner the audit is
running and that the checkout is frozen until it lands.

An auditor may use a throwaway `git worktree` for a measurement that needs another commit — a
baseline test count off `main` is the one that comes up — with one edge to know. `pip install -e`
writes an absolute path to *this* `src/` into the venv, so `python -m kelpcatalog.generate` run from
a worktree imports the main checkout's code and would silently render the wrong tree. `python
gate.py` and `pytest` are unaffected: `gate.py` puts its own `src/` at `sys.path[0]` and
`pyproject.toml` sets `pythonpath = ["src"]`, and both beat the `.pth`. Audit the branch in this
checkout; borrow a worktree for a number, not for a verdict.

## 4. Relay it, and stop

Write nothing of your own into the report file — it is the auditor's.

Relay the ranked findings in the auditor's words, its blocking call, and the report's path. Then
**stop**. The next move is the owner's: which findings to act on is a judgement about this repo's
direction, not about whether the code is right.

If you disagree with a finding, say so as disagreement, after the finding and marked as yours.
Relaying a finding you have already argued away is how an audit becomes a formality.

**Then file what the owner decides not to fix here.** The auditor opens no issue, so a finding left
unacted is yours to route or it is lost: `CLAUDE.md`'s in-flight rule 3 for a defect in a file this
PR does not touch, and a one-line comment on the pinned Parking-lot issue for anything that is a
choice rather than a defect. Say in the relay which findings you will file and where, so the owner
can redirect you before you do.

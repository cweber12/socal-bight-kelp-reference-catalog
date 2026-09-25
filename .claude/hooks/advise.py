"""Two advisory PostToolUse checks: `ruff` on an edited `.py`, `wrap` on an edited `.md`.

`advise.sh` passes the mode as the first argument and the hook payload on stdin.
Every path out of `main` returns 0: both hooks report and neither blocks (#221's
non-goals), and a PostToolUse hook could not undo the edit in any case.

`gate.py` remains the authority on whether the repo is green. These two checks are
per-file and immediate, so they say nothing about the repo as a whole.

The `ruff` mode looks at `.py` files, which is what #221's Seam specifies, and that
is narrower than the `lint` gate row it anticipates: `CONTEXT.md` has that row clean
over "`.py` files, notebook code cells, and Python fenced in Markdown". Measured
2026-09-25: a badly formatted notebook cell reddens both ruff commands and a badly
formatted `python` fence in a `.md` reddens `ruff format --check`, and this mode is
silent on both. Widening it is parked on #5, not decided here.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIMIT = 100


def edited_path(payload: dict) -> Path | None:
    """The file the tool wrote, absolute, or None when the payload names none.

    `tool_input.file_path` is the field Claude Code's PostToolUse payload carries
    for both `Edit` and `Write`. Its documentation shows an absolute path but does
    not say it always is one, so a relative path is resolved against the payload's
    own `cwd` rather than against whatever directory the hook happens to run in.
    """
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    raw = tool_input.get("file_path")
    if not raw:
        return None
    path = Path(str(raw))
    if not path.is_absolute():
        path = Path(str(payload.get("cwd") or ".")) / path
    try:
        return path.resolve()
    except OSError:
        return None


def governed(path: Path) -> bool:
    """True when this repo's conventions reach this file.

    Three tests. A file outside this checkout is not this repo's to wrap, and a
    file that is gone or is a directory cannot be read — those two fail closed. A
    git-ignored file is not a repo document: `.gitignore` calls `Claude outputs/`
    "session notes and review drafts, not repo documents", and an advisory hook
    reporting on every audit brief is one that gets switched off. That third test
    fails open, so a missing or erroring git leaves the file checked.

    `check-ignore` runs in the edited file's own directory, not in ROOT, and the
    difference decides whether this hook is any use to #227-#230. A worktree under
    `.claude/worktrees/` is git-ignored by the outer repo (`.gitignore`, added by
    #233) and is a checkout in its own right, so asking ROOT skips every file an
    implementer edits there, while asking the file's own directory reaches the inner
    repo, which does not ignore it. Measured on a real `git worktree add`: outer
    exits 0, inner exits 1. `Claude outputs/` has no inner repo, so it still
    resolves to ROOT and is still skipped.
    """
    try:
        path.relative_to(ROOT)
    except ValueError:
        return False
    if not path.is_file():
        return False
    try:
        ignored = subprocess.run(
            ["git", "-C", str(path.parent), "check-ignore", "-q", str(path)],
            capture_output=True,
        )
    except OSError:
        return True
    return ignored.returncode != 0


def check_ruff(path: Path) -> str:
    """`ruff format --check` then `ruff check`, on this one file. Empty when clean.

    Both commands run even when the first fails, so one edit reports both — the
    same reason `gate.py`'s `lint` row gives for running them together.

    `--force-exclude` is what makes ruff apply `pyproject.toml`'s `extend-exclude`
    to a path handed to it explicitly; without it, a path under either excluded
    tree gets linted. Measured on one deliberately unformatted file placed in each
    tree, 2026-09-25: `ruff format --check` exits 1 without the flag and 0 with it,
    under `catalog/` and under `tests/fixtures/` alike. `pyproject.toml` gives the
    reason for the `catalog` half, and it is about a gate, not about this hook.

    Run through `-m` rather than the `ruff` script so the check uses the
    interpreter's own pinned ruff rather than whatever is first on PATH — which is
    also why an absent ruff has to be tested for here rather than in `advise.sh`.
    #221's Seam puts the constraint on the binary, not on the interpreter: a venv
    that exists but has not been installed into would otherwise report "No module
    named ruff" on every clean edit, which is the noise that gets a hook switched
    off. `find_spec` answers for this interpreter, which is the one `-m` will use.
    """
    if importlib.util.find_spec("ruff") is None:
        return ""
    reports = []
    for argv in (["format", "--check"], ["check"]):
        result = subprocess.run(
            [sys.executable, "-m", "ruff", *argv, "--force-exclude", str(path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            reports.append((result.stdout + result.stderr).strip())
    return "\n".join(report for report in reports if report)


def check_wrap(path: Path) -> str:
    """Prose lines over LIMIT characters. Empty when there are none.

    `len(line)` counts characters, not bytes, which is the whole point: an em dash
    is three bytes in UTF-8 and this repo's prose is built on them, so a byte-based
    check reports lines that are within the limit. #221 measures how many, on the
    set it names, at the time it was written.

    Three kinds are exempt, per #221's Seam: a table row, which cannot be wrapped;
    YAML frontmatter; and a fenced block, whose content is not prose.

    The frontmatter exemption is much the largest of the three, and not only for the
    one-line `description:` that motivates it. A record is frontmatter nearly all the
    way down, so this exempts a record's whole content: measured 2026-09-25, 198 of
    the 217 tracked `.md` files are records or record fixtures, and `catalog/*.md`
    holds 41 lines over the limit that are silent for this reason alone. Narrowing
    the exemption to `description:` would turn all 41 into advice about records.
    """
    try:
        lines = path.read_text(encoding="utf-8").split("\n")
    except (OSError, UnicodeDecodeError):
        return ""
    over = []
    in_fence = False
    in_yaml = False
    for number, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if number == 1 and line.strip() == "---":
            in_yaml = True
            continue
        if in_yaml:
            if line.strip() == "---":
                in_yaml = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if len(line) > LIMIT and not in_fence and not stripped.startswith("|"):
            over.append(f"  {path.name}:{number}  {len(line)} characters")
    return "\n".join(over)


def advisory(message: str) -> dict:
    """The payload that carries `message` back without blocking the edit.

    Measured on 2026-09-25, in the session that wrote this file, and again by that
    PR's audit: `hookSpecificOutput.additionalContext` reaches the agent that made
    the edit. Two other channels were tried and reached it with nothing — plain text
    on stdout, and a top-level `systemMessage`, which is top-level and not nested
    under `hookSpecificOutput`. Whether `systemMessage` reaches the user's terminal
    was not observable from here, so this uses the channel that was demonstrated.
    Those three are the ones that were measured, not the whole set a hook has: exit
    2, and `decision` with a `reason`, also reach the agent, and both are the
    blocking channel #221's non-goals rule out. A `PostToolUse` hook cannot undo the
    edit whichever is used.
    """
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": message,
        }
    }


def main(argv: list[str]) -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return 0
    if not isinstance(payload, dict):
        return 0
    mode = argv[1] if len(argv) > 1 else ""
    path = edited_path(payload)
    if path is None:
        return 0
    # Suffix before `governed`, because the suffix test is free and `governed` spawns
    # git. Each hook sees every Edit and Write, including the other's extension.
    if mode == "ruff" and path.suffix == ".py":
        checker = check_ruff
        heading = "ruff, on the file just edited:"
    elif mode == "wrap" and path.suffix == ".md":
        checker = check_wrap
        heading = f"prose lines over {LIMIT} characters, on the file just edited:"
    else:
        return 0
    if not governed(path):
        return 0
    report = checker(path)
    if report:
        print(json.dumps(advisory(f"{heading}\n{report}")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

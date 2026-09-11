"""Tests for `gate.py`, the runner that decides whether the repo is green.

Until #68 nothing in `tests/` imported it and `--cov=src/kelpcatalog` did not reach it, so
every row could be renamed, deleted, or have its verdict inverted with the whole suite green.

These tests cover the runner and the thin wrappers in this file - the verdict each wrapper
returns, the message it builds, and the root it walks. What a check itself asserts is tested
beside that check's own module and is not retested here, which is #68's "this is about the
runner, not the rows".

Every row name, status word, command and message this file expects is written out as a
literal below and never imported from `gate.py`. A test that spells its expectation
`{g.name for g in gate.GATES}` passes just as happily after a row is renamed, because both
sides move together. PR #69 shipped that shape three times - two mutants of it survived a
sweep during the slice, and its audit found a third - and this file exists not to repeat it.
The cost is that adding a row means editing this file, which is the point.

`import gate` reaches the repo root through `pythonpath = ["src", "."]` in pyproject.toml -
see the comment there for why that rather than a conftest.py. Importing it runs its module
scope, which puts `src` on `sys.path` and imports four `kelpcatalog` modules; under pytest
those are already imported, so it is a no-op here.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

import gate

# --- the row table -----------------------------------------------------------------
#
# Typed from gate.py's GATES, and from CONTEXT.md's "Gates" table, by hand. Not imported.

GATE_ROWS = {
    "unit",
    "catalog-schema",
    "notebook-structure",
    "notebook-outputs",
    "notebook-fresh",
    "figure-provenance",
    "lint",
}

# CONTEXT.md, "Gates": the first column against the third, top to bottom. The
# `lock-consistency` / `lock-verify` cell names two gates and is transcribed as two.
CONTEXT_GATES = {
    "unit": "scaffold",
    "catalog-schema": "scaffold",
    "notebook-structure": "milestone 6.2",
    "notebook-outputs": "milestone 6.2",
    "notebook-fresh": "milestone 6.2",
    "figure-provenance": "milestone 6.2",
    "lint": "milestone 6.2",
    "lock-consistency": "milestone 6.5",
    "lock-verify": "milestone 6.5",
}

# Rows CONTEXT.md's table names that gate.py does not run yet: the lock pair, milestone
# 6.5. Moving a name out of here is part of landing its row - `notebook-fresh` left with
# #48.
SCHEDULED_NOT_YET_RUN = {"lock-consistency", "lock-verify"}

_ROW = re.compile(r"^(\S+)( +)(ok|FAIL|SKIP)(?= )")


def _rows(out: str) -> list[tuple[str, str]]:
    """(name, status) for each gate row in the runner's output, ignoring message blocks."""
    return [(m.group(1), m.group(3)) for line in out.splitlines() if (m := _ROW.match(line))]


def _indented(out: str) -> list[str]:
    """The lines of a failing gate's reprinted message block, which the runner indents."""
    return [line[4:] for line in out.splitlines() if line.startswith("    ")]


def _passing(name: str, message: str = "") -> gate.Gate:
    return gate.Gate(name, lambda: (True, message))


def _explodes() -> tuple[bool, str]:
    raise AssertionError("a skipped gate must not run its fn")


# --- the rows gate.py holds --------------------------------------------------------


def test_the_gate_rows_are_exactly_these_names() -> None:
    """The set, not the count: a renamed row and a deleted row both fail here."""
    assert {g.name for g in gate.GATES} == GATE_ROWS


def test_every_row_gate_py_runs_is_a_row_context_md_names() -> None:
    """CONTEXT.md's Gates table, transcribed above, against the live GATES list.

    What this asserts: every row `gate.py` runs is a row that table names - the module
    docstring's "a row here that is not a row there is a gate nothing asked for" - and every
    row the table names has either arrived in GATES or is listed as scheduled.

    What it does not assert: that the transcription above still matches CONTEXT.md. Nothing
    here reads CONTEXT.md, because CLAUDE.md forbids a parser for any prose file, so an edit
    to that table which nobody copies down here is invisible to this test. That gap is the
    Parking lot's "Nothing checks CONTEXT.md against schema.py", which is unresolved and
    wider than this file; `plan.py` and `test_plan.py` took the same route for the same
    reason. One difference from theirs is worth naming, and is narrower than it sounds:
    `GATES` is the list the runner actually walks rather than a second transcription, so a
    `GATES` row that drifts from the transcription below fails here. A `CONTEXT.md` row that
    drifts from it does not, and editing both literals below lands a row that table never
    named. Only one of the two directions is mechanical.
    """
    assert {g.name for g in gate.GATES} == set(CONTEXT_GATES) - SCHEDULED_NOT_YET_RUN


def test_every_scheduled_row_is_a_row_context_md_names_and_dates() -> None:
    """The mirror of the docstring's rule: a row there that is not a row here is scheduled,
    not forgotten, so CONTEXT.md has to both name it and say when it arrives."""
    assert SCHEDULED_NOT_YET_RUN <= set(CONTEXT_GATES)
    assert all(CONTEXT_GATES[name] for name in SCHEDULED_NOT_YET_RUN)


# --- what the runner does with a verdict -------------------------------------------


def test_a_passing_gate_prints_ok_and_prints_no_message_block(monkeypatch, capsys) -> None:
    monkeypatch.setattr(gate, "GATES", [_passing("unit", "457 passed in 9.55s")])

    assert gate.main() == 0

    out = capsys.readouterr().out
    assert "unit  ok    457 passed in 9.55s" in out
    # No indented block. Asserted on whole lines: the row itself ends in "ok" plus four
    # spaces, so a substring check for the indented message matches the row and passes.
    assert _indented(out) == []
    assert "1/1 gates passed" in out


def test_a_failing_gate_prints_FAIL_its_message_beneath_and_exits_non_zero(
    monkeypatch, capsys
) -> None:
    """The inline text is the message's *last* line - every gate builds its message so the
    counts land there - and the whole message is reprinted indented beneath the row."""
    monkeypatch.setattr(
        gate,
        "GATES",
        [gate.Gate("catalog-schema", lambda: (False, "sources/x.md: no such topic\n3 sources"))],
    )

    assert gate.main() == 1

    out = capsys.readouterr().out
    assert "catalog-schema  FAIL  3 sources" in out
    assert _indented(out) == ["sources/x.md: no such topic", "3 sources"]
    assert "0/1 gates passed" in out


def test_a_gate_that_raises_is_a_failure_and_the_rows_after_it_still_run(
    monkeypatch, capsys
) -> None:
    def boom() -> tuple[bool, str]:
        raise RuntimeError("the catalog fell over")

    monkeypatch.setattr(
        gate, "GATES", [gate.Gate("catalog-schema", boom), _passing("lint", "clean")]
    )

    assert gate.main() == 1

    out = capsys.readouterr().out
    assert ("catalog-schema", "FAIL") in _rows(out)
    assert ("lint", "ok") in _rows(out)
    assert "RuntimeError: the catalog fell over" in out
    assert "1/2 gates passed" in out


def test_a_keyboard_interrupt_still_takes_the_run_down(monkeypatch) -> None:
    """`except Exception`, not `except BaseException`: catching everything would make the
    runner unstoppable from the terminal."""

    def interrupted() -> tuple[bool, str]:
        raise KeyboardInterrupt

    monkeypatch.setattr(gate, "GATES", [gate.Gate("unit", interrupted)])

    with pytest.raises(KeyboardInterrupt):
        gate.main()


# --- skipping ----------------------------------------------------------------------


def test_a_skipped_gate_prints_SKIP_and_is_not_counted_as_a_pass(monkeypatch, capsys) -> None:
    """A skip leaves the exit code alone - the module docstring says skipping "is for the
    clone, not the author" - but it must not be summed into the passed count, or a gate that
    silently never runs reads exactly like one that ran and passed."""
    monkeypatch.setattr(
        gate,
        "GATES",
        [
            _passing("unit", "457 passed in 9.55s"),
            gate.Gate("notebook-fresh", _explodes, skip_if=lambda: "needs data/ for figures"),
        ],
    )

    assert gate.main() == 0

    out = capsys.readouterr().out
    assert ("notebook-fresh", "SKIP") in _rows(out)
    assert "needs data/ for figures" in out
    assert "1/2 gates passed, 1 skipped" in out


def test_a_skip_if_that_raises_is_a_failure_and_the_rows_after_it_still_run(
    monkeypatch, capsys
) -> None:
    """`skip_if` is the half of a Gate that reaches for machine state, so it is the half more
    likely to raise. Guarding only `fn` left a raising `skip_if` taking the whole run down -
    no summary, no rows after it - which is what #48's first real `skip_if` would have met."""

    def boom() -> str:
        raise OSError("no such drive")

    monkeypatch.setattr(
        gate,
        "GATES",
        [gate.Gate("notebook-fresh", _explodes, skip_if=boom), _passing("lint", "clean")],
    )

    assert gate.main() == 1

    out = capsys.readouterr().out
    assert ("notebook-fresh", "FAIL") in _rows(out)
    assert ("lint", "ok") in _rows(out)
    assert "OSError: no such drive" in out
    assert "1/2 gates passed" in out


def test_a_skip_if_that_returns_none_runs_the_gate(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        gate,
        "GATES",
        [gate.Gate("notebook-fresh", lambda: (True, "11 notebooks"), skip_if=lambda: None)],
    )

    assert gate.main() == 0

    out = capsys.readouterr().out
    assert ("notebook-fresh", "ok") in _rows(out)
    assert "1/1 gates passed" in out
    assert "skipped" not in out


def test_a_run_with_nothing_skipped_says_nothing_about_skipping(monkeypatch, capsys) -> None:
    monkeypatch.setattr(gate, "GATES", [_passing("unit", "457 passed")])

    gate.main()

    assert "1/1 gates passed\n" in capsys.readouterr().out


# --- the shape of the report -------------------------------------------------------


def test_main_prints_one_row_per_gate_and_no_others(monkeypatch, capsys) -> None:
    monkeypatch.setattr(gate, "GATES", [_passing(name, "counts") for name in sorted(GATE_ROWS)])

    gate.main()

    printed = _rows(capsys.readouterr().out)
    assert [name for name, _ in printed] == sorted(GATE_ROWS)
    assert {status for _, status in printed} == {"ok"}


def test_the_status_column_is_aligned_to_the_longest_row_name(monkeypatch, capsys) -> None:
    """Names of three different lengths, so a width that is not the maximum misaligns."""
    monkeypatch.setattr(
        gate,
        "GATES",
        [_passing("lint"), _passing("unit"), _passing("figure-provenance")],
    )

    gate.main()

    columns = {
        len(m.group(1)) + len(m.group(2))
        for line in capsys.readouterr().out.splitlines()
        if (m := _ROW.match(line))
    }
    assert columns == {len("figure-provenance") + 2}


# --- the wrappers around each check ------------------------------------------------
#
# Each of these rows is a thin wrapper: call the check with the repo root, turn its problems
# into a verdict, and build a counts line. All three are mutable without the suite noticing -
# a verdict inversion makes a failing gate print `ok` and exit 0, a changed count noun goes
# unread, and a wrong root reports nothing and passes. The checks themselves are stubbed, so
# nothing here re-asserts what a check finds.

# Two notebooks holding three items between them, so a count that is really a length shows.
FAKE_WALK = {"1_physical/11_ocean_climate.ipynb": ["a", "b"], "2_kelp/21_canopy.ipynb": ["c"]}
FAKE_CATALOG = SimpleNamespace(records={"sources": ["a", "b", "c"], "regions": ["scb"]})

# (wrapper, the check it calls, the counts line it builds). The count nouns are transcribed
# from gate.py by hand; a row that silently renames "figure cells" to "cells" fails here.
WRAPPERS = [
    ("gate_notebook_structure", "check_structure", "2 notebooks, 3 sections"),
    ("gate_notebook_outputs", "check_outputs", "2 notebooks, 3 code cells"),
    ("gate_notebook_fresh", "check_fresh", "2 notebooks, 3 cells re-executed"),
    ("gate_figure_provenance", "check_figure_provenance", "2 notebooks, 3 figure cells"),
    ("gate_catalog_schema", "check_catalog", "3 sources, 1 regions"),
]


def _stub(check_name: str, problems: list[str], seen: list[Path] | None = None):
    """The check's return shape: (walk, problems) for the notebook rows, (catalog, problems)
    for catalog-schema."""
    payload = FAKE_CATALOG if check_name == "check_catalog" else FAKE_WALK

    def check(root):
        if seen is not None:
            seen.append(root)
        return payload, problems

    return check


@pytest.mark.parametrize(("wrapper", "check_name", "counts"), WRAPPERS)
def test_a_wrapper_passes_with_its_counts_when_the_check_finds_no_problems(
    monkeypatch, wrapper, check_name, counts
) -> None:
    monkeypatch.setattr(gate, check_name, _stub(check_name, []))

    ok, message = getattr(gate, wrapper)()

    assert ok
    assert message == counts


@pytest.mark.parametrize(("wrapper", "check_name", "counts"), WRAPPERS)
def test_a_wrapper_fails_and_prints_the_problems_above_its_counts(
    monkeypatch, wrapper, check_name, counts
) -> None:
    """The verdict inversion the Parking lot and #68 both lead with: flipping this `False`
    makes a failing gate print `ok`, suppress the problem block, and exit 0."""
    monkeypatch.setattr(gate, check_name, _stub(check_name, ["11_ocean_climate.ipynb: broken"]))

    ok, message = getattr(gate, wrapper)()

    assert not ok
    assert message.splitlines() == ["11_ocean_climate.ipynb: broken", f"({counts})"]


@pytest.mark.parametrize(("wrapper", "check_name", "counts"), WRAPPERS)
def test_a_wrapper_walks_the_repo_root(monkeypatch, wrapper, check_name, counts) -> None:
    """A gate pointed at a tree that is not there reports nothing and passes. The expected
    root is computed from `gate.__file__`, not read from `gate.ROOT`, so a mutated ROOT fails
    here rather than moving both sides together."""
    seen: list[Path] = []
    monkeypatch.setattr(gate, check_name, _stub(check_name, [], seen))

    getattr(gate, wrapper)()

    assert seen == [Path(gate.__file__).parent]
    assert (seen[0] / "CONTEXT.md").is_file(), "the root the gates walk is the repo root"


# --- _run, the subprocess helper ---------------------------------------------------


def test_run_passes_when_the_child_exits_zero_and_captures_both_streams() -> None:
    script = "import sys; print('on stdout'); print('on stderr', file=sys.stderr)"
    ok, out = gate._run([sys.executable, "-c", script])

    assert ok
    assert "on stdout" in out
    assert "on stderr" in out


def test_run_fails_when_the_child_exits_non_zero() -> None:
    ok, out = gate._run([sys.executable, "-c", "import sys; print('nope'); sys.exit(3)"])

    assert not ok
    assert "nope" in out


def test_run_runs_the_child_in_the_repo_root_whatever_the_caller_s_cwd(monkeypatch, tmp_path):
    """`unit` and `lint` reach their tree by subprocess rather than by walking it, so the
    wrong-root mutation for those two rows is `cwd=ROOT` going missing: both would then report
    on whatever directory the caller happened to be in, and pass having examined nothing of
    the repo. Asserted as a path equality rather than a substring, because `tmp_path` carries
    the test's own name and would satisfy a looser check."""
    monkeypatch.chdir(tmp_path)

    ok, out = gate._run([sys.executable, "-c", "import os; print(os.getcwd())"])

    assert ok
    assert Path(out.strip()).resolve() == Path(gate.__file__).parent.resolve()


# --- the unit row ------------------------------------------------------------------


def test_unit_runs_pytest_with_branch_coverage_and_the_ninety_percent_floor(monkeypatch) -> None:
    """CONTEXT.md's `unit` row is "the schema seams, >= 90 % coverage"; `--cov-branch` is
    #68 folding in the Parking lot's line-coverage-only entry, and `--cov=gate` puts this
    file's own runner under that floor for the first time."""
    calls: list[list[str]] = []
    monkeypatch.setattr(gate, "_run", lambda cmd: (calls.append(cmd), (True, ""))[1])

    gate.gate_unit()

    assert calls == [
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--cov=src/kelpcatalog",
            "--cov=gate",
            "--cov-branch",
            "--cov-fail-under=90",
        ]
    ]


# --- the lint row ------------------------------------------------------------------


def test_lint_runs_exactly_the_two_ruff_commands_ci_runs(monkeypatch) -> None:
    """Written out as literals: dropping `--check` from the format command would make the
    row rewrite the repo instead of reporting on it, and nothing else would notice."""
    calls: list[list[str]] = []
    monkeypatch.setattr(gate, "_run", lambda cmd: (calls.append(cmd), (True, ""))[1])

    ok, message = gate.gate_lint()

    assert ok
    assert calls == [
        [sys.executable, "-m", "ruff", "check", "."],
        [sys.executable, "-m", "ruff", "format", "--check", "."],
    ]
    assert message == "ruff check and ruff format --check clean"


@pytest.mark.parametrize(
    ("failing", "label"),
    [("check", "ruff check"), ("format", "ruff format --check")],
)
def test_lint_fails_when_either_ruff_command_fails(monkeypatch, failing, label) -> None:
    calls: list[list[str]] = []

    def fake_run(cmd: list[str]) -> tuple[bool, str]:
        calls.append(cmd)
        return cmd[3] != failing, "E501 line too long"

    monkeypatch.setattr(gate, "_run", fake_run)

    ok, message = gate.gate_lint()

    assert not ok
    assert len(calls) == 2, "both commands run, so one pass reports both"
    assert "E501 line too long" in message
    assert message.splitlines()[-1] == f"{label} failed"


def test_lint_names_both_commands_when_both_fail(monkeypatch) -> None:
    monkeypatch.setattr(gate, "_run", lambda cmd: (False, "E501 line too long"))

    ok, message = gate.gate_lint()

    assert not ok
    assert message.splitlines()[-1] == "ruff check and ruff format --check failed"


def test_the_interpreter_can_run_ruff_as_a_module() -> None:
    """The one thing the stubbed lint tests cannot see: that `-m ruff` is a real invocation
    path in this environment. Without it a `lint` row that never runs anything would pass
    every test above and only fail in `gate.py` itself."""
    ok, out = gate._run([sys.executable, "-m", "ruff", "--version"])

    assert ok
    assert out.startswith("ruff ")


# --- the notebook-fresh row --------------------------------------------------------------
#
# The repo's first real `skip_if`. The skip machinery itself is tested above against fake
# rows; these two are about the wiring of the one row that uses it.


def test_notebook_fresh_is_the_only_row_that_can_skip() -> None:
    """The set, written out. A `skip_if` added to another row would make it skippable in a
    fresh clone, and a `skip_if` dropped from this one would make it fail in CI rather than
    skip - neither is visible in the report until the row concerned is red."""
    assert {g.name for g in gate.GATES if g.skip_if} == {"notebook-fresh"}


def test_the_notebook_fresh_row_asks_about_the_repo_root(monkeypatch, tmp_path) -> None:
    """A skip predicate pointed at a tree that is not there answers about the wrong machine:
    aimed at the working directory it would skip whenever `gate.py` was run from elsewhere,
    and the row would silently never run. The expected root is computed from `gate.__file__`
    rather than read from `gate.ROOT`, so a mutated ROOT fails here."""
    seen: list[Path] = []
    monkeypatch.setattr(gate, "skip_reason", lambda root: (seen.append(root), "no data/")[1])
    # The working directory moved away from the repo root first. Without this the test passes
    # on `skip_reason(Path.cwd())` too, because pytest runs from the repo root and the two are
    # then the same path - so the hazard the docstring above names went unpinned. The audit of
    # PR #71 found it: that mutant survived all 526 tests.
    monkeypatch.chdir(tmp_path)

    row = next(g for g in gate.GATES if g.name == "notebook-fresh")

    assert row.skip_if is not None
    assert row.skip_if() == "no data/"
    assert seen == [Path(gate.__file__).parent]

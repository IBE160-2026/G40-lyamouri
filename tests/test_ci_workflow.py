"""The CI workflow runs the README's checks (Story 1.2; AD-17, NFR-2, DR-7).

The test reads .github/workflows/ci.yml as text, one step per `      - ` item,
because none of the project's dependencies parses YAML.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
SETUP_AND_TESTS = ["uv sync --locked", "docker compose up -d --wait", "uv run pytest"]
RUFF = ["uv run ruff check", "uv run ruff format --check"]


def steps():
    """The keys and values of each step in the workflow's job."""
    blocks = re.findall(r"^      - (.*(?:\n        .*)*)", WORKFLOW, re.MULTILINE)
    return [
        dict(
            line.strip().partition(": ")[::2]
            for line in block.splitlines()
            if ": " in line
        )
        for block in blocks
    ]


def test_ci_runs_the_readme_commands():
    """AD-17, NFR-2: CI installs the locked dependencies, starts the database
    from compose.yaml and runs the README's three checks, and nothing else."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8").splitlines()
    commands = [step["run"] for step in steps() if "run" in step]

    assert commands == [*SETUP_AND_TESTS, *RUFF]
    assert [command for command in commands if command not in readme] == []


def test_no_check_is_skipped_and_ruff_runs_after_a_pytest_failure():
    """DR-7: the install, database and pytest steps always run, and a failure
    fails the run; both Ruff steps still run when the install worked, so one
    run reports every broken check."""
    by_command = {step.get("run"): step for step in steps()}

    assert by_command["uv sync --locked"].get("id") == "sync"
    assert [
        command
        for command in SETUP_AND_TESTS
        if {"if", "continue-on-error"} & by_command[command].keys()
    ] == []
    assert [by_command[command].get("if") for command in RUFF] == [
        "${{ !cancelled() && steps.sync.outcome == 'success' }}"
    ] * 2


def test_every_action_is_pinned_to_a_commit_sha():
    """DR-7, AD-17: each action is pinned to a full commit SHA, so a moved tag
    cannot change what CI runs."""
    actions = [step["uses"].partition(" #")[0] for step in steps() if "uses" in step]

    assert actions
    assert [
        a for a in actions if not re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", a)
    ] == []

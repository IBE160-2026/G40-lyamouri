"""The CI workflow runs the README's checks (Story 1.2; AD-17, NFR-2, DR-7).

The tests read the workflow files as text, because none of the project's
dependencies parses YAML. They check the spec's rules for CI: when and where it
runs, its rights and actions, that it runs the README's commands and nothing
else, and that no check can be skipped or ignored. A YAML construct that a
line-based read does not see, such as an anchor, is left to review.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"
WORKFLOW = (WORKFLOW_DIR / "ci.yml").read_text(encoding="utf-8")
SETUP = ["uv sync --locked", "docker compose up -d --wait"]
CHECKS = ["uv run pytest", "uv run ruff check", "uv run ruff format --check"]
RUFF_IF = "${{ !cancelled() && steps.sync.outcome == 'success' }}"


def values(key, text=WORKFLOW):
    """Every value of key in text, at any level and quoted or not."""
    pattern = rf"""^\s*(?:-\s+)?['"]?{re.escape(key)}['"]?\s*:\s*(.*?)\s*$"""
    return re.findall(pattern, text, re.MULTILINE)


def block(key):
    """The lines under a top-level key of the workflow."""
    return WORKFLOW.split(f"\n{key}:\n", 1)[1].split("\n\n", 1)[0].splitlines()


def steps():
    """The keys and values of each step in the workflow's job."""
    items = re.findall(r"^      - (.*(?:\n        .*)*)", WORKFLOW, re.MULTILINE)
    return [
        dict(
            line.strip().partition(": ")[::2]
            for line in item.splitlines()
            if ": " in line
        )
        for item in items
    ]


def readme_checks():
    """The commands in the code block of the README's «Tester» section."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    section = readme.split("\n## Tester\n", 1)[1].split("\n## ", 1)[0]
    return re.search(r"```\n(.*?)\n```", section, re.DOTALL).group(1).splitlines()


def test_ci_runs_the_readme_commands_and_nothing_else():
    """AD-17, NFR-2: CI installs the locked dependencies, starts the database
    from compose.yaml and runs the README's checks, the same both ways."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8").splitlines()

    assert readme_checks() == CHECKS
    assert values("run") == [*SETUP, *readme_checks()]
    assert [command for command in SETUP if command not in readme] == []


def test_ci_runs_on_linux_for_every_pull_request_and_push_to_main():
    """DR-7, AD-17: CI starts on every pull request and every push to main,
    runs on Linux, and gives each run outside a pull request its own group,
    so no push to main is cancelled."""
    assert block("on") == [
        "  pull_request:",
        "  push:",
        "    branches: [main]",
        "  workflow_dispatch:",
    ]
    assert values("runs-on") == ["ubuntu-24.04"]
    assert values("group") == [
        "ci-${{ github.event_name == 'pull_request' && github.ref || github.run_id }}"
    ]


def test_no_check_can_be_skipped_or_ignored():
    """DR-7: no job or step is skipped by a condition or allowed to fail, and no
    environment variable can change the checks; only the two Ruff steps have
    the condition that lets them run after a pytest failure, when the install
    worked."""
    ruff = [step.get("if") for step in steps() if step.get("run") in CHECKS[1:]]

    assert values("if") == [RUFF_IF, RUFF_IF]
    assert ruff == [RUFF_IF, RUFF_IF]
    assert values("id") == ["sync"]
    assert values("continue-on-error") == []
    assert values("env") == []


def test_the_windows_workflow_runs_the_readme_setup_without_docker():
    """SM-2, NFR-1: the Windows workflow runs every setup command in the README
    except the database start, which needs Docker Desktop, and it runs when
    the code or the dependencies change, so it follows the README."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    windows = (WORKFLOW_DIR / "windows-setup.yml").read_text(encoding="utf-8")
    block = re.search(
        r"```\n(docker compose up -d --wait\n.*?)\n```", readme, re.DOTALL
    )
    setup = block.group(1).splitlines()
    paths = [".python-version", "pyproject.toml", "src/**", "uv.lock"]

    assert [
        command for command in setup[1:] if f"name: {command}\n" not in windows
    ] == []
    assert [path for path in paths if f"      - {path}\n" not in windows] == []


def test_ci_can_only_read_and_uses_only_the_pinned_setup_actions():
    """DR-7, AD-17: CI may only read the repository, keeps no credentials and
    uses no secrets. Every workflow file uses only actions pinned to a full
    commit SHA, with the version in a comment, and CI uses only the two setup
    actions."""
    pinned = r"[\w.-]+/[\w.-]+(?:/[\w.-]+)*@[0-9a-f]{40} # v\d+\.\d+\.\d+"

    assert block("permissions") == ["  contents: read"]
    assert values("persist-credentials") == ["false"]
    for path in sorted(WORKFLOW_DIR.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        assert "secrets." not in text, path.name
        assert [a for a in values("uses", text) if not re.fullmatch(pinned, a)] == []
    assert [action.split("@")[0] for action in values("uses")] == [
        "actions/checkout",
        "astral-sh/setup-uv",
    ]

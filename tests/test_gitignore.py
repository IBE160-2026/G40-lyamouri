"""Git keeps the session secret and .env out of the repository (Story 1.1; NFR-3, AD-13, DR-2).

The tests are skipped when git is missing or the project is not a git working
tree, for example in a copy without .git.
"""

import shutil
import subprocess

import pytest
from django.conf import settings


def git(*args):
    return subprocess.run(
        ["git", *args],
        cwd=settings.BASE_DIR,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture(autouse=True)
def git_working_tree():
    if (
        shutil.which("git") is None
        or git("rev-parse", "--is-inside-work-tree").returncode
    ):
        pytest.skip("git or a git working tree is missing")


@pytest.mark.parametrize("name", [".secret_key", ".env"])
def test_git_ignores_the_secret_file_and_dotenv(name):
    """NFR-3, AD-13: git ignores .secret_key, which load_seed writes, and .env,
    which may hold a database password, so neither can be committed."""
    assert git("check-ignore", "-q", name).returncode == 0


def test_git_keeps_env_example():
    """DR-2: .env.example is not ignored, so the optional variables stay documented."""
    assert git("check-ignore", "-q", ".env.example").returncode == 1

"""compose.yaml publishes the database only on this computer (Story 1.2; NFR-3, AD-14).

The test reads Docker Compose's own view of compose.yaml with
`docker compose --file compose.yaml config`, so a COMPOSE_FILE set for another
project cannot replace it, and it is skipped where docker is not on PATH.
GitHub Actions starts the database with docker, so the test always runs there
(VG-4).
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_compose_publishes_every_port_only_on_127_0_0_1():
    """NFR-3, AD-14: the database has no password, so compose.yaml publishes it
    on 127.0.0.1 only, and no other computer can connect."""
    if shutil.which("docker") is None:
        pytest.skip("docker is not on PATH")
    result = subprocess.run(
        ["docker", "compose", "--file", "compose.yaml", "config", "--format", "json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    services = json.loads(result.stdout)["services"]
    ports = [
        (name, port)
        for name, service in services.items()
        for port in service.get("ports", [])
    ]

    assert ports, "compose.yaml publishes no port"
    assert [name for name, port in ports if port.get("host_ip") != "127.0.0.1"] == []


def test_compose_test_is_skipped_without_docker(monkeypatch):
    """NFR-3: where docker is not on PATH, the compose test is skipped with its
    reason instead of failing."""
    monkeypatch.setattr(shutil, "which", lambda name: None)

    with pytest.raises(pytest.skip.Exception, match="docker is not on PATH"):
        test_compose_publishes_every_port_only_on_127_0_0_1()

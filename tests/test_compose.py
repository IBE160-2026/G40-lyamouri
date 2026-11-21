"""compose.yaml publishes the database only on this computer (Story 1.2; NFR-3, AD-14).

The test reads Docker Compose's own view of the configuration that
`docker compose up` loads: compose.yaml, merged with a compose.override.yaml if
there is one, and without a COMPOSE_FILE set for another project. It is skipped
where docker is not on PATH. GitHub Actions starts the database with docker, so
the test always runs there (VG-4).
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_compose_publishes_every_port_only_on_127_0_0_1():
    """NFR-3, AD-14: the database has no password, so the compose configuration
    publishes it on 127.0.0.1 only, and no other computer can connect."""
    docker = shutil.which("docker")
    if docker is None:
        pytest.skip("docker is not on PATH")
    result = subprocess.run(
        [docker, "compose", "config", "--format", "json"],
        cwd=REPO_ROOT,
        env={
            name: value for name, value in os.environ.items() if name != "COMPOSE_FILE"
        },
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

    assert ports, "the compose configuration publishes no port"
    assert [name for name, port in ports if port.get("host_ip") != "127.0.0.1"] == []


def test_compose_test_is_skipped_without_docker(monkeypatch):
    """NFR-3: where docker is not on PATH, the compose test is skipped with its
    reason instead of failing."""
    monkeypatch.setattr(shutil, "which", lambda name: None)

    with pytest.raises(pytest.skip.Exception, match="docker is not on PATH"):
        test_compose_publishes_every_port_only_on_127_0_0_1()

"""InfraAgent plane stories through the unified orchestrator."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from infra.bootstrap import UNIFIED_ROOT  # noqa: E402
from framework.orchestrator import Orchestrator  # noqa: E402

EX = UNIFIED_ROOT / "examples"
FAIL = EX / "checkov_fail.json"
PASS = EX / "checkov_pass.json"
HOT = EX / "telemetry_hot.json"
OK = EX / "telemetry_ok.json"
DD = EX / "telemetry_datadog.json"


def _run(checkov: Path, telemetry: Path) -> dict:
    tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False)
    tmp.close()
    return Orchestrator(Path(tmp.name)).run(checkov, telemetry, service="infra-test")


class StayUpPlane(unittest.TestCase):
    def test_hot_telemetry_blocks_clean_iac(self) -> None:
        result = _run(PASS, HOT)
        self.assertGreater(result["infraagent"]["phi_1h"], 0.7)
        self.assertFalse(result["crc"]["residual_high"])
        self.assertEqual(result["governance"]["decision"]["dsa"], "BLOCK")
        kinds = {p["type"] for p in result["governance"]["remediation"]["proposals"]}
        self.assertTrue(kinds & {"rollback", "hold"})
        self.assertFalse(result["governance"]["remediation"]["apply"])

    def test_calm_telemetry_allows_clean_iac(self) -> None:
        result = _run(PASS, OK)
        self.assertLess(result["infraagent"]["phi_1h"], 0.5)
        self.assertEqual(result["governance"]["decision"]["action"], "ALLOW")

    def test_datadog_shaped_metrics_run(self) -> None:
        result = _run(PASS, DD)
        self.assertIn("omega", result["infraagent"])
        self.assertIn("kappa", result["infraagent"])


class InfraCli(unittest.TestCase):
    def test_focus_prints_stay_up(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "infra",
                str(PASS),
                "--telemetry",
                str(HOT),
                "--focus",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["plane"], "infraagent")
        self.assertIn("phi_1h", payload["infraagent"])

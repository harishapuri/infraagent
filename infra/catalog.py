"""Demo stories and expected gate picks for the InfraAgent plane."""

from __future__ import annotations

from pathlib import Path

from infra.bootstrap import ROOT, UNIFIED_ROOT

EXAMPLES = UNIFIED_ROOT / "examples"
STATIC = ROOT / "demo" / "static"
DEMO_AUDIT = ROOT / "data" / "demo_audit.jsonl"
PORT = 8872
HOST = "127.0.0.1"
SITE = f"http://{HOST}:{PORT}"
TITLE = "Infra — stay-up demo"
KICKER = "Infra · InfraAgent plane"

STORIES: dict[str, tuple[Path, Path, str, str]] = {
    "pass": (
        EXAMPLES / "checkov_pass.json",
        EXAMPLES / "telemetry_ok.json",
        "chatbot-api",
        "Traffic is quiet and capacity is fine. If rules and trust agree, go.",
    ),
    "fail": (
        EXAMPLES / "checkov_fail.json",
        EXAMPLES / "telemetry_hot.json",
        "chatbot-api",
        "Errors are high and the setup is unsafe. Stop — do not move customers.",
    ),
    "secure_but_hot": (
        EXAMPLES / "checkov_pass.json",
        EXAMPLES / "telemetry_hot.json",
        "chatbot-api",
        "φ_1h is hot on a clean scan. Stay-up rolls back even when CRC is green.",
    ),
    "open_sg_but_calm": (
        EXAMPLES / "checkov_fail.json",
        EXAMPLES / "telemetry_ok.json",
        "chatbot-api",
        "Stay-up looks healthy, but the fused gate still stops on an open door.",
    ),
    "warn_rising_errors": (
        EXAMPLES / "checkov_pass.json",
        EXAMPLES / "telemetry_warn_phi6.json",
        "chatbot-api",
        "φ_6h is rising. Hold a 10% canary — wait.",
    ),
    "warn_capacity": (
        EXAMPLES / "checkov_pass.json",
        EXAMPLES / "telemetry_warn_kappa.json",
        "chatbot-api",
        "Demand is about to pass capacity (κ). Scale before the switch.",
    ),
    "rollback": (
        EXAMPLES / "checkov_pass.json",
        EXAMPLES / "telemetry_rollback.json",
        "chatbot-api",
        "The live site is already failing. Undo. Keep customers on blue.",
    ),
}

STORY_ORDER = [
    "pass",
    "warn_capacity",
    "warn_rising_errors",
    "fail",
    "secure_but_hot",
    "open_sg_but_calm",
    "rollback",
]

EXPECTED = {
    "pass": ("PASS", "ALLOW"),
    "fail": ("BLOCK", "BLOCK_DEPLOYMENT"),
    "secure_but_hot": ("BLOCK", "ROLLBACK"),
    "open_sg_but_calm": ("BLOCK", "BLOCK_DEPLOYMENT"),
    "warn_rising_errors": ("WARN", "WARN"),
    "warn_capacity": ("WARN", "WARN"),
    "rollback": ("BLOCK", "ROLLBACK"),
}

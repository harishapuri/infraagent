# CICD_Compliance — InfraAgent stay-up

GitHub: [harishapuri/CICD_Compliance](https://github.com/harishapuri/CICD_Compliance)

Predictive stay-up and rollout (InfraAgent, paper 1239). Failure probability φ, capacity deficit κ, and posture Ω still join CRC η and ZeroGuard Ψ on the unified bus. One DSA pick: go / wait / stop. RPA suggestions are never auto-applied. Traffic stays on blue unless the fused pick is go.

Python module name after clone is `infra`.

```bash
git clone https://github.com/harishapuri/CICD_Compliance.git
cd CICD_Compliance
```

## Related repos

| Repo | Plane |
| --- | --- |
| [unifiedframework](https://github.com/harishapuri/unifiedframework) | Fused CRC × ZeroGuard × InfraAgent gate (source of `vendor/unified_framework`) |
| [MAWS](https://github.com/harishapuri/MAWS) | Hive orchestrator (named agents, stay-on-blue) |
| [infraagent](https://github.com/harishapuri/infraagent) | CRC / CI-CD rules (η) |
| [ZeroGuard](https://github.com/harishapuri/ZeroGuard) | Trust / ZTA (Ψ) |

This repo runs alone via `vendor/unified_framework`. To use a live checkout instead:

```bash
export UNIFIED_FRAMEWORK=/path/to/unifiedframework
```

A sibling folder named `unified_framework` (same parent directory) wins over vendor.

Full figures: [ARCHITECTURE.md](ARCHITECTURE.md). Industry comparison: [INDUSTRY_VS_OURS.md](INDUSTRY_VS_OURS.md). Module plan: [PLAN.md](PLAN.md).

## What this repo owns

- Datadog / Prometheus / flat telemetry mapping
- Holt CFA on demand history
- φ_1h / φ_6h / φ_24h, κ, Ω
- DSA gate + suggest-only hold / scale / canary / rollback

## Demo and automation

Hot traffic on a clean scan is the stay-up story: the page should show **Undo**, not a green CRC-only pass.

```bash
python3 -m infra.demo          # http://127.0.0.1:8872/
python3 -m infra.automate      # exit 1 if a pick drifts
```

| Story | Expected pick |
| --- | --- |
| All clear | Go (`ALLOW`) |
| Almost full / errors rising | Wait (`WARN`) |
| Unsafe setup / open door | Stop (`BLOCK_DEPLOYMENT`) |
| Safe setup, bad traffic / site down | Undo (`ROLLBACK`) |

## CLI

```bash
python3 -m infra vendor/unified_framework/examples/checkov_pass.json \
  --telemetry vendor/unified_framework/examples/telemetry_hot.json \
  --focus

python3 -m infra vendor/unified_framework/examples/checkov_pass.json \
  --telemetry vendor/unified_framework/examples/telemetry_datadog.json \
  --service chatbot-api
```

`--enforce` exits `2` on BLOCK. Default is shadow.

## Tests and CI

```bash
python3 -m unittest tests.test_infra tests.test_automate -v
```

`.github/workflows/gate.yml` runs unit tests, `python3 -m infra.automate`, and a shadow pass fixture on every push and pull request.

## Layout

| Path | Role |
| --- | --- |
| `infra/` | Stay-up CLI, browser demo, headless automate |
| `demo/static/` | Autoplay UI (SSE) |
| `vendor/unified_framework/` | Shared ingest, forecast, DSA, RPA, audit |
| `.github/workflows/gate.yml` | Tests + automate + shadow gate |

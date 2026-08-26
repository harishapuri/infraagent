# Infra — InfraAgent plane

Predictive stay-up and rollout (paper 1239) as its **own repo**. Failure probability φ, capacity deficit κ, and posture Ω still join CRC η and ZeroGuard Ψ on the **unified framework** bus. One DSA pick: go / wait / stop. RPA suggestions are never auto-applied.

Sibling products: [`CICD`](../CICD) (rules) and [`zeroguard`](../zeroguard) (trust). Shared library: [`unified_framework`](../unified_framework). Snapshot: `vendor/unified_framework`.

## What this repo owns

- Datadog / Prometheus / flat telemetry mapping
- Holt CFA on demand history
- φ_1h / φ_6h / φ_24h, κ, Ω
- DSA gate + suggest-only hold / scale / canary / rollback

Traffic stays on blue unless the fused pick is go.

## Demo and automation

```bash
cd infra
python3 -m infra.demo          # http://127.0.0.1:8872/
python3 -m infra.automate      # all 7 stories, exit 1 if a pick drifts
```

Hot traffic on a clean scan is the stay-up story: the page should show **Undo**, not a green CRC-only pass.

## Run

```bash
cd infra
python3 -m infra vendor/unified_framework/examples/checkov_pass.json \
  --telemetry vendor/unified_framework/examples/telemetry_hot.json \
  --focus

python3 -m infra vendor/unified_framework/examples/checkov_pass.json \
  --telemetry vendor/unified_framework/examples/telemetry_datadog.json \
  --service chatbot-api
```

`--enforce` exits `2` on BLOCK. Default is shadow.

```bash
export UNIFIED_FRAMEWORK=/path/to/unified_framework
```

A sibling `../unified_framework` wins over vendor.

## Tests

```bash
python3 -m unittest tests.test_infra tests.test_automate -v
```

## Layout

| Path | Role |
| --- | --- |
| `infra/` | Stay-up CLI, browser demo, headless automate |
| `demo/static/` | Autoplay UI (SSE) |
| `vendor/unified_framework/` | Shared ingest, forecast, DSA, RPA, audit |
| `.github/workflows/gate.yml` | Tests + automate + shadow gate |

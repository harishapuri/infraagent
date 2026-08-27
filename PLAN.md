# Plan — InfraAgent stay-up plane

GitHub: [harishapuri/CICD_Compliance](https://github.com/harishapuri/CICD_Compliance)

Implementation plan for the **InfraAgent (1239)** plane as its own product, still fused with CRC and ZeroGuard.

1. **InfraAgent (1239)** — this repo: predictive stay-up and rollout
2. **CRC (207)** — [infraagent](https://github.com/harishapuri/infraagent)
3. **ZeroGuard (2143)** — [ZeroGuard](https://github.com/harishapuri/ZeroGuard)

Shared library: [unifiedframework](https://github.com/harishapuri/unifiedframework), vendored at `vendor/unified_framework`.

They share one message bus, one autonomy policy, one hash-chained audit, and **one gate**. This repo does not flip traffic from telemetry alone.

**Shipped first:** heuristic φ / Holt κ / Ω, DSA, suggest-only RPA, shadow gate, demo on :8872, `python3 -m infra.automate`.

---

## 1. Why stay-up must not run alone

| Gap if InfraAgent is a lone autoscaler | What the other papers supply |
| --- | --- |
| φ is low but IaC is wide open | CRC residual-high; ZeroGuard pillars / Γ |
| Scale-up suggestion fights a security patch | GRA wins security attributes; RPA owns canary and scale |
| Forecast ignores compliance debt | η multiplies Ω |

Join rule: **η multiplies Ω** (and Ψ).

```
Ω  = exp(-α1 φ̄) · exp(-α2 κ̄) · exp(-α3 δ̄) · η

BLOCK  if φ_1h > 0.7  OR  CRC residual-high  OR  critical IaC
WARN   if φ_6h > 0.5  OR  any ZTA pillar fail  OR  κ > 0.15
PASS   otherwise
```

Shared autonomy default **α2**. RPA `apply = false`.

---

## 2. Architecture (this repo)

```
Telemetry + demand history (+ Checkov)
        │
        ▼
 InfraAgent — φ, Holt κ, Ω, DSA, RPA     ← owned here
        │
        ├─ CRC η (vendor)
        └─ ZeroGuard Ψ (vendor)
        │
        ▼
 Typed bus · SHA-256 audit · traffic switch last
        │
        ▼
 python3 -m infra  |  infra.demo :8872  |  infra.automate
```

### InfraAgent plane — shipped vs later

Shipped: `framework/infraagent/forecast.py` (heuristic φ/κ/Ω), `dsa.py`, `rpa.py` (suggest-only), Datadog/Prometheus mapper, Holt on `history.demand`.

Later: T-GAN / XGBoost φ, Prophet CFA, graph attention.

---

## 3. One pipeline run

1. Ingest Checkov JSON + telemetry JSON.
2. InfraAgent publishes `Forecast` (`φ`, `κ`, `Ω`).
3. CRC and ZeroGuard still publish on the same bus.
4. DSA classifies. RPA emits hold / scale / canary / rollback with `apply: false`.
5. Append audit. `--focus` keeps stay-up scores + `decision`.

---

## 4. Demo stories (stay-up-shaped)

**Success:** clean IaC + healthy telemetry → ALLOW.

**Capacity wait:** clean scan, demand > capacity → WARN.

**Hot on clean scan:** clean IaC + hot errors → ROLLBACK (the stay-up story).

**Severe outage:** φ_1h > 0.85 → ROLLBACK.

**Cross-plane:** open SG on calm traffic still BLOCK — this CLI must not treat stay-up as the only vote.

Headless: `python3 -m infra.automate`.

---

## 5. File map

| Path | Role |
| --- | --- |
| `infra/cli.py` | Shadow / `--enforce` / `--focus` |
| `infra/demo.py` | SSE demo |
| `infra/automate.py` | Story catalog runner |
| `infra/catalog.py` | Seven stories, expected picks |
| `vendor/unified_framework/framework/infraagent/` | Forecast, DSA, RPA |
| `vendor/unified_framework/framework/ingest/telemetry.py` | Metric aliases |

---

## 6. Build order

1. **Done.** Split repo, vendor fusion, shadow DSA, `--focus`.
2. **Done.** Demo site :8872, automate, GitHub Actions, Holt CFA.
3. Label real releases (ok / incident / rollback / brownout); scorecard before `--enforce`.
4. XGBoost φ on incident-labeled windows; longer CFA once utilization is stored.
5. Ticket/PR comments from RPA templates — still never auto-apply.

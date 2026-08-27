# Architecture — InfraAgent stay-up plane

GitHub: [harishapuri/infraagent](https://github.com/harishapuri/infraagent)

This repo owns the **stay-up** plane (InfraAgent, paper 1239). Question: will it fail soon, or will we run out of room?

Scoring still runs the **fused** gate. CRC η, ZeroGuard Ψ, and InfraAgent Ω share one bus and one go / wait / stop. `--focus` only changes what the CLI prints. Library source: [unifiedframework](https://github.com/harishapuri/unifiedframework) (vendored here as `vendor/unified_framework`).

Sibling planes: [CICD_Compliance](https://github.com/harishapuri/CICD_Compliance) (rules), [ZeroGuard](https://github.com/harishapuri/ZeroGuard) (trust).

## This repo in the loop

```
Checkov JSON + telemetry / demand history
                ↓
Ingest (vendor/unified_framework)
                ↓
InfraAgent φ, κ, Ω, DSA, suggest-only RPA   ← this plane
CRC η · ZeroGuard Ψ                         ← still computed
                ↓
Typed bus → DSA go / wait / stop
                ↓
Traffic switch LAST · SHA-256 audit · shadow unless --enforce
```

Traffic stays on **blue** unless the fused pick is go. RPA suggestions are never auto-applied.

## All in one — upstream to downstream

```mermaid
flowchart TB
  TEL[Runtime] --> IN[Ingest mapper]
  DEM[Demand history] --> IN
  IAC[IaC / Checkov] --> IN

  IN --> CRC
  IN --> ZG
  IN --> IA

  subgraph CRC[CRC rules]
    ETA["η + residual"]
  end

  subgraph ZG[ZeroGuard trust]
    PSI["Ψ × η"]
  end

  subgraph IA[InfraAgent stay-up — this repo]
    direction TB
    PHI["φ_1h / φ_6h / φ_24h"] --> CFA[Holt CFA]
    CFA --> KAP["κ 24 / 48 / 72h"]
    KAP --> OME["Ω × η"]
    OME --> DSA[DSA go / wait / stop]
    DSA --> RPA[RPA suggest only]
  end

  ETA --> BUS[Fuse on typed bus]
  PSI --> BUS
  OME --> BUS
  BUS --> DSA
  DSA -->|stop| BLUE[Stay on blue]
  DSA -->|wait| HOLD[Hold / 10% canary]
  DSA -->|go| GREEN[Move customers to green]
  BLUE --> AUD[SHA-256 audit]
  HOLD --> AUD
  GREEN --> AUD
```

## InfraAgent complete flow (paper 1239)

```mermaid
flowchart TB
  WIN[Telemetry window] --> TGAN[T-GAN — later]
  G[Service graph] --> ATTN[Neighbor attention — later]
  TGAN --> ATTN
  ATTN --> PHI["φ_1h / φ_6h / φ_24h"]
  HIST[Demand history] --> CFA[CFA Holt — shipped]
  CFA --> KAP["κ"]
  PHI --> OME["Ω = exp(-αφ̄)·exp(-ακ̄)·exp(-αδ̄)·η"]
  KAP --> OME
  OME --> DSA[DSA]
  DSA --> RPA[Suggest hold / scale / canary / rollback]
  GRA[GRA security] -.->|wins security attrs| RPA
  DSA --> SW[Traffic switch last]
```

**Shipped in this repo:** φ from error / cpu / p95 (rising history lifts φ_6h). κ from Holt on `history.demand` or snapshot deficit. Same DSA thresholds. RPA `apply = false`. `python3 -m infra --focus` prints stay-up plus the fused decision.

Hot traffic on a **clean** Checkov scan is the stay-up story: the pick should be **Undo** (`ROLLBACK`), not a green CRC-only pass.

## Gate (same join as unified)

```
η multiplies both Ψ and Ω.

BLOCK  if  φ_1h > 0.7  OR  residual-high  OR  critical IaC
WARN   if  φ_6h > 0.5  OR  any ZTA pillar < 0.5  OR  κ > 0.15
PASS   otherwise → ALLOW

Conflict: GRA owns security attributes; RPA owns traffic and capacity.
Autonomy α2: never auto-apply.
```

## One pipeline run

```mermaid
sequenceDiagram
  participant CLI as python3 -m infra
  participant In as Ingest
  participant CRC as CRC
  participant ZG as ZeroGuard
  participant IA as InfraAgent
  participant DSA as DSA gate
  participant Aud as Audit
  participant Ops as Release

  CLI->>In: Checkov JSON + metrics
  In->>CRC: findings
  In->>ZG: findings + telemetry
  In->>IA: telemetry + history
  IA->>DSA: Forecast Ω φ κ
  CRC->>DSA: RiskReport η
  ZG->>DSA: ZtaScore Ψ
  DSA->>Aud: action + prev hash
  DSA->>Ops: go / wait / stop
  Note over DSA: RPA apply=false
```

## Feedback loop

```
shadow pick  →  customers stay or move  →  record actual
     ok | incident | rollback | brownout
                    ↓
              scorecard → ready_for_enforce? → --enforce
```

## File map (this repo)

| Path | Role |
| --- | --- |
| `infra/cli.py` | Checkov + telemetry → orchestrator; `--focus` / `--enforce` |
| `infra/demo.py` | SSE site on http://127.0.0.1:8872/ |
| `infra/automate.py` | Headless seven stories |
| `vendor/unified_framework/framework/infraagent/` | φ, κ, Ω, DSA, RPA |
| `vendor/unified_framework/framework/ingest/telemetry.py` | Datadog / Prometheus aliases |
| `.github/workflows/gate.yml` | Tests + automate + shadow pass |

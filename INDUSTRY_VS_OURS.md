# Industry deploy vs our stay-up gate

GitHub: [harishapuri/CICD_Compliance](https://github.com/harishapuri/CICD_Compliance)

**Northstar Bank** ships a customer chatbot with two copies: **blue** (customers now) and **green** (empty new assistant). This repo is the **stay-up** plane: will the chat graph fail, or will we run out of room?

Today capacity is a pager after the flip. We still produce **one** go / wait / stop **before** anyone leaves blue. InfraAgent Ω is fused with CRC η and ZeroGuard Ψ. A clean Checkov scan plus hot traffic still **stops**.

Complete figures: [ARCHITECTURE.md](ARCHITECTURE.md). Plan: [PLAN.md](PLAN.md). Fused library: [unifiedframework](https://github.com/harishapuri/unifiedframework).

---

## Typical bank deploy today

1. CI is green. The image is in the registry.
2. Stage, then a change meeting. Capacity is someone else’s ticket.
3. Platform flips traffic. Customers move first.
4. Autoscaler reacts after load hits.
5. Dashboards fire. Rollback is a human after the outage.

No fused stay-up decision **before** customers leave the old assistant.

---

## Our stay-up deploy

1. Same two copies. Blue stays live until the fused gate says go.
2. Checkov plus live traffic enter together (`python3 -m infra`). Datadog series and Prometheus exports map into the same keys. Demand history can Holt-forecast capacity.
3. This plane answers: **will it fail soon, or will we run out of room?** φ_1h / φ_6h / φ_24h, κ, Ω.
4. The same run still scores rules and trust. Open doors still **Stop** even if telemetry is calm.
5. One decision: go / wait / stop. Suggest hold / scale / canary / rollback — never auto-apply.
6. Then move customers. If chatbot or fraud stops, they never leave blue.
7. Label outcomes. `--enforce` only after the scorecard is clean.

Demo: http://127.0.0.1:8872/ (`python3 -m infra.demo`).

---

## Where we are better (stay-up plane)

| Area | Typical deploy | Ours | Why it helps a bank |
| --- | --- | --- | --- |
| When customers move | After CI is green | Only after code + trust + stay-up agree | A clean PR cannot ship a failing chat graph |
| Cross-plane block | Security pass can still brown out | Safe setup + hot traffic still **Undo** | Fraud/chat spikes block the switch |
| Capacity | Autoscaler after load | Holt on demand history, then wait | Wait instead of paging at 2am |
| Rollout actions | Human after the outage | Suggest hold / scale / canary / rollback | A human applies the change |
| Evidence | Datadog in one tab, CI in another | Signed hash chain + fused pick | Examiner can replay why customers stayed on blue |
| Default | Ship unless someone objects | Stay on blue unless the gate says go | Safer for chat-driven transfers |

---

## Benefits you can claim

The claim is not “we built T-GAN in production.” Banks already watch Datadog. This plane is the **stay-up join**: predicted failure and capacity deficit share a gate with scanners and IAM.

- Customers move **after** the fused pick.
- Real exporter metrics go in. Holt can force a wait when the last snapshot looks fine.
- Shadow first. `--enforce` only after outcomes match the log.
- Suggest a patch. Do not apply it.

---

## What we do not claim

| Still later | Why we left it |
| --- | --- |
| T-GAN / graph attention φ | Heuristic φ from error / cpu / p95 is the shipped sensor |
| XGBoost on labeled incidents | Needs weeks of labeled windows |
| Prophet long CFA | Holt on `history.demand` was the safer first upgrade |
| Auto canary | RPA `apply = false` |

Industry already has Datadog. The edge is the **join with rules and trust**, not a new APM.

---

## Short paragraph you can reuse

Banks already watch production. Those signals live in a different tool from Checkov, so a chatbot release can look green in CI and still move customers onto a copy that will fail within the hour. This repo is the InfraAgent plane of one orchestrator: failure probability and capacity deficit are scored with CRC η and ZeroGuard Ψ. The only customer-facing output is go, wait, or stop. Suggested remediations are never applied automatically. The old chatbot stays live until the output is go. Every decision is hash-chained and later scored against what actually happened.

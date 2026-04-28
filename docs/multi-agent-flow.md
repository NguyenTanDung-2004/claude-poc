# Multi-agent dev-flow POC

A POC that simulates a 3-role software delivery pipeline (BA → DEV → QC) using Claude Code subagents.

## Layout

- `roles/` — role definitions (responsibilities + output schemas). The source of truth for what each role does.
- `.claude/agents/` — Claude Code subagent files (`ba`, `dev`, `qc`). Thin wrappers that point each agent at its `roles/*.md` contract and constrain its tool surface.
- `.claude/commands/dev-flow.md` — orchestrator slash command.
- `samples/app/` — minimal FastAPI scaffold the DEV agent extends.
- `samples/requirement-01.md` — sample requirement that drives a demo run.

## Pipeline

```
Requirement ──► BA ──► Stories + ACs ──► DEV ──► Code + Notes ──► QC ──► Verdict + Evidence
```

Single pass in v1 — no retry loop. QC's verdict is the deliverable.

## Running the demo

In a Claude Code session at the repo root:

```
/dev-flow samples/requirement-01.md
```

The orchestrator runs the three subagents sequentially and prints the final QC verdict + per-AC findings.

## Hand-off contract

See [`roles/README.md`](../roles/README.md) for the exact markdown sections each role must emit. The contract is the only thing that keeps this composable — agents must not deviate from it.

## Why subagents (not one big prompt)?

- **Tool isolation** — BA can't accidentally edit code; QC can't modify the implementation.
- **Context isolation** — each role only sees what its predecessor produced, mirroring real hand-offs.
- **Independent iteration** — you can swap or tune one role without touching the others.

## Out of scope (v1)

- Iteration loop on QC FAIL (DEV gets one chance).
- Persistence in the sample app.
- Multiple BA / DEV / QC instances per pipeline.
- Real authentication or production-grade error handling in `samples/app/`.

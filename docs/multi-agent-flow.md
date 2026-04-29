# Multi-agent dev-flow POC

A POC that simulates a 3-role software delivery pipeline (BA → DEV → QC) using Claude Code subagents, with DEV and QC each running in two phases and one parallel branch in the middle.

## Layout

- `roles/` — role definitions (responsibilities, phase contracts, output schemas). The source of truth for what each role does.
- `.claude/agents/` — Claude Code subagent files (`ba`, `dev`, `qc`). Thin wrappers that point each agent at its `roles/*.md` contract and constrain its tool surface.
- `.claude/commands/dev-flow.md` — orchestrator slash command.
- `samples/app/` — minimal FastAPI scaffold the DEV (code phase) agent extends.
- `samples/requirement1/` — one requirement and the artifacts produced for it (`requirement.md`, plus `ba-analyze.md`, `dev-specs.md`, `test-scenario.md` written by the agents).

## Pipeline

```
Requirement ──► BA ──► ba-analyze.md
                      │
                      ▼
                DEV (spec) ──► dev-specs.md
                      │
       ┌──────────────┴───────────────┐
       ▼                              ▼   (parallel)
DEV (code) → samples/app/    QC (scenarios) → test-scenario.md
       │                              │
       └──────────────┬───────────────┘
                      ▼
               QC (verdict) ──► pytest under samples/app/tests/, run, report
```

Single pass in v1 — no retry loop. QC's verdict is the deliverable.

## Per-requirement folder

Each requirement gets its own folder under `samples/`. The input `requirement.md` is the only file you write by hand; everything else is produced by the pipeline:

```
samples/requirement1/
  requirement.md      ← you write this
  ba-analyze.md       ← BA writes
  dev-specs.md        ← DEV (spec phase) writes
  test-scenario.md    ← QC (scenarios phase) writes
```

## Running the demo

In a Claude Code session at the repo root:

```
/dev-flow samples/requirement1
```

The orchestrator runs BA, then DEV (spec), then DEV (code) and QC (scenarios) **in parallel**, then QC (verdict). At the end it prints the verdict and the list of every artifact created.

## Hand-off contract

See [`roles/README.md`](../roles/README.md) for the exact files each phase reads and writes. The contract is the only thing that keeps this composable — agents must not deviate from it.

## Why subagents (not one big prompt)?

- **Tool isolation** — BA can't accidentally edit code; QC's scenarios phase can't peek at the implementation.
- **Context isolation** — each role only sees what its predecessor produced, mirroring real hand-offs.
- **Independent iteration** — you can swap or tune one role without touching the others.
- **Parallelism** — DEV (code) and QC (scenarios) both work from `dev-specs.md` and have no shared writes, so they run concurrently.

## Out of scope (v1)

- Iteration loop on QC FAIL (DEV gets one chance).
- Persistence in the sample app.
- Multiple BA / DEV / QC instances per pipeline.
- Real authentication or production-grade error handling in `samples/app/`.

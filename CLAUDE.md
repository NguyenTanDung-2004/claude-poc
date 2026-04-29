# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A POC that simulates a 3-role software delivery pipeline (BA → DEV → QC) using Claude Code subagents. The product *is* the pipeline — the FastAPI scaffold under `samples/app/` exists only as something for the agents to extend. When changing this repo, you are almost always editing the pipeline (roles, agents, orchestrator), not building features in `samples/app/` by hand.

## The hand-off contract is the whole point

`roles/README.md` defines the exact files each phase reads and writes. Agents must not deviate, and the orchestrator must not "improve" any subagent's output between hand-offs. If you change role behavior or output schema, update **both** the `roles/*.md` source-of-truth file **and** any wrapper assumptions in `.claude/agents/*.md` and `.claude/commands/dev-flow.md` — these three layers must stay aligned.

The pipeline:

```
Requirement → BA → ba-analyze.md
                 → DEV (spec) → dev-specs.md
                              ┌→ DEV (code)      → samples/app/*.py     ┐ parallel
                              └→ QC (scenarios)  → test-scenario.md     ┘
                                          → QC (verdict) → pytest under samples/app/tests/, run, report
```

Single pass — no retry loop on FAIL in v1.

## Three-layer architecture

1. **`roles/{ba,dev,qc}.md`** — source of truth for each role's mission, output schema, and rules. Edit here first when changing behavior.
2. **`.claude/agents/{ba,dev,qc}.md`** — thin Claude Code subagent wrappers. They constrain the tool surface (e.g. BA gets Read/Grep/Glob/Write only — no code edits) and point each agent at its `roles/*.md` contract. Keep them thin; don't duplicate role logic here.
3. **`.claude/commands/dev-flow.md`** — orchestrator slash command. Sequences the four phases and dispatches the parallel branch.

DEV and QC each run in **two phases** invoked separately by the orchestrator (`phase=spec`/`phase=code` for DEV, `phase=scenarios`/`phase=verdict` for QC). The agent wrapper expects the orchestrator to pass the phase explicitly.

## Per-requirement folder layout

Each requirement lives in its own folder under `samples/`. Only `requirement.md` is hand-written; the rest are produced by the pipeline:

```
samples/<requirement-name>/
  requirement.md      ← input you write
  ba-analyze.md       ← BA writes
  dev-specs.md        ← DEV (spec phase) writes
  test-scenario.md    ← QC (scenarios phase) writes
  report.md           ← orchestrator writes; updated after every phase (running ledger)
```

`report.md` is a **running ledger** maintained by the orchestrator: initialized before Phase 1 with all phases `pending`, then updated after each phase returns. It must remain a valid, complete report at every point so that a crash mid-pipeline still leaves a coherent record. The orchestrator copies QC's `## Verdict` and `## Findings` into it verbatim — never paraphrase.

Code and tests live in the **shared** scaffold (not per-requirement):
- `samples/app/` — DEV (code phase) writes here
- `samples/app/tests/` — QC (verdict phase) writes here

## Running the pipeline

In a Claude Code session at the repo root:

```
/dev-flow samples/<requirement-name>
```

The orchestrator runs BA → DEV (spec) → [DEV (code) ∥ QC (scenarios)] → QC (verdict).

## Sample app dev commands

The scaffold is a tiny FastAPI app. Run from `samples/app/`:

```
pip install -r requirements.txt
uvicorn main:app --reload
pytest -q
```

`samples/app/tests/conftest.py` adds `samples/app/` to `sys.path` so `from main import app` works regardless of where pytest is invoked from. QC's verdict-phase tests rely on this — don't remove it.

## Parallelism rules (important)

DEV (code) and QC (scenarios) both consume `dev-specs.md` and run **concurrently**. To keep the parallel branch safe:
- DEV (code) must **not** read `<folder>/test-scenario.md` (it may not exist yet).
- QC (scenarios) must **not** read or modify anything under `samples/app/` (the implementation may not exist yet).
- They have no shared writes: DEV touches `samples/app/` (excluding `tests/`), QC touches `<folder>/test-scenario.md`.

When the orchestrator dispatches phase 3, it must issue **both Agent calls in a single message** so they actually run in parallel.

## Out of scope (v1)

No retry loop on QC FAIL, no persistence in the sample app, no auth/rate-limiting, no multiple instances of any role per pipeline. Don't add these without an explicit ask — they change the pipeline contract.

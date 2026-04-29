# Roles

Three roles drive the dev-flow POC: **BA**, **DEV**, **QC**. Each role has a single, focused responsibility and a deterministic output (markdown sections + named files) so the next role can consume it without ambiguity.

## Pipeline

```
Requirement
     │
     ▼
   BA  ─────────────► ba-analyze.md          (Stories + AC)
     │
     ▼
  DEV (spec phase) ─► dev-specs.md           (API contract, data, errors)
     │
     ├──────────────────────────┬──────────────────────────┐
     ▼                          ▼                          │  ◄── run in parallel
  DEV (code phase)           QC (scenarios phase)          │
  samples/app/*.py           test-scenario.md              │
     │                          │                          │
     └────────────┬─────────────┘                          │
                  ▼
            QC (verdict phase) ─► pytest under samples/app/tests/, run, report
```

Single pass — no re-loop in v1. QC's verdict (PASS or FAIL) is the deliverable.

## Per-requirement folder layout

Each requirement lives in its own folder under `samples/`:

```
samples/requirement1/
  requirement.md      ← input you write
  ba-analyze.md       ← BA writes
  dev-specs.md        ← DEV (spec phase) writes
  test-scenario.md    ← QC (scenarios phase) writes
  report.md           ← orchestrator writes; updated after every phase
```

Code and tests stay in the shared scaffold:
- `samples/app/` — DEV (code phase) writes here
- `samples/app/tests/` — QC (verdict phase) writes here

Throughout this doc, `<folder>` means the requirement's folder (e.g. `samples/requirement1`).

## Hand-off contract

Each step MUST emit the artifact below verbatim. The next step parses by section heading or reads the named file.

### Requirement → BA
- Input: `<folder>/requirement.md`
- Output: `<folder>/ba-analyze.md` containing
  - `## Stories` — one user story per bullet (`As a … I want … so that …`)
  - `## Acceptance Criteria` — numbered checklist; each item independently testable

### BA → DEV (spec phase)
- Input: `<folder>/ba-analyze.md`
- Output: `<folder>/dev-specs.md` containing
  - `## API` — endpoints, methods, request/response shapes, status codes
  - `## Data` — in-memory data structures (no persistence)
  - `## Errors` — error responses per failure mode
  - `## Notes` — assumptions, anything explicitly out of scope
- Spec phase writes **specs only** — no implementation code in this phase.

### DEV (spec phase) → DEV (code phase) ∥ QC (scenarios phase)
Both branches read `<folder>/dev-specs.md` (and `<folder>/ba-analyze.md`) and run **in parallel**.

**DEV (code phase)** — emits markdown to chat:
- `## Changes` — file list, one line per file (`path/to/file — what changed`)
- `## Notes` — assumptions made, deviations from specs

**QC (scenarios phase)** — writes `<folder>/test-scenario.md` containing
- One Given/When/Then scenario per AC, each labelled with the AC number it covers
- No pytest code in this phase — scenarios are the human-readable test plan

### → QC (verdict phase)
- Input: `<folder>/test-scenario.md`, `<folder>/dev-specs.md`, and DEV's code under `samples/app/`
- QC translates each scenario into pytest under `samples/app/tests/`, runs `pytest -q`, and emits to chat:
  - `## Verdict: PASS` or `## Verdict: FAIL`
  - `## Evidence` — commands run + output excerpts
  - `## Findings` — per-AC pass/fail mapped back to BA's numbering

### Orchestrator → `<folder>/report.md` (running ledger)
The orchestrator owns `<folder>/report.md` and **updates it after every phase**, not only at the end. The file must always be a valid, complete report of the run *as far as it has gotten* — so if the pipeline crashes mid-run, the report still tells you what finished, what was running, and what is pending.

Required sections (always present, even on the initial write):

- `## Run summary` — requirement folder, final verdict (`pending` until QC verdict completes, then `PASS`/`FAIL`), one-line outcome.
- `## Phases` — markdown table, one row per phase. Columns: **Phase**, **Role**, **Output**, **Status**. Status values:
  - `pending` — not yet started
  - `running` — currently in flight (set when the orchestrator dispatches the agent)
  - `done` — completed successfully
  - `PASS` / `FAIL` — only used for the QC verdict row
  - `blocked: <reason>` — phase failed or could not run; pipeline halts
- `## Verdict` — the verbatim verdict line emitted by QC (verdict phase). Before QC verdict runs, this section reads `_pending — QC verdict has not run yet._`.
- `## Findings` — the verbatim `## Findings` block emitted by QC (verdict phase). Before QC verdict runs, this section reads `_pending — QC verdict has not run yet._`.
- `## Artifacts` — bullet list of every file created or modified by completed phases (extended after each phase).

Update cadence:

1. **Before Phase 1** — initialize `report.md` with all phases marked `pending`, verdict `pending`, empty artifact list (plus `<folder>/report.md` itself).
2. **After each phase agent returns** — set that phase's status to `done` (or `blocked: …` on failure), and append any newly produced artifact paths.
3. **After Phase 4 (QC verdict)** — set the QC verdict row to `PASS` or `FAIL`, replace the `## Verdict` and `## Findings` placeholders with QC's verbatim output, and ensure all pytest files written under `samples/app/tests/` are in `## Artifacts`.

The orchestrator must not paraphrase QC's verdict or findings — copy them verbatim. The report is an aggregator, not an interpreter.

## Files

- [ba.md](ba.md) — Business Analyst
- [dev.md](dev.md) — Developer
- [qc.md](qc.md) — Quality Control

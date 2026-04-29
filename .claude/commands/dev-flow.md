---
description: Run the BA → DEV → QC dev-flow pipeline against a requirement folder
argument-hint: <path/to/requirement-folder>
---

Orchestrate the dev-flow POC against the requirement folder at: $ARGUMENTS

The folder must already contain `requirement.md`. The other artifacts (`ba-analyze.md`, `dev-specs.md`, `test-scenario.md`) will be created by the agents during the run.

Read `roles/README.md` first to refresh the pipeline contract — pay particular attention to the "Orchestrator → `<folder>/report.md` (running ledger)" section, which is what you maintain across phases. Then run the four phases in this exact order. Phases 1–2 are sequential. Phase 3 has two branches that must run **in parallel**. Phase 4 is sequential after phase 3.

### Phase 0 — Initialize `<folder>/report.md`
Before invoking any subagent, write `<folder>/report.md` with all required sections per `roles/README.md`. Mark every phase status `pending`, verdict `pending`, and seed the `## Artifacts` list with `<folder>/report.md` itself. This is the running ledger — it must remain a complete, valid report after every subsequent update so that a crash mid-pipeline still leaves something coherent on disk.

### Phase 1 — BA
Set the BA row in `report.md` to `running`, then invoke the `ba` subagent with the folder path. Tell it to read `<folder>/requirement.md` and write `<folder>/ba-analyze.md`. Wait for completion. **After BA returns**, update `report.md`: BA row → `done`, append `<folder>/ba-analyze.md` to `## Artifacts`.

### Phase 2 — DEV (spec)
Set the DEV (spec) row to `running`, then invoke the `dev` subagent with the folder path **and** `phase=spec`. Tell it to read `<folder>/ba-analyze.md` and write `<folder>/dev-specs.md`. **No code is written in this phase.** Wait for completion. **After DEV (spec) returns**, update `report.md`: DEV (spec) row → `done`, append `<folder>/dev-specs.md` to `## Artifacts`.

### Phase 3 — DEV (code) ∥ QC (scenarios) — parallel
Set both Phase 3 rows (DEV code and QC scenarios) to `running`. In a **single message**, dispatch two Agent calls concurrently:
- `dev` subagent with the folder path and `phase=code` — implements under `samples/app/`, returns `## Changes` + `## Notes`.
- `qc` subagent with the folder path and `phase=scenarios` — writes `<folder>/test-scenario.md`, must not read `samples/app/`.

Wait for **both** to finish before moving on. If either fails, set its row to `blocked: <reason>`, update `report.md`, then stop and report. **After both return**, update `report.md`: each row → `done`, append every file from DEV's `## Changes` list and `<folder>/test-scenario.md` to `## Artifacts`.

### Phase 4 — QC (verdict)
Set the QC (verdict) row to `running`, then invoke the `qc` subagent with the folder path and `phase=verdict`. It writes pytest under `samples/app/tests/`, runs `pytest -q`, and emits `## Verdict` + `## Evidence` + `## Findings`. **After QC (verdict) returns**, update `report.md`:
- QC (verdict) row status → `PASS` or `FAIL` (matching QC's verdict line).
- `## Run summary` final-verdict field → `PASS` or `FAIL`.
- Replace the `## Verdict` placeholder with QC's verbatim verdict line.
- Replace the `## Findings` placeholder with QC's verbatim `## Findings` block.
- Append every pytest file written under `samples/app/tests/` to `## Artifacts`.

Copy QC's verdict and findings **verbatim** — do not paraphrase, summarize, or "clean up" wording. The report is an aggregator, not an interpreter.

### Final chat summary
After the last `report.md` update, print to the user:
- The QC verdict line (`## Verdict: PASS` or `## Verdict: FAIL`).
- The full `## Findings` section.
- Path to `<folder>/report.md` and the artifact list it references.

Do not interpret, edit, or "improve" any subagent's output between hand-offs. Pass artifacts through unchanged — the contract is the whole point of the POC.

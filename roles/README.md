# Roles

Three roles drive the dev-flow POC: **BA**, **DEV**, **QC**. Each role has a single, focused responsibility and a deterministic output schema so the next role can consume it without ambiguity.

## Pipeline

```
Requirement ──► BA ──► Stories + ACs ──► DEV ──► Code + Notes ──► QC ──► Verdict + Evidence
```

Single pass — no re-loop in v1. QC's verdict (PASS or FAIL) is the deliverable.

## Hand-off contract

Each role MUST emit the markdown sections below verbatim. The next role parses by section heading.

### BA → DEV
- `## Stories` — one user story per bullet (`As a … I want … so that …`).
- `## Acceptance Criteria` — numbered checklist; each item must be independently testable.

### DEV → QC
- `## Changes` — file list, one line per file (`path/to/file — what changed`).
- `## Notes` — assumptions made, anything explicitly out of scope.

### QC → user
- `## Verdict: PASS` or `## Verdict: FAIL`
- `## Evidence` — commands run + relevant output excerpts.
- `## Findings` — per-AC pass/fail, mapped back to BA's numbering.

## Files

- [ba.md](ba.md) — Business Analyst
- [dev.md](dev.md) — Developer
- [qc.md](qc.md) — Quality Control

---
description: Run the BA → DEV → QC dev-flow pipeline against a requirement file
argument-hint: <path/to/requirement.md>
---

Orchestrate the 3-role dev-flow POC against the requirement at: $ARGUMENTS

Read `roles/README.md` first to refresh the pipeline contract, then run the three subagents **sequentially** (each must finish before the next starts):

1. **BA** — invoke the `ba` subagent with the requirement file path. Capture its full markdown output.
2. **DEV** — invoke the `dev` subagent. Pass it the BA output verbatim as input. Capture its full markdown output.
3. **QC** — invoke the `qc` subagent. Pass it both the BA output (acceptance criteria) and the DEV output (file list + notes). Capture its full markdown output.

After QC finishes, print a concise summary to the user:
- The QC verdict line (`## Verdict: PASS` or `## Verdict: FAIL`)
- The full Findings section (per-AC results)
- Paths to any files created or modified by DEV/QC

Do not interpret, edit, or "improve" any subagent's output between hand-offs. The whole point is to exercise the contract — pass markdown through unchanged.

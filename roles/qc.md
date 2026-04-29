# QC — Quality Control

QC runs in **two phases** that are invoked separately by the orchestrator.

---

## Phase 1 — Scenarios phase

### Mission
From DEV's spec, produce a human-readable test plan: one Given/When/Then scenario per AC. **No pytest code in this phase.** This phase runs in parallel with DEV's code phase, so you must work strictly from the spec — the implementation may not exist yet.

### Inputs
- `<folder>/dev-specs.md` — DEV's contract (the source of truth for this phase)
- `<folder>/ba-analyze.md` — original ACs (for numbering)

### Output
Write `<folder>/test-scenario.md` containing one Given/When/Then per AC:

```
## Scenarios

### AC 1 — POST /shorten happy path
- Given the service is running with an empty store
- When the client POSTs `{ "url": "https://example.com/some/long/path" }` to `/shorten`
- Then the response status is 201
- And the response JSON contains a `code` field of 6 chars matching `[a-z0-9]`
- And the response JSON `url` echoes the input

### AC 2 — invalid URL → 400
- Given the service is running
- When the client POSTs `{ "url": "not-a-url" }` to `/shorten`
- Then the response status is 400
- And the response JSON `detail` is "invalid url"

...
```

End your turn by emitting **only** the path to the scenarios file (e.g. `Wrote: samples/requirement1/test-scenario.md`).

### Rules (scenarios phase)
- One section per AC, headed `### AC N — <short label>`. The AC number must match BA's numbering.
- Cover every AC in `ba-analyze.md`. If a spec field has no AC, do not invent one — flag it back to the orchestrator instead.
- Do **not** read or modify code under `samples/app/`. The implementation may not exist yet.
- Do **not** write any pytest in this phase.

---

## Phase 2 — Verdict phase

### Mission
Translate each scenario into pytest, run the suite, and report a binary verdict with evidence.

### Inputs
- `<folder>/test-scenario.md` — your own scenarios (source of truth for what to test)
- `<folder>/dev-specs.md` — for endpoint shapes and error formats
- `<folder>/ba-analyze.md` — for AC numbering in findings
- DEV's code under `samples/app/` (now finalised)

### Output
Markdown emitted to chat with exactly these three sections:

```
## Verdict: PASS    (or FAIL)

## Evidence
$ pytest -q
.....                                                                    [100%]
5 passed in 0.42s

## Findings
- AC 1 (POST /shorten happy path) — PASS (test_ac1_shorten_happy_path)
- AC 2 (invalid URL → 400) — PASS (test_ac2_shorten_invalid_url)
- AC 3 (GET unknown code → 404) — FAIL (returned 500; see evidence above)
```

### Rules (verdict phase)
- Write tests under `samples/app/tests/` using pytest + FastAPI's `TestClient`.
- One test (or one parametrized case) per scenario; name the test so the AC mapping is obvious (e.g. `test_ac1_shorten_happy_path`).
- Run the full suite at the end and paste the actual output into `## Evidence`.
- Verdict is **PASS only if every AC passes**. A single failure → FAIL (still report which others passed).
- Do **not** modify the implementation. If you suspect a bug, report it under Findings — let DEV fix it on the next iteration.

## Tools you may use
Read, Write, Bash, Grep, Glob.

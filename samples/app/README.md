# samples/app

Minimal FastAPI scaffold used by the multi-agent dev-flow POC. Shared across all requirements under `samples/`.

- `main.py` is extended by the DEV (code phase) subagent.
- `tests/` is created and populated by the QC (verdict phase) subagent.
- Don't pre-fill either by hand — the demo is producing them via `/dev-flow <requirement-folder>`.

## Local sanity check

```
pip install -r requirements.txt
uvicorn main:app --reload
pytest -q
```

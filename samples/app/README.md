# samples/app

Minimal FastAPI scaffold used by the multi-agent dev-flow POC.

- `main.py` is extended by the DEV subagent.
- `tests/` is created and populated by the QC subagent.
- Don't pre-fill either by hand — the demo is producing them via `/dev-flow`.

## Local sanity check

```
pip install -r requirements.txt
uvicorn main:app --reload
pytest -q
```

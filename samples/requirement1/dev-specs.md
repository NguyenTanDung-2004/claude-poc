## API
- GET /hello
  - Request: no path params, no query params, no body.
  - Success: 200 with JSON body exactly `{"message": "Hello, World!"}`.
  - Response `Content-Type` header begins with `application/json` (FastAPI default `application/json`).
  - Behavior is stateless and idempotent: repeating the request returns the same status code and the same JSON body.
  - Maps to AC #1, AC #6, AC #7.

- GET /hello/{name}
  - Request: path param `name: str` (no body, no query params).
  - Validation:
    - `name` must have length >= 2 after FastAPI path decoding (no trim, no strip — length is `len(name)` of the raw decoded path segment).
    - `name` of length 1 fails validation (see Errors, AC #4).
    - `name` of length >= 2 passes validation (AC #5).
  - Success: 200 with JSON body exactly `{"message": f"Hello, {Name}!"}` where `Name` is `name` with the first character upper-cased and remaining characters left untouched (Python `name[0].upper() + name[1:]`).
    - For `name = "John"` -> `{"message": "Hello, John!"}` (AC #2).
    - For `name = "john"` -> `{"message": "Hello, John!"}` (AC #3).
    - For `name = "Jo"` -> `{"message": "Hello, Jo!"}` (AC #5).
  - Response `Content-Type` header begins with `application/json` on success (AC #6).
  - Behavior is stateless and idempotent: repeating the same request yields the same status code and the same JSON body (AC #7).
  - Maps to AC #2, AC #3, AC #5, AC #6, AC #7.

## Data
- No persistence, no database, no in-memory store. Both endpoints are pure functions of their inputs.
- No module-level mutable state is introduced; the FastAPI `app` instance defined in `samples/app/main.py` is the only module-level object.
- Greeting template is the literal Python f-string `f"Hello, {value}!"` where `value` is `"World"` for `GET /hello` and the capitalized `name` for `GET /hello/{name}`.

## Errors
- 400 on `GET /hello/{name}` when `len(name) < 2` (i.e. length 1):
  - Status code: 400.
  - JSON body shape: `{"detail": "<non-empty string describing the validation failure>"}`.
  - `detail` MUST be a non-empty string. Recommended literal value: `"name must be at least 2 characters"`. QC and DEV-code MAY rely only on `detail` being present and non-empty (not on the exact string), per AC #4.
  - Raised via `fastapi.HTTPException(status_code=400, detail=...)` so FastAPI emits a JSON body of the form `{"detail": "..."}`.
  - Maps to AC #4.
- No other client-error or server-error responses are defined for these endpoints in this requirement.
- Path routing: a request to `GET /hello/` (empty name) is not exercised by any AC. FastAPI will redirect or 404 by default; this requirement does not prescribe behavior for that path. See Notes.

## Notes
- Framework: FastAPI (already in `samples/app/requirements.txt`). Both endpoints are added to the existing `app` in `samples/app/main.py`. No new dependencies required.
- Capitalization rule (AC #3): interpreted as "upper-case the first character; leave the rest of the string unchanged" (`name[0].upper() + name[1:]`). This is deliberately NOT Python's `str.capitalize()`, because `str.capitalize()` lower-cases the tail (e.g. `"jOHN".capitalize() == "John"`), which would change characters beyond the first and is not required by AC #3. AC #3 only constrains the first letter; AC #2 (`"John"` -> `"John"`) and AC #5 (`"Jo"` -> `"Jo"`) are both satisfied by the chosen rule.
- Length rule (AC #4 vs AC #5): the boundary is `len(name) >= 2` passes, `len(name) == 1` fails. AC #4 specifies length 1 -> 400; AC #5 specifies length 2 -> 200. No upper bound on `name` length is imposed (no AC requires one).
- `name` character set: ACs only show ASCII alphabetic examples. Spec does not restrict character set; any non-empty path segment of length >= 2 is accepted. Non-ASCII first characters are upper-cased via Python's default `str.upper()` semantics on the first code point.
- AC #4 `detail` wording: AC #4 only requires a non-empty `detail` string. The exact wording is an implementation choice; QC scenarios should assert presence and non-emptiness rather than an exact string match.
- AC #6 `Content-Type`: satisfied by FastAPI's default JSON response. No custom response class is required. Asserting that the header value starts with `application/json` is sufficient (FastAPI may append `; charset=utf-8`).
- AC #7 statelessness: enforced by not introducing any module-level mutable state. Two sequential calls with identical inputs MUST produce identical status codes and identical JSON bodies.
- Out of scope (per requirement): persistence, authentication, authorization, rate limiting, logging, CORS configuration, internationalization, request body parsing, query parameters, and any endpoint other than `GET /hello` and `GET /hello/{name}`.
- Files expected to change in the code phase: `samples/app/main.py` only. No new modules are required, though DEV may extract a small helper if it keeps `main.py` readable — that is an implementation detail and does not alter this contract.

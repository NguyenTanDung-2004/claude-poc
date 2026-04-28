# Requirement 01 — URL shortener

## Background
We need a tiny service to turn long URLs into short codes. This is a POC for the BA → DEV → QC dev-flow pipeline; persistence and auth are explicitly out of scope.

## Ask
Add two endpoints to the FastAPI app under `samples/app/`:

1. **`POST /shorten`** — accepts a long URL, returns a short code.
2. **`GET /{code}`** — looks up the code and either redirects to the original URL or returns it in a JSON body (BA's call).

Storage may be in-memory (a dict is fine). The service does not need to survive a restart.

## Notes for BA
- Decide what counts as a "valid URL" and what the code format/length should be.
- Define what happens when the same URL is shortened twice (return the existing code, or mint a new one — pick and justify).
- Define error responses for the obvious failure modes (bad input, unknown code).
- Keep the AC list focused on **observable HTTP behavior** — status codes, response shape, headers. No internal-implementation ACs.

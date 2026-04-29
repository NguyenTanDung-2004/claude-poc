## Scenarios

### AC 1 — GET /hello default greeting
- Given the FastAPI service is running with no persisted state
- When the client sends `GET /hello` (no path params, no query, no body)
- Then the response status is 200
- And the response JSON body is exactly `{"message": "Hello, World!"}`

### AC 2 — GET /hello/John capitalized name passthrough
- Given the FastAPI service is running
- When the client sends `GET /hello/John`
- Then the response status is 200
- And the response JSON body is exactly `{"message": "Hello, John!"}`

### AC 3 — GET /hello/{name} lowercases first letter capitalized
- Given the FastAPI service is running
- When the client sends `GET /hello/john` (lowercase first letter)
- Then the response status is 200
- And the response JSON body is exactly `{"message": "Hello, John!"}`
- And the `message` field's name segment starts with an upper-cased first character of the supplied `name`

### AC 4 — GET /hello/{name} length 1 → 400
- Given the FastAPI service is running
- When the client sends `GET /hello/J` (single-character name)
- Then the response status is 400
- And the response JSON body contains a `detail` field
- And `detail` is a non-empty string describing the validation failure (exact wording not asserted)

### AC 5 — GET /hello/{name} length 2 boundary → 200
- Given the FastAPI service is running
- When the client sends `GET /hello/Jo` (two-character name)
- Then the response status is 200
- And the response JSON body is exactly `{"message": "Hello, Jo!"}`

### AC 6 — Content-Type is application/json on success
- Given the FastAPI service is running
- When the client sends `GET /hello` and separately `GET /hello/Jo` (both successful)
- Then each response status is 200
- And each response `Content-Type` header value starts with `application/json` (a `; charset=utf-8` suffix is acceptable)

### AC 7 — Stateless / idempotent responses
- Given the FastAPI service is running with no persisted state
- When the client sends `GET /hello` twice in succession
- Then both responses have identical status codes and identical JSON bodies
- And when the client also sends `GET /hello/John` twice in succession
- Then both of those responses likewise have identical status codes and identical JSON bodies

## Stories
- As an API consumer, I want to fetch a generic greeting from `GET /hello`, so that I can confirm the service is reachable and returns a default message.
- As an API consumer, I want to fetch a personalized greeting from `GET /hello/{name}`, so that I receive a message addressed to the supplied name.
- As an API consumer, I want the service to reject names that are too short, so that invalid input is surfaced as a client error rather than a malformed greeting.

## Acceptance Criteria
1. `GET /hello` returns HTTP 200 and a JSON body exactly equal to `{"message": "Hello, World!"}`.
2. `GET /hello/John` returns HTTP 200 and a JSON body exactly equal to `{"message": "Hello, John!"}`.
3. `GET /hello/{name}` with a lowercase name (e.g. `GET /hello/john`) returns HTTP 200 and a JSON body whose `message` field is exactly `{"message": "Hello, John!"}` — the first letter of the supplied name is capitalized in the response.
4. `GET /hello/{name}` with a name of length 1 (e.g. `GET /hello/J`) returns HTTP 400 and a JSON response body containing a non-empty `detail` field describing the validation failure.
5. `GET /hello/{name}` with a name of length exactly 2 (e.g. `GET /hello/Jo`) returns HTTP 200 and a JSON body exactly equal to `{"message": "Hello, Jo!"}` (boundary: 2 characters is the minimum accepted length).
6. The response `Content-Type` header for both `GET /hello` and a successful `GET /hello/{name}` starts with `application/json`.
7. `GET /hello` and `GET /hello/{name}` are stateless — issuing the same request twice in succession yields identical HTTP status codes and identical JSON response bodies.

"""QC verdict-phase pytest suite.

One test per AC scenario from samples/requirement1/test-scenario.md.
Test names embed the AC number so the mapping back to BA's numbering is obvious.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# AC 1 — GET /hello default greeting
# ---------------------------------------------------------------------------
def test_ac1_hello_world_default_greeting():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


# ---------------------------------------------------------------------------
# AC 2 — GET /hello/John capitalized name passthrough
# ---------------------------------------------------------------------------
def test_ac2_hello_john_capitalized_passthrough():
    response = client.get("/hello/John")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, John!"}


# ---------------------------------------------------------------------------
# AC 3 — GET /hello/{name} lowercases first letter capitalized
# ---------------------------------------------------------------------------
def test_ac3_hello_lowercase_name_first_letter_capitalized():
    response = client.get("/hello/john")
    assert response.status_code == 200
    body = response.json()
    assert body == {"message": "Hello, John!"}
    # Extra check: the name segment of the message starts with an uppercase
    # version of the first character of the supplied name.
    prefix = "Hello, "
    suffix = "!"
    assert body["message"].startswith(prefix) and body["message"].endswith(suffix)
    name_segment = body["message"][len(prefix):-len(suffix)]
    assert name_segment[:1] == "john"[0].upper()


# ---------------------------------------------------------------------------
# AC 4 — GET /hello/{name} length 1 → 400
# ---------------------------------------------------------------------------
def test_ac4_short_name_returns_400():
    response = client.get("/hello/J")
    assert response.status_code == 400
    body = response.json()
    assert "detail" in body
    assert isinstance(body["detail"], str)
    assert body["detail"]  # non-empty


# ---------------------------------------------------------------------------
# AC 5 — GET /hello/{name} length 2 boundary → 200
# ---------------------------------------------------------------------------
def test_ac5_two_char_name_boundary_returns_200():
    response = client.get("/hello/Jo")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Jo!"}


# ---------------------------------------------------------------------------
# AC 6 — Content-Type is application/json on success
# ---------------------------------------------------------------------------
def test_ac6_content_type_application_json_on_success():
    r1 = client.get("/hello")
    r2 = client.get("/hello/Jo")
    assert r1.status_code == 200
    assert r2.status_code == 200
    ct1 = r1.headers.get("content-type", "")
    ct2 = r2.headers.get("content-type", "")
    assert ct1.startswith("application/json"), f"unexpected content-type: {ct1!r}"
    assert ct2.startswith("application/json"), f"unexpected content-type: {ct2!r}"


# ---------------------------------------------------------------------------
# AC 7 — Stateless / idempotent responses
# ---------------------------------------------------------------------------
def test_ac7_stateless_idempotent_responses():
    a1 = client.get("/hello")
    a2 = client.get("/hello")
    assert a1.status_code == a2.status_code == 200
    assert a1.json() == a2.json() == {"message": "Hello, World!"}

    b1 = client.get("/hello/John")
    b2 = client.get("/hello/John")
    assert b1.status_code == b2.status_code == 200
    assert b1.json() == b2.json() == {"message": "Hello, John!"}

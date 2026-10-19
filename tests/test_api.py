"""API behaviour tests.

ONE example is written for you. Replace each `assert False` TODO with a real test.
Use the helpers from conftest:  login(client, user, pw) -> token,  auth(token) -> header.
Ask for the `client` fixture by adding it as a parameter (it gives you a fresh DB each time).

Run the suite:   pytest -q
Run one file:    pytest tests/test_api.py -q
"""
from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


# ----- TODO 1 -------------------------------------------------------------
def test_register_then_login(client):
    # Register a new user, then log in as that user.
    # Assert login returns 200 AND the access_token looks like a JWT
    # (three dot-separated parts: token.count(".") == 2).
    res_reg = client.post("/register", json={"username": "charlie", "password": "charliepass"})
    assert res_reg.status_code == 200

    res_login = client.post("/login", json={"username": "charlie", "password": "charliepass"})
    assert res_login.status_code == 200
    token = res_login.json().get("access_token")
    assert token is not None
    assert token.count(".") == 2


# ----- TODO 2 -------------------------------------------------------------
def test_login_wrong_password_is_401(client):
    # Log in as 'alice' with the WRONG password. Assert the status code is 401.
    res = client.post("/login", json={"username": "alice", "password": "wrongpassword"})
    assert res.status_code == 401


# ----- TODO 3 -------------------------------------------------------------
def test_create_then_list_own_note(client):
    # Log in as alice, POST a new note, then GET /notes and assert the new
    # note's title appears in the list.
    token = login(client, "alice", "alicepass")
    assert token is not None

    res_post = client.post(
        "/notes",
        headers=auth(token),
        json={"title": "Alice's New Note", "body": "Top secret content"},
    )
    assert res_post.status_code == 200

    res_list = client.get("/notes", headers=auth(token))
    assert res_list.status_code == 200
    titles = [note["title"] for note in res_list.json()]
    assert "Alice's New Note" in titles

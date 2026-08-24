"""End-to-end API tests (register -> login -> item CRUD)."""

from app.core.security import create_access_token


def _auth_header(email: str) -> dict[str, str]:
    token = create_access_token(subject=email)
    return {"Authorization": f"Bearer {token}"}


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_register_login_and_item_crud(client):
    # Register
    r = client.post(
        "/api/v1/users",
        json={"email": "alice@example.com", "password": "secret123", "full_name": "Alice"},
    )
    assert r.status_code == 201, r.text
    user = r.json()
    assert user["email"] == "alice@example.com"

    # Login (OAuth2 form)
    r = client.post(
        "/api/v1/auth/login",
        data={"username": "alice@example.com", "password": "secret123"},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # /auth/me
    r = client.get("/api/v1/auth/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["email"] == "alice@example.com"

    # Create item
    r = client.post(
        "/api/v1/items",
        headers=headers,
        json={"title": "Widget", "description": "A useful widget", "price": 9.99},
    )
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["title"] == "Widget"
    assert item["owner_id"] == user["id"]

    # List items
    r = client.get("/api/v1/items", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1

    # Update item
    r = client.patch(
        f"/api/v1/items/{item['id']}", headers=headers, json={"price": 19.99}
    )
    assert r.status_code == 200
    assert r.json()["price"] == 19.99

    # Delete item
    r = client.delete(f"/api/v1/items/{item['id']}", headers=headers)
    assert r.status_code == 204
    r = client.get("/api/v1/items", headers=headers)
    assert r.json() == []


def test_login_wrong_password(client):
    client.post(
        "/api/v1/users",
        json={"email": "bob@example.com", "password": "rightpass"},
    )
    r = client.post(
        "/api/v1/auth/login",
        data={"username": "bob@example.com", "password": "wrongpass"},
    )
    assert r.status_code == 401

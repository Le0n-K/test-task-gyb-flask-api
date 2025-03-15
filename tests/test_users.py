import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import json
from app import create_app
from app.database import db


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_create_user(client):
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = client.post(
        "/users",
        data=json.dumps(user_data),
        content_type="application/json"
    )
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_email(client):
    user_data = {
        "name": "Test User",
        "email": "duplicate@example.com"
    }
    
    client.post(
        "/users",
        data=json.dumps(user_data),
        content_type="application/json"
    )
    response = client.post(
        "/users",
        data=json.dumps(user_data),
        content_type="application/json"
    )
    assert response.status_code in [400, 409]
    data = json.loads(response.data)
    assert "email" in str(data).lower() or "exists" in str(data).lower()


def test_create_user_missing_fields(client):
    user_data = {
        "name": "Test User"
    }
    response = client.post(
        "/users",
        data=json.dumps(user_data),
        content_type="application/json"
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "email" in str(data).lower() or "required" in str(data).lower()


def test_get_users(client):
    users = [
        {"name": "User 1", "email": "user1@example.com"},
        {"name": "User 2", "email": "user2@example.com"}
    ]
    
    for user in users:
        client.post(
            "/users",
            data=json.dumps(user),
            content_type="application/json"
        )
    response = client.get("/users")
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 2
    
    emails = [user["email"] for user in data]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails


def test_get_user(client):
    user_data = {
        "name": "Get Test User",
        "email": "get_test@example.com"
    }
    
    response = client.post(
        "/users",
        data=json.dumps(user_data),
        content_type="application/json"
    )
    user_id = json.loads(response.data)["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data["id"] == user_id
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]


def test_get_nonexistent_user(client):
    response = client.get("/users/9999")
    assert response.status_code == 404


def test_update_user(client):
    user_data = {
        "name": "Update Test User",
        "email": "update_test@example.com"
    }
    
    response = client.post(
        "/users",
        data=json.dumps(user_data),
        content_type="application/json"
    )
    
    user_id = json.loads(response.data)["id"]

    update_data = {
        "name": "Updated User",
        "email": "updated@example.com"
    }
    response = client.put(
        f"/users/{user_id}",
        data=json.dumps(update_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data["id"] == user_id
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]
    
    response = client.get(f"/users/{user_id}")
    data = json.loads(response.data)
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]


def test_update_user_duplicate_email(client):
    client.post(
        "/users",
        data=json.dumps({"name": "User 1", "email": "existing@example.com"}),
        content_type="application/json"
    )
    
    response = client.post(
        "/users",
        data=json.dumps({"name": "User 2", "email": "user2@example.com"}),
        content_type="application/json"
    )
    
    user_id = json.loads(response.data)["id"]
    response = client.put(
        f"/users/{user_id}",
        data=json.dumps({"email": "existing@example.com"}),
        content_type="application/json"
    )
    assert response.status_code in [400, 409]

    data = json.loads(response.data)
    assert "email" in str(data).lower() or "exists" in str(data).lower()


def test_update_nonexistent_user(client):
    response = client.put(
        "/users/9999",
        data=json.dumps({"name": "Nonexistent User"}),
        content_type="application/json"
    )
    assert response.status_code == 404


def test_delete_user(client):
    user_data = {
        "name": "Delete Test User",
        "email": "delete_test@example.com"
    }
    
    response = client.post(
        "/users",
        data=json.dumps(user_data),
        content_type="application/json"
    )
    
    user_id = json.loads(response.data)["id"]
    
    response = client.delete(f"/users/{user_id}")
    assert response.status_code in [200, 204]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404


def test_delete_nonexistent_user(client):
    response = client.delete("/users/9999")
    assert response.status_code == 404

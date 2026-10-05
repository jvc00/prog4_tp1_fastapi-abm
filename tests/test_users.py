import pytest
from fastapi.testclient import TestClient

from main import app
from models.users import User
from routers import users

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_data():
    # Datos iniciales limpios antes de cada test
    users.usuarios[:] = [
        User(id=1, name="juan perez"),
        User(id=2, name="pepe sanchez", is_active=False),
    ]


def test_list_all():
    r = client.get("/users")
    assert r.status_code == 200
    assert len(r.json()["users"]) == 2


@pytest.mark.parametrize("valor,esperado", [("true", [1]), ("false", [2])])
def test_filter_by_active(valor, esperado):
    r = client.get("/users", params={"is_active": valor})
    assert [u["id"] for u in r.json()["users"]] == esperado


def test_get_by_id_and_404():
    assert client.get("/users/1").json()["name"] == "juan perez"
    assert client.get("/users/99").status_code == 404


def test_create_and_duplicate():
    nuevo = {"id": 3, "name": "ana"}
    assert client.post("/users", json=nuevo).status_code == 201
    assert client.post("/users", json=nuevo).status_code == 409


def test_put_replaces_whole_user():
    r = client.put("/users/1", json={"name": "juan", "is_active": False})
    assert r.status_code == 200
    assert r.json() == {"id": 1, "name": "juan", "is_active": False}


def test_put_requires_all_fields():
    r = client.put("/users/1", json={"name": "juan"})
    assert r.status_code == 422


def test_patch_changes_only_sent_fields():
    r = client.patch("/users/1", json={"is_active": False})
    assert r.json() == {"id": 1, "name": "juan perez", "is_active": False}


def test_patch_and_put_404():
    assert client.patch("/users/99", json={"name": "x"}).status_code == 404
    body = {"name": "x", "is_active": True}
    assert client.put("/users/99", json=body).status_code == 404


def test_delete():
    assert client.delete("/users/1").status_code == 200
    assert client.get("/users/1").status_code == 404
    assert client.delete("/users/1").status_code == 404

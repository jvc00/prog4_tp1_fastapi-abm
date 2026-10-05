from datetime import date

import pytest
from fastapi.testclient import TestClient

from main import app
from models.movies import Genre, Movie
from routers import movies

client = TestClient(app)

NUEVA = {"id": 10, "title": "Alien", "director": "Ridley Scott",
         "genre": "terror", "year": 1979}


@pytest.fixture(autouse=True)
def reset_data():
    # Datos iniciales limpios antes de cada test
    movies.peliculas[:] = [
        Movie(id=1, title="El Padrino", director="Francis Ford Coppola",
              genre=Genre.DRAMA, year=1972),
        Movie(id=2, title="Metropolis", director="Fritz Lang",
              genre=Genre.CIENCIA_FICCION, year=1927),
        Movie(id=3, title="Pulp Fiction", director="Quentin Tarantino",
              genre=Genre.DRAMA, year=1994),
    ]


def ids(response):
    return [m["id"] for m in response.json()["movies"]]


def test_list_all():
    assert ids(client.get("/movies")) == [1, 2, 3]


@pytest.mark.parametrize("params,esperado", [
    ({"genre": "drama"}, [1, 3]),
    ({"genre": "ciencia_ficcion"}, [2]),
    ({"director": "lang"}, [2]),
    ({"year": 1994}, [3]),
    ({"genre": "drama", "year": 1972}, [1]),   # filtros combinados
    ({"genre": "terror"}, []),
])
def test_filters(params, esperado):
    assert ids(client.get("/movies", params=params)) == esperado


def test_invalid_genre_rejected():
    assert client.get("/movies", params={"genre": "xyz"}).status_code == 422
    r = client.post("/movies", json={**NUEVA, "genre": "xyz"})
    assert r.status_code == 422


def test_get_by_id_and_404():
    assert client.get("/movies/2").json()["title"] == "Metropolis"
    assert client.get("/movies/99").status_code == 404


def test_create_and_duplicate():
    assert client.post("/movies", json=NUEVA).status_code == 201
    assert client.post("/movies", json=NUEVA).status_code == 409


@pytest.mark.parametrize("year,status", [
    (1888, 201),                      # límite mínimo
    (1887, 422),                      # antes del cine
    (date.today().year, 201),         # límite máximo
    (date.today().year + 1, 422),     # futuro
])
def test_year_limits(year, status):
    r = client.post("/movies", json={**NUEVA, "year": year})
    assert r.status_code == status


def test_empty_text_rejected():
    assert client.post("/movies", json={**NUEVA, "title": "  "}
                       ).status_code == 422


def test_put_replaces_whole_movie():
    cuerpo = {k: v for k, v in NUEVA.items() if k != "id"}
    r = client.put("/movies/1", json=cuerpo)
    assert r.json() == {**NUEVA, "id": 1}


def test_put_requires_all_fields():
    assert client.put("/movies/1", json={"title": "X"}).status_code == 422


def test_patch_changes_only_sent_fields():
    r = client.patch("/movies/1", json={"genre": "crimen"})
    assert r.json()["genre"] == "crimen"
    assert r.json()["title"] == "El Padrino"


def test_patch_validates_year():
    r = client.patch("/movies/1", json={"year": 1700})
    assert r.status_code == 422


def test_patch_and_put_404():
    r = client.patch("/movies/99", json={"genre": "drama"})
    assert r.status_code == 404
    cuerpo = {k: v for k, v in NUEVA.items() if k != "id"}
    assert client.put("/movies/99", json=cuerpo).status_code == 404


def test_delete():
    assert client.delete("/movies/1").status_code == 200
    assert client.get("/movies/1").status_code == 404
    assert client.delete("/movies/1").status_code == 404

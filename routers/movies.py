from fastapi import APIRouter, HTTPException, status
from models.movies import (
    Genre,
    Movie,
    MovieUpdate,
    MoviePatch,
    GetMoviesResponse,
    CreateMovieResponse,
    DeleteMovieResponse,
)

router = APIRouter(tags=["Movies"])

peliculas: list[Movie] = [
    Movie(id=1, title="El Padrino", director="Francis Ford Coppola",
          genre=Genre.DRAMA, year=1972),
    Movie(id=2, title="Metropolis", director="Fritz Lang",
          genre=Genre.CIENCIA_FICCION, year=1927),
    Movie(id=3, title="Pulp Fiction", director="Quentin Tarantino",
          genre=Genre.CRIMEN, year=1994),
]


def _find_movie(id: int) -> Movie:
    """Devuelve la película o responde 404 si no existe."""
    for movie in peliculas:
        if movie.id == id:
            return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Película no encontrada"
    )


# Filtros opcionales y combinables (se aplican todos los enviados)
@router.get("/movies")
def get_movies(
    genre: Genre | None = None,
    director: str | None = None,
    year: int | None = None,
) -> GetMoviesResponse:
    resultado = peliculas

    if genre is not None:
        resultado = [m for m in resultado if m.genre == genre]
    if director is not None:  # coincidencia parcial
        resultado = [m for m in resultado
                     if director.lower() in m.director.lower()]
    if year is not None:
        resultado = [m for m in resultado if m.year == year]

    return GetMoviesResponse(movies=resultado)


@router.get("/movies/{id}")
def get_movie(id: int) -> Movie:
    return _find_movie(id)


@router.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> CreateMovieResponse:
    # 409 si el id ya existe
    if any(m.id == movie.id for m in peliculas):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una película con ese id"
        )

    peliculas.append(movie)
    return CreateMovieResponse(message="película creada")


# PUT: reemplaza la película completa (el id viene de la URL)
@router.put("/movies/{id}")
def replace_movie(id: int, datos: MovieUpdate) -> Movie:
    actual = _find_movie(id)
    nueva = Movie(id=id, **datos.model_dump())
    peliculas[peliculas.index(actual)] = nueva
    return nueva


# PATCH: cambia solo los campos enviados
@router.patch("/movies/{id}")
def patch_movie(id: int, cambios: MoviePatch) -> Movie:
    actual = _find_movie(id)
    datos = cambios.model_dump(exclude_unset=True, exclude_none=True)
    nueva = Movie.model_validate({**actual.model_dump(), **datos})
    peliculas[peliculas.index(actual)] = nueva
    return nueva


@router.delete("/movies/{id}")
def delete_movie(id: int) -> DeleteMovieResponse:
    peliculas.remove(_find_movie(id))
    return DeleteMovieResponse(message="película borrada")

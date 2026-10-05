from datetime import date
from enum import StrEnum
from typing import Annotated, List

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
)

# Primera película de la historia: 1888
MIN_YEAR = 1888


def _check_not_future(year: int) -> int:
    # El máximo se calcula al validar, así no queda desactualizado
    if year > date.today().year:
        raise ValueError("el año no puede ser futuro")
    return year


class Genre(StrEnum):
    """Géneros permitidos (lista cerrada, se ve como desplegable en /docs)."""
    ACCION = "accion"
    ANIMACION = "animacion"
    AVENTURA = "aventura"
    CIENCIA_FICCION = "ciencia_ficcion"
    COMEDIA = "comedia"
    CRIMEN = "crimen"
    DOCUMENTAL = "documental"
    DRAMA = "drama"
    FANTASIA = "fantasia"
    MUSICAL = "musical"
    ROMANCE = "romance"
    SUSPENSO = "suspenso"
    TERROR = "terror"
    WESTERN = "western"


Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Year = Annotated[int, Field(ge=MIN_YEAR), AfterValidator(_check_not_future)]


class Movie(BaseModel):
    # Ejemplo que /docs precarga en el body
    model_config = ConfigDict(json_schema_extra={
        "examples": [{"id": 10, "title": "Alien",
                      "director": "Ridley Scott",
                      "genre": "terror", "year": 1979}]
    })

    id: int = Field(gt=0)
    title: Text
    director: Text
    genre: Genre
    year: Year


class MovieUpdate(BaseModel):
    """Body de PUT: reemplazo completo, todos obligatorios."""
    # Ejemplo que /docs precarga en el body
    model_config = ConfigDict(json_schema_extra={
        "examples": [{"title": "Alien", "director": "Ridley Scott",
                      "genre": "terror", "year": 1979}]
    })

    title: Text
    director: Text
    genre: Genre
    year: Year


class MoviePatch(BaseModel):
    """Body de PATCH: todos opcionales, solo se cambia lo enviado."""
    # Ejemplo que /docs precarga en el body
    model_config = ConfigDict(json_schema_extra={
        "examples": [{"genre": "suspenso"}]
    })

    title: Text | None = None
    director: Text | None = None
    genre: Genre | None = None
    year: Year | None = None


class GetMoviesResponse(BaseModel):
    movies: List[Movie]


class CreateMovieResponse(BaseModel):
    message: str


class DeleteMovieResponse(BaseModel):
    message: str

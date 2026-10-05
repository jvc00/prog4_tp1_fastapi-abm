from pydantic import BaseModel, ConfigDict, Field
from typing import List


class User(BaseModel):
    # Ejemplo que /docs precarga en el body
    model_config = ConfigDict(json_schema_extra={
        "examples": [{"id": 3, "name": "ana", "is_active": True}]
    })

    id: int
    name: str = Field(min_length=1)
    is_active: bool = True  # default value, field becomes optional


class UserUpdate(BaseModel):
    """Body de PUT: reemplazo completo, todos los campos obligatorios."""
    # Ejemplo que /docs precarga en el body
    model_config = ConfigDict(json_schema_extra={
        "examples": [{"name": "ana maria", "is_active": True}]
    })

    name: str = Field(min_length=1)
    is_active: bool


class UserPatch(BaseModel):
    """Body de PATCH: todos opcionales, solo se cambia lo enviado."""
    # Ejemplo que /docs precarga en el body
    model_config = ConfigDict(json_schema_extra={
        "examples": [{"is_active": False}]
    })

    name: str | None = Field(default=None, min_length=1)
    is_active: bool | None = None


class GetUsersResponse(BaseModel):
    users: List[User]


class CreateUserResponse(BaseModel):
    message: str


class DeleteUserResponse(BaseModel):
    message: str

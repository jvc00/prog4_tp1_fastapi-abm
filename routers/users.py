from fastapi import APIRouter, HTTPException, status
from models.users import (
    User,
    UserUpdate,
    UserPatch,
    GetUsersResponse,
    CreateUserResponse,
    DeleteUserResponse,
)

router = APIRouter(tags=["Users"])

usuarios: list[User] = [
    User(id=1, name="juan perez"),
    User(id=2, name="pepe sanchez"),
]


def _find_user(id: int) -> User:
    """Devuelve el usuario o responde 404 si no existe."""
    for user in usuarios:
        if user.id == id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


# is_active: True = activos, False = inactivos, sin valor = todos
@router.get("/users")
def get_users(is_active: bool | None = None) -> GetUsersResponse:
    if is_active is None:
        return GetUsersResponse(users=usuarios)

    filtrados = [u for u in usuarios if u.is_active == is_active]
    return GetUsersResponse(users=filtrados)


@router.get("/users/{id}")
def get_user(id: int) -> User:
    return _find_user(id)


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User) -> CreateUserResponse:
    # 409 si el id ya existe
    if any(u.id == user.id for u in usuarios):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese id"
        )

    usuarios.append(user)
    return CreateUserResponse(message="usuario creado")


# PUT: reemplaza el usuario completo (el id viene de la URL)
@router.put("/users/{id}")
def replace_user(id: int, datos: UserUpdate) -> User:
    actual = _find_user(id)
    nuevo = User(id=id, **datos.model_dump())
    usuarios[usuarios.index(actual)] = nuevo
    return nuevo


# PATCH: cambia solo los campos enviados
@router.patch("/users/{id}")
def patch_user(id: int, cambios: UserPatch) -> User:
    actual = _find_user(id)
    # exclude_unset: ignora lo no enviado; exclude_none: ignora nulls
    datos = cambios.model_dump(exclude_unset=True, exclude_none=True)
    nuevo = User.model_validate({**actual.model_dump(), **datos})
    usuarios[usuarios.index(actual)] = nuevo
    return nuevo


@router.delete("/users/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    usuarios.remove(_find_user(id))
    return DeleteUserResponse(message="usuario borrado")

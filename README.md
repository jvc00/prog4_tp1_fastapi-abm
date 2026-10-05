# Clase FastAPI

Clase para aprender **FastAPI** y **Pydantic**.

## Crear el entorno virtual (venv)

Desde esta carpeta (`clase-fastapi`):

```bash
python3 -m venv .venv
```

Activar el entorno virtual:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

## Instalar los requerimientos

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación

```bash
fastapi dev main.py
```

La API quedará disponible en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`.

## Estructura

```
clase-fastapi/
├── main.py             # app y registro de routers
├── models/
│   ├── users.py        # modelos Pydantic de Usuario
│   └── movies.py       # modelos Pydantic de Película (+ Enum Genre)
├── routers/
│   ├── users.py        # endpoints de Usuario
│   └── movies.py       # endpoints de Película
└── tests/              # tests con pytest
```

El almacenamiento es **en memoria** (listas): los datos se pierden al reiniciar.

## Endpoints

### Usuarios (`/users`)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/users` | Lista usuarios. Filtro opcional `?is_active=true\|false` (sin filtro: todos) |
| `GET` | `/users/{id}` | Obtiene un usuario |
| `POST` | `/users` | Crea un usuario (`201`; `409` si el id existe) |
| `PUT` | `/users/{id}` | Reemplaza el usuario completo |
| `PATCH` | `/users/{id}` | Modifica solo los campos enviados |
| `DELETE` | `/users/{id}` | Elimina un usuario |

### Películas (`/movies`)

Campos: `id`, `title`, `director`, `genre`, `year`.

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/movies` | Lista películas. Filtros opcionales y combinables: `genre`, `director`, `year` |
| `GET` | `/movies/{id}` | Obtiene una película |
| `POST` | `/movies` | Crea una película (`201`; `409` si el id existe) |
| `PUT` | `/movies/{id}` | Reemplaza la película completa |
| `PATCH` | `/movies/{id}` | Modifica solo los campos enviados |
| `DELETE` | `/movies/{id}` | Elimina una película |

Ejemplo: `GET /movies?genre=drama&director=coppola&year=1972`

**Validaciones de película**
- `genre` debe ser uno de los valores de `Genre` (por ejemplo `drama`, `terror`, `ciencia_ficcion`); se ve como desplegable en `/docs`.
- `year` entre 1888 y el año actual.
- `title`, `director` no pueden estar vacíos.
- `director` en el filtro busca coincidencia parcial sin distinguir mayúsculas.

### PUT vs PATCH

- **PUT** reemplaza el recurso: hay que enviar todos los campos.
- **PATCH** modifica solo los campos enviados; el resto queda igual.

## Tests

```bash
pytest
```

`pytest` ya se instala con `requirements.txt`.

## Lint y chequeo de tipos

El proyecto incluye configuración local para dos herramientas:

- **[`setup.cfg`](./setup.cfg)**: configuración de [`pycodestyle`](https://pycodestyle.pycqa.org/) (chequeo de estilo PEP 8). Define `max-line-length = 130` y excluye `.venv` y `__pycache__` del análisis.
- **[`pyrightconfig.json`](./pyrightconfig.json)**: configuración de [`pyright`](https://microsoft.github.io/pyright/) (chequeo de tipos). Apunta al entorno virtual local (`.venv`) para resolver las dependencias instaladas y excluye `.venv` y `__pycache__`.

`pyright` ya está incluido en `requirements.txt`. `pycodestyle` no, así que hay que instalarlo aparte.

Con el entorno virtual activado, correr:

```bash
pip install pycodestyle
python -m pycodestyle .
```

```bash
pyright
```

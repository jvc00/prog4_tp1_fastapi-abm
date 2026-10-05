from fastapi import FastAPI
from routers import users, movies

# Create the application instance
app = FastAPI()

# Routers to user and movie endpoints
app.include_router(users.router)
app.include_router(movies.router)


# Define a GET route for the root URL
@app.get("/", tags=["Root"])
def read_root():
    mensaje = "Primer clase de FastAPI, ahora primer tp de prog4. Entidad elegida: películas"
    return {"message": mensaje}

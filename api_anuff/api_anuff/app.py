from fastapi import FastAPI

from routers.usuarios import router as usuarios_router

app = FastAPI()

# Registrar as rotas de usuários
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuários"])


@app.get("/", response_model=dict)
def read_root():
    return {"message": "Olá mundo!"}

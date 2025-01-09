from fastapi import FastAPI

from routers.usuarios import router as usuarios_router
from routers.anuncios import router as anuncios_router
from routers.login import router as login_router

app = FastAPI()

# Registrar as rotas de usuários
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuários"])
app.include_router(anuncios_router, prefix="/anuncios", tags=["Anúncios"])
app.include_router(login_router, prefix="/login", tags=["Login"])

@app.get("/", response_model=dict)
def read_root():
    return {"message": "Olá mundo!"}

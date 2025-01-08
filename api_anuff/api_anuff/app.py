from fastapi import FastAPI

from routers.usuarios import router as usuarios_router
from routers.anuncios import router as anuncios_router
from routers.chats import router as chats_router
from routers.mensagens import router as mensagens_router
from routers.avaliacoes import router as avaliacoes_router

app = FastAPI()

# Registrar as rotas de usuários
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuários"])
app.include_router(anuncios_router, prefix="/anuncios", tags=["Anúncios"])
app.include_router(chats_router, prefix="/chats", tags=["Chats"])
app.include_router(mensagens_router, prefix="/mensagens", tags=["Mensagens"])
app.include_router(avaliacoes_router, prefix="/avaliacoes", tags=["Avaliações"])



@app.get("/", response_model=dict)
def read_root():
    return {"message": "Olá mundo!"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.usuarios import router as usuarios_router
from routers.anuncios import router as anuncios_router
from routers.chats import router as chats_router
from routers.mensagens import router as mensagens_router
from routers.avaliacoes import router as avaliacoes_router
from routers.login import router as login_router
from database import create_db_and_tables


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    #criar as tabelas relacionadas aos modelos
    create_db_and_tables()

# Registrar as rotas de usuários
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuários"])
app.include_router(anuncios_router, prefix="/anuncios", tags=["Anúncios"])
app.include_router(chats_router, prefix="/chats", tags=["Chats"])
app.include_router(mensagens_router, prefix="/mensagens", tags=["Mensagens"])
app.include_router(avaliacoes_router, prefix="/avaliacoes", tags=["Avaliações"])
app.include_router(login_router, prefix="/login", tags=["Login"])


@app.get("/", response_model=dict)
def read_root():
    return {"message": "Olá mundo!"}

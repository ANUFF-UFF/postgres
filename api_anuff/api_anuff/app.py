from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from typing import List

from api_anuff.api_anuff.schemas import Message, UsuarioBase, UsuarioRead

app = FastAPI()

# Simulação do "banco de dados" em memória
database = []
current_id = 1


# Funções auxiliares
def get_usuario_by_id(usuario_id: int):
    for usuario in database:
        if usuario['id'] == usuario_id:
            return usuario
    return None

# Rotas para a entidade Usuario
@app.post("/usuarios/", status_code=HTTPStatus.CREATED, response_model=UsuarioRead)
def criar_usuario(usuario: UsuarioBase):
    global current_id
    novo_usuario = usuario.dict()
    novo_usuario['id'] = current_id
    current_id += 1
    database.append(novo_usuario)
    return novo_usuario


@app.get("/usuarios/", status_code=HTTPStatus.OK, response_model=List[UsuarioRead])
def listar_usuarios():
    return database


@app.get("/usuarios/{usuario_id}", status_code=HTTPStatus.OK, response_model=UsuarioRead)
def obter_usuario(usuario_id: int):
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    return usuario


@app.put("/usuarios/{usuario_id}", status_code=HTTPStatus.OK, response_model=UsuarioRead)
def atualizar_usuario(usuario_id: int, usuario: UsuarioBase):
    existente = get_usuario_by_id(usuario_id)
    if not existente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    # Atualizar o usuário
    existente.update(usuario.dict())
    return existente


@app.delete("/usuarios/{usuario_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_usuario(usuario_id: int):
    global database
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    # Remove o usuário do "banco de dados"
    database = [u for u in database if u['id'] != usuario_id]
    return

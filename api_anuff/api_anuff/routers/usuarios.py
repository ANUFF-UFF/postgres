from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List

from api_anuff.schemas import UsuarioBase, UsuarioRead

router = APIRouter()

# Simulação do "banco de dados" em memória
database = []
current_id = 1


# Funções auxiliares
def get_usuario_by_id(usuario_id: int):
    for usuario in database:
        if usuario['id'] == usuario_id:
            return usuario
    return None


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UsuarioRead)
def criar_usuario(usuario: UsuarioBase):
    global current_id
    novo_usuario = usuario.dict()
    novo_usuario["id"] = current_id
    current_id += 1
    database.append(novo_usuario)
    return novo_usuario


@router.get("/", status_code=HTTPStatus.OK, response_model=List[UsuarioRead])
def listar_usuarios():
    return database


@router.get("/{usuario_id}", status_code=HTTPStatus.OK, response_model=UsuarioRead)
def obter_usuario(usuario_id: int):
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    return usuario


@router.put("/{usuario_id}", status_code=HTTPStatus.OK, response_model=UsuarioRead)
def atualizar_usuario(usuario_id: int, usuario: UsuarioBase):
    existente = get_usuario_by_id(usuario_id)
    if not existente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    existente.update(usuario.dict())
    return existente


@router.delete("/{usuario_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_usuario(usuario_id: int):
    global database
    usuario = get_usuario_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    database = [u for u in database if u['id'] != usuario_id]
    return

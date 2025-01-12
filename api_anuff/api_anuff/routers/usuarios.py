from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List
from sqlmodel import select

from database import SessionDep, try_block
from api_anuff.schemas import UsuarioBase, UsuarioRead  # Usuario não existe aqui

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UsuarioRead)
def criar_usuario(usuario: UsuarioBase, session: SessionDep):
    """
    Adiciona um novo usuário ao banco de dados.
    """
    def inner():
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

    return try_block(session, inner)


@router.get("/", status_code=HTTPStatus.OK, response_model=List[UsuarioRead])
def listar_usuarios(session: SessionDep):
    """
    Retorna a lista de todos os usuários cadastrados no banco de dados.
    """
    def inner():
        return session.exec(select(UsuarioBase)).all()

    return try_block(session, inner)


@router.get("/{usuario_id}", status_code=HTTPStatus.OK, response_model=UsuarioRead)
def obter_usuario(usuario_id: int, session: SessionDep):
    """
    Recupera os detalhes de um usuário específico pelo ID.
    """
    def inner():
        usuario = session.exec(select(UsuarioBase).where(UsuarioBase.id == usuario_id)).first()
        if not usuario:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
        return usuario

    return try_block(session, inner)


@router.put("/{usuario_id}", status_code=HTTPStatus.OK, response_model=UsuarioRead)
def atualizar_usuario(usuario_id: int, usuario: UsuarioBase, session: SessionDep):
    """
    Atualiza os dados de um usuário no banco de dados, removendo o registro antigo e adicionando um novo.
    """
    def inner():
        existente = session.exec(select(UsuarioBase).where(UsuarioBase.id == usuario_id)).first()
        if not existente:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
        session.delete(existente)
        session.commit()
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

    return try_block(session, inner)


@router.delete("/{usuario_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_usuario(usuario_id: int, session: SessionDep):
    """
    Remove um usuário do banco de dados pelo ID.
    """
    def inner():
        usuario = session.exec(select(UsuarioBase).where(UsuarioBase.id == usuario_id)).first()
        if not usuario:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
        session.delete(usuario)
        session.commit()

    return try_block(session, inner)

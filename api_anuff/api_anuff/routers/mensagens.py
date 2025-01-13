from fastapi import APIRouter, HTTPException, Query
from http import HTTPStatus
from typing import List
from sqlmodel import select

from database import SessionDep, try_block
from api_anuff.schemas import MensagemBase, MensagemRead 

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED, response_model=MensagemRead)
def criar_mensagem(mensagem: MensagemBase, session: SessionDep):
    """
    Cria uma nova mensagem no banco de dados.
    """
    def inner():
        session.add(mensagem)
        session.commit()
        session.refresh(mensagem)
        return mensagem

    return try_block(session, inner)


@router.get("/", status_code=HTTPStatus.OK, response_model=List[MensagemRead])
def listar_mensagens(session: SessionDep):
    """
    Lista todas as mensagens disponíveis no banco de dados.
    """
    def inner():
        return session.exec(select(MensagemBase)).all()

    return try_block(session, inner)


@router.get("/{mensagem_id}", status_code=HTTPStatus.OK, response_model=MensagemRead)
def obter_mensagem(mensagem_id: int, session: SessionDep):
    """
    Obtém uma mensagem pelo ID.
    """
    def inner():
        mensagem = session.exec(select(MensagemBase).where(MensagemBase.id == mensagem_id)).first()
        if not mensagem:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Mensagem não encontrada")
        return mensagem

    return try_block(session, inner)


@router.delete("/{mensagem_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_mensagem(mensagem_id: int, session: SessionDep):
    """
    Deleta uma mensagem pelo ID.
    """
    def inner():
        mensagem = session.exec(select(MensagemBase).where(MensagemBase.id == mensagem_id)).first()
        if not mensagem:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Mensagem não encontrada")
        session.delete(mensagem)
        session.commit()

    return try_block(session, inner)


@router.get("/chats/{chat_id}", status_code=HTTPStatus.OK, response_model=List[MensagemRead])
def listar_mensagens_por_chat(chat_id: int, session: SessionDep):
    """
    Lista todas as mensagens associadas a um chat específico.
    """
    def inner():
        return session.exec(select(MensagemBase).where(MensagemBase.chat_id == chat_id)).all()

    return try_block(session, inner)

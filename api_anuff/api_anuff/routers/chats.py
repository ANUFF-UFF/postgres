from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List
from sqlmodel import select, and_, or_

from api_anuff.schemas import ChatBase, ChatRead
from database import SessionDep, try_block, Session

router = APIRouter()

def get_chat_by_id(session, chat_id: int):
    def inner():
        return session.exec(select(ChatBase).where(
            ChatBase.id == chatd_id
        )).all()
    return try_block(session, inner)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=ChatRead)
def criar_chat(session: SessionDep, chat: ChatBase):
    def inner():
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat
    return try_block(session, inner)


@router.get("/", status_code=HTTPStatus.OK, response_model=List[ChatRead])
def listar_chats(session: SessionDep):
    def inner():
        return session.exec(select(ChatBase)).all()
    return try_block(session, inner)


@router.get("/usuarios", status_code=HTTPStatus.OK, response_model=ChatRead)
def obter_chat_por_usuarios(session: SessionDep, usuario_1_id: int, usuario_2_id: int):
    """
    Obtém um chat com base nos IDs dos dois usuários.
    
    EXEMPLO:
    GET /chats/usuarios?usuario_1_id=1&usuario_2_id=2
    """
    def inner():
        return session(select(ChatBase).where(
            or_(
                and_(
                    ChatBase.usuario_1_id == usuario_1_id,
                    ChatBase.usuario_2_id == usuario_2_id
                ),
                and_(
                    ChatBase.usuario_2_id == usuario_1_id,
                    ChatBase.usuario_1_id == usuario_2_id
                )
            )
        )).all()
    return try_block(session, inner)


@router.get("/{chat_id}", status_code=HTTPStatus.OK, response_model=ChatRead)
def obter_chat(session: SessionDep, chat_id: int):
    def inner():
        chat = get_chat_by_id(session, chat_id)
        if chat is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Chat não encontrado")
        return chat
    return try_block(session, inner)


@router.delete("/{chat_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_chat(session: SessioDep, chat_id: int):
    def inner():
        chat = get_chat_by_id(session, chat_id)
        if chat is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Chat não encontrado")
        return chat
    return try_block(session, inner)



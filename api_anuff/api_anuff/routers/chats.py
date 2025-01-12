from fastapi import APIRouter, HTTPException, Query
from http import HTTPStatus
from typing import List
from sqlmodel import select

from database import SessionDep, try_block
from api_anuff.schemas import ChatBase, ChatRead 

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED, response_model=ChatRead)
def criar_chat(chat: ChatBase, session: SessionDep):
    """
    Cria um novo chat no banco de dados.
    """
    def inner():
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat

    return try_block(session, inner)


@router.get("/", status_code=HTTPStatus.OK, response_model=List[ChatRead])
def listar_chats(session: SessionDep):
    """
    Lista todos os chats disponíveis no banco de dados.
    """
    def inner():
        return session.exec(select(ChatBase)).all()

    return try_block(session, inner)


@router.get("/{chat_id}", status_code=HTTPStatus.OK, response_model=ChatRead)
def obter_chat(chat_id: int, session: SessionDep):
    """
    Obtém um chat pelo ID.
    """
    def inner():
        chat = session.exec(select(ChatBase).where(ChatBase.id == chat_id)).first()
        if not chat:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Chat não encontrado")
        return chat

    return try_block(session, inner)


@router.delete("/{chat_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_chat(chat_id: int, session: SessionDep):
    """
    Deleta um chat pelo ID.
    """
    def inner():
        chat = session.exec(select(ChatBase).where(ChatBase.id == chat_id)).first()
        if not chat:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Chat não encontrado")
        session.delete(chat)
        session.commit()

    return try_block(session, inner)


@router.get("/usuarios", status_code=HTTPStatus.OK, response_model=ChatRead)
def obter_chat_por_usuarios(
    usuario_1_id: int = Query(..., description="ID do primeiro usuário"),
    usuario_2_id: int = Query(..., description="ID do segundo usuário"),
    session: SessionDep = None
):
    """
    Obtém um chat com base nos IDs dos dois usuários.
    
    EXEMPLO:
    GET /chats/usuarios?usuario_1_id=1&usuario_2_id=2
    """
    def inner():
        # Tenta encontrar o chat 
        chat = session.exec(
            select(ChatBase).where(
                (ChatBase.usuario_1_id == usuario_1_id) & (ChatBase.usuario_2_id == usuario_2_id) |
                (ChatBase.usuario_1_id == usuario_2_id) & (ChatBase.usuario_2_id == usuario_1_id)
            )
        ).first()
        
        # Se o chat não existir, cria um novo
        if not chat:
            novo_chat = ChatBase(usuario_1_id=usuario_1_id, usuario_2_id=usuario_2_id)
            session.add(novo_chat)
            session.commit()
            session.refresh(novo_chat)
            return novo_chat
        
        return chat

    return try_block(session, inner)

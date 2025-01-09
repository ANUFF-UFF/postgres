from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List

from api_anuff.schemas import ChatBase, ChatRead

router = APIRouter()

# Simulação do "banco de dados" em memória
chats_database = []
current_chat_id = 1


def get_chat_by_id(chat_id: int):
    for chat in chats_database:
        if chat['id'] == chat_id:
            return chat
    return None


@router.post("/", status_code=HTTPStatus.CREATED, response_model=ChatRead)
def criar_chat(chat: ChatBase):
    global current_chat_id
    novo_chat = chat.dict()
    novo_chat["id"] = current_chat_id
    current_chat_id += 1
    chats_database.append(novo_chat)
    return novo_chat


@router.get("/", status_code=HTTPStatus.OK, response_model=List[ChatRead])
def listar_chats():
    return chats_database


@router.get("/{chat_id}", status_code=HTTPStatus.OK, response_model=ChatRead)
def obter_chat(chat_id: int):
    chat = get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Chat não encontrado")
    return chat


@router.delete("/{chat_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_chat(chat_id: int):
    global chats_database
    chat = get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Chat não encontrado")
    chats_database = [c for c in chats_database if c['id'] != chat_id]
    return

@router.get("/usuarios", status_code=HTTPStatus.OK, response_model=ChatRead)
def obter_chat_por_usuarios(usuario_1_id: int, usuario_2_id: int):
    """
    Obtém um chat com base nos IDs dos dois usuários.
    
    EXEMPLO:
    GET /chats/usuarios?usuario_1_id=1&usuario_2_id=2
    """
    for chat in chats_database:
        if (chat['usuario_1_id'] == usuario_1_id and chat['usuario_2_id'] == usuario_2_id) or \
           (chat['usuario_1_id'] == usuario_2_id and chat['usuario_2_id'] == usuario_1_id):
            return chat
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Chat entre os usuários não encontrado")

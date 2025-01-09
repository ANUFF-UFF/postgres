from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List

from api_anuff.schemas import MensagemBase, MensagemRead

router = APIRouter()

# Simulação do "banco de dados" em memória
mensagens_database = []
current_mensagem_id = 1


def get_mensagem_by_id(mensagem_id: int):
    for mensagem in mensagens_database:
        if mensagem['id'] == mensagem_id:
            return mensagem
    return None


@router.post("/", status_code=HTTPStatus.CREATED, response_model=MensagemRead)
def criar_mensagem(mensagem: MensagemBase):
    global current_mensagem_id
    nova_mensagem = mensagem.dict()
    nova_mensagem["id"] = current_mensagem_id
    current_mensagem_id += 1
    mensagens_database.append(nova_mensagem)
    return nova_mensagem


@router.get("/", status_code=HTTPStatus.OK, response_model=List[MensagemRead])
def listar_mensagens():
    return mensagens_database


@router.get("/{mensagem_id}", status_code=HTTPStatus.OK, response_model=MensagemRead)
def obter_mensagem(mensagem_id: int):
    mensagem = get_mensagem_by_id(mensagem_id)
    if not mensagem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Mensagem não encontrada")
    return mensagem


@router.delete("/{mensagem_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_mensagem(mensagem_id: int):
    global mensagens_database
    mensagem = get_mensagem_by_id(mensagem_id)
    if not mensagem:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Mensagem não encontrada")
    mensagens_database = [m for m in mensagens_database if m['id'] != mensagem_id]
    return

@router.get("/chat/{chat_id}", status_code=HTTPStatus.OK, response_model=List[MensagemRead])
def listar_mensagens_por_chat(chat_id: int):
    """
    Obtém todas as mensagens de um chat específico pelo chat_id.
    EXEMPLO:
    GET /mensagens/chat/{chat_id}
    """
    mensagens_chat = [mensagem for mensagem in mensagens_database if mensagem['chat_id'] == chat_id]
    if not mensagens_chat:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Nenhuma mensagem encontrada para este chat")
    return mensagens_chat
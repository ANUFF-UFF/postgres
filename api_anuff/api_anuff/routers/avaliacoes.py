from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List

from api_anuff.schemas import AvaliacaoBase, AvaliacaoCreate, AvaliacaoRead

router = APIRouter()

# Simulação do "banco de dados" em memória
avaliacoes_database = []
current_avaliacao_id = 1


# Funções auxiliares
def get_avaliacao_by_id(avaliacao_id: int):
    for avaliacao in avaliacoes_database:
        if avaliacao["id"] == avaliacao_id:
            return avaliacao
    return None


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AvaliacaoRead)
def criar_avaliacao(avaliacao: AvaliacaoCreate):
    global current_avaliacao_id
    nova_avaliacao = avaliacao.dict()
    nova_avaliacao["id"] = current_avaliacao_id
    current_avaliacao_id += 1

    # Verificar se o autor já avaliou o anúncio
    for a in avaliacoes_database:
        if a["autor"] == avaliacao.autor and a["anuncio"] == avaliacao.anuncio:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="O autor já avaliou este anúncio."
            )

    avaliacoes_database.append(nova_avaliacao)
    return nova_avaliacao


@router.get("/", status_code=HTTPStatus.OK, response_model=List[AvaliacaoRead])
def listar_avaliacoes():
    return avaliacoes_database


@router.get("/{avaliacao_id}", status_code=HTTPStatus.OK, response_model=AvaliacaoRead)
def obter_avaliacao(avaliacao_id: int):
    avaliacao = get_avaliacao_by_id(avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Avaliação não encontrada")
    return avaliacao


@router.delete("/{avaliacao_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_avaliacao(avaliacao_id: int):
    global avaliacoes_database
    avaliacao = get_avaliacao_by_id(avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Avaliação não encontrada")
    avaliacoes_database = [a for a in avaliacoes_database if a["id"] != avaliacao_id]
    return

@router.get("/anuncio/{anuncio_id}", status_code=HTTPStatus.OK, response_model=List[AvaliacaoRead])
def listar_avaliacoes_por_anuncio(anuncio_id: int):
    """
    Lista todas as avaliações de um anúncio específico.
    EXEMPLO:
    GET /avaliacoes/anuncio/1
    """
    avaliacoes = [a for a in avaliacoes_database if a["anuncio"] == anuncio_id]
    if not avaliacoes:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Nenhuma avaliação encontrada para este anúncio")
    return avaliacoes

@router.get("/autor/{autor_id}", status_code=HTTPStatus.OK, response_model=List[AvaliacaoRead])
def listar_avaliacoes_por_autor(autor_id: int):
    """
    Lista todas as avaliações feitas por um autor específico.
    EXEMPLO:
    GET /avaliacoes/autor/1
    """
    avaliacoes = [a for a in avaliacoes_database if a["autor"] == autor_id]
    if not avaliacoes:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Nenhuma avaliação encontrada para este autor")
    return avaliacoes

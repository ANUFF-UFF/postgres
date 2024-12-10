from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List

from api_anuff.schemas import AnuncioBase, AnuncioRead

router = APIRouter()

# Simulação do "banco de dados" em memória
anuncios_database = []
current_anuncio_id = 1


def get_anuncio_by_id(anuncio_id: int):
    for anuncio in anuncios_database:
        if anuncio['id'] == anuncio_id:
            return anuncio
    return None


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AnuncioRead)
def criar_anuncio(anuncio: AnuncioBase):
    global current_anuncio_id
    novo_anuncio = anuncio.dict()
    novo_anuncio["id"] = current_anuncio_id
    current_anuncio_id += 1
    anuncios_database.append(novo_anuncio)
    return novo_anuncio


@router.get("/", status_code=HTTPStatus.OK, response_model=List[AnuncioRead])
def listar_anuncios():
    return anuncios_database


@router.get("/{anuncio_id}", status_code=HTTPStatus.OK, response_model=AnuncioRead)
def obter_anuncio(anuncio_id: int):
    anuncio = get_anuncio_by_id(anuncio_id)
    if not anuncio:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Anúncio não encontrado")
    return anuncio


@router.put("/{anuncio_id}", status_code=HTTPStatus.OK, response_model=AnuncioRead)
def atualizar_anuncio(anuncio_id: int, anuncio: AnuncioBase):
    existente = get_anuncio_by_id(anuncio_id)
    if not existente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Anúncio não encontrado")
    existente.update(anuncio.dict())
    return existente


@router.delete("/{anuncio_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_anuncio(anuncio_id: int):
    global anuncios_database
    anuncio = get_anuncio_by_id(anuncio_id)
    if not anuncio:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Anúncio não encontrado")
    anuncios_database = [a for a in anuncios_database if a['id'] != anuncio_id]
    return

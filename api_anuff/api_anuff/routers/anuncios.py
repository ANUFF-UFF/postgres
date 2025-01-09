from fastapi import APIRouter, HTTPException, Query
from http import HTTPStatus
from typing import List
from rapidfuzz import fuzz


from api_anuff.schemas import AnuncioBase, AnuncioResponse

router = APIRouter()

# Simulação do "banco de dados" em memória
anuncios_database = []
current_anuncio_id = 1


def get_anuncio_by_id(anuncio_id: int):
    for anuncio in anuncios_database:
        if anuncio['id'] == anuncio_id:
            return anuncio
    return None


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AnuncioResponse)
def criar_anuncio(anuncio: AnuncioBase):
    global current_anuncio_id
    novo_anuncio = anuncio.dict()
    novo_anuncio["id"] = current_anuncio_id
    current_anuncio_id += 1
    anuncios_database.append(novo_anuncio)
    return novo_anuncio


@router.get("/", status_code=HTTPStatus.OK, response_model=List[AnuncioResponse])
def listar_anuncios():
    return anuncios_database


@router.get("/{anuncio_id}", status_code=HTTPStatus.OK, response_model=AnuncioResponse)
def obter_anuncio(anuncio_id: int):
    anuncio = get_anuncio_by_id(anuncio_id)
    if not anuncio:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Anúncio não encontrado")
    return anuncio


@router.put("/{anuncio_id}", status_code=HTTPStatus.OK, response_model=AnuncioResponse)
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

@router.get("/buscar", status_code=HTTPStatus.OK, response_model=List[AnuncioResponse])
def buscar_anuncios_por_titulo(nome: str = Query(..., description="Título ou parte do título do anúncio"), similaridade_minima: int = 80):
    """
    Busca anúncios pelo título com base na semelhança de palavras.
    - similaridade_minima (int): A pontuação mínima de similaridade (de 0 a 100) para incluir um anúncio nos resultados.
    
    EXEMPLO:
    GET /anuncios/buscar?nome=produto&similaridade_minima=80
    """
    resultados = []
    for anuncio in anuncios_database:
        pontuacao = fuzz.partial_ratio(nome.lower(), anuncio["titulo"].lower())
        if pontuacao >= similaridade_minima:
            resultados.append(anuncio)

    if not resultados:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Nenhum anúncio encontrado com base no critério fornecido")
    
    return resultados
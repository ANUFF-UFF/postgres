from fastapi import APIRouter, HTTPException, Query
from http import HTTPStatus
from typing import List
from rapidfuzz import fuzz
from typing import List, Optional


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
def buscar_e_filtrar_anuncios(
    nome: Optional[str] = Query(None, description="Título ou parte do título do anúncio"),
    similaridade_minima: int = Query(80, description="Pontuação mínima de similaridade (0 a 100)"),
    preco_min: Optional[float] = Query(None, description="Filtrar por preço mínimo"),
    preco_max: Optional[float] = Query(None, description="Filtrar por preço máximo"),
    ordenar_por: Optional[List[str]] = Query(
        None,
        description="Ordenar por uma combinação de critérios: 'mais_caros', 'mais_baratos', 'mais_novos', 'mais_antigos'"
    ),
):
    """
    Combina busca por título com filtros e ordenação:
    - `nome`: Busca anúncios pelo título com base na similaridade de palavras.
    - `similaridade_minima`: Pontuação mínima de similaridade para incluir anúncios.
    - `preco_min` e `preco_max`: Filtros de preço.
    - `ordenar_por`: Ordena os resultados com base nos critérios fornecidos.
    """
    anuncios_filtrados = anuncios_database

    # Filtrar por título (similaridade)
    if nome:
        anuncios_filtrados = [
            anuncio for anuncio in anuncios_filtrados
            if fuzz.partial_ratio(nome.lower(), anuncio["titulo"].lower()) >= similaridade_minima
        ]

    # Filtrar por preço
    if preco_min is not None:
        anuncios_filtrados = [a for a in anuncios_filtrados if a["preco"] >= preco_min]
    if preco_max is not None:
        anuncios_filtrados = [a for a in anuncios_filtrados if a["preco"] <= preco_max]

    # Ordenar por critérios
    if ordenar_por:
        for criterio in reversed(ordenar_por):
            if criterio == "mais_caros":
                anuncios_filtrados.sort(key=lambda x: x["preco"], reverse=True)
            elif criterio == "mais_baratos":
                anuncios_filtrados.sort(key=lambda x: x["preco"])
            elif criterio == "mais_novos":
                anuncios_filtrados.sort(key=lambda x: x["criado_em"], reverse=True)
            elif criterio == "mais_antigos":
                anuncios_filtrados.sort(key=lambda x: x["criado_em"])

    # Retornar erro se nenhum resultado encontrado
    if not anuncios_filtrados:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Nenhum anúncio encontrado com base nos critérios fornecidos")

    return anuncios_filtrados

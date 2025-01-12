from fastapi import APIRouter, HTTPException, Query
from http import HTTPStatus
from typing import List, Literal, Optional
from sqlmodel import select
from sqlalchemy import and_
from datetime import datetime

from database import SessionDep, try_block
from api_anuff.schemas import AnuncioBase

router = APIRouter()

@router.post("/", status_code=HTTPStatus.CREATED, response_model=AnuncioBase)
def criar_anuncio(anuncio: AnuncioBase, session: SessionDep):
    """
    Cria um novo anúncio no banco de dados.
    """
    def inner():
        anuncio.criado_em = datetime.now() 
        session.add(anuncio)
        session.commit()
        session.refresh(anuncio)
        return anuncio
    try_block(session, inner)

@router.get(
    "/",
    status_code=HTTPStatus.OK,
    response_model=List[AnuncioBase]
)
def listar_anuncios(session: SessionDep):
    """
    Lista todos os anúncios disponíveis no banco de dados.
    """
    def inner():
        return session.exec(select(AnuncioBase)).all()
    return try_block(session, inner)

   
@router.get("/buscar", status_code=HTTPStatus.OK, response_model=List[AnuncioBase])
def buscar_e_filtrar_anuncios(
    session: SessionDep,
    titulo: Optional[str] = Query(None, description="Título ou parte do título do anúncio"),
    # similaridade_minima: int = Query(None, description="Pontuação mínima de similaridade (0 a 100)"),
    preco_min: Optional[float] = Query(None, description="Filtrar por preço mínimo"),
    preco_max: Optional[float] = Query(None, description="Filtrar por preço máximo"),
    ordenar_por: Optional[List[Literal['mais_caros', 'mais_baratos', 'mais_novos', 'mais_antigos']]] = Query(
        None,
        description="Ordenar por uma combinação de critérios: 'mais_caros', 'mais_baratos', 'mais_novos', 'mais_antigos'"
    ),
):
    """
    Combina busca por título com filtros e ordenação:
    - `nome`: Busca anúncios pelo título com base na similaridade de palavras.
    - `preco_min` e `preco_max`: Filtros de preço.
    - `ordenar_por`: Ordena os resultados com base nos critérios fornecidos.
    """
    # pedaço removido da documentação
    # - `similaridade_minima`: Pontuação mínima de similaridade para incluir anúncios.
    def inner():
        if titulo is not None:
            titulo_regex = "".join([f"(?=.*{t})" for t in titulo.split()]) if titulo is not None else None
        where_clauses = filter(
            lambda e: e is not None,
            [
                AnuncioBase.titulo.regexp_match(titulo_regex) if titulo is not None else None,
                AnuncioBase.preco >= preco_min if preco_min is not None else None, 
                AnuncioBase.preco <= preco_max if preco_max is not None else None, 
            ]
        )
        query = select(AnuncioBase)
        if where_clauses != []:
            query = query.where(and_(
                *where_clauses
            ))

        if ordenar_por is not None:
            query = query.order_by(*[
                AnuncioBase.preco.desc() if o == "mais_caros" else 
                AnuncioBase.preco.asc() if o == "mais_baratos" else 
                AnuncioBase.criado_em.desc() if o == "mais_novos" else 
                AnuncioBase.criado_em.desc()
                for o in ordenar_por
            ])

        return session.exec(
            query
        ).all()

    return try_block(session, inner)
    # # Filtrar por título (similaridade)
    # if nome:
    #     anuncios_filtrados = [
    #         anuncio for anuncio in anuncios_filtrados
    #         if fuzz.partial_ratio(nome.lower(), anuncio["titulo"].lower()) >= similaridade_minima
    #     ]

@router.get("/{anuncio_id}", status_code=HTTPStatus.OK, response_model=AnuncioBase)
def obter_anuncio(anuncio_id: int, session: SessionDep):
    """
    Obtém um único anúncio pelo ID.
    """
    def inner():
        anuncio = session.exec(select(AnuncioBase).where(AnuncioBase.id == anuncio_id)).first()
        if anuncio is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Anúncio não encontrado")
        return anuncio

    return try_block(session, inner)


@router.put("/{anuncio_id}", status_code=HTTPStatus.OK, response_model=AnuncioBase)
def atualizar_anuncio(anuncio_id: int, anuncio: AnuncioBase, session: SessionDep):
    """
    Atualiza os dados de um anúncio pelo ID.
    """
    def inner():
        existente = session.exec(select(AnuncioBase).where(AnuncioBase.id == anuncio_id)).first()
        if existente is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Anúncio não encontrado")
        session.delete(existente)
        session.add(anuncio)
        return anuncio
    return try_block(session, inner)


@router.delete("/{anuncio_id}", status_code=HTTPStatus.ACCEPTED, response_model=AnuncioBase)
def deletar_anuncio(anuncio_id: int, session: SessionDep):
    """
    Deleta um anúncio pelo ID.
    """
    def inner():
        anuncio = session.exec(select(AnuncioBase).where(AnuncioBase.id == anuncio_id)).first()
        if anuncio is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Anúncio não encontrado")
        session.delete(anuncio)
        return anuncio
    return try_block(session, inner)


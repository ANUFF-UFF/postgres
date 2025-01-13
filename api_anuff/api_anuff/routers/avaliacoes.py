from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List
from sqlmodel import select, and_
from datetime import datetime

from api_anuff.schemas import AvaliacaoBase, AnuncioBase, UsuarioBase
from database import SessionDep, try_block, Session

router = APIRouter()

# Funções auxiliares
def get_avaliacao_by_id(session: Session, avaliacao_id: int):
    return session.exec(select(AvaliacaoBase).where(AvaliacaoBase.id == avaliacao_id)).first()

def calcular_reputacao_usuario(usuario_id: int, session):
    """
    Calcula a reputação de um usuário com base nas avaliações dos anúncios que ele criou.
    """
    anuncios = session.exec(select(AnuncioBase).where(AnuncioBase.autor == usuario_id)).all()
    if not anuncios:
        return 0.0  

    avaliacoes = []
    for anuncio in anuncios:
        avaliacoes.extend(session.exec(select(AvaliacaoBase).where(AvaliacaoBase.anuncio == anuncio.id)).all())

    if not avaliacoes:
        return 0.0

    soma_notas = sum(avaliacao.nota for avaliacao in avaliacoes)
    media = soma_notas / len(avaliacoes)

    usuario = session.exec(select(UsuarioBase).where(UsuarioBase.id == usuario_id)).first()
    if usuario:
        usuario.reputacao = media
        session.add(usuario)
        session.commit()

    return media

def calcular_media_anuncio(anuncio_id: int, session):
    """
    Calcula a média das notas de um anúncio com base nas avaliações associadas.
    """
    avaliacoes = session.exec(select(AvaliacaoBase).where(AvaliacaoBase.anuncio_id == anuncio_id)).all()
    if not avaliacoes:
        return 0.0  

    soma_notas = sum(avaliacao.nota for avaliacao in avaliacoes)
    media = soma_notas / len(avaliacoes)

    anuncio = session.exec(select(AnuncioBase).where(AnuncioBase.id == anuncio_id)).first()
    if anuncio:
        anuncio.nota = media
        session.add(anuncio)
        session.commit()

    return media


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AvaliacaoBase)
def criar_avaliacao(session: SessionDep, avaliacao: AvaliacaoBase):
    def inner():
        # Verificar se o autor já avaliou o anúncio
        avaliacao_ja_feita = session.exec(select(AvaliacaoBase).where(and_(
            AvaliacaoBase.autor == avaliacao.autor,
            AvaliacaoBase.anuncio == avaliacao.anuncio
        ))).first()
        if avaliacao_ja_feita is not None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="O autor já avaliou este anúncio."
            )
        
        avaliacao.criada_em = datetime.now()
        session.add(avaliacao)
        session.commit()
        session.refresh(avaliacao)
        # calcular_media_anuncio(avaliacao.anuncio, session)
        # calcular_reputacao_usuario(avaliacao.anuncio.autor, session)
        return avaliacao

    return try_block(session, inner)


@router.get("/", status_code=HTTPStatus.OK, response_model=List[AvaliacaoBase])
def listar_avaliacoes(session: SessionDep):
    def inner():
        return session.exec(select(AvaliacaoBase)).all()
    return try_block(session, inner)


@router.get("/anuncio/{anuncio_id}", status_code=HTTPStatus.OK, response_model=List[AvaliacaoBase])
def listar_avaliacoes_por_anuncio(session: SessionDep, anuncio_id: int):
    """
    Lista todas as avaliações de um anúncio específico.
    EXEMPLO:
    GET /avaliacoes/anuncio/1
    """
    def inner():
        return session.exec(
            select(AvaliacaoBase).where(
                AvaliacaoBase.anuncio == anuncio_id
            )
        ).all()
    return try_block(session, inner)


@router.get("/autor/{autor_id}", status_code=HTTPStatus.OK, response_model=List[AvaliacaoBase])
def listar_avaliacoes_por_autor(session: SessionDep, autor_id: int):
    """
    Lista todas as avaliações feitas por um autor específico.
    EXEMPLO:
    GET /avaliacoes/autor/1
    """
    def inner():
        return session.exec(
            select(AvaliacaoBase).where(
                AvaliacaoBase.autor == autor_id
            )
        ).all()
    return try_block(session, inner)


@router.get("/{avaliacao_id}", status_code=HTTPStatus.OK, response_model=AvaliacaoBase)
def obter_avaliacao(session: SessionDep, avaliacao_id: int):
    def inner():
        avaliacao = get_avaliacao_by_id(session, avaliacao_id)
        if avaliacao is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Avaliação não encontrada")
        return avaliacao
    return try_block(session, inner)


@router.delete("/{avaliacao_id}", status_code=HTTPStatus.ACCEPTED, response_model=AvaliacaoBase)
def deletar_avaliacao(session: SessionDep, avaliacao_id: int):
    def inner():
        avaliacao = get_avaliacao_by_id(session, avaliacao_id)
        if avaliacao is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Avaliação não encontrada")
        session.delete(avaliacao)
        session.commit()
        # calcular_media_anuncio(avaliacao.anuncio, session)
        # calcular_reputacao_usuario(avaliacao.anuncio.autor, session)
        return avaliacao
    return try_block(session, inner)

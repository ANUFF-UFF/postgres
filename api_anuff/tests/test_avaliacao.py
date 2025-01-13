import pytest
from fastapi.testclient import TestClient
from api_anuff.app import app
from api_anuff.schemas import AvaliacaoBase

client = TestClient(app)

# Dados de teste
mock_avaliacao = {
    "autor": 1,
    "anuncio_id": 1,
    "nota": 4.5,
    "comentario": "Ótimo anúncio!"
}


@pytest.fixture
def criar_avaliacao_teste():
    """
    Fixture para criar uma avaliação de teste.
    """
    response = client.post("/avaliacoes/", json=mock_avaliacao)
    return response.json()


def test_criar_avaliacao():
    """
    Testa a criação de uma avaliação.
    """
    response = client.post("/avaliacoes/", json=mock_avaliacao)
    assert response.status_code == 201
    data = response.json()
    assert data["nota"] == mock_avaliacao["nota"]
    assert data["comentario"] == mock_avaliacao["comentario"]


def test_listar_avaliacoes(criar_avaliacao_teste):
    """
    Testa a listagem de avaliações.
    """
    response = client.get("/avaliacoes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_listar_avaliacoes_por_anuncio(criar_avaliacao_teste):
    """
    Testa a listagem de avaliações por anúncio.
    """
    anuncio_id = criar_avaliacao_teste["anuncio_id"]
    response = client.get(f"/avaliacoes/anuncio/{anuncio_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_listar_avaliacoes_por_autor(criar_avaliacao_teste):
    """
    Testa a listagem de avaliações por autor.
    """
    autor_id = criar_avaliacao_teste["autor"]
    response = client.get(f"/avaliacoes/autor/{autor_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_obter_avaliacao(criar_avaliacao_teste):
    """
    Testa a obtenção de uma avaliação específica por ID.
    """
    avaliacao_id = criar_avaliacao_teste["id"]
    response = client.get(f"/avaliacoes/{avaliacao_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == avaliacao_id


def test_deletar_avaliacao(criar_avaliacao_teste):
    """
    Testa a exclusão de uma avaliação.
    """
    avaliacao_id = criar_avaliacao_teste["id"]
    response = client.delete(f"/avaliacoes/{avaliacao_id}")
    assert response.status_code == 202
    response = client.get(f"/avaliacoes/{avaliacao_id}")
    assert response.status_code == 404

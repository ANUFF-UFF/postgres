import pytest
from fastapi.testclient import TestClient
from api_anuff.app import app
from api_anuff.schemas import AnuncioBase

client = TestClient(app)

# Dados para testes
mock_anuncio = {
    "titulo": "Notebook Gamer",
    "descricao": "Notebook em excelente estado, ótimo para jogos.",
    "preco": 3500.0,
    "autor": 1
}

@pytest.fixture
def criar_anuncio_teste():
    """
    Fixture para criar um anúncio de teste.
    """
    response = client.post("/anuncios/", json=mock_anuncio)
    return response.json()


def test_criar_anuncio():
    """
    Testa a criação de um anúncio.
    """
    response = client.post("/anuncios/", json=mock_anuncio)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == mock_anuncio["titulo"]
    assert data["preco"] == mock_anuncio["preco"]


def test_listar_anuncios(criar_anuncio_teste):
    """
    Testa a listagem de anúncios.
    """
    response = client.get("/anuncios/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_obter_anuncio(criar_anuncio_teste):
    """
    Testa a obtenção de um anúncio por ID.
    """
    anuncio_id = criar_anuncio_teste["id"]
    response = client.get(f"/anuncios/{anuncio_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == anuncio_id
    assert data["titulo"] == mock_anuncio["titulo"]


def test_atualizar_anuncio(criar_anuncio_teste):
    """
    Testa a atualização de um anúncio.
    """
    anuncio_id = criar_anuncio_teste["id"]
    updated_anuncio = {
        "titulo": "Notebook Gamer Atualizado",
        "descricao": "Descrição atualizada",
        "preco": 4000.0,
        "autor": 1
    }
    response = client.put(f"/anuncios/{anuncio_id}", json=updated_anuncio)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == updated_anuncio["titulo"]
    assert data["preco"] == updated_anuncio["preco"]


def test_deletar_anuncio(criar_anuncio_teste):
    """
    Testa a exclusão de um anúncio.
    """
    anuncio_id = criar_anuncio_teste["id"]
    response = client.delete(f"/anuncios/{anuncio_id}")
    assert response.status_code == 202
    response = client.get(f"/anuncios/{anuncio_id}")
    assert response.status_code == 404

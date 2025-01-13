import pytest
from fastapi.testclient import TestClient
from api_anuff.app import app
from api_anuff.schemas import MensagemBase

client = TestClient(app)

# Dados para testes
mock_mensagem = {
    "conteudo": "Olá, tudo bem?",
    "chat_id": 1,
    "autor_id": 1
}


@pytest.fixture
def criar_mensagem_teste():
    """
    Fixture para criar uma mensagem de teste.
    """
    response = client.post("/mensagens/", json=mock_mensagem)
    assert response.status_code == 201  # Garantir que a mensagem foi criada
    return response.json()


def test_criar_mensagem():
    """
    Testa a criação de uma mensagem.
    """
    response = client.post("/mensagens/", json=mock_mensagem)
    assert response.status_code == 201
    data = response.json()
    assert data["conteudo"] == mock_mensagem["conteudo"]
    assert data["chat_id"] == mock_mensagem["chat_id"]
    assert data["autor_id"] == mock_mensagem["autor_id"]


def test_listar_mensagens(criar_mensagem_teste):
    """
    Testa a listagem de todas as mensagens.
    """
    response = client.get("/mensagens/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_obter_mensagem(criar_mensagem_teste):
    """
    Testa a obtenção de uma mensagem pelo ID.
    """
    mensagem_id = criar_mensagem_teste["id"]
    response = client.get(f"/mensagens/{mensagem_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mensagem_id
    assert data["conteudo"] == mock_mensagem["conteudo"]


def test_deletar_mensagem(criar_mensagem_teste):
    """
    Testa a exclusão de uma mensagem.
    """
    mensagem_id = criar_mensagem_teste["id"]
    response = client.delete(f"/mensagens/{mensagem_id}")
    assert response.status_code == 204
    response = client.get(f"/mensagens/{mensagem_id}")
    assert response.status_code == 404


def test_listar_mensagens_por_chat(criar_mensagem_teste):
    """
    Testa a listagem de mensagens por chat.
    """
    chat_id = mock_mensagem["chat_id"]
    response = client.get(f"/mensagens/chats/{chat_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(msg["chat_id"] == chat_id for msg in data)


def test_obter_mensagem_nao_existente():
    """
    Testa a obtenção de uma mensagem inexistente.
    """
    response = client.get("/mensagens/9999")  # ID inexistente
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Mensagem não encontrada"


def test_deletar_mensagem_nao_existente():
    """
    Testa a exclusão de uma mensagem inexistente.
    """
    response = client.delete("/mensagens/9999")  # ID inexistente
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Mensagem não encontrada"

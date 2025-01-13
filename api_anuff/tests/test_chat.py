import pytest
from fastapi.testclient import TestClient
from api_anuff.app import app

client = TestClient(app)

# Dados de teste
mock_chat = {
    "usuario_1_id": 1,
    "usuario_2_id": 2
}

@pytest.fixture
def criar_chat_teste():
    """
    Fixture para criar um chat de teste.
    """
    response = client.post("/chats/", json=mock_chat)
    assert response.status_code == 201  # Garante que o chat foi criado
    return response.json()


def test_criar_chat():
    """
    Testa a criação de um chat.
    """
    response = client.post("/chats/", json=mock_chat)
    assert response.status_code == 201
    data = response.json()
    assert data["usuario_1_id"] == mock_chat["usuario_1_id"]
    assert data["usuario_2_id"] == mock_chat["usuario_2_id"]


def test_listar_chats(criar_chat_teste):
    """
    Testa a listagem de todos os chats.
    """
    response = client.get("/chats/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_obter_chat(criar_chat_teste):
    """
    Testa a obtenção de um chat pelo ID.
    """
    chat_id = criar_chat_teste["id"]
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == chat_id
    assert data["usuario_1_id"] == mock_chat["usuario_1_id"]
    assert data["usuario_2_id"] == mock_chat["usuario_2_id"]


def test_deletar_chat(criar_chat_teste):
    """
    Testa a exclusão de um chat.
    """
    chat_id = criar_chat_teste["id"]
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404


def test_obter_chat_por_usuarios(criar_chat_teste):
    """
    Testa a obtenção de um chat com base nos IDs dos usuários.
    """
    response = client.get("/chats/usuarios", params={
        "usuario_1_id": mock_chat["usuario_1_id"],
        "usuario_2_id": mock_chat["usuario_2_id"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["usuario_1_id"] == mock_chat["usuario_1_id"]
    assert data["usuario_2_id"] == mock_chat["usuario_2_id"]


def test_criar_chat_automatico_por_usuarios():
    """
    Testa a criação automática de um chat se ele não existir ao buscar por usuários.
    """
    new_chat_data = {"usuario_1_id": 3, "usuario_2_id": 4}
    response = client.get("/chats/usuarios", params=new_chat_data)
    assert response.status_code == 200
    data = response.json()
    assert data["usuario_1_id"] == new_chat_data["usuario_1_id"]
    assert data["usuario_2_id"] == new_chat_data["usuario_2_id"]

    # Confirma que o chat foi criado ao listar todos os chats
    all_chats = client.get("/chats/")
    assert any(
        chat["usuario_1_id"] == new_chat_data["usuario_1_id"] and
        chat["usuario_2_id"] == new_chat_data["usuario_2_id"]
        for chat in all_chats.json()
    )


def test_obter_chat_nao_existente():
    """
    Testa a obtenção de um chat inexistente pelo ID.
    """
    response = client.get("/chats/9999")  # ID inexistente
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Chat não encontrado"


def test_deletar_chat_nao_existente():
    """
    Testa a exclusão de um chat inexistente.
    """
    response = client.delete("/chats/9999")  # ID inexistente
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Chat não encontrado"

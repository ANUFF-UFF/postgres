import pytest
from fastapi.testclient import TestClient
from api_anuff.app import app

client = TestClient(app)

# Dados para testes
mock_usuario = {
    "nome": "Usuário Teste",
    "email": "usuario@teste.com",
    "senha": "senha123"
}

@pytest.fixture
def criar_usuario_teste():
    """
    Fixture para criar um usuário de teste.
    """
    response = client.post("/usuarios/", json=mock_usuario)
    assert response.status_code == 201  # Garantir que o usuário foi criado
    return response.json()


def test_criar_usuario():
    """
    Testa a criação de um usuário.
    """
    response = client.post("/usuarios/", json=mock_usuario)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == mock_usuario["nome"]
    assert data["email"] == mock_usuario["email"]


def test_listar_usuarios(criar_usuario_teste):
    """
    Testa a listagem de todos os usuários.
    """
    response = client.get("/usuarios/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_obter_usuario(criar_usuario_teste):
    """
    Testa a obtenção de um usuário pelo ID.
    """
    usuario_id = criar_usuario_teste["id"]
    response = client.get(f"/usuarios/{usuario_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == usuario_id
    assert data["nome"] == mock_usuario["nome"]


def test_atualizar_usuario(criar_usuario_teste):
    """
    Testa a atualização de um usuário.
    """
    usuario_id = criar_usuario_teste["id"]
    updated_usuario = {
        "nome": "Usuário Atualizado",
        "email": "atualizado@teste.com",
        "senha": "nova_senha123"
    }
    response = client.put(f"/usuarios/{usuario_id}", json=updated_usuario)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == updated_usuario["nome"]
    assert data["email"] == updated_usuario["email"]


def test_deletar_usuario(criar_usuario_teste):
    """
    Testa a exclusão de um usuário.
    """
    usuario_id = criar_usuario_teste["id"]
    response = client.delete(f"/usuarios/{usuario_id}")
    assert response.status_code == 204
    response = client.get(f"/usuarios/{usuario_id}")
    assert response.status_code == 404


def test_obter_usuario_nao_existente():
    """
    Testa a obtenção de um usuário inexistente.
    """
    response = client.get("/usuarios/9999")  # ID inexistente
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Usuário não encontrado"


def test_deletar_usuario_nao_existente():
    """
    Testa a exclusão de um usuário inexistente.
    """
    response = client.delete("/usuarios/9999")  # ID inexistente
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Usuário não encontrado"

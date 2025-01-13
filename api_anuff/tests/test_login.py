import pytest
from fastapi.testclient import TestClient
from api_anuff.app import app
from api_anuff.schemas import LoginData

client = TestClient(app)

# Dados para testes
mock_usuario = {
    "nome": "João Silva",
    "email": "joao@email.com",
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


def test_login_sucesso(criar_usuario_teste):
    """
    Testa um login com credenciais corretas.
    """
    login_data = {
        "email": mock_usuario["email"],
        "senha": mock_usuario["senha"]
    }
    response = client.post("/login/", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data["mensagem"] == "Login realizado com sucesso"
    assert data["usuario"] == mock_usuario["nome"]


def test_login_credenciais_invalidas(criar_usuario_teste):
    """
    Testa um login com credenciais inválidas.
    """
    login_data = {
        "email": mock_usuario["email"],
        "senha": "senha_incorreta"
    }
    response = client.post("/login/", json=login_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Credenciais inválidas"


def test_login_usuario_nao_existente():
    """
    Testa um login com email de usuário inexistente.
    """
    login_data = {
        "email": "naoexiste@email.com",
        "senha": "qualquer_senha"
    }
    response = client.post("/login/", json=login_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Credenciais inválidas"

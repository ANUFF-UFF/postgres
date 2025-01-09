from fastapi import APIRouter, HTTPException, Depends
from routers.usuarios import listar_usuarios  # Importar a função de listar usuários
from api_anuff.schemas import LoginData, LoginResponse

router = APIRouter()

@router.post("/", response_model=LoginResponse)
def login(dados: LoginData, usuarios=Depends(listar_usuarios)):
    """
    Verifica se o email e a senha correspondem a um usuário válido na lista de usuários.
    """
    # Busca o usuário pelo email
    usuario = next((u for u in usuarios if u["email"] == dados.email), None)

    if not usuario or usuario["senha"] != dados.senha:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    return {
        "mensagem": "Login bem-sucedido!",
        "usuario": usuario["nome"]
    }

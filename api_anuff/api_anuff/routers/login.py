from fastapi import APIRouter, HTTPException, Depends
from routers.usuarios import listar_usuarios  # Importar a função de listar usuários
from api_anuff.schemas import LoginData, LoginResponse, UsuarioBase
from sqlmodel import select, and_, or_

from api_anuff.schemas import ChatBase
from database import SessionDep, try_block, Session

router = APIRouter()

@router.post("/", response_model=LoginResponse)
def login(session: SessionDep, dados: LoginData, usuarios=Depends(listar_usuarios)):
    """
    Verifica se o email e a senha correspondem a um usuário válido na lista de usuários.
    """
    def inner():
        usuario = session.exec(select(UsuarioBase).where(and_(
            UsuarioBase.email == dados.email,
            UsuarioBase.senha == dados.senha
        ))).first()

        if usuario is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        return LoginResponse(usuario=usuario.nome, mensagem="Login realizado com sucesso")

    return try_block(session, inner)

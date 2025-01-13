from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
# from routers.usuarios import listar_usuarios  # Importar a função de listar usuários
from api_anuff.schemas import LoginData, UsuarioRead, UsuarioBase, usuario_base_to_read
from sqlmodel import select, and_

from database import SessionDep, try_block, hash_password

router = APIRouter()

@router.post("/", status_code=HTTPStatus.OK, response_model=UsuarioRead)
def login(session: SessionDep, dados: LoginData):
    """
    Verifica se o email e a senha correspondem a um usuário válido na lista de usuários.
    """
    def inner():
        usuario = session.exec(select(UsuarioBase).where(and_(
            UsuarioBase.email == dados.email,
            UsuarioBase.senha == hash_password(dados.senha)
        ))).first()

        if usuario is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        # return LoginResponse(usuario=usuario.nome, mensagem="Login realizado com sucesso")
        return usuario_base_to_read(usuario)


    return try_block(session, inner)

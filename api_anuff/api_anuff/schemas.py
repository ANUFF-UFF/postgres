from pydantic import EmailStr
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    message: str

class UsuarioBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    email: EmailStr
    reputacao: float = 0.0
    senha: str

class UsuarioRead(UsuarioBase):
    id: int = Field(default=None, primary_key=True)
    nome: str
    email: EmailStr

    # class Config:
    #     orm_mode = True


class AnuncioBase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    preco: float
    autor: int
    criado_em: Optional[datetime]

# class AnuncioCreate(AnuncioBase):
#     id: int = Field(default=None, primary_key=True)
#     autor: int
#
# class AnuncioResponse(AnuncioBase):
#     id: int = Field(default=None, primary_key=True)
#     # criado_em: datetime
#
#     # class Config:
#     #     orm_mode = True

class ChatBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    usuario_1_id: int
    usuario_2_id: int


class ChatRead(ChatBase):
    id: int = Field(default=None, primary_key=True)
    criado_em: datetime

    # class Config:
    #     orm_mode = True


class MensagemBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int
    remetente_id: int
    conteudo: str


class MensagemRead(MensagemBase):
    id: int = Field(default=None, primary_key=True)
    enviada_em: datetime

    # class Config:
    #     orm_mode = True


class AvaliacaoBase(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
    )
    nota: int
    comentario: Optional[str]
    criada_em: Optional[datetime]
    autor: int
    anuncio: int

# class AvaliacaoRead(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     nota: int
#     comentario: Optional[str]
#     criada_em: datetime
#     autor: int
#     anuncio: int
#
#     # class Config:
#     #     orm_mode = True
#
# class AvaliacaoCreate(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     #todo
#     pass

class LoginData(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    senha: str

class LoginResponse(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    mensagem: str
    usuario: str


from pydantic import EmailStr, BaseModel
from datetime import datetime
from typing import Optional
from sqlmodel import ForeignKey, SQLModel, Field, UniqueConstraint

class UsuarioBase(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("email"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: EmailStr
    reputacao: float = 0.0
    ocupacao: str
    senha: str
    foto: Optional[str]

class UsuarioRead(BaseModel):
    id: int = Field(default=None, primary_key=True)
    nome: str
    email: EmailStr

def usuario_base_to_read(u: UsuarioBase) -> UsuarioRead:
    return UsuarioRead(
        id=u.id,
        nome=u.nome,
        email=u.email
    )

   # class Config:
   #     orm_mode = True


class AnuncioBase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    preco: float
    autor: int = Field(foreign_key="usuariobase.id")
    nota: float = 0.0
    criado_em: Optional[datetime]
    foto: str

class AnuncioRead(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    preco: float
    autor: int = Field(foreign_key="usuariobase.id")
    nome_autor: str
    nota: float = 0.0
    criado_em: Optional[datetime]
    foto: str

def anuncio_read(a: AnuncioBase, nome_autor: str) -> AnuncioRead:
    return AnuncioRead(
        id=a.id,
        titulo=a.titulo,
        descricao=a.descricao,
        preco=a.preco,
        autor=a.autor,
        nome_autor=nome_autor,
        nota=a.nota,
        criado_em=a.criado_em,
        foto=a.foto
    )
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
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_1_id: int = Field(foreign_key="usuariobase.id")
    usuario_2_id: int = Field(foreign_key="usuariobase.id")

# class ChatRead(ChatBase):
#     id: int

class MensagemBase(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chatbase.id")
    remetente_id: int = Field(foreign_key="usuariobase.id")
    conteudo: str
    enviada_em: datetime


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

class LoginData(BaseModel):
    email: EmailStr
    senha: str

# class LoginResponse(SQLModel, table=True):
#     usuario: UsuarioBase


from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Message(BaseModel):
    message: str

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    reputacao: float = 0.0
    senha: str

class UsuarioRead(UsuarioBase):
    id: int
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True


class AnuncioBase(BaseModel):
    titulo: str
    descricao: str
    preco: float
    autor: int

class AnuncioCreate(AnuncioBase):
    autor: int

class AnuncioResponse(AnuncioBase):
    id: int
    criado_em: datetime

    class Config:
        orm_mode = True

class ChatBase(BaseModel):
    usuario_1_id: int
    usuario_2_id: int


class ChatRead(ChatBase):
    id: int
    criado_em: datetime

    class Config:
        orm_mode = True


class MensagemBase(BaseModel):
    chat_id: int
    remetente_id: int
    conteudo: str


class MensagemRead(MensagemBase):
    id: int
    enviada_em: datetime

    class Config:
        orm_mode = True


class AvaliacaoBase(BaseModel):
    nota: int
    comentario: Optional[str]
    autor: int
    anuncio: int


class AvaliacaoRead(BaseModel):
    id: int
    nota: int
    comentario: Optional[str]
    criada_em: datetime
    autor: int
    anuncio: int

    class Config:
        orm_mode = True
 

class LoginData(BaseModel):
    email: str
    senha: str

class LoginResponse(BaseModel):
    mensagem: str
    usuario: str


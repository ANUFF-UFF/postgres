from pydantic import BaseModel, EmailStr
from datetime import datetime

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

class LoginData(BaseModel):
    email: str
    senha: str

class LoginResponse(BaseModel):
    mensagem: str
    usuario: str
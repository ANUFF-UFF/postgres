from pydantic import BaseModel, EmailStr

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
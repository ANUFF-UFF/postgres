from sqlalchemy import Column, Integer, String, Float, DateTime, func, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import (Base)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    reputacao = Column(Float, default=0.0)

class Anuncio(Base):
    __tablename__ = 'anuncio'

    id = Column(Integer, primary_key=True, index=True)
    autor = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    titulo = Column(String, nullable=False) 
    descricao = Column(String, nullable=True)  
    preco = Column(Numeric(9, 2), nullable=True)  
    criado_em = Column(DateTime, default=func.now())  

    autor_rel = relationship("Usuario", back_populates="anuncios")
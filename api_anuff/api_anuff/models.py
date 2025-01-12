from sqlalchemy import Column, Integer, String, Float, DateTime, func, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    reputacao = Column(Float, default=0.0)

    # Relacionamentos
    anuncios = relationship("Anuncio", back_populates="autor_rel", cascade="all, delete")
    chats_1 = relationship("Chat", foreign_keys="[Chat.usuario_1_id]", back_populates="usuario_1_rel")
    chats_2 = relationship("Chat", foreign_keys="[Chat.usuario_2_id]", back_populates="usuario_2_rel")
    mensagens = relationship("Mensagem", back_populates="remetente_rel", cascade="all, delete")
    avaliacoes_feitas = relationship("Avaliacao", back_populates="autor_rel", cascade="all, delete")


class Anuncio(Base):
    __tablename__ = 'anuncio'

    id = Column(Integer, primary_key=True, index=True)
    autor = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Numeric(9, 2), nullable=True)
    nota = Column(Integer, nullable=True)
    criado_em = Column(DateTime, default=func.now())

    # Relacionamentos
    autor_rel = relationship("Usuario", back_populates="anuncios")
    avaliacoes = relationship("Avaliacao", back_populates="anuncio_rel", cascade="all, delete")


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    usuario_1_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    usuario_2_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    criado_em = Column(DateTime, server_default=func.now())

    # Relacionamentos
    usuario_1_rel = relationship("Usuario", foreign_keys="[Chat.usuario_1_id]", back_populates="chats_1")
    usuario_2_rel = relationship("Usuario", foreign_keys="[Chat.usuario_2_id]", back_populates="chats_2")
    mensagens = relationship("Mensagem", back_populates="chat_rel", cascade="all, delete")


class Mensagem(Base):
    __tablename__ = "mensagem"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=False)
    remetente_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    conteudo = Column(String, nullable=False)
    enviada_em = Column(DateTime, server_default=func.now())

    # Relacionamentos
    chat_rel = relationship("Chat", back_populates="mensagens")
    remetente_rel = relationship("Usuario", back_populates="mensagens")


class Avaliacao(Base):
    __tablename__ = "avaliacao"

    id = Column(Integer, primary_key=True, index=True)
    nota = Column(Integer, nullable=False)
    comentario = Column(String, nullable=True)
    criada_em = Column(DateTime, server_default=func.now())
    autor = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    anuncio = Column(Integer, ForeignKey("anuncio.id"), nullable=False)

    # Garantir que um autor só avalie um anúncio uma vez
    __table_args__ = (UniqueConstraint("autor", "anuncio", name="unique_autor_anuncio"),)

    # Relacionamentos
    autor_rel = relationship("Usuario", back_populates="avaliacoes_feitas")
    anuncio_rel = relationship("Anuncio", back_populates="avaliacoes")

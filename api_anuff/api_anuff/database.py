# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
from sqlalchemy import URL
from os import getenv

USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")
DATABASE = getenv("DATABASE")
HOSTNAME = getenv("HOSTNAME")
# URL do banco de dados (substitua os valores pelas suas configurações)
# DATABASE_URL = "postgresql+asyncpg://admin:<sua_senha>@localhost:5432/anuff"
DATABASE_URL = URL.create(
    drivername="postgresql",
    username=USERNAME,
    password=PASSWORD,
    database=DATABASE,
    host=HOSTNAME
)

# Configuração do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Base para os modelos
# Base = declarative_base()

# async
def get_session():
    """Fornece a sessão de banco de dados para as rotas"""
    with Session(engine) as session:
        return lambda: session
    # async with async_session() as session:
    #     yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session())]

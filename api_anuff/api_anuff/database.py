from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL do banco de dados (substitua os valores pelas suas configurações)
DATABASE_URL = "postgresql+asyncpg://admin:<sua_senha>@localhost:5432/anuff"

# Configuração do SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base para os modelos
Base = declarative_base()

async def get_db():
    """Fornece a sessão de banco de dados para as rotas"""
    async with async_session() as session:
        yield session

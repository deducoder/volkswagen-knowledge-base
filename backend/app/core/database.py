from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os

# Leemos la URL y validamos
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("FATAL: La variable de entorno DATABASE_URL no está definida.")

# Creamos el motor asíncrono
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Creamos la fábrica de sesiones
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependencia para inyectar la sesión en los endpoints
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
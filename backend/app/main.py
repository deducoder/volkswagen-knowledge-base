# backend/app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from contextlib import asynccontextmanager
import os

# Importamos la función de seguridad que creamos en core/security.py
from app.core.security import get_current_username

# 1. Configuración de Base de Datos
# Leemos la URL y validamos que exista para evitar errores de tipo (str | None)
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("FATAL: La variable de entorno DATABASE_URL no está definida.")

# Creamos el motor asíncrono compatible con postgresql+asyncpg
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 2. Ciclo de Vida de la Aplicación (Startup/Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando aplicación y verificando conexión a DB...")
    try:
        # Creamos una conexión para probar la DB
        async with engine.connect() as conn:
            # A. Verificación simple de conectividad
            await conn.execute(text("SELECT 1"))
            print("✅ Conexión a Base de Datos exitosa.")
            
            # B. Verificación de la extensión pgvector (Requerimiento Fase 1)
            result = await conn.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector'"))
            if result.fetchone():
                print("✅ Extensión 'vector' detectada correctamente.")
            else:
                print("⚠️  ADVERTENCIA: Extensión 'vector' NO detectada. Revisa tu init.sql.")
    except Exception as e:
        print(f"❌ Error CRÍTICO conectando a la DB: {e}")
        # En un entorno real, aquí podríamos detener la app si la DB es crítica
    
    yield
    # Aquí iría código de limpieza al apagar la app (si fuera necesario)

# 3. Definición de la App FastAPI
app = FastAPI(title="Volkswagen Knowledge Base API", lifespan=lifespan)

# --- ENDPOINTS ---

@app.get("/health")
async def health_check():
    """
    Endpoint PÚBLICO de salud. 
    No requiere autenticación para que Docker/K8s puedan monitorearlo.
    """
    return {"status": "ok", "service": "backend-api"}

@app.get("/", dependencies=[Depends(get_current_username)])
async def root():
    """
    Endpoint PROTEGIDO.
    Requiere usuario y contraseña definidos en .env (Basic Auth).
    """
    return {
        "message": "Acceso Autorizado: Sistema Volkswagen Knowledge Base",
        "phase": "Fase 3 Completada (Seguridad Básica)"
    }
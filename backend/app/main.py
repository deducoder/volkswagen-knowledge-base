# backend/app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy import text
from contextlib import asynccontextmanager

# Importamos la seguridad existente
from app.core.security import get_current_username

# --- CAMBIO: Importamos engine de la nueva ubicación para evitar ciclos ---
from app.core.database import engine

# --- NUEVO: Importamos el router de casos ---
from app.api.endpoints import cases

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
            
            # B. Verificación de la extensión pgvector
            result = await conn.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector'"))
            if result.fetchone():
                print("✅ Extensión 'vector' detectada correctamente.")
            else:
                print("⚠️  ADVERTENCIA: Extensión 'vector' NO detectada.")
                
            # C. Inicialización de Tablas (Opcional si usas init.sql, pero útil para SQLModel)
            # Nota: Esto creará las columnas nuevas si no existen y la DB lo permite, 
            # pero en producción se recomienda Alembic.
            # from app.models import SQLModel
            # await conn.run_sync(SQLModel.metadata.create_all)
            
    except Exception as e:
        print(f"❌ Error CRÍTICO conectando a la DB: {e}")
    
    yield
    print("🛑 Apagando aplicación...")

# 3. Definición de la App FastAPI
app = FastAPI(title="Volkswagen Knowledge Base API", lifespan=lifespan)

# --- REGISTRO DE ROUTERS ---
app.include_router(cases.router, prefix="/api/cases", tags=["Casos de Diagnóstico"])

# --- ENDPOINTS EXISTENTES ---

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "backend-api"}

@app.get("/", dependencies=[Depends(get_current_username)])
async def root():
    return {
        "message": "Acceso Autorizado: Sistema Volkswagen Knowledge Base",
        "phase": "Fase 2: Captura de Conocimiento Activada"
    }
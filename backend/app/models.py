from enum import Enum
from typing import Optional
from datetime import datetime
from sqlalchemy import String
from sqlmodel import SQLModel, Field, Column
from pgvector.sqlalchemy import Vector

# 1. Definición del Enum
class ConstructionGroup(str, Enum):
    MOTOR = "Motor"
    TRANSMISION = "Transmisión"
    ELECTRICO = "Eléctrico"
    SUSPENSION = "Suspensión"
    CARROCERIA = "Carrocería"
    FRENOS = "Frenos"
    CLIMATIZACION = "Climatización"
    INFOENTRETENIMIENTO = "Infoentretenimiento"

# 2. Clase Base
class DiagnosisCaseBase(SQLModel):
    title: str = Field(max_length=255, description="Resumen corto del problema")
    vehicle_model: str = Field(max_length=100)
    year: int
    
    # Se persiste como String en PG, se valida como Enum en Python
    construction_group: ConstructionGroup = Field(sa_column=Column(String))

    problem_description: str
    solution_description: str

# 3. DTO de Creación
class DiagnosisCaseCreate(DiagnosisCaseBase):
    pass

# 4. Modelo de Base de Datos
class DiagnosisCase(DiagnosisCaseBase, table=True):
    __tablename__ = "diagnosis_cases"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Columna Vectorial (pgvector)
    embedding: Optional[list[float]] = Field(default=None, sa_column=Column(Vector(1536)))

    class Config:
        arbitrary_types_allowed = True

# --- NUEVO: DTOs para Búsqueda (Épica 3) ---
class SearchRequest(SQLModel):
    query: str
    model_filter: Optional[str] = None
    group_filter: Optional[ConstructionGroup] = None

class SearchResult(DiagnosisCaseBase):
    id: int
    score: float = 0.0
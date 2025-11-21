from enum import Enum
from typing import Optional
from datetime import datetime
# AGREGADO: Importamos 'String' de sqlalchemy
from sqlalchemy import String
from sqlmodel import SQLModel, Field, Column
from pgvector.sqlalchemy import Vector

# 1. Definición del Enum (Se mantiene igual)
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
    
    # --- CAMBIO CRÍTICO AQUÍ ---
    # Forzamos que en la DB sea una columna de tipo String (VARCHAR),
    # aunque en Python siga siendo un Enum validado.
    construction_group: ConstructionGroup = Field(sa_column=Column(String))
    # ---------------------------

    problem_description: str
    solution_description: str

# 3. DTO de Creación (Igual)
class DiagnosisCaseCreate(DiagnosisCaseBase):
    pass

# 4. Modelo de Base de Datos (Igual)
class DiagnosisCase(DiagnosisCaseBase, table=True):
    __tablename__ = "diagnosis_cases"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    embedding: Optional[list[float]] = Field(default=None, sa_column=Column(Vector(1536)))

    class Config:
        arbitrary_types_allowed = True
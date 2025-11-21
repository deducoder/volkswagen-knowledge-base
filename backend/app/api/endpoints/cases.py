from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import get_current_username
from app.models import DiagnosisCase, DiagnosisCaseCreate, SearchRequest, SearchResult
from app.services.case_service import CaseService

router = APIRouter()

# --- NUEVO ENDPOINT: LISTA MAESTRA DE MODELOS ---
@router.get("/models", response_model=List[str])
async def get_vehicle_models(
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_username)
):
    """
    Devuelve la lista oficial de modelos para estandarizar la entrada de datos
    y alimentar los autocompletados del frontend.
    """
    official_models = [
        "Amarok", "Arteon", "Atlas", "Beetle", "Caddy", "Crafter", 
        "Golf", "Golf GTI", "Golf R", "ID.3", "ID.4", "ID.Buzz", 
        "Jetta", "Jetta GLI", "Passat", "Polo", "Saveiro", 
        "T-Cross", "Taos", "Tiguan", "Touareg", "Transporter", 
        "Virtus", "Vento"
    ]
    # Ordenamos alfabéticamente para mejor UX
    return sorted(official_models)

# --- ENDPOINTS EXISTENTES ---
@router.post("/", response_model=DiagnosisCase, status_code=status.HTTP_201_CREATED)
async def create_new_case(
    case_data: DiagnosisCaseCreate,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_username)
):
    """
    Registra un nuevo caso y genera su embedding.
    """
    service = CaseService(session)
    new_case = await service.create_case(case_data)
    return new_case

@router.post("/search", response_model=List[SearchResult])
async def search_cases(
    search_data: SearchRequest,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_username)
):
    """
    Busca casos usando IA o texto tradicional.
    """
    service = CaseService(session)
    results = await service.search_cases(search_data)
    return results
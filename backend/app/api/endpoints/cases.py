from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import get_current_username
from app.models import DiagnosisCase, DiagnosisCaseCreate
from app.services.case_service import CaseService

router = APIRouter()

@router.post("/", response_model=DiagnosisCase, status_code=status.HTTP_201_CREATED)
async def create_new_case(
    case_data: DiagnosisCaseCreate,
    session: AsyncSession = Depends(get_session),
    username: str = Depends(get_current_username) # Seguridad: Requiere Auth
):
    """
    Registra un nuevo caso de diagnóstico en la base de conocimiento.
    Requiere autenticación Basic Auth.
    """
    # Instanciamos el servicio inyectando la sesión
    service = CaseService(session)
    
    # Delegamos la lógica al servicio
    new_case = await service.create_case(case_data)
    
    return new_case
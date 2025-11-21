from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from app.models import DiagnosisCase, DiagnosisCaseCreate

class CaseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def refine_text_with_ai(self, text: str) -> str:
        """
        Placeholder para la Historia 2.3 (Copiloto de Calidad).
        En el futuro, esto llamará a OpenAI/Llama para mejorar la redacción.
        Por ahora, devuelve el texto tal cual.
        """
        # TODO: Implementar llamada a LLM
        return text

    async def create_case(self, case_create: DiagnosisCaseCreate) -> DiagnosisCase:
        """
        Crea un nuevo caso de diagnóstico con validaciones de negocio.
        """
        # 1. Validación de Negocio: Año lógico
        current_year = datetime.now().year
        if case_create.year < 1950 or case_create.year > current_year + 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"El año debe estar entre 1950 y {current_year + 1}"
            )

        # 2. "Refinamiento" (simulado)
        # Aquí prepararíamos los textos para ser vectorizados en el futuro
        refined_problem = await self.refine_text_with_ai(case_create.problem_description)

        # 3. Mapeo a Modelo de DB
        db_case = DiagnosisCase.model_validate(case_create)
        db_case.problem_description = refined_problem # Asignamos el texto refinado
        
        # 4. Persistencia
        self.session.add(db_case)
        await self.session.commit()
        await self.session.refresh(db_case)
        
        return db_case
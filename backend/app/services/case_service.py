from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import text, select, or_
from app.models import DiagnosisCase, DiagnosisCaseCreate, SearchRequest, SearchResult
from app.core.ai_client import AIClient

class CaseService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.ai_client = AIClient()

    async def create_case(self, case_create: DiagnosisCaseCreate) -> DiagnosisCase:
        # 1. Validación de Negocio
        current_year = datetime.now().year
        if case_create.year < 1950 or case_create.year > current_year + 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"El año debe estar entre 1950 y {current_year + 1}"
            )

        # 2. Preparación del Modelo
        db_case = DiagnosisCase.model_validate(case_create)

        # 3. Generación de Embeddings (IA)
        text_to_vectorize = f"Problema: {case_create.problem_description}. Solución: {case_create.solution_description}"
        print(f"🤖 Generando vector para caso: '{case_create.title}'...")
        
        vector = await self.ai_client.get_embedding(text_to_vectorize)
        
        if vector:
            db_case.embedding = vector
        else:
            print("⚠️  Advertencia: No se pudo generar el vector (se guardará sin IA).")
            db_case.embedding = None

        # 4. Persistencia
        self.session.add(db_case)
        await self.session.commit()
        await self.session.refresh(db_case)
        
        # Fix: Convertir numpy array a lista nativa para JSON
        if db_case.embedding is not None and hasattr(db_case.embedding, 'tolist'):
            db_case.embedding = db_case.embedding.tolist()
        
        return db_case

    async def search_cases(self, search_params: SearchRequest) -> list[SearchResult]:
        """
        Motor de Búsqueda Híbrido: Vectorial (Semántico) + Fallback SQL (Texto).
        """
        results = []
        search_vector = await self.ai_client.get_embedding(search_params.query)

        # Consulta base
        statement = select(DiagnosisCase)

        # Filtros SQL (siempre se aplican)
        if search_params.model_filter:
            statement = statement.where(
                DiagnosisCase.vehicle_model.ilike(f"%{search_params.model_filter}%")
            )
        
        if search_params.group_filter:
            statement = statement.where(
                DiagnosisCase.construction_group == search_params.group_filter
            )

        # Estrategia Híbrida
        if search_vector:
            print(f"🔍 Búsqueda Semántica (Vector) para: '{search_params.query}'")
            # Ordenar por distancia coseno
            statement = statement.order_by(
                DiagnosisCase.embedding.cosine_distance(search_vector)
            ).limit(5)
        else:
            print(f"⚠️ Fallback: Búsqueda de Texto (LIKE) para: '{search_params.query}'")
            statement = statement.where(
                or_(
                    DiagnosisCase.problem_description.ilike(f"%{search_params.query}%"),
                    DiagnosisCase.solution_description.ilike(f"%{search_params.query}%")
                )
            ).limit(10)

        # Ejecución
        exec_result = await self.session.execute(statement)
        cases = exec_result.scalars().all()

        # Mapeo a respuesta
        for case in cases:
            results.append(SearchResult(
                id=case.id,
                title=case.title,
                vehicle_model=case.vehicle_model,
                year=case.year,
                construction_group=case.construction_group,
                problem_description=case.problem_description,
                solution_description=case.solution_description,
                score=0.9 if search_vector else 0.5
            ))
            
        return results
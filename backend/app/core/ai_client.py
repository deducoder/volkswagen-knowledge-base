import os
import asyncio
from typing import List, Optional
from openai import AsyncOpenAI, OpenAIError

class AIClient:
    """
    Adaptador para interactuar con proveedores de LLM (OpenRouter).
    Responsabilidad: Generar embeddings vectoriales para búsqueda semántica.
    """
    
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        # Inicializamos el cliente asíncrono apuntando a OpenRouter
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        # Modelo compatible con 1536 dimensiones (text-embedding-3-small)
        # OpenRouter mapea esto al modelo adecuado de OpenAI
        self.model = "text-embedding-3-small"

    async def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Genera un vector de 1536 dimensiones para el texto dado.
        Implementa un patrón de resiliencia (Circuit Breaker simple):
        Si falla, retorna None en lugar de romper la ejecución.
        """
        if not text:
            return None

        # Limpieza básica para mejorar la calidad del embedding
        cleaned_text = text.replace("\n", " ").strip()

        try:
            # Llamada a la API externa
            response = await self.client.embeddings.create(
                input=[cleaned_text],
                model=self.model
            )
            
            # Extraer el vector (array de floats)
            embedding = response.data[0].embedding
            return embedding

        except OpenAIError as e:
            # Loguear error pero NO detener la aplicación (Fallback Strategy)
            print(f"⚠️  AI Error (OpenRouter): {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado en AIClient: {str(e)}")
            return None

# --- Bloque de Prueba Unitaria (Ejecutar directamente: python app/core/ai_client.py) ---
if __name__ == "__main__":
    async def test_connection():
        print("🔄 Probando conexión con OpenRouter...")
        
        # Verificamos que la KEY exista antes de probar
        if not os.getenv("OPENROUTER_API_KEY"):
            print("❌ ERROR: Variable OPENROUTER_API_KEY no definida.")
            return

        client = AIClient()
        test_text = "Fallo en el sistema de suspensión del Tiguan"
        
        vector = await client.get_embedding(test_text)
        
        if vector:
            print("✅ Éxito: Vector generado.")
            print(f"📊 Dimensiones: {len(vector)}")
            print(f"🔍 Muestra: {vector[:5]}...")
            
            if len(vector) == 1536:
                print("🎯 Validación de dimensiones: CORRECTA (1536)")
            else:
                print(f"⚠️  ADVERTENCIA: Dimensiones incorrectas ({len(vector)})")
        else:
            print("❌ Fallo: No se obtuvo vector (Revisar logs arriba).")

    asyncio.run(test_connection())
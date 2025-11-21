-- Habilitar la extensión vectorial
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Eliminar la tabla vieja si existe para asegurar que se cree limpia
DROP TABLE IF EXISTS diagnosis_cases;

-- 2. (Opcional) Crear el tipo ENUM si SQLAlchemy lo requiere, 
-- pero para evitar problemas de casting, usaremos VARCHAR en la tabla
-- y dejaremos que Python maneje la validación.

-- 3. Crear la tabla con los NUEVOS campos de la Épica 2
CREATE TABLE diagnosis_cases (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    
    -- Nuevos campos requeridos por tu código Python
    vehicle_model VARCHAR(100),
    year INT,
    construction_group VARCHAR(50),  -- Aquí se guardará 'Suspensión', 'Motor', etc.
    problem_description TEXT,
    solution_description TEXT,
    
    -- Campo vectorial
    embedding vector(1536),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
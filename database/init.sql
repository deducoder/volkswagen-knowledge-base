CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS diagnosis_cases (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    vehicle_model VARCHAR(100),
    year INT,
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
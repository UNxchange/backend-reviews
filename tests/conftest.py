"""
Configuración de pytest para los tests del microservicio de reviews
"""
import pytest
import asyncio
from typing import Generator
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos de prueba
TEST_MONGO_URI = os.getenv("TEST_MONGO_URI", "mongodb://localhost:27017")
TEST_DATABASE_NAME = "unxchange_reviews_test"

@pytest.fixture(scope="session")
def event_loop():
    """Crea un event loop para los tests asíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def test_db():
    """
    Crea una base de datos de prueba y la limpia después de cada test
    """
    client = AsyncIOMotorClient(TEST_MONGO_URI)
    db = client[TEST_DATABASE_NAME]
    
    # Proporcionar la base de datos al test
    yield db
    
    # Limpiar después del test
    await client.drop_database(TEST_DATABASE_NAME)
    client.close()

@pytest.fixture(scope="function")
async def test_collection(test_db):
    """
    Proporciona la colección de reviews para los tests
    """
    return test_db.get_collection("reviews")

@pytest.fixture
def sample_review_data():
    """
    Datos de ejemplo para crear una reseña
    """
    return {
        "author_id": "test@ejemplo.com",
        "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
        "rating": 5,
        "content": "Esta es una reseña de prueba con suficiente contenido."
    }

@pytest.fixture
def auth_headers():
    """
    Headers de autenticación para los tests
    Nota: En tests reales, deberías generar un token válido
    """
    return {
        "Authorization": "Bearer test-token-here"
    }

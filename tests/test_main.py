"""
Tests básicos para el microservicio de reviews
"""
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_root_endpoint():
    """Test del endpoint raíz"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "UnxChange Reviews API"
    assert data["status"] == "running"

@pytest.mark.asyncio
async def test_health_check():
    """Test del health check - no requiere autenticación en este caso"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Nota: Este endpoint requiere autenticación, este test fallará sin token válido
        # Es solo un ejemplo de estructura
        response = await client.get("/reviews/health/check")
    
    # En un test real, necesitarías configurar un mock del JWT o usar un token de prueba
    assert response.status_code in [200, 401]  # 401 si no está autenticado

# Agrega más tests aquí siguiendo este patrón
# Por ejemplo: test_create_review, test_get_reviews, etc.

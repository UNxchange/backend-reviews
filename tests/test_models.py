"""
Tests para los modelos Pydantic
"""
import pytest
from bson import ObjectId
from datetime import datetime
from app.models import Review, ReviewCreate, ReviewUpdate, PyObjectId

def test_review_create_valid():
    """Test de creación de ReviewCreate con datos válidos"""
    data = {
        "convocatoria_id": str(ObjectId()),
        "rating": 5,
        "content": "Esta es una reseña válida con más de 10 caracteres"
    }
    review = ReviewCreate(**data)
    assert review.rating == 5
    assert len(review.content) >= 10

def test_review_create_invalid_rating():
    """Test de creación con rating inválido"""
    data = {
        "convocatoria_id": str(ObjectId()),
        "rating": 6,  # Inválido, debe ser 1-5
        "content": "Contenido válido"
    }
    with pytest.raises(Exception):  # ValidationError de Pydantic
        ReviewCreate(**data)

def test_review_create_content_too_short():
    """Test de creación con contenido muy corto"""
    data = {
        "convocatoria_id": str(ObjectId()),
        "rating": 5,
        "content": "Corto"  # Menos de 10 caracteres
    }
    with pytest.raises(Exception):  # ValidationError de Pydantic
        ReviewCreate(**data)

def test_review_update_partial():
    """Test de actualización parcial"""
    update = ReviewUpdate(rating=4)
    assert update.rating == 4
    assert update.content is None

def test_review_update_content_validation():
    """Test de validación de contenido en actualización"""
    # Contenido válido
    update = ReviewUpdate(content="Contenido actualizado y válido")
    assert update.content is not None
    
    # Contenido vacío debe fallar
    with pytest.raises(Exception):
        ReviewUpdate(content="")

def test_py_object_id_validation():
    """Test de validación de PyObjectId"""
    valid_id = str(ObjectId())
    py_oid = PyObjectId.validate(valid_id)
    assert isinstance(py_oid, ObjectId)
    
    # ID inválido debe fallar
    with pytest.raises(ValueError):
        PyObjectId.validate("invalid-id")

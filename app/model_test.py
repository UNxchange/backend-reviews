from datetime import datetime
from models import Review, ReviewCreate, ReviewUpdate, PyObjectId

# Prueba de creación de un objeto Review
def test_review_model():
    try:
        review = Review(
            id=PyObjectId("60e9c0a4d1f3c4c8fbd9a7e0"),
            author_id=PyObjectId("60e9c0a4d1f3c4c8fbd9a7e1"),
            convocatoria_id=PyObjectId("60e9c1f0d1f3c4c8fbd9a7e3"),
            rating=5,
            content="Una experiencia excelente",
            created_at=datetime.utcnow()
        )
        print("✅ Modelo Review creado exitosamente:")
        print(review.model_dump_json(indent=2))
    except Exception as e:
        print("❌ Error al crear el modelo Review:", e)

# Ejecuta la prueba
if __name__ == "__main__":
    test_review_model()

import pytest
import httpx
from bson import ObjectId

CONVOCATORIAS_URL = "http://localhost:8001/convocatorias/"
REVIEWS_URL = "http://localhost:8002/reviews/"
AUTH_URL = "http://localhost:8000/api/v1/auth/login"

@pytest.fixture
def user_credentials():
    return {
        "username": "admin@mail.com",
        "password": "1234"
    }

def get_jwt_token(credentials):
    resp = httpx.post(AUTH_URL, data=credentials)
    print("LOGIN RESPONSE:", resp.status_code, resp.text)
    assert resp.status_code == 200, f"Login failed: {resp.status_code} {resp.text}"
    token = resp.json()["access_token"]
    print("TOKEN:", token)
    return token

def test_reviews_convocatorias_integration(user_credentials):
    # 1. Obtener JWT válido
    token = get_jwt_token(user_credentials)
    headers = {"Authorization": f"Bearer {token}"}
    print("HEADERS:", headers)

    # 2. Crear convocatoria (usa todos los campos requeridos por ConvocatoriaCreate)
    convocatoria_data = {
        "subscriptionYear": "2025",
        "country": "Colombia",
        "institution": "Universidad Nacional",
        "agreementType": "Intercambio",
        "validity": "2025-12-31",
        "state": "Vigente",
        "subscriptionLevel": "Universidad Nacional de Colombia",
        "languages": ["Español"],
        "dreLink": "https://unal.edu.co/drelink",
        "agreementLink": "https://unal.edu.co/agreementlink",
        "properties": "Propiedades de prueba",
        "internationalLink": "https://unal.edu.co/internacional",
        "interestedUsers": []
    }
    resp_conv = httpx.post(CONVOCATORIAS_URL, json=convocatoria_data, headers=headers)
    print("CONVOCATORIA RESPONSE:", resp_conv.status_code, resp_conv.text)
    assert resp_conv.status_code in (200, 201)
    convocatoria_id = resp_conv.json().get("id") or resp_conv.json().get("_id")
    print("CONVOCATORIA ID:", convocatoria_id)
    assert ObjectId.is_valid(convocatoria_id), "El id de la convocatoria no es un ObjectId válido"

    # 3. Crear reseña asociada (el modelo espera un ObjectId como string)
    review_data = {
        "convocatoria_id": convocatoria_id,
        "rating": 5,
        "content": "¡Excelente experiencia!"
    }
    resp_review = httpx.post(REVIEWS_URL, json=review_data, headers=headers)
    print("REVIEW RESPONSE:", resp_review.status_code, resp_review.text)
    assert resp_review.status_code in (200, 201)
    review_id = resp_review.json().get("id") or resp_review.json().get("_id")
    print("REVIEW ID:", review_id)
    assert resp_review.json()["convocatoria_id"] == convocatoria_id

    # 4. Consultar reseña
    resp_get = httpx.get(f"{REVIEWS_URL}{review_id}", headers=headers)
    print("GET REVIEW RESPONSE:", resp_get.status_code, resp_get.text)
    assert resp_get.status_code == 200
    assert resp_get.json()["convocatoria_id"] == convocatoria_id

    # 5. Error: reseña con convocatoria inexistente
    review_data_bad = {
        "convocatoria_id": "000000000000000000000000",
        "rating": 4,
        "content": "Intento inválido"
    }
    resp_bad = httpx.post(REVIEWS_URL, json=review_data_bad, headers=headers)
    print("BAD REVIEW RESPONSE:", resp_bad.status_code, resp_bad.text)
    assert resp_bad.status_code in (400, 404)

    # 6. Error: crear reseña sin autenticación
    resp_no_auth = httpx.post(REVIEWS_URL, json=review_data)
    print("NO AUTH REVIEW RESPONSE:", resp_no_auth.status_code, resp_no_auth.text)
    assert resp_no_auth.status_code == 401
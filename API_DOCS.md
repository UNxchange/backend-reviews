# Documentación de la API - Microservicio de Reviews

## Información General

- **Base URL**: `http://localhost:8003`
- **Versión**: 1.0.1
- **Autenticación**: JWT Bearer Token
- **Formato**: JSON

## Autenticación

Todos los endpoints requieren un token JWT válido en el header:

```http
Authorization: Bearer <tu-token-jwt>
```

### Obtener un Token

El token se obtiene del servicio de autenticación (`backend-auth-roles`):

```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/json

{
  "email": "usuario@ejemplo.com",
  "password": "tu-password"
}
```

## Endpoints

### 1. Root

**GET** `/`

Información básica del servicio.

**Respuesta:**
```json
{
  "service": "UnxChange Reviews API",
  "version": "1.0.1",
  "status": "running",
  "docs": "/docs",
  "health": "/reviews/health/check"
}
```

---

### 2. Health Check

**GET** `/reviews/health/check`

Verifica el estado del servicio.

**Headers:**
```http
Authorization: Bearer <token>
```

**Respuesta:** `200 OK`
```json
{
  "status": "healthy",
  "service": "reviews-service",
  "timestamp": "2025-10-16T10:30:00.000000"
}
```

---

### 3. Crear Reseña

**POST** `/reviews/`

Crea una nueva reseña para una convocatoria.

**Headers:**
```http
Authorization: Bearer <token>
Content-Type: application/json
```

**Body:**
```json
{
  "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
  "rating": 5,
  "content": "Mi experiencia fue increíble. Aprendí mucho sobre la cultura local."
}
```

**Validaciones:**
- `convocatoria_id`: ObjectId válido de MongoDB
- `rating`: Entero entre 1 y 5
- `content`: String de 10 a 2000 caracteres

**Respuesta:** `201 Created`
```json
{
  "id": "67056a1b2c3d4e5f6a7b8c9d",
  "author_id": "usuario@ejemplo.com",
  "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
  "rating": 5,
  "content": "Mi experiencia fue increíble. Aprendí mucho sobre la cultura local.",
  "created_at": "2025-10-16T10:30:00.000000",
  "updated_at": null
}
```

**Errores:**
- `401 Unauthorized`: Token inválido o faltante
- `400 Bad Request`: Datos de entrada inválidos
- `500 Internal Server Error`: Error del servidor

---

### 4. Obtener Lista de Reseñas

**GET** `/reviews/`

Obtiene una lista paginada de reseñas con filtros opcionales.

**Headers:**
```http
Authorization: Bearer <token>
```

**Query Parameters:**
- `convocatoria_id` (opcional): Filtrar por ID de convocatoria
- `author_id` (opcional): Filtrar por email del autor
- `limit` (default: 20, max: 100): Número de resultados
- `skip` (default: 0): Resultados a saltar (paginación)
- `sort_by` (default: "created_at"): Campo para ordenar
- `sort_order` (default: -1): -1 descendente, 1 ascendente

**Ejemplo:**
```http
GET /reviews/?convocatoria_id=60f7c2b8e1b1c8a1b8e1b1c8&limit=10&skip=0
```

**Respuesta:** `200 OK`
```json
{
  "total": 50,
  "limit": 10,
  "skip": 0,
  "reviews": [
    {
      "id": "67056a1b2c3d4e5f6a7b8c9d",
      "author_id": "usuario@ejemplo.com",
      "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
      "rating": 5,
      "content": "Excelente experiencia...",
      "created_at": "2025-10-16T10:30:00.000000",
      "updated_at": null
    }
  ]
}
```

---

### 5. Obtener Reseña por ID

**GET** `/reviews/{id}`

Obtiene una reseña específica por su ID.

**Headers:**
```http
Authorization: Bearer <token>
```

**Path Parameters:**
- `id`: ObjectId de la reseña

**Ejemplo:**
```http
GET /reviews/67056a1b2c3d4e5f6a7b8c9d
```

**Respuesta:** `200 OK`
```json
{
  "id": "67056a1b2c3d4e5f6a7b8c9d",
  "author_id": "usuario@ejemplo.com",
  "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
  "rating": 5,
  "content": "Excelente experiencia...",
  "created_at": "2025-10-16T10:30:00.000000",
  "updated_at": null
}
```

**Errores:**
- `400 Bad Request`: ID inválido
- `404 Not Found`: Reseña no encontrada

---

### 6. Actualizar Reseña

**PATCH** `/reviews/{id}`

Actualiza una reseña existente. Solo el autor puede editar.

**Headers:**
```http
Authorization: Bearer <token>
Content-Type: application/json
```

**Path Parameters:**
- `id`: ObjectId de la reseña

**Body (ambos campos opcionales):**
```json
{
  "rating": 4,
  "content": "Actualizo mi opinión: muy buena experiencia."
}
```

**Validaciones:**
- Solo el autor de la reseña puede actualizarla
- `rating` (opcional): Entero entre 1 y 5
- `content` (opcional): String de 10 a 2000 caracteres

**Respuesta:** `200 OK`
```json
{
  "id": "67056a1b2c3d4e5f6a7b8c9d",
  "author_id": "usuario@ejemplo.com",
  "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
  "rating": 4,
  "content": "Actualizo mi opinión: muy buena experiencia.",
  "created_at": "2025-10-16T10:30:00.000000",
  "updated_at": "2025-10-16T12:00:00.000000"
}
```

**Errores:**
- `403 Forbidden`: No eres el autor de la reseña
- `404 Not Found`: Reseña no encontrada
- `400 Bad Request`: Datos inválidos

---

### 7. Eliminar Reseña

**DELETE** `/reviews/{id}`

Elimina una reseña. Solo el autor o un administrador pueden eliminar.

**Headers:**
```http
Authorization: Bearer <token>
```

**Path Parameters:**
- `id`: ObjectId de la reseña

**Ejemplo:**
```http
DELETE /reviews/67056a1b2c3d4e5f6a7b8c9d
```

**Respuesta:** `204 No Content`

**Errores:**
- `403 Forbidden`: No tienes permisos para eliminar
- `404 Not Found`: Reseña no encontrada

---

### 8. Obtener Estadísticas por Convocatoria

**GET** `/reviews/statistics/{convocatoria_id}`

Obtiene estadísticas detalladas de reseñas para una convocatoria.

**Headers:**
```http
Authorization: Bearer <token>
```

**Path Parameters:**
- `convocatoria_id`: ObjectId de la convocatoria

**Ejemplo:**
```http
GET /reviews/statistics/60f7c2b8e1b1c8a1b8e1b1c8
```

**Respuesta:** `200 OK`
```json
{
  "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
  "average_rating": 4.3,
  "total_reviews": 25,
  "rating_distribution": {
    "1": 1,
    "2": 2,
    "3": 5,
    "4": 8,
    "5": 9
  }
}
```

**Descripción de campos:**
- `average_rating`: Promedio de calificaciones (redondeado a 2 decimales)
- `total_reviews`: Número total de reseñas
- `rating_distribution`: Cantidad de reseñas por cada estrella (1-5)

---

### 9. Obtener Mis Reseñas

**GET** `/reviews/me/reviews`

Obtiene todas las reseñas creadas por el usuario autenticado.

**Headers:**
```http
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (default: 10, max: 50): Número de resultados
- `skip` (default: 0): Resultados a saltar

**Ejemplo:**
```http
GET /reviews/me/reviews?limit=5
```

**Respuesta:** `200 OK`
```json
[
  {
    "id": "67056a1b2c3d4e5f6a7b8c9d",
    "author_id": "usuario@ejemplo.com",
    "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
    "rating": 5,
    "content": "Mi reseña...",
    "created_at": "2025-10-16T10:30:00.000000",
    "updated_at": null
  }
]
```

---

## Códigos de Estado HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado exitosamente
- **204 No Content**: Operación exitosa sin contenido de respuesta
- **400 Bad Request**: Datos de entrada inválidos
- **401 Unauthorized**: Token faltante o inválido
- **403 Forbidden**: No tienes permisos para esta acción
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

## Estructura de Errores

```json
{
  "detail": "Descripción del error"
}
```

## Ejemplos de Uso con cURL

### Crear una reseña
```bash
curl -X POST http://localhost:8003/reviews/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
    "rating": 5,
    "content": "Excelente experiencia de intercambio."
  }'
```

### Obtener lista de reseñas
```bash
curl -X GET "http://localhost:8003/reviews/?limit=10" \
  -H "Authorization: Bearer <token>"
```

### Obtener estadísticas
```bash
curl -X GET http://localhost:8003/reviews/statistics/60f7c2b8e1b1c8a1b8e1b1c8 \
  -H "Authorization: Bearer <token>"
```

### Actualizar reseña
```bash
curl -X PATCH http://localhost:8003/reviews/67056a1b2c3d4e5f6a7b8c9d \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 4,
    "content": "Actualizo mi reseña."
  }'
```

### Eliminar reseña
```bash
curl -X DELETE http://localhost:8003/reviews/67056a1b2c3d4e5f6a7b8c9d \
  -H "Authorization: Bearer <token>"
```

## Límites y Restricciones

- **Autenticación**: Obligatoria en todos los endpoints
- **Rating**: Debe ser un entero entre 1 y 5
- **Contenido**: Mínimo 10 caracteres, máximo 2000
- **Paginación**: Máximo 100 resultados por página (endpoint `/reviews/`)
- **Mis reseñas**: Máximo 50 resultados por página (endpoint `/reviews/me/reviews`)

## Notas Importantes

1. **ObjectId**: Todos los IDs deben ser ObjectIds válidos de MongoDB (24 caracteres hexadecimales)
2. **Timestamps**: Todas las fechas están en formato ISO 8601 UTC
3. **author_id**: Se establece automáticamente desde el token JWT (email del usuario)
4. **Permisos**: 
   - Cualquier usuario autenticado puede crear y leer reseñas
   - Solo el autor puede editar su reseña
   - Solo el autor o un administrador pueden eliminar
5. **CORS**: Configurado para permitir requests desde los orígenes especificados en `.env`

## Swagger UI

Para una documentación interactiva, visita:
- http://localhost:8003/docs (Swagger UI)
- http://localhost:8003/redoc (ReDoc)

Aquí puedes probar todos los endpoints directamente desde el navegador.

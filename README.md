# Microservicio de Reseñas - UnxChange

Este microservicio gestiona las reseñas de experiencias de movilidad académica en la plataforma UnxChange.

## 🚀 Funcionalidades

- Crear reseñas sobre convocatorias de movilidad
- Consultar reseñas por convocatoria, autor o ID
- Editar reseñas (solo el autor)
- Eliminar reseñas (autor o administrador)
- Validación y control de acceso mediante JWT
- API REST para integración con otros microservicios

## 🛠 Tecnologías

- FastAPI
- MongoDB (Motor)
- Pydantic
- Python 3.12+
- JWT para autenticación

## 📋 Endpoints Principales

### POST `/reviews/`

Crea una nueva reseña. Solo usuarios autenticados.

**Request Body:**

```json
{
  "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
  "rating": 5,
  "content": "¡Excelente experiencia!"
}
```

### GET `/reviews/`

Obtiene todas las reseñas, con filtros opcionales por convocatoria o autor.

**Parámetros opcionales:**

- `convocatoria_id`: Filtrar por convocatoria
- `author_id`: Filtrar por autor
- `limit`: Límite de resultados (default: 20)
- `skip`: Saltar resultados (default: 0)

### GET `/reviews/{id}`

Obtiene una reseña por su ID.

### PATCH `/reviews/{id}`

Actualiza una reseña existente. Solo el autor puede editar.

**Request Body:**

```json
{
  "rating": 4,
  "content": "Muy buena experiencia, pero podría mejorar."
}
```

### DELETE `/reviews/{id}`

Elimina una reseña. Solo el autor o un administrador pueden eliminar.

## ⚙️ Configuración

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Crear archivo `.env` basado en `env.example`:

```env
MONGODB_URL=mongodb://localhost:27017/unxchange_reviews
JWT_SECRET=your-secret-key-here
```

3. Ejecutar la aplicación:

```bash
uvicorn app.main:app --reload --port 8003
```

## 🔗 Integración con Microservicio de Autenticación

Todos los endpoints requieren autenticación mediante JWT. El token debe enviarse en el header `Authorization` como `Bearer <token>`.

## 🧪 Testing

Ejecutar pruebas:

```bash
pytest tests/ -v
```

## 📝 Logs

Los logs se muestran en consola con información sobre:

- Creación, edición y eliminación de reseñas
- Errores de autenticación y autorización

## 🔧 Desarrollo

### Estructura de archivos

```plaintext
app/
├── main.py                 # Aplicación FastAPI
├── routes/
│   └── reviews.py          # Endpoints de reseñas
├── models.py               # Modelos Pydantic
├── database.py             # Conexión a MongoDB
├── security.py             # Autenticación y roles
└── tests/                  # Pruebas unitarias
```

### Agregar nuevos campos o funcionalidades

1. Modificar o crear modelos en `models.py`
2. Actualizar lógica en `routes/reviews.py`
3. Agregar pruebas en `tests/`

## 📜 Licencia

Este proyecto está licenciado bajo la licencia MIT.

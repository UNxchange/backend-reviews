# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-14

### Agregado

- **Microservicio de reseñas inicial** para la plataforma UnxChange
- **Sistema de creación de reseñas** (`POST /reviews/`)
  - Validación de campos requeridos y autenticación JWT
  - Asociación automática del autor a partir del token
- **Consulta de reseñas** (`GET /reviews/` y `GET /reviews/{id}`)
  - Filtros por convocatoria y autor
  - Paginación con parámetros `limit` y `skip`
- **Edición de reseñas** (`PATCH /reviews/{id}`)
  - Solo el autor puede editar su reseña
  - Validación de campos editables
- **Eliminación de reseñas** (`DELETE /reviews/{id}`)
  - Solo el autor o un administrador pueden eliminar una reseña
  - Verificación de permisos basada en el token JWT
- **Base de datos MongoDB**
  - Modelos Pydantic para validación y serialización
  - Integración asíncrona con Motor
  - Conversión automática de ObjectId
- **Arquitectura de microservicio FastAPI**
  - API REST con documentación automática (`/docs`)
  - Configuración CORS para integración con frontend
  - Estructura modular y separación de responsabilidades
- **Sistema de seguridad**
  - Autenticación JWT obligatoria en todos los endpoints
  - Validación de permisos para edición y eliminación
  - Manejo de errores y respuestas HTTP adecuadas
- **Configuración de despliegue**
  - Variables de entorno para conexión a MongoDB y JWT
  - Ejemplo de archivo `.env`
  - Soporte para ejecución local con Uvicorn

### Tecnologías utilizadas

- FastAPI como framework web principal
- Motor para acceso asíncrono a MongoDB
- Pydantic para validación y serialización de datos
- JWT para autenticación y autorización
- Python 3.12+
- Uvicorn para servidor ASGI

### Funcionalidades principales

- ✅ Creación de reseñas autenticadas
- ✅ Consulta de reseñas con filtros y paginación
- ✅ Edición y eliminación segura de reseñas
- ✅ Validación de datos y control de acceso
- ✅ API REST documentada
- ✅ Configuración para múltiples entornos

### Seguridad

- Autenticación JWT obligatoria
- Validación de permisos para edición y eliminación
- Validación de datos de entrada con Pydantic
- Variables de entorno para credenciales sensibles
- CORS configurado para producción

### Arquitectura

- **Endpoints**: `/reviews/` - Rutas de gestión de reseñas
- **Modelos**: Sistema de reseñas con campos de autor, convocatoria, rating y contenido
- **CRUD**: Operaciones optimizadas sobre MongoDB
- **Core**: Configuración y funciones de seguridad
- **Schemas**: Validación y serialización de datos

### Integración

- **Microservicio de autenticación**: Validación de tokens JWT y roles
- **Frontend**: API REST con CORS habilitado
- **Base de datos**: MongoDB
- **Despliegue**: Uvicorn y variables de entorno

---

## Documentación técnica

### Endpoints disponibles

- `POST /reviews/` - Crear reseña
- `GET /reviews/` - Listar reseñas (con filtros)
- `GET /reviews/{id}` - Obtener reseña por ID
- `PATCH /reviews/{id}` - Editar reseña (solo autor)
- `DELETE /reviews/{id}` - Eliminar reseña (autor o admin)

### Modelos de datos

- **Review**: Modelo principal con id, author_id, convocatoria_id, rating, content, created_at
- **ReviewCreate**: Schema para creación de reseñas
- **ReviewUpdate**: Schema para edición parcial de reseñas

---

## Notas de desarrollo

- **Pruebas**: Agregar tests unitarios y de integración en futuras versiones
- **Logs**: Mejorar sistema de logging para auditoría
- **Monitoreo**: Implementar métricas de rendimiento y salud del servicio
- **Documentación**: La documentación interactiva está

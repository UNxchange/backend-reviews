# Microservicio de Reseñas - UnxChange

Este microservicio gestiona las reseñas de experiencias de movilidad académica en la plataforma UnxChange. Permite a los estudiantes compartir sus experiencias y calificar las convocatorias de intercambio.

## 🚀 Funcionalidades

- ✅ **CRUD completo de reseñas** con autenticación JWT
- ⭐ **Sistema de calificación** de 1 a 5 estrellas
- 📊 **Estadísticas detalladas** por convocatoria
- 🔍 **Filtros avanzados** por convocatoria, autor, con paginación
- 👥 **Control de acceso** basado en roles (autor/administrador)
- 📈 **Distribución de ratings** y promedios calculados
- 🏥 **Health check** para monitoreo
- 📝 **Validaciones robustas** de contenido

## 🛠 Tecnologías

- **Spring Boot 3.2.0** - Framework web moderno y robusto
- **Spring Data MongoDB** - Integración con MongoDB
- **Spring Security** - Autenticación y autorización
- **Java 17** - Lenguaje de programación
- **JWT (jjwt)** - Autenticación y autorización
- **Maven** - Gestión de dependencias y construcción

## 📋 Endpoints Principales

### 🔐 Todos los endpoints requieren autenticación JWT

#### POST `/reviews/`

Crea una nueva reseña. Solo usuarios autenticados.

**Request Body:**
```json
{
  "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
  "rating": 5,
  "content": "¡Excelente experiencia! Aprendí mucho y conocí personas increíbles."
}
```

**Response:** `201 Created`
```json
{
  "id": "60f7c2b8e1b1c8a1b8e1b1c9",
  "author_id": "usuario@ejemplo.com",
  "convocatoria_id": "60f7c2b8e1b1c8a1b8e1b1c8",
  "rating": 5,
  "content": "¡Excelente experiencia! Aprendí mucho y conocí personas increíbles.",
  "created_at": "2025-10-16T10:30:00Z",
  "updated_at": null
}
```

#### GET `/reviews/`

Obtiene todas las reseñas con filtros opcionales y paginación.

**Parámetros Query:**
- `convocatoria_id` (opcional): Filtrar por ID de convocatoria
- `author_id` (opcional): Filtrar por email del autor
- `limit` (default: 20, max: 100): Número de resultados
- `skip` (default: 0): Resultados a saltar
- `sort_by` (default: "created_at"): Campo para ordenar
- `sort_order` (default: -1): -1 descendente, 1 ascendente

**Response:** `200 OK`
```json
{
  "total": 50,
  "limit": 20,
  "skip": 0,
  "reviews": [...]
}
```

#### GET `/reviews/{id}`

Obtiene una reseña específica por su ID.

**Response:** `200 OK` o `404 Not Found`

#### PATCH `/reviews/{id}`

Actualiza una reseña existente. Solo el autor puede editar.

**Request Body:**
```json
{
  "rating": 4,
  "content": "Actualizo mi reseña: muy buena experiencia."
}
```

**Response:** `200 OK`

#### DELETE `/reviews/{id}`

Elimina una reseña. Solo el autor o un administrador pueden eliminar.

**Response:** `204 No Content`

#### GET `/reviews/statistics/{convocatoria_id}`

Obtiene estadísticas detalladas de una convocatoria.

**Response:** `200 OK`
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

#### GET `/reviews/me/reviews`

Obtiene todas las reseñas del usuario autenticado.

**Parámetros Query:**
- `limit` (default: 10, max: 50): Número de resultados
- `skip` (default: 0): Resultados a saltar

**Response:** `200 OK`

#### GET `/reviews/health/check`

Verifica el estado del servicio.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "reviews-service",
  "timestamp": "2025-10-16T10:30:00Z"
}
```

## ⚙️ Configuración

### 1. Prerrequisitos

- **Java 17** o superior
- **Maven 3.6+**
- **MongoDB** ejecutándose localmente o remotamente

### 2. Configurar variables de entorno

Crea un archivo `.env` basado en `.env.example` o configura las variables de entorno:

```env
# MongoDB
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=unxchange_reviews

# JWT (debe coincidir con backend-auth-roles)
SECRET_KEY=your-super-secret-key-change-this-in-production-unxchange-2025
ALGORITHM=HS256

# CORS
CORS_ORIGINS=http://localhost,http://localhost:80,http://localhost:3000
```

### 3. Compilar y ejecutar la aplicación

#### Desarrollo
```bash
# Compilar el proyecto
mvn clean compile

# Ejecutar en modo desarrollo
mvn spring-boot:run
```

#### Producción
```bash
# Crear JAR ejecutable
mvn clean package

# Ejecutar el JAR
java -jar target/reviews-service-1.0.1.jar
```

#### Con Docker
```bash
# Crear imagen Docker
docker build -t reviews-service .

# Ejecutar contenedor
docker run -p 8003:8003 --env-file .env reviews-service
```

## 🗄️ Base de Datos

### Estructura de MongoDB

**Colección:** `reviews`

```javascript
{
  "_id": ObjectId("..."),
  "author_id": "usuario@ejemplo.com",
  "convocatoria_id": ObjectId("..."),
  "rating": 5,
  "content": "Excelente experiencia...",
  "created_at": ISODate("2025-10-16T10:30:00Z"),
  "updated_at": ISODate("2025-10-16T12:00:00Z") // null si no se ha actualizado
}
```

### Índices Recomendados

```javascript
// Para búsquedas por convocatoria
db.reviews.createIndex({ "convocatoria_id": 1 })

// Para búsquedas por autor
db.reviews.createIndex({ "author_id": 1 })

// Para ordenamiento por fecha
db.reviews.createIndex({ "created_at": -1 })

// Índice compuesto para estadísticas
db.reviews.createIndex({ "convocatoria_id": 1, "rating": 1 })
```

## 🔗 Integración con Otros Microservicios

### Backend de Autenticación (`backend-auth-roles`)

Este servicio depende del microservicio de autenticación para:
- Validar tokens JWT
- Obtener información del usuario (email, rol)
- Controlar permisos de acceso

**Configuración:**
- El `SECRET_KEY` debe ser el mismo en ambos servicios
- El `ALGORITHM` debe coincidir (normalmente "HS256")

### Backend de Convocatorias (`backend-convocatorias`)

Las reseñas están vinculadas a convocatorias mediante `convocatoria_id`:
- Las reseñas referencian convocatorias existentes
- Se recomienda validar la existencia de la convocatoria antes de crear la reseña
- Las estadísticas se pueden mostrar en el detalle de cada convocatoria

## 🔒 Seguridad

### Autenticación
- Todos los endpoints requieren token JWT válido
- Token debe enviarse en header: `Authorization: Bearer <token>`

### Autorización
- **Crear reseña**: Cualquier usuario autenticado
- **Leer reseñas**: Cualquier usuario autenticado
- **Editar reseña**: Solo el autor
- **Eliminar reseña**: Solo el autor o administrador

### Validaciones
- Rating: 1-5 estrellas obligatorio
- Contenido: 10-2000 caracteres, no puede estar vacío
- ObjectIds: Validación estricta de formato MongoDB
- Tokens: Verificación de firma y expiración

## 🏗️ Arquitectura

```
reviews-service/
├── src/main/java/com/unxchange/reviews/
│   ├── ReviewsServiceApplication.java    # Aplicación principal Spring Boot
│   ├── config/
│   │   ├── SecurityConfig.java          # Configuración de seguridad
│   │   ├── CorsConfig.java              # Configuración CORS
│   │   └── OpenApiConfig.java           # Configuración Swagger/OpenAPI
│   ├── controller/
│   │   ├── ReviewController.java        # Endpoints API de reseñas
│   │   └── RootController.java          # Endpoint raíz
│   ├── dto/
│   │   ├── ReviewCreateDto.java         # DTO para crear reseñas
│   │   ├── ReviewUpdateDto.java         # DTO para actualizar reseñas
│   │   ├── ReviewListResponseDto.java   # DTO para respuesta paginada
│   │   └── ReviewStatisticsDto.java     # DTO para estadísticas
│   ├── exception/
│   │   ├── ReviewNotFoundException.java  # Excepción reseña no encontrada
│   │   ├── UnauthorizedException.java   # Excepción sin permisos
│   │   └── GlobalExceptionHandler.java  # Manejador global de excepciones
│   ├── model/
│   │   └── Review.java                  # Entidad de reseña
│   ├── repository/
│   │   └── ReviewRepository.java        # Repositorio MongoDB
│   ├── security/
│   │   ├── JwtAuthenticationFilter.java # Filtro JWT
│   │   └── UserPrincipal.java          # Principal del usuario
│   └── service/
│       └── ReviewService.java           # Lógica de negocio
├── src/main/resources/
│   └── application.yml                  # Configuración de la aplicación
├── pom.xml                              # Dependencias Maven
├── .env.example                         # Plantilla de configuración
├── .gitignore
├── CHANGELOG.md                         # Historial de cambios
├── Dockerfile                           # Imagen Docker
└── README.md                            # Este archivo
```

### Separación de Capas

1. **Controller** (`controller/`): Endpoints HTTP, validación de requests
2. **Service** (`service/`): Lógica de negocio
3. **Repository** (`repository/`): Acceso a datos con Spring Data MongoDB
4. **Model** (`model/`): Entidades de dominio
5. **DTO** (`dto/`): Objetos de transferencia de datos
6. **Security** (`security/`): Autenticación y autorización JWT
7. **Config** (`config/`): Configuraciones de Spring

## 🧪 Testing

### Ejecutar pruebas

```bash
# Ejecutar todas las pruebas
mvn test

# Ejecutar pruebas con reporte de cobertura
mvn test jacoco:report

# Ejecutar solo pruebas unitarias
mvn test -Dtest="*UnitTest"

# Ejecutar solo pruebas de integración
mvn test -Dtest="*IntegrationTest"
```

### Probar endpoints manualmente

Accede a la documentación interactiva:
- Swagger UI: http://localhost:8003/docs
- API Docs: http://localhost:8003/api-docs

## 📊 Monitoreo

### Health Check

```bash
curl http://localhost:8003/reviews/health/check
```

### Logs

El servicio usa el sistema de logging de Spring Boot:

```bash
# Ver logs en tiempo real
tail -f logs/reviews-service.log

# Configurar nivel de logs en application.yml
logging:
  level:
    com.unxchange: DEBUG
```

## 🚢 Despliegue

### Con Docker Compose

Agrega al `docker-compose.yml`:

```yaml
reviews-service:
  build: ./reviews-service
  ports:
    - "8003:8003"
  environment:
    - MONGO_URI=mongodb://mongo:27017
    - DATABASE_NAME=unxchange_reviews
    - SECRET_KEY=${SECRET_KEY}
  depends_on:
    - mongo
    - auth-service
```

## 📝 Documentación API

Una vez ejecutado el servicio, accede a:
- **Swagger UI**: http://localhost:8003/docs
- **ReDoc**: http://localhost:8003/redoc
- **OpenAPI JSON**: http://localhost:8003/openapi.json

## 🤝 Contribuir

1. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
2. Commit tus cambios: `git commit -am 'Agrega nueva funcionalidad'`
3. Push a la rama: `git push origin feature/nueva-funcionalidad`
4. Crea un Pull Request

## 📄 Licencia

Este proyecto es parte de UnxChange - Plataforma de Movilidad Académica.

## 📧 Contacto

Para preguntas o soporte, contacta al equipo de desarrollo de UnxChange.

## 📝 Logs

Los logs se muestran en consola con información sobre:

- Creación, edición y eliminación de reseñas
- Errores de autenticación y autorización

## 🔧 Desarrollo

### Estructura de archivos

```plaintext
src/main/java/com/unxchange/reviews/
├── ReviewsServiceApplication.java  # Aplicación Spring Boot
├── controller/
│   └── ReviewController.java       # Endpoints de reseñas
├── model/
│   └── Review.java                 # Entidad de reseña
├── service/
│   └── ReviewService.java          # Lógica de negocio
├── repository/
│   └── ReviewRepository.java       # Repositorio MongoDB
├── security/
│   └── JwtAuthenticationFilter.java # Autenticación JWT
└── config/
    └── SecurityConfig.java         # Configuración de seguridad
```

### Agregar nuevos campos o funcionalidades

1. Modificar entidades en `model/`
2. Actualizar DTOs en `dto/`
3. Modificar servicios en `service/`
4. Actualizar controladores en `controller/`
5. Agregar pruebas en `src/test/java/`

## 📜 Licencia

Este proyecto está licenciado bajo la licencia MIT.

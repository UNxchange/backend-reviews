import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .routes import reviews

# Cargar variables de entorno
load_dotenv()

# Configuración
PORT = int(os.getenv("PORT", 8003))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:80,http://localhost:3000,http://localhost:8080").split(",")

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Reseñas UnxChange",
    description="""
    Microservicio para gestionar reseñas de estudiantes sobre sus experiencias de movilidad académica.
    
    ## Funcionalidades principales
    
    * **Crear reseñas** - Los usuarios pueden compartir sus experiencias
    * **Consultar reseñas** - Filtrar por convocatoria, autor, con paginación
    * **Editar reseñas** - Solo el autor puede modificar sus reseñas
    * **Eliminar reseñas** - Autor o administrador pueden eliminar
    * **Estadísticas** - Obtener promedios y distribución de ratings por convocatoria
    * **Autenticación JWT** - Todos los endpoints requieren autenticación
    
    ## Seguridad
    
    Todos los endpoints están protegidos con JWT. Incluye el token en el header:
    
    ```
    Authorization: Bearer <tu-token-jwt>
    ```
    """,
    version="1.0.1",
    debug=DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware, 
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir routers
app.include_router(reviews.router)

# Endpoint raíz
@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz del servicio de reseñas.
    Retorna información básica del servicio.
    """
    return {
        "service": "UnxChange Reviews API",
        "version": "1.0.1",
        "status": "running",
        "docs": "/docs",
        "health": "/reviews/health/check"
    }

# Evento de inicio
@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación.
    Útil para inicializar conexiones, cachés, etc.
    """
    print("🚀 Iniciando servicio de reseñas...")
    print(f"📝 Documentación disponible en: http://localhost:{PORT}/docs")
    print(f"🔒 CORS habilitado para: {CORS_ORIGINS}")

# Evento de cierre
@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta al cerrar la aplicación.
    Útil para cerrar conexiones, limpiar recursos, etc.
    """
    print("👋 Cerrando servicio de reseñas...")

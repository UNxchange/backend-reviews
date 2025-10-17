from fastapi import APIRouter, HTTPException, Query, Body, status, Depends
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from ..models import (
    Review, 
    ReviewCreate, 
    ReviewUpdate, 
    ReviewStatistics,
    ReviewListResponse
)
from ..database import get_review_collection
from ..security import get_current_user, require_admin_role, TokenData
from ..crud.reviews import ReviewCRUD

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

# Inicializar la capa CRUD
def get_review_crud():
    collection = get_review_collection()
    return ReviewCRUD(collection)

# ==================== ENDPOINTS DE RESEÑAS ====================

# Crear una nueva reseña (POST)
@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate = Body(...),
    current_user: TokenData = Depends(get_current_user),
    crud: ReviewCRUD = Depends(get_review_crud)
):
    """
    Crea una nueva reseña para una convocatoria.
    
    - **convocatoria_id**: ID de la convocatoria a reseñar
    - **rating**: Calificación de 1 a 5 estrellas
    - **content**: Texto de la reseña (mínimo 10 caracteres)
    
    Requiere autenticación.
    """
    if not current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado correctamente"
        )

    try:
        new_review = await crud.create_review(review, current_user.sub)
        return new_review
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la reseña: {str(e)}"
        )


# Obtener todas las reseñas con paginación (GET)
@router.get("/", response_model=ReviewListResponse)
async def get_reviews(
    convocatoria_id: Optional[str] = Query(None, description="Filtrar por ID de convocatoria"),
    author_id: Optional[str] = Query(None, description="Filtrar por email del autor"),
    limit: int = Query(20, gt=0, le=100, description="Número máximo de resultados"),
    skip: int = Query(0, ge=0, description="Número de resultados a saltar"),
    sort_by: str = Query("created_at", description="Campo por el cual ordenar"),
    sort_order: int = Query(-1, ge=-1, le=1, description="Orden: -1 descendente, 1 ascendente"),
    current_user: TokenData = Depends(get_current_user),
    crud: ReviewCRUD = Depends(get_review_crud)
):
    """
    Obtiene una lista paginada de reseñas con filtros opcionales.
    
    - **convocatoria_id**: Filtra por convocatoria específica
    - **author_id**: Filtra por autor específico (email)
    - **limit**: Cantidad máxima de resultados (default: 20, max: 100)
    - **skip**: Cantidad de resultados a saltar para paginación
    - **sort_by**: Campo para ordenar (default: created_at)
    - **sort_order**: -1 para descendente, 1 para ascendente
    
    Requiere autenticación.
    """
    try:
        reviews = await crud.get_reviews(
            convocatoria_id=convocatoria_id,
            author_id=author_id,
            limit=limit,
            skip=skip,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        total = await crud.count_reviews(
            convocatoria_id=convocatoria_id,
            author_id=author_id
        )
        
        return ReviewListResponse(
            total=total,
            limit=limit,
            skip=skip,
            reviews=reviews
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener reseñas: {str(e)}"
        )


# Obtener reseña por ID (GET)
@router.get("/{id}", response_model=Review)
async def get_review_by_id(
    id: str,
    current_user: TokenData = Depends(get_current_user),
    crud: ReviewCRUD = Depends(get_review_crud)
):
    """
    Obtiene una reseña específica por su ID.
    
    - **id**: ID de la reseña
    
    Requiere autenticación.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválido"
        )
    
    review = await crud.get_review_by_id(id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reseña con id {id} no encontrada"
        )
    
    return review


# Actualizar reseña por ID (PATCH)
@router.patch("/{id}", response_model=Review)
async def update_review(
    id: str,
    review_update: ReviewUpdate = Body(...),
    current_user: TokenData = Depends(get_current_user),
    crud: ReviewCRUD = Depends(get_review_crud)
):
    """
    Actualiza una reseña existente. Solo el autor puede editar su propia reseña.
    
    - **id**: ID de la reseña a actualizar
    - **rating**: Nueva calificación (opcional)
    - **content**: Nuevo contenido (opcional)
    
    Requiere autenticación y ser el autor de la reseña.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválido"
        )

    # Buscar la reseña
    existing_review = await crud.get_review_by_id(id)
    if not existing_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reseña con id {id} no encontrada"
        )

    # Verificar si el autor es el mismo que el usuario loggeado
    if existing_review.author_id != current_user.sub:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar esta reseña"
        )

    # Actualizar la reseña
    updated_review = await crud.update_review(id, review_update)
    if not updated_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudieron aplicar los cambios"
        )
    
    return updated_review


# Eliminar reseña por ID (DELETE)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    id: str,
    current_user: TokenData = Depends(get_current_user),
    crud: ReviewCRUD = Depends(get_review_crud)
):
    """
    Elimina una reseña. Solo el autor o un administrador pueden eliminar.
    
    - **id**: ID de la reseña a eliminar
    
    Requiere autenticación y ser el autor de la reseña o tener rol de administrador.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválido"
        )

    review = await crud.get_review_by_id(id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reseña con id {id} no encontrada"
        )

    # Verificación: autor o administrador
    is_author = review.author_id == current_user.sub
    is_admin = current_user.role == "administrador"

    if not (is_author or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar esta reseña"
        )

    deleted = await crud.delete_review(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la reseña"
        )
    
    return


# ==================== ENDPOINTS DE ESTADÍSTICAS ====================

# Obtener estadísticas de una convocatoria
@router.get("/statistics/{convocatoria_id}", response_model=ReviewStatistics)
async def get_convocatoria_statistics(
    convocatoria_id: str,
    current_user: TokenData = Depends(get_current_user),
    crud: ReviewCRUD = Depends(get_review_crud)
):
    """
    Obtiene estadísticas detalladas de reseñas para una convocatoria específica.
    
    - **convocatoria_id**: ID de la convocatoria
    
    Retorna:
    - Promedio de calificaciones
    - Número total de reseñas
    - Distribución de calificaciones (1-5 estrellas)
    
    Requiere autenticación.
    """
    if not ObjectId.is_valid(convocatoria_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de convocatoria inválido"
        )
    
    try:
        stats = await crud.get_statistics_by_convocatoria(convocatoria_id)
        return ReviewStatistics(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )


# Obtener reseñas del usuario actual
@router.get("/me/reviews", response_model=List[Review])
async def get_my_reviews(
    limit: int = Query(10, gt=0, le=50),
    skip: int = Query(0, ge=0),
    current_user: TokenData = Depends(get_current_user),
    crud: ReviewCRUD = Depends(get_review_crud)
):
    """
    Obtiene todas las reseñas creadas por el usuario autenticado.
    
    - **limit**: Cantidad máxima de resultados (default: 10, max: 50)
    - **skip**: Cantidad de resultados a saltar
    
    Requiere autenticación.
    """
    try:
        reviews = await crud.get_user_reviews(
            author_id=current_user.sub,
            limit=limit,
            skip=skip
        )
        return reviews
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tus reseñas: {str(e)}"
        )


# Endpoint de health check
@router.get("/health/check", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    """
    Verifica que el servicio de reseñas esté funcionando correctamente.
    """
    return {
        "status": "healthy",
        "service": "reviews-service",
        "timestamp": datetime.utcnow().isoformat()
    }
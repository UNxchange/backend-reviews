from fastapi import APIRouter, HTTPException, Query, Body, status, Depends
from typing import List, Optional
from bson import ObjectId

from ..models import Review, ReviewCreate, ReviewUpdate
from ..database import get_review_collection
from ..security import get_current_user, require_admin_role, TokenData

router = APIRouter(
    prefix="/reviews",
   tags=["Reviews"]
)

collection = get_review_collection()

 # Crear una nueva reseña POST
@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate = Body(...),
    current_user: TokenData = Depends(get_current_user) # <-- Dependencia de usuario autenticado
):
    review_dict = review.dict(by_alias=True)
    
    review_dict["author_id"] = ObjectId()
    review_dict["created_at"] = review_dict.get("created_at") or  __import__('datetime').datetime.utcnow()
    result = await collection.insert_one(review_dict)
    new_review = await collection.find_one({"_id": result.inserted_id})
    return new_review

# Obtener todas las reseñas GET
@router.get("/", response_model=List[Review])
async def get_reviews(
    convocatoria_id: Optional[str] = Query(None, description="Filtrar por ID de convocatoria"),
    author_id: Optional[str] = Query(None, description="Filtrar por ID de autor"),
    limit: int = Query(20, gt=0, le=100),
    skip: int =Query(0, ge=0),
    current_user: TokenData = Depends(get_current_user) # <-- Dependencia de usuario autenticado
):
    query ={}
    if convocatoria_id and ObjectId.is_valid(convocatoria_id):
        query["convocatoria_id"] = ObjectId(convocatoria_id)
    if author_id and ObjectId.is_valid(author_id):
        query ["author_id"] = ObjectId(author_id)

    cursor = collection.find(query).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

# Obtener reseña por ID (GET)
@router.get("/{id}", response_model=Review)
async def get_review_by_id(id: str,
    current_user: TokenData = Depends(get_current_user)                           
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    review = await collection.find_one({"_id": ObjectId(id)})
    if not review:
        raise HTTPException(status_code=404, detail=f"Reseña con id {id} no encontrada")
    return review


# Actualizar reseña por ID (PATCH)
@router.patch("/{id}", response_model=Review)
async def update_review(
    id: str,
    review_update: ReviewUpdate = Body(...),
    current_user: TokenData = Depends(get_current_user)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Buscar la reseña
    existing_review = await collection.find_one({"_id": ObjectId(id)})
    if not existing_review:
        raise HTTPException(status_code=404, detail=f"Reseña con id {id} no encontrada")

    # Verificar si el autor es el mismo que el usuario loggeado
    # if str(existing_review["author_id"]) != current_user.sub:
    #     raise HTTPException(status_code=403, detail="No tienes permisos para editar esta reseña")
    if current_user.role != "administrador" and str(existing_review["author_id"]) != current_user.sub:
        raise HTTPException(status_code=403, detail="No tienes permisos para editar esta reseña")

    update_data = {k: v for k, v in review_update.dict(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

    await collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    updated_review = await collection.find_one({"_id": ObjectId(id)})
    return updated_review

# Eliminar reseña por ID (DELETE)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    id: str,
    current_user: TokenData = Depends(get_current_user)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    review = await collection.find_one({"_id": ObjectId(id)})
    if not review:
        raise HTTPException(status_code=404, detail=f"Reseña con id {id} no encontrada")

    # Verificar si el usuario es el autor o tiene rol de administrador
    is_author = str(review["author_id"]) == current_user.sub
    is_admin = current_user.role == "administrador"

    if not (is_author or is_admin):
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta reseña")

    await collection.delete_one({"_id": ObjectId(id)})
    return
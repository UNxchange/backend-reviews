from fastapi import APIRouter, HTTPException, Query, Body, status, Depends
from typing import List, Optional
from bson import ObjectId

from ..models import Review, ReviewCreate, ReviewUpdate
from ..database import get_review_collection

router = APIRouter(
    prefix="/reviews",
   tags=["Reviews"]
)

collection = get_review_collection()

# Crear una nueva reseña POST
@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate = Body(...)):
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
    skip: int =Query(0, ge=0)
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
async def get_review_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    review = await collection.find_one({"_id": ObjectId(id)})
    if not review:
        raise HTTPException(status_code=404, detail=f"Reseña con id {id} no encontrada")
    return review


# Actualizar reseña por ID (PATCH)
@router.patch("/{id}", response_model=Review)
async def update_review(id: str, review_update: ReviewUpdate = Body(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    update_data = {k: v for k, v in review_update.dict(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")
    result = await collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Reseña con id {id} no encontrada")
    updated_review = await collection.find_one({"_id": ObjectId(id)})
    return updated_review


# Eliminar reseña por ID (DELETE)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Reseña con id {id} no encontrada")
    return

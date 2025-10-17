"""
CRUD operations para Reviews
Separación de lógica de base de datos
"""
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorCollection

from ..models import Review, ReviewCreate, ReviewUpdate


class ReviewCRUD:
    """Clase para operaciones CRUD de reseñas"""
    
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection
    
    async def create_review(self, review_data: ReviewCreate, author_id: str) -> Review:
        """Crea una nueva reseña"""
        review_dict = review_data.model_dump(by_alias=True)
        review_dict["author_id"] = author_id
        review_dict["created_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(review_dict)
        new_review = await self.collection.find_one({"_id": result.inserted_id})
        return Review(**new_review)
    
    async def get_review_by_id(self, review_id: str) -> Optional[Review]:
        """Obtiene una reseña por su ID"""
        if not ObjectId.is_valid(review_id):
            return None
        
        review = await self.collection.find_one({"_id": ObjectId(review_id)})
        if review:
            return Review(**review)
        return None
    
    async def get_reviews(
        self,
        convocatoria_id: Optional[str] = None,
        author_id: Optional[str] = None,
        limit: int = 20,
        skip: int = 0,
        sort_by: str = "created_at",
        sort_order: int = -1
    ) -> List[Review]:
        """Obtiene lista de reseñas con filtros opcionales"""
        query = {}
        
        if convocatoria_id and ObjectId.is_valid(convocatoria_id):
            query["convocatoria_id"] = ObjectId(convocatoria_id)
        
        if author_id:
            query["author_id"] = author_id
        
        cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        reviews = await cursor.to_list(length=limit)
        
        return [Review(**review) for review in reviews]
    
    async def update_review(self, review_id: str, review_update: ReviewUpdate) -> Optional[Review]:
        """Actualiza una reseña existente"""
        if not ObjectId.is_valid(review_id):
            return None
        
        update_data = review_update.model_dump(exclude_unset=True)
        if not update_data:
            return None
        
        # Agregar timestamp de actualización
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(review_id)},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            updated_review = await self.collection.find_one({"_id": ObjectId(review_id)})
            return Review(**updated_review)
        
        return None
    
    async def delete_review(self, review_id: str) -> bool:
        """Elimina una reseña"""
        if not ObjectId.is_valid(review_id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(review_id)})
        return result.deleted_count > 0
    
    async def count_reviews(
        self,
        convocatoria_id: Optional[str] = None,
        author_id: Optional[str] = None
    ) -> int:
        """Cuenta el número total de reseñas con filtros opcionales"""
        query = {}
        
        if convocatoria_id and ObjectId.is_valid(convocatoria_id):
            query["convocatoria_id"] = ObjectId(convocatoria_id)
        
        if author_id:
            query["author_id"] = author_id
        
        return await self.collection.count_documents(query)
    
    async def get_average_rating(self, convocatoria_id: str) -> Optional[float]:
        """Obtiene el rating promedio de una convocatoria"""
        if not ObjectId.is_valid(convocatoria_id):
            return None
        
        pipeline = [
            {"$match": {"convocatoria_id": ObjectId(convocatoria_id)}},
            {"$group": {
                "_id": None,
                "avg_rating": {"$avg": "$rating"},
                "total_reviews": {"$sum": 1}
            }}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        
        if result:
            return {
                "average_rating": round(result[0]["avg_rating"], 2),
                "total_reviews": result[0]["total_reviews"]
            }
        
        return {"average_rating": 0, "total_reviews": 0}
    
    async def get_statistics_by_convocatoria(self, convocatoria_id: str) -> Dict[str, Any]:
        """Obtiene estadísticas detalladas de una convocatoria"""
        if not ObjectId.is_valid(convocatoria_id):
            return None
        
        pipeline = [
            {"$match": {"convocatoria_id": ObjectId(convocatoria_id)}},
            {"$group": {
                "_id": None,
                "avg_rating": {"$avg": "$rating"},
                "total_reviews": {"$sum": 1},
                "rating_1": {"$sum": {"$cond": [{"$eq": ["$rating", 1]}, 1, 0]}},
                "rating_2": {"$sum": {"$cond": [{"$eq": ["$rating", 2]}, 1, 0]}},
                "rating_3": {"$sum": {"$cond": [{"$eq": ["$rating", 3]}, 1, 0]}},
                "rating_4": {"$sum": {"$cond": [{"$eq": ["$rating", 4]}, 1, 0]}},
                "rating_5": {"$sum": {"$cond": [{"$eq": ["$rating", 5]}, 1, 0]}}
            }}
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        
        if result:
            data = result[0]
            return {
                "convocatoria_id": convocatoria_id,
                "average_rating": round(data["avg_rating"], 2),
                "total_reviews": data["total_reviews"],
                "rating_distribution": {
                    "1": data["rating_1"],
                    "2": data["rating_2"],
                    "3": data["rating_3"],
                    "4": data["rating_4"],
                    "5": data["rating_5"]
                }
            }
        
        return {
            "convocatoria_id": convocatoria_id,
            "average_rating": 0,
            "total_reviews": 0,
            "rating_distribution": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        }
    
    async def get_user_reviews(self, author_id: str, limit: int = 10, skip: int = 0) -> List[Review]:
        """Obtiene todas las reseñas de un usuario específico"""
        cursor = self.collection.find({"author_id": author_id}).sort("created_at", -1).skip(skip).limit(limit)
        reviews = await cursor.to_list(length=limit)
        return [Review(**review) for review in reviews]

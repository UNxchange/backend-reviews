from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_core import core_schema
from typing import List, Optional, Dict
from bson import ObjectId
from datetime import datetime

# Helper para ObjectId con pydantic v2
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate)
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            )
        )
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)



# Modelo principal de la Reseña
class Review(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "60c72b2f9b1e8d001c8e4a2f",
                "author_id": "usuario@ejemplo.com",
                "convocatoria_id": "60c72b2f9b1e8d001c8e4a31",
                "rating": 4,
                "content": "Excelente experiencia de movilidad.",
                "created_at": "2025-07-08T12:00:00Z",
                "updated_at": None
            }
        }
    )
    
    id: PyObjectId = Field(default_factory=PyObjectId, validation_alias="_id", serialization_alias="id")
    author_id: str = Field(..., description="Email del autor de la reseña")
    convocatoria_id: PyObjectId = Field(..., description="ID de la convocatoria reseñada")
    rating: int = Field(..., ge=1, le=5, description="Calificación de 1 a 5 estrellas")
    content: str = Field(..., min_length=10, max_length=2000, description="Contenido de la reseña")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Valida que el contenido no esté vacío y no tenga solo espacios"""
        if not v or not v.strip():
            raise ValueError('El contenido no puede estar vacío')
        return v.strip()


# Modelo para crear una nueva reseña
class ReviewCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "convocatoria_id": "60c72b2f9b1e8d001c8e4a31",
                "rating": 5,
                "content": "Mi experiencia fue increíble. Aprendí mucho y conocí personas maravillosas."
            }
        }
    )
    
    convocatoria_id: PyObjectId = Field(..., description="ID de la convocatoria a reseñar")
    rating: int = Field(..., ge=1, le=5, description="Calificación de 1 a 5 estrellas")
    content: str = Field(..., min_length=10, max_length=2000, description="Contenido de la reseña")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Valida que el contenido no esté vacío y no tenga solo espacios"""
        if not v or not v.strip():
            raise ValueError('El contenido no puede estar vacío')
        return v.strip()


# Modelo para actualizar una reseña
class ReviewUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rating": 4,
                "content": "Actualizo mi reseña: muy buena experiencia, pero podría mejorar en algunos aspectos."
            }
        }
    )
    
    rating: Optional[int] = Field(None, ge=1, le=5, description="Nueva calificación")
    content: Optional[str] = Field(None, min_length=10, max_length=2000, description="Nuevo contenido")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        """Valida que el contenido no esté vacío si se proporciona"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('El contenido no puede estar vacío')
        return v.strip() if v else None


# Modelo para estadísticas de reseñas
class ReviewStatistics(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "convocatoria_id": "60c72b2f9b1e8d001c8e4a31",
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
        }
    )
    
    convocatoria_id: str
    average_rating: float = Field(..., ge=0, le=5)
    total_reviews: int = Field(..., ge=0)
    rating_distribution: Dict[str, int]


# Modelo para la respuesta paginada de reseñas
class ReviewListResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 50,
                "limit": 20,
                "skip": 0,
                "reviews": []
            }
        }
    )
    
    total: int
    limit: int
    skip: int
    reviews: List[Review]
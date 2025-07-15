from pydantic import BaseModel, Field, field_validator
from pydantic_core import core_schema
from typing import List, Optional
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
    id: PyObjectId = Field(default_factory=PyObjectId, validation_alias="_id")
    author_id: str
    convocatoria_id: PyObjectId
    rating: int = Field(..., ge=1, le=5)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_schema_example={
            "example": {
                "id": "60c72b2f9b1e8d001c8e4a2f",
                "author_id": "60c72b2f9b1e8d001c8e4a30",
                "convocatoria_id": "60c72b2f9b1e8d001c8e4a31",
                "rating": 4,
                "content": "Excelente experiencia de movilidad.",
                "created_at": "2025-07-08T12:00:00Z"
            }
        }

# Modelo para crear una nueva reseña
class ReviewCreate(BaseModel):
    convocatoria_id: PyObjectId
    rating: int = Field(..., ge=1, le=5)
    content: str

# Modelo para actualizar una reseña
class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    content: Optional[str] = None
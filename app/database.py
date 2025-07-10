import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()  # Carga las variables desde el archivo .env

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

#Crear cliente de MongoDB
client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]

def get_review_collection():
    """Obtiene la colección de reseñas."""
    return database.get_collection("reviews")
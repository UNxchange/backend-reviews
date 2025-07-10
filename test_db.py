import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

async def test_connection():
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        # Intenta obtener los nombres de las colecciones como prueba
        db = client[DATABASE_NAME]
        collections = await db.list_collection_names()
        print(f"✅ Conexión exitosa a la base de datos '{DATABASE_NAME}'")
        print("📂 Colecciones encontradas:", collections)
    except Exception as e:
        print("❌ Error al conectar con MongoDB:")
        print(e)
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_connection())

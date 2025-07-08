from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import reviews


app = FastAPI(
    title="API de Reseñas UnxChange",
    description="Provee acceso a las reseñas de estudiantes sobre sus experiencias de movilidad académica.",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],# En desarrollo se puede usar "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(reviews.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Reseñas UnxChange"}
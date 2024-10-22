from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as recipe_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Permite solo este origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)
# Incluir las rutas
app.include_router(recipe_router)

from fastapi import FastAPI
from app.routes import router as recipe_router

app = FastAPI()

# Incluir las rutas
app.include_router(recipe_router)

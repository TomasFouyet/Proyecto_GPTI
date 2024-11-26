from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.ml import RecipeModel
from app.database import Ingredient, Recipe, User
from app.dependencies import get_db
from pydantic import BaseModel
from typing import List
from app.schemas import RegisterRequest
import jwt

router = APIRouter()

# Inicializar el modelo RecipeNLG
recipe_model = RecipeModel()

@router.get("/ingredients/", response_model=List[str])
async def get_ingredients(db: Session = Depends(get_db)):
    # Obtener ingredientes desde la base de datos
    ingredients = db.query(Ingredient).all()
    return [ingredient.name for ingredient in ingredients]

@router.post("/generate-recipe/")
async def generate_recipe(ingredients: List[str], db: Session = Depends(get_db)):
    if len(ingredients) > 10:
        raise HTTPException(status_code=400, detail="You can select a maximum of 10 ingredients.")

    # Unir los ingredientes en una cadena para el modelo RecipeNLG
    ingredients_str = ", ".join(ingredients)
    ingredients_str = "Ingredients: " + ingredients_str
    print(f"Ingredients received: {ingredients_str}")
    # Generar receta usando RecipeNLG
    recipe_text = recipe_model.generate_recipe(ingredients_str)

    return {"recipe": recipe_text}

class RecipeRequest(BaseModel):
    ingredient_list: List[str]  # Lista de ingredientes como strings

@router.post("/recommendation")
def recommend_recipe(request: RecipeRequest, db: Session = Depends(get_db)):
    # Extrae la lista de ingredientes del request
    ingredient_list = request.ingredient_list
    print(f"Ingredientes recibidos: {ingredient_list}")
    # Limitar la cantidad de ingredientes a 10
    if len(ingredient_list) > 10:
        raise HTTPException(status_code=400, detail="Puedes proporcionar un máximo de 10 ingredientes.")
    # Crear un diccionario para asignar puntos a cada receta
    recipe_scores = {}

    # Convertir los ingredientes proporcionados a minúsculas para una búsqueda insensible a mayúsculas
    ingredient_list = [ingredient.lower() for ingredient in ingredient_list]

    # Buscar cada ingrediente en la base de datos y relacionarlo con las recetas
    for ingredient_name in ingredient_list:
        ingredient = db.query(Ingredient).filter(func.lower(Ingredient.name) == ingredient_name).first()

        # Si el ingrediente existe en la base de datos
        if ingredient:
            # Obtener todas las recetas que usan este ingrediente
            recipes_with_ingredient = ingredient.recipes

            # Asignar puntos a cada receta
            for recipe in recipes_with_ingredient:
                if recipe.id not in recipe_scores:
                    recipe_scores[recipe.id] = 0
                recipe_scores[recipe.id] += 1

    # Si no se encontraron recetas, devolver un error
    if not recipe_scores:
        raise HTTPException(status_code=404, detail="No se encontraron recetas con los ingredientes proporcionados.")

    # Obtener la receta con la mayor cantidad de puntos
    best_recipe_id = max(recipe_scores, key=recipe_scores.get)

    # Obtener la receta con más puntos desde la base de datos
    best_recipe = db.query(Recipe).filter(Recipe.id == best_recipe_id).first()

    return {
        "recipe_id": best_recipe.id,
        "title": best_recipe.title,
        "instructions": best_recipe.instructions,
        "ingredient_count": recipe_scores[best_recipe_id],
        "ingredients": [ingredient.name for ingredient in best_recipe.ingredients]
    }

@router.post("/register", status_code=201)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Comprobar que email sea único
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        raise HTTPException(status_code=400, detail="El email ingresado ya se encuentra registrado")
    new_user = User(email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    return {"message": "Usuario registrado con éxito"}

@router.post("/login", status_code=201)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Comprobar que email sea único
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="El email ingresado no se encuentra registrado")
    if user.password != request.password:
        raise HTTPException(status_code=400, detail="La contraseña ingresada es inválida")
    token = jwt.encode({"email": request.email}, "secret", algorithm="HS256")
    return {"token": token}

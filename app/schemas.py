from pydantic import BaseModel
from typing import List

class IngredientBase(BaseModel):
    name: str

class IngredientCreate(IngredientBase):
    pass

class IngredientResponse(IngredientBase):
    id: int

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    title: str
    instructions: str
    ingredients: List[str]

class RecipeCreate(RecipeBase):
    pass

class RecipeResponse(RecipeBase):
    id: int
    ingredients: List[IngredientResponse]

    class Config:
        orm_mode = True

class RecipeRequest(BaseModel):
    prompt: str

class IngredientsList(BaseModel):
    ingredients: List[str]

class RegisterRequest(BaseModel):
    email: str
    password: str

class HistorialRequest(BaseModel):
    token: str
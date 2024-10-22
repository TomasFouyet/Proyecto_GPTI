import re
from sqlalchemy.orm import Session
from sqlalchemy import func, exists
from dependencies import get_db
from database import Recipe, Ingredient, recipe_ingredient, engine, SessionLocal

# Función para poblar la base de datos
def populate_database_from_file(file_path: str, db: Session):
    with open(file_path, 'r') as file:
        content = file.read()

    # Dividir recetas por <RECIPE_START> y <RECIPE_END>
    recipes_data = re.split(r'<RECIPE_START>|<RECIPE_END>', content)

    for recipe_data in recipes_data:
        if recipe_data.strip():
            # Extraer ingredientes
            ingredients_section = re.search(r'<INPUT_START>(.*?)<INPUT_END>', recipe_data, re.DOTALL)
            ingredients_list = []
            if ingredients_section:
                ingredients = re.split(r'<NEXT_INPUT>', ingredients_section.group(1))
                for ingredient in ingredients:
                    ingredient_name = ingredient.strip()
                    # Buscar si el ingrediente ya existe en la BD (case-insensitive)
                    db_ingredient = db.query(Ingredient).filter(func.lower(Ingredient.name) == ingredient_name.lower()).first()

                    if not db_ingredient:
                        # Insertar ingrediente si no existe
                        new_ingredient = Ingredient(name=ingredient_name)
                        db.add(new_ingredient)
                        db.commit()
                        db_ingredient = new_ingredient

                    ingredients_list.append(db_ingredient)

            # Extraer el título
            title_section = re.search(r'<TITLE_START>(.*?)<TITLE_END>', recipe_data)
            title = title_section.group(1).strip() if title_section else None

            # Extraer las instrucciones
            instr_section = re.search(r'<INSTR_START>(.*?)<INSTR_END>', recipe_data, re.DOTALL)
            instructions = re.sub(r'<NEXT_INSTR>', ' ', instr_section.group(1)).strip() if instr_section else None

            # Insertar la receta
            new_recipe = Recipe(title=title, instructions=instructions)
            db.add(new_recipe)
            db.commit()

            for ingredient in ingredients_list:
                # Verificar si la relación ya existe
                existing_relation = db.query(exists().where(
                    recipe_ingredient.c.recipe_id == new_recipe.id,
                    recipe_ingredient.c.ingredient_id == ingredient.id
                )).scalar()

                if not existing_relation:
                    stmt = recipe_ingredient.insert().values(recipe_id=new_recipe.id, ingredient_id=ingredient.id)
                    db.execute(stmt)
            db.commit()

# Función principal para ejecutar el script
def main(file_path: str):
    # Crear una sesión de base de datos usando SessionLocal
    db = SessionLocal()

    try:
        # Poblar la base de datos
        populate_database_from_file(file_path, db)
        print("Base de datos poblada con éxito.")
    except Exception as e:
        print(f"Error al poblar la base de datos: {e}")
    finally:
        db.close()

# Ejecutar la función principal
if __name__ == "__main__":
    file_path = "../processed_recipes.txt"  # Cambia esta ruta por la ubicación de tu archivo
    main(file_path)

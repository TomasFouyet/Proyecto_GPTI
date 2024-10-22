from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "postgresql://tfouyet:tfouyet@localhost/recipe_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Tabla de asociación para la relación muchos a muchos entre Recipe e Ingredient
recipe_ingredient = Table(
    'recipe_ingredient',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'), primary_key=True)
)

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    instructions = Column(Text, nullable=False)

    # Relación muchos a muchos con Ingredient
    ingredients = relationship('Ingredient', secondary=recipe_ingredient, back_populates='recipes')

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relación inversa con Recipe
    recipes = relationship('Recipe', secondary=recipe_ingredient, back_populates='ingredients')

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

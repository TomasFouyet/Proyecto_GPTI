from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "postgresql://:@localhost/recipe_db"

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

user_recipe = Table(
    'user_recipe',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

favorites = Table(
    'favorites',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    instructions = Column(Text, nullable=False)

    # Relación muchos a muchos con Ingredient
    ingredients = relationship('Ingredient', secondary=recipe_ingredient, back_populates='recipes')

    # Relación inversa con User
    users = relationship('User', secondary=user_recipe, back_populates='recipes')
    
    # Relación inversa con User
    users_favorites = relationship('User', secondary=favorites, back_populates='favorites')

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relación inversa con Recipe
    recipes = relationship('Recipe', secondary=recipe_ingredient, back_populates='ingredients')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=False, nullable=False)
    
    # Relación muchos a muchos con Recipe
    recipes = relationship('Recipe', secondary=user_recipe, back_populates='users')

    # Relación muchos a muchos con Recipe
    favorites = relationship('Recipe', secondary=favorites, back_populates='users_favorites')

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

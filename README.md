# Proyecto de Generación de Recetas

Este proyecto implementa un sistema para la gestión y generación de recetas culinarias, incluyendo una base de datos, un modelo de Machine Learning (ML) para generar recetas basadas en ingredientes, y una API para interactuar con el sistema.

## Archivos del Proyecto

### 1. `database.py`
- Define las clases `Recipe` e `Ingredient` para manejar recetas e ingredientes en la base de datos.
- Configura la conexión a la base de datos utilizando SQLAlchemy y crea las tablas necesarias automáticamente.
- Incluye una tabla de asociación para la relación muchos-a-muchos entre recetas e ingredientes.

### 2. `dependencies.py`
- Proporciona una función de utilidad `get_db` para obtener una sesión de la base de datos y garantizar que se cierre después de su uso.

### 3. `ml.py`
- Implementa un modelo basado en **Hugging Face** (`RecipeNLG`) para generar recetas automáticamente a partir de ingredientes.
- Define la clase `RecipeModel` con el método `generate_recipe` para procesar una lista de ingredientes y devolver una receta generada.

### 4. `populate_db.py`
- Proporciona funciones para poblar la base de datos con recetas e ingredientes desde un archivo de texto.
- Procesa las recetas utilizando delimitadores como `<RECIPE_START>` y `<RECIPE_END>` para identificar las secciones de cada receta.

### 5. `routes.py`
- Define rutas de la API utilizando **FastAPI**.
- Incluye:
  - `/ingredients/`: Recupera una lista de ingredientes de la base de datos.
  - `/recommendation`: Recomienda la receta más adecuada basada en una lista de ingredientes.

### 6. `schemas.py`
- Contiene los modelos Pydantic para validar datos que se envían o reciben en las rutas.
- Modelos principales:
  - `IngredientBase`, `IngredientResponse`: Para datos de ingredientes.
  - `RecipeBase`, `RecipeResponse`: Para datos de recetas.

---

## Configuración del Proyecto

Sigue estos pasos para configurar el proyecto en tu máquina local:

### 1. Clonar el repositorio
Clona este repositorio en tu máquina local:
```bash
git clone <URL-del-repositorio>
cd <nombre-del-directorio>

### 2. Configurar el entorno virtual
Crea un entorno virtual y actívalo:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

### 3. Instalar dependencias
Instalar las dependencias necesarias:
```bash
pip install -r requirements.txt

### 4. Configurar la base de datos
Sigue estos pasos para configurar la base de datos:

1. Asegúrate de tener **PostgreSQL** instalado.
2. Crea una base de datos llamada `recipe_db`.
3. Actualiza la URL de conexión en el archivo `database.py`:

   ```python
   DATABASE_URL = "postgresql://<usuario>:<contraseña>@localhost/recipe_db"

### 5. Poblar la base de datos

Para cargar los datos a la base de datos, se tiene que ejecutar el archivo `populate_db.py`.
Asegurate de tener el archivo `processed_recipes.txt`

### 6. Ejecutar el servidor

Iniciar el servidor FastAPi ejecutadno el siguiente comando:
   ```python
   unicorn main:app --reload
 Accede a **http://127.0.0.1:8000**

### 7. Documentacion

Se puede ver la documentacion del proyecto en **http://127.0.0.1:8000/docs**
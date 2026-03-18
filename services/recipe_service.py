from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models.recipe_model import Recipes as Recipe


def serialize_recipe(recipe: Recipe) -> dict:
    """
    Convert SQLAlchemy Recipe object into JSON-serializable dictionary.

    Args:
        recipe (Recipe): SQLAlchemy model instance

    Returns:
        dict: Serialized recipe
    """
    return {
        "id": recipe.id,
        "title": recipe.title,
        "making_time": recipe.making_time,
        "serves": recipe.serves,
        "ingredients": recipe.ingredients,
        "cost": str(recipe.cost),  # Ensure decimal is serializable
        "created_at": recipe.created_at.strftime("%Y-%m-%d %H:%M:%S") if recipe.created_at else None,
        "updated_at": recipe.updated_at.strftime("%Y-%m-%d %H:%M:%S") if recipe.updated_at else None,
    }


def create_recipe(db: Session, recipe):
    """
    Create a new recipe in the database.

    Validates required fields before inserting.

    Args:
        db (Session): Database session
        recipe: Incoming request schema

    Returns:
        dict / JSONResponse
    """
    required_fields = [
        recipe.title,
        recipe.making_time,
        recipe.serves,
        recipe.ingredients,
        recipe.cost,
    ]

    # Validate required fields
    if any(field is None or field == "" for field in required_fields):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Recipe creation failed!",
                "required": "title, making_time, serves, ingredients, cost",
            },
        )

    try:
        # Create DB object
        new_recipe = Recipe(
            title=recipe.title,
            making_time=recipe.making_time,
            serves=recipe.serves,
            ingredients=recipe.ingredients,
            cost=recipe.cost,
        )

        db.add(new_recipe)
        db.commit()  # Persist changes
        db.refresh(new_recipe)  # Load DB-generated values (like ID)

        return {
            "message": "Recipe successfully created!",
            "recipe": [serialize_recipe(new_recipe)],
        }

    except Exception as e:
        db.rollback()  # Important for data integrity
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error", "error": str(e)},
        )


def get_all_recipe(db: Session):
    """
    Retrieve all recipes.

    Args:
        db (Session): Database session

    Returns:
        dict: List of recipes
    """
    recipes = db.query(Recipe).all()

    return {
        "recipes": [serialize_recipe(recipe) for recipe in recipes]
    }


def get_recipe_by_id(db: Session, recipe_id: int):
    """
    Fetch a recipe by ID.

    Args:
        db (Session): Database session
        recipe_id (int): Recipe ID

    Returns:
        dict: Recipe details or not found message
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        return {"message": "Recipe not found"}

    return {
        "message": "Recipe details by id",
        "recipe": [serialize_recipe(recipe)],
    }


def update_recipe(db: Session, recipe_id: int, recipe_data):
    """
    Update an existing recipe.

    Only updates fields provided in request.

    Args:
        db (Session): Database session
        recipe_id (int): Recipe ID
        recipe_data: Partial update schema

    Returns:
        dict: Updated recipe or error message
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        return {"message": "Recipe not found"}

    try:
        # Update only provided fields (PATCH behavior)
        update_data = recipe_data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(recipe, key, value)

        db.commit()
        db.refresh(recipe)

        return {
            "message": "Recipe successfully updated!",
            "recipe": [serialize_recipe(recipe)],
        }

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": "Update failed", "error": str(e)},
        )


def delete_recipe(db: Session, recipe_id: int):
    """
    Delete a recipe by ID.

    Args:
        db (Session): Database session
        recipe_id (int): Recipe ID

    Returns:
        dict: Success or failure message
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        return {"message": "No recipe found"}

    try:
        db.delete(recipe)
        db.commit()

        return {"message": "Recipe successfully removed!"}

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": "Delete failed", "error": str(e)},
        )
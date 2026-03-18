from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.recipes_schema import (
    RecipeCreateResponse,
    RecipeCreate,
    RecipeResponse,
    RecipeByIdResponse,
    RecipeUpdateResponse,
    RecipeUpdate,
    RecipeErrorResponse,
    RecipesAllResponse,
)
from services.recipe_service import (
    create_recipe,
    get_all_recipe,
    get_recipe_by_id,
    update_recipe,
    delete_recipe,
)

# Initialize router
router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post(
    "/",
    response_model=RecipeCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": RecipeErrorResponse}},
)
def create_recipe_route(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """
    Create a new recipe.

    Args:
        recipe (RecipeCreate): Incoming recipe data from request body.
        db (Session): Database session dependency.

    Returns:
        RecipeCreateResponse: Created recipe details.
    """
    # Debug log (replace with proper logging in production)
    print("Received recipe data:", recipe)

    created_recipe = create_recipe(db, recipe)
    return created_recipe


@router.get("/", response_model=RecipesAllResponse)
def get_all_recipes_route(db: Session = Depends(get_db)):
    """
    Fetch all recipes from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        RecipesAllResponse: List of all recipes.
    """
    recipes = get_all_recipe(db)
    return recipes


@router.get("/{recipe_id}", response_model=RecipeByIdResponse)
def get_recipe_route(recipe_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single recipe by its ID.

    Args:
        recipe_id (int): ID of the recipe.
        db (Session): Database session dependency.

    Returns:
        RecipeByIdResponse: Recipe details.

    Raises:
        HTTPException: If recipe not found.
    """
    recipe = get_recipe_by_id(db, recipe_id)

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found",
        )

    return recipe


@router.patch("/{recipe_id}", response_model=RecipeUpdateResponse)
def update_recipe_route(
    recipe_id: int,
    recipe_data: RecipeUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing recipe.

    Args:
        recipe_id (int): ID of the recipe to update.
        recipe_data (RecipeUpdate): Updated recipe fields.
        db (Session): Database session dependency.

    Returns:
        RecipeUpdateResponse: Updated recipe details.

    Raises:
        HTTPException: If recipe not found.
    """
    print("Received update data:", recipe_data)

    updated_recipe = update_recipe(db, recipe_id, recipe_data)

    if not updated_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found",
        )

    return updated_recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe_route(recipe_id: int, db: Session = Depends(get_db)):
    """
    Delete a recipe by its ID.

    Args:
        recipe_id (int): ID of the recipe to delete.
        db (Session): Database session dependency.

    Returns:
        None

    Raises:
        HTTPException: If recipe not found.
    """
    deleted = delete_recipe(db, recipe_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with id {recipe_id} not found",
        )

    return None
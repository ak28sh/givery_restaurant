from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from db.database import engine, get_db
from db.database import SessionLocal
from schemas.recipes_schema import RecipeCreateResponse, RecipeCreate, RecipeResponse, RecipeByIdResponse, \
    RecipeUpdateResponse, RecipeUpdate, RecipeErrorResponse, RecipesAllResponse
from services.recipe_service import create_recipe, get_all_recipe, get_recipe_by_id, update_recipe, delete_recipe

router = APIRouter()

@router.post("/", response_model=RecipeCreateResponse,
             responses={400: {"model": RecipeErrorResponse}})
def create_recipe_route(recipe: RecipeCreate, db: Session = Depends(get_db)):
    print("Received recipe data:", recipe)
    return create_recipe(db, recipe)

@router.get("/", response_model=RecipesAllResponse)
def get_all_recipes_route(db: Session = Depends(get_db)):
    return get_all_recipe(db)

@router.get("/{recipe_id}", response_model=RecipeByIdResponse)
def get_recipe_route(recipe_id: int, db: Session = Depends(get_db)):
    return get_recipe_by_id(db, recipe_id)

@router.patch("/{recipe_id}", response_model=RecipeUpdateResponse)
def update_recipe_route(recipe_id: int, recipe_data: RecipeUpdate, db: Session = Depends(get_db)):
    print("Received update data:", recipe_data)
    updated_recipe = update_recipe(db, recipe_id, recipe_data)
    # if not updated_recipe:
    #     raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe

@router.delete("/{recipe_id}")
def delete_recipe_route(recipe_id: int, db: Session = Depends(get_db)):
    deleted_recipe = delete_recipe(db, recipe_id)
    return deleted_recipe
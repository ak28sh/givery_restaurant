from fastapi.responses import JSONResponse
from models.recipe_model import Recipes as Recipe

def serialize_recipe(recipe):
    return {
        "id": recipe.id,
        "title": recipe.title,
        "making_time": recipe.making_time,
        "serves": recipe.serves,
        "ingredients": recipe.ingredients,
        "cost": str(recipe.cost),
        "created_at": recipe.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": recipe.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }

def create_recipe(db, recipe):

    required_fields = [
        recipe.title,
        recipe.making_time,
        recipe.serves,
        recipe.ingredients,
        recipe.cost
    ]

    if any(field is None or field == "" for field in required_fields):
        return JSONResponse(
            status_code=200,
            content={"message": "Recipe creation failed!", "required": "title, making_time, serves, ingredients, cost"}
        )


    new_recipe = Recipe(
        title=recipe.title,
        making_time=recipe.making_time,
        serves=recipe.serves,
        ingredients=recipe.ingredients,
        cost=recipe.cost
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    print(new_recipe)

    return {"message": "Recipe successfully created!", "recipe": [serialize_recipe(new_recipe)]}

def get_all_recipe(db):
    all_recipes = db.query(Recipe).all()
    return {"recipes": [serialize_recipe(recipe) for recipe in all_recipes]}

def get_recipe_by_id(db, recipe_id):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    return {"message": "Recipe details by id", "recipe": [serialize_recipe(recipe)]} if recipe else {"message": "Recipe not found"}

def update_recipe(db, recipe_id, recipe_data):
    updated_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    # if not updated_recipe:
    #     return {"message": "Recipe not found"}

    for key, value in recipe_data.dict(exclude_unset=True).items():
        setattr(updated_recipe, key, value)

    db.commit()
    db.refresh(updated_recipe)
    return {"message": "Recipe successfully updated!", "recipe": [serialize_recipe(updated_recipe)]}

def delete_recipe(db, recipe_id):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        return {"message": "No recipe found"}
    db.delete(recipe)
    db.commit()
    return {"message": "Recipe successfully removed!"}
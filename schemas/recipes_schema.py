import datetime
from typing import List, Optional
from pydantic import BaseModel


class RecipeCreate(BaseModel):
    title: Optional[str] = None
    making_time: Optional[str] = None
    serves: Optional[str] = None
    ingredients: Optional[str] = None
    cost: Optional[int] = None

class Recipe(BaseModel):
    id: int
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class RecipeCreateResponse(BaseModel):
    message: str
    recipe: List[Recipe]

class RecipeErrorResponse(BaseModel):
    message: str
    required: str

class RecipeResponse(BaseModel):
    id: int
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: str

    class Config:
        orm_mode = True

class RecipesAllResponse(BaseModel):
    recipes: List[RecipeResponse]

class RecipeByIdResponse(BaseModel):
    message: str
    recipe: List[RecipeResponse]

class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    making_time: Optional[str] = None
    serves: Optional[str] = None
    ingredients: Optional[str] = None
    cost: Optional[int] = None

class RecipeUpdateResponse(BaseModel):
    message: str
    recipe: List[RecipeResponse]

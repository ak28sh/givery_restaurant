from fastapi import APIRouter
from .routes import recipes

api_router = APIRouter()

api_router.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
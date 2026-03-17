from fastapi import FastAPI

from api.router import api_router

app = FastAPI()
print("Starting FastAPI application...")
app.include_router(api_router)


from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import products, users, webhook
from database.models import Base
from database.connection import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"error creating tables: {e}")
        raise
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Inventory API",
    description="API for inventory management",
    version="1.0.0")
app.include_router(products.router)
app.include_router(users.router)
app.include_router(webhook.router)

@app.get("/")
async def root():
    return {"message": "Hello Inventory"}

from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise
from src.core.database.connection import database_initialize


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await database_initialize(app)
    yield
    # Shutdown logic
    await Tortoise.close_connections()

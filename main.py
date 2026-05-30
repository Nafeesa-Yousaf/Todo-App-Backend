from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.routes import register_routes
@asynccontextmanager
async def life_splan(app:FastAPI):
    create_tables()
    yield
    #

app=FastAPI(lifespan=life_splan)
register_routes(app)

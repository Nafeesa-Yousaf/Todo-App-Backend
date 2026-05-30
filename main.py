from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter

@asynccontextmanager
async def life_splan(app:FastAPI):
    create_tables()
    yield
    #

app=FastAPI(lifespan=life_splan)
app.include_router(router=authRouter, tags=["Auth"], prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Hello World"}

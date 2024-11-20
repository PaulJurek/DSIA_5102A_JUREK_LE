from fastapi import FastAPI, Request
from models import BaseSQL, engine
import routers
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.include_router(routers.ProduitRouter)
app.include_router(routers.CommandeRouter)

# Monter le répertoire static
app.mount("/static", StaticFiles(directory="./templates/static"), name="static")

@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)

@app.get("/")
def get_root():
    return {"message": "Hello, World!"}

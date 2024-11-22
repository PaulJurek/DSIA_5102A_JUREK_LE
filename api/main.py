from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from models import BaseSQL, engine
import routers

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)

# Monter le répertoire static
app.mount("/static", StaticFiles(directory="./templates/static"), name="static")

app.include_router(routers.router_Produit)
app.include_router(routers.router_Auth)
app.include_router(routers.router_Panier)
app.include_router(routers.router_Commande)

@app.get("/")
def get_root():
    return {"message": "Hello, World!"}
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from schemas.legumes import Produit
from services.legumes import ajouter_un_legume, lister_legumes

legume_router = APIRouter(prefix="/produits")


@legume_router.post("/", tags=["legumes"])
async def post_legume(db: Session = Depends(models.get_db)):
    return ajouter_un_legume(db=db)

@legume_router.get("/", tags=["legumes"])
async def lister_produits(db: Session = Depends(models.get_db)) -> List[Produit]:
    return lister_legumes(db=db)

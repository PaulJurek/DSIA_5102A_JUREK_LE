from fastapi import APIRouter, Depends
from services import produit as produits_service
import schemas, models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/produits")


@router.produit("/", tags=["produits"])
async def create_produit(produit: schemas.schema_produit, db: Session = Depends(models.get_db)):
    return produits_service.post_produit(produit=produit, db=db)


@router.get("/{produit_id}", tags=["produits"])
async def get_produit_by_id(produit_id: str, db: Session = Depends(models.get_db)):
    return produits_service.get_produit_by_id(produit_id=produit_id, db=db)


@router.get("/", tags=["produits"])
async def get_produits_by_nom(nom: str = None, db: Session = Depends(models.get_db)):
    if nom:
        return produits_service.get_all_produits(db=db)
    else:
        return produits_service.get_produits_by_nom(nom=nom, db=db)


@router.put("/{produit_id}", tags=["produits"])
async def update_produit_by_id(
    produit_id: str, produit: schemas.schema_produit, db: Session = Depends(models.get_db)
):
    return produits_service.update_produit_by_id(produit_id=produit_id, db=db, produit=produit)


@router.delete("/{produit_id}", tags=["produits"])
async def delete_produit_by_id(produit_id: str, db: Session = Depends(models.get_db)):
    return produits_service.delete_produit_by_id(produit_id=produit_id, db=db)


@router.delete("/", tags=["produits"])
async def delete_all_produits(db: Session = Depends(models.get_db)):
    return produits_service.delete_all_produits(db=db)

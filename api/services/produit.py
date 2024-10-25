from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import models, schemas


def get_all_produits(db: Session, skip: int = 0, limit: int = 10) -> List[models.Produit]:
    records = db.query(models.Produit).filter().offset(skip).limit(limit).all()
    for record in records:
        record.id = str(record.id)
    return records


def get_produit_by_id(Produit_id: str, db: Session) -> models.Produit:
    record = db.query(models.Produit).filter(models.Produit.id == Produit_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found")
    record.id = str(record.id)
    return record


def get_produits_by_nom(nom: str, db: Session) -> List[models.Produit]:
    records = db.query(models.Produit).filter(models.Produit.nom == nom).all()
    for record in records:
        record.id = str(record.id)
    return records


def update_produit_by_id(Produit_id: str, db: Session, Produit: schemas.Produit) -> models.Produit:
    db_Produit = get_produit_by_id(Produit_id=Produit_id, db=db)
    for var, value in vars(Produit).items():
        setattr(db_Produit, var, value) if value else None
    db.add(db_Produit)
    db.commit()
    db.refresh(db_Produit)
    return db_Produit


def delete_produit_by_id(Produit_id: str, db: Session) -> models.Produit:
    db_Produit = get_produit_by_id(Produit_id=Produit_id, db=db)
    db.delete(db_Produit)
    db.commit()
    return db_Produit


def delete_all_produits(db: Session) -> List[models.Produit]:
    records = db.query(models.Produit).filter()
    for record in records:
        db.delete(record)
    db.commit()
    return records


def post_produit(db: Session, Produit: schemas.Produit) -> models.Produit:
    record = db.query(models.Produit).filter(models.Produit.id == Produit.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")
    db_Produit = models.Produit(**Produit.dict())
    db.add(db_Produit)
    db.commit()
    db.refresh(db_Produit)
    db_Produit.id = str(db_Produit.id)
    return db_Produit

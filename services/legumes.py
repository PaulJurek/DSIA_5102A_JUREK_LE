from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import models.user
import models, schemas
import schemas.legumes


def lister_legumes(db: Session, skip: int = 0, limit: int = 10) -> List[models.legumes]:
    records = db.query(models.user.Legumes).filter().all()
    for record in records:
        record.id = str(record.id)
    return records


def infos_sur_un_legume_par_id(legume_id: str, db: Session) -> models.legumes:
    record = db.query(models.user.Legumes).filter(models.user.Legumes.id == legume_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Not Found")
    record.id = str(record.id)
    return record


def mise_a_jour_infos_legume(legume_id: str, db: Session, post: schemas.legumes.Legume) -> models.legumes:
    db_post = infos_sur_un_legume_par_id(legume_id=legume_id, db=db)
    for var, value in vars(post).items():
        setattr(db_post, var, value) if value else None
    db_post.date_de_mise_a_jour = datetime.now()
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def supprimer_un_legume(legume_id: str, db: Session) -> models.legumes:
    db_post = infos_sur_un_legume_par_id(legume_id=legume_id, db=db)
    db.delete(db_post)
    db.commit()
    return db_post


def supprimer_tous_les_legumes(db: Session) -> List[models.legumes]:
    records = db.query(models.legumes).filter()
    for record in records:
        db.delete(record)
    db.commit()
    return records


def ajouter_un_legume(db: Session, post: schemas.legumes.Legume) -> models.legumes:
    record = db.query(models.user.Legumes).filter(models.legumes.id == post.id).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")
    db_post = models.user.Legumes(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    db_post.id = str(db_post.id)
    return db_post

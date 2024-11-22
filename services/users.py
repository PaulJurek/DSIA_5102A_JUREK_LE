from typing import Optional, List
from uuid import uuid4

import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from ..models.user import User as model_user
from ..schemas.users import User
from ..services.auth import JWT_SECRET_KEY, JWT_SECRET_ALGORITHM

def create_user(db: Session, user: User, pConfirmerMDP: str ) -> model_user:
    record = db.query(user).filter(user.pseudo == user.pseudo).first()
    if record:
        raise HTTPException(status_code=409, detail="Pseudo déjà utilisé")

    if user.mot_de_passe == pConfirmerMDP:
        db_item = User(id=uuid4(), 
                             prenom=user.prenom, 
                             nom=user.nom, 
                             pseudo=user.pseudo,
                             email=user.email,
                             date_naissance=user.date_naissance,
                             adresse_numero=user.adresse_numero,
                             adresse_rue=user.adresse_rue,
                             adresse_ville=user.adresse_ville,
                             mot_de_passe=user.mot_de_passe)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        


def get_user_by_id(db: Session, user_id: int) -> Optional[model_user]:
    return db.query(model_user).filter(model_user.id == user_id).first()


def get_user_id(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_SECRET_ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user_id
    except InvalidTokenError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
